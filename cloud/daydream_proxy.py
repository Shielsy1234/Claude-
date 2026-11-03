"""A small gatekeeper in front of ComfyUI for the Daydream cloud GPU.

Only requests whose path starts with /k/<your password>/ get through, so nobody
who finds the web address can spend your GPU credit. It also adds the CORS
headers the Daydream app needs, waits for ComfyUI while the cloud GPU is still
starting, and passes websockets (live progress) through.
"""
import asyncio
import os

import aiohttp
from aiohttp import web

KEY = os.environ["DAYDREAM_KEY"].strip()
PREFIX = "/k/" + KEY
UPSTREAM = os.environ.get("DAYDREAM_UPSTREAM", "http://127.0.0.1:8188")
PORT = int(os.environ.get("DAYDREAM_PORT", "8000"))
START_WAIT = int(os.environ.get("DAYDREAM_START_WAIT", "110"))  # stay under the cloud's ~150 s request limit; the app retries

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Max-Age": "86400",
}
# Headers that belong to one connection, or that aiohttp sets again itself.
SKIP = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers",
        "transfer-encoding", "upgrade", "host", "content-length", "content-encoding", "origin", "referer"}

_ready = asyncio.Event()


async def wait_for_comfy(session):
    """ComfyUI takes a little while to start on a fresh cloud GPU; hold requests until it answers."""
    if _ready.is_set():
        return True
    for _ in range(START_WAIT):
        try:
            async with session.get(UPSTREAM + "/system_stats", timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status == 200:
                    _ready.set()
                    return True
        except Exception:
            pass
        await asyncio.sleep(1)
    return False


async def proxy_ws(request, url):
    client = web.WebSocketResponse(heartbeat=30, max_msg_size=0)
    await client.prepare(request)
    try:
        upstream_cm = request.app["session"].ws_connect(url.replace("http", "ws", 1), max_msg_size=0)
        upstream = await upstream_cm.__aenter__()
    except Exception:
        await client.close()  # live progress is optional; the app falls back to polling
        return client
    try:
        async def pump(src, dst):
            async for msg in src:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await dst.send_str(msg.data)
                elif msg.type == aiohttp.WSMsgType.BINARY:
                    await dst.send_bytes(msg.data)
                else:
                    break
        tasks = [asyncio.create_task(pump(client, upstream)), asyncio.create_task(pump(upstream, client))]
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for t in tasks:
            t.cancel()
    finally:
        await upstream_cm.__aexit__(None, None, None)
    await client.close()
    return client


async def handle(request):
    path = request.rel_url.raw_path
    if not (path == PREFIX or path.startswith(PREFIX + "/")):
        return web.Response(status=404, text="Not found")
    if request.method == "OPTIONS":
        return web.Response(status=204, headers=CORS)
    session = request.app["session"]
    if not await wait_for_comfy(session):
        return web.Response(status=503, text="ComfyUI didn't start", headers=CORS)
    tail = path[len(PREFIX):] or "/"
    query = request.rel_url.raw_query_string
    url = UPSTREAM + tail + ("?" + query if query else "")
    if request.headers.get("Upgrade", "").lower() == "websocket":
        return await proxy_ws(request, url)
    headers = {k: v for k, v in request.headers.items() if k.lower() not in SKIP}
    body = await request.read()
    async with session.request(request.method, url, headers=headers, data=body or None, allow_redirects=False) as up:
        out_headers = {k: v for k, v in up.headers.items() if k.lower() not in SKIP and not k.lower().startswith("access-control-")}
        resp = web.StreamResponse(status=up.status, headers={**out_headers, **CORS})
        await resp.prepare(request)
        async for chunk in up.content.iter_chunked(1 << 16):
            await resp.write(chunk)
        await resp.write_eof()
        return resp


async def on_start(app):
    app["session"] = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=None, sock_connect=10))


async def on_stop(app):
    await app["session"].close()


def main():
    app = web.Application(client_max_size=512 * 1024 * 1024)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_stop)
    app.router.add_route("*", "/{tail:.*}", handle)
    web.run_app(app, host="0.0.0.0", port=PORT, access_log=None)


if __name__ == "__main__":
    main()
