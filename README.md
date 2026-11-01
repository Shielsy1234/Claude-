# Daydream Studio

Your private AI on your own PC: chat with a local AI model, and create realistic images and videos, in one installable app.

The app is `index.html` plus `manifest.webmanifest`, `sw.js` and `icons/`. Host it with GitHub Pages (recommended) or any static web server. It must be opened from a web address (`https://…` or `http://localhost`), not by double-clicking the file.

## Install it as a PC app

Open the site in **Edge or Chrome** and press **Install app** in the header (or use the browser menu: *Apps → Install Daydream Studio*). It then has its own window, a Start menu and desktop shortcut, and opens without the browser around it. After the first run, the app and its downloaded AI models work **offline**.

## Chat

The **Chat** tab talks to an AI running on your PC. Ask it to make a picture or a video and it creates one inside the conversation ("draw me…", "make a 3 second video of…", "now animate it").

| Source | Notes |
| --- | --- |
| **Built in** (default) | Runs in the app on your GPU with [WebLLM](https://github.com/mlc-ai/web-llm). Models: Qwen 3.5 9B (6.4 GB), Qwen 3.5 4B (3.9 GB), Hermes 3 8B (4.9 GB), Llama 3.1 8B (5 GB). One-time download. |
| **Ollama** | Uses any model installed with [Ollama](https://ollama.com). Run `ollama pull <model>`, then `setx OLLAMA_ORIGINS "*"` and restart Ollama so the app can connect. |

Conversations are saved on your PC. **Custom instructions** let you set how the AI behaves. With **Free graphics memory for videos** on, the chat and image models are unloaded while ComfyUI makes a video so it gets the whole GPU.

When a local AI is loaded, **Ideas** and **Improve prompt** use it too instead of the online text service.

## Image engines

| Engine | Where it runs | Cost | Notes |
| --- | --- | --- | --- |
| **This PC** | Your graphics card, in the browser (WebGPU) | Free, unlimited | Z-Image Turbo, highly realistic. One-time 5.6 GB download, stored by the browser. Private: prompts and images never leave your PC. No safety checker. |
| Free online | Pollinations | Free | Basic quality, 768 px, watermark, one image every 45 seconds |
| Pollinations account | Pollinations | Free daily allowance | Key from [enter.pollinations.ai](https://enter.pollinations.ai) |
| OpenAI | OpenAI | Paid per image | Key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |

### This PC requirements

- Chrome or Edge (recent version) on Windows, Linux or macOS
- A GPU with WebGPU and 16-bit float support (for example AMD RX 6000/7000/9000, NVIDIA RTX, Apple Silicon); about 8 GB of VRAM or more
- About 6 GB of free disk space

Quality settings: **Quick** (512 px, 6 steps), **Standard** (1024 px, 8 steps) and **Large** (about 1300 px, 9 steps).

The pipeline is a port of Microsoft's MIT-licensed [WebNN developer preview Z-Image Turbo demo](https://github.com/microsoft/webnn-developer-preview/tree/main/demos/z-image-turbo), using the ONNX models from [webnn/Z-Image-Turbo](https://huggingface.co/webnn/Z-Image-Turbo) (Apache-2.0) and [ONNX Runtime Web](https://onnxruntime.ai/).

## Video (ComfyUI on your PC)

Browsers can't run video models yet, so the **Video** tab sends jobs to [ComfyUI](https://www.comfy.org/) running on your own PC, using the **Wan 2.2 TI2V 5B** model. It does text-to-video and image-to-video (press **Animate** on any image).

One-time setup:

1. Install [ComfyUI Desktop](https://www.comfy.org/download). On an AMD card, choose **AMD (ROCm)** when asked. Windows ROCm support is new: if ComfyUI crashes on your card, AMD's guide for [ComfyUI with ROCm on WSL](https://rocm.blogs.amd.com/software-tools-optimization/rocm-on-wsl/README.html) is the fallback.
2. Download these files into your ComfyUI `models` folder:
   - [`wan2.2_ti2v_5B_fp16.safetensors`](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors) → `models/diffusion_models`
   - [`umt5_xxl_fp8_e4m3fn_scaled.safetensors`](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors) → `models/text_encoders`
   - [`wan2.2_vae.safetensors`](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/vae/wan2.2_vae.safetensors) → `models/vae`
3. Allow the page to talk to ComfyUI: in ComfyUI Desktop, **Settings → Server Config → Enable CORS header** = `*`, then restart. For portable or manual installs, launch with `--enable-cors-header "*"`.
4. In the Video tab, enter ComfyUI's address (Desktop usually `http://127.0.0.1:8000`, manual installs `http://127.0.0.1:8188`) and press **Check**. If the browser asks to allow access to local network devices, allow it.

Video settings: **Quick** (832×480) or **Full 720p** (1280×704), 2, 3 or 5 seconds at 24 fps.

## Other features

- **Look presets** and an **Extra realism** switch for photographic results
- **Improve prompt** rewrites a short idea into a detailed prompt (free Pollinations text service)
- **Ideas** mode brainstorms 6 ideas with a **Picture this** button on each
- Everything you make is saved in the browser's gallery, with full-size viewing and download
