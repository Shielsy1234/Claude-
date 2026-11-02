# Daydream Studio

Your private AI on your own PC: chat with a local AI model, and create realistic images and videos, in one installable app.

The app is `index.html` plus `manifest.webmanifest`, `sw.js` and `icons/`. Host it with GitHub Pages (recommended) or any static web server. It must be opened from a web address (`https://…` or `http://localhost`), not by double-clicking the file.

## PC or Phone

The **PC / Phone** switch at the top picks which version you see. It's chosen automatically the first time (phones get Phone) and you can change it any time.

- **PC**: everything, including what runs on your own graphics card (This PC images, ComfyUI video, built-in and Ollama chat).
- **Phone**: only what works without your PC: Free online HD images, free online video (LTX Video, Wan 2.2 14B Fast) and Free online chat.

Each mode remembers its own engine, video model and chat choices, so switching back to PC restores your PC setup.

## Install it as a PC app

Open the site in **Edge or Chrome** and press **Install app** in the header (or use the browser menu: *Apps → Install Daydream Studio*). It then has its own window, a Start menu and desktop shortcut, and opens without the browser around it. After the first run, the app and its downloaded AI models work **offline**.

## Chat

The **Chat** tab talks to an AI running on your PC. Ask it to make a picture or a video and it creates one inside the conversation ("draw me…", "make a 3 second video of…", "now animate it").

| Source | Notes |
| --- | --- |
| **Free online** | Works anywhere, including phones, with nothing to install. Uses the free [Pollinations](https://pollinations.ai) text service (an open model). Not private: messages go to that service. |
| **Built in** (default) | Runs in the app on your GPU with [WebLLM](https://github.com/mlc-ai/web-llm). Models: Qwen 3.5 9B (6.4 GB), Qwen 3.5 4B (3.9 GB), Hermes 3 8B (4.9 GB), Llama 3.1 8B (5 GB). One-time download. |
| **Ollama** | Uses any model installed with [Ollama](https://ollama.com). Run `ollama pull <model>`, then `setx OLLAMA_ORIGINS "*"` and restart Ollama so the app can connect. |

**Characters**: chat with different AI personalities, like companions. Each has a name, an avatar (upload one or generate it from their appearance), a personality, a greeting and an optional voice that reads replies aloud. They can send pictures of themselves. Four starters are included (Daydream, Nova, Sage, Rook); create as many as you like with **+ New**.

**Memory**: when you mention something lasting (your name, likes, projects), the AI saves it under **Memory** and uses it in future chats with every character. You can add, remove or clear memories, or turn automatic memory off.

**Voice**: the speaker button reads replies aloud using a voice picked per character; the microphone button lets you talk instead of typing (uses the browser's online speech service).

Conversations are saved on your PC. **Custom instructions** let you set how the AI behaves. With **Free graphics memory for videos** on, the chat and image models are unloaded while ComfyUI makes a video so it gets the whole GPU.

When a local AI is loaded, **Ideas** and **Improve prompt** use it too instead of the online text service.

## Image engines

| Engine | Where it runs | Cost | Notes |
| --- | --- | --- | --- |
| **This PC** | Your graphics card, in the browser (WebGPU) | Free, unlimited | Z-Image Turbo, highly realistic. One-time 5.6 GB download, stored by the browser. Private: prompts and images never leave your PC. No safety checker. Chrome or Edge only. |
| **ComfyUI on this PC** | Your graphics card, in ComfyUI | Free, unlimited | The same Z-Image Turbo model running natively in ComfyUI: faster, and works in any browser including Firefox. Needs the 3 Z-Image files ([diffusion model](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors), [text encoder](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors), [VAE](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors)) and the CORS setting described under Video. |
| **Free online HD** (default) | Hugging Face's free shared GPUs | Free daily allowance | The same realistic Z-Image Turbo model as This PC, at 1024 px (1280×720 wide), via the public [mrfakename/Z-Image-Turbo](https://huggingface.co/spaces/mrfakename/Z-Image-Turbo) demo, with the official [Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/spaces/Tongyi-MAI/Z-Image-Turbo) demo as a backup. Works on phones. A free [Hugging Face token](https://huggingface.co/settings/tokens) gives more daily time; when the time runs out the app switches to Free online basic until it refills. |
| Free online basic | Pollinations | Free | Basic quality, 768 px, watermark, one image every 45 seconds |
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

Video settings: **Quick** (480p) or **Full 720p**, 2, 3 or 5 seconds.

### Video models

Pick under **Video model** in the Video tab:

| Model | Files | Notes |
| --- | --- | --- |
| **Wan 2.2 5B** | about 18 GB | Quicker to set up; 24 fps; 20 sampling steps |
| **Wan 2.2 14B** (best) | about 62 GB extra | The biggest open Wan model; better motion and prompt following. Uses the official lightx2v **4-step** LoRAs (two passes: high-noise then low-noise model), 16 fps. Text-to-video and image-to-video each need their own 4 files (about 31 GB each); image-to-video is used by Animate, storyboard pictures and Extend. |

The 14B files are the fp8 versions from [Comfy-Org/Wan_2.2_ComfyUI_Repackaged](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged); the full list with links is in the app under **Video engine → How to set up**. On a 16 GB card ComfyUI streams parts of the 14B model from system RAM, so 32 GB of RAM or more is recommended.

### Free online video (no PC needed)

Under **Video model → Free online** there are two models that run on Hugging Face's free shared GPUs, so they work anywhere, including on your phone:

- **LTX Video** ([Lightricks/ltx-video-distilled](https://huggingface.co/spaces/Lightricks/ltx-video-distilled)): text-to-video or image-to-video, fast, short clips.
- **Wan 2.2 14B Fast** ([zerogpu-aoti/wan2-2-fp8da-aoti-faster](https://huggingface.co/spaces/zerogpu-aoti/wan2-2-fp8da-aoti-faster)): animates a picture; with only a description, the app makes a picture first with your Image engine.

No free video service is truly unlimited: free online video always runs on someone's shared GPUs with a daily allowance. The only unlimited option is your own PC (ComfyUI). There's a free daily GPU allowance (shared with Free online HD images, which use very little): small without an account, more with a free [Hugging Face token](https://huggingface.co/settings/tokens) (Read access) pasted under **Video engine**. These are public demos, so they can be busy or change.

### Use from your phone

Your phone can make videos (and ComfyUI images) using your PC's GPU, at home or away, through [Tailscale](https://tailscale.com/download) (free):

1. Install Tailscale on the PC and the iPhone, signed in to the same account.
2. In the Tailscale admin console → DNS, turn on **MagicDNS** and **HTTPS Certificates**.
3. On the PC, run `tailscale serve --bg 8188` (your ComfyUI port). It prints an `https://<pc>.<tailnet>.ts.net` address.
4. On the phone, open Daydream, and enter that https address under **Video → Video engine → ComfyUI address**.

The phone needs the https address: browsers block a secure page from talking to plain `http://` addresses on other devices. The app explains this if you enter an `http://` address on a phone.

### Long videos

Choose **Video type → Long video** for 30 seconds up to 5 minutes. Video models make about 5 seconds at a time, so the app makes many 5-second clips and joins them into one file (with [ffmpeg.wasm](https://github.com/ffmpegwasm/ffmpeg.wasm)):

- **Storyboard**: the AI plans a shot list from your idea, with characters and setting described the same way in every shot. With **Make a picture for each shot first**, each shot is drawn with your Image engine and then animated, for sharper, more consistent results.
- **Extend**: one continuous shot; each clip starts from the last frame of the previous one. Details slowly drift over long lengths.

Progress is saved after every step: press **Stop** any time, close the app, and **Resume** later from the Video tab. A 2-minute video is 24 clips, so expect hours on a home GPU; it suits an overnight run.

You can also ask a character in Chat for a long video ("make me a 2 minute video about…"); it sets it up in the Video tab for you.

## Other features

- **Help**: setup guides and tips live in one Help panel (header button, or the small **?** next to a setting opens the matching section)

- **Light, dark or auto theme**: the button in the header switches between Auto (follows Windows), Light and Dark

- **Look presets** and an **Extra realism** switch for photographic results
- **Improve prompt** rewrites a short idea into a detailed prompt (free Pollinations text service)
- **Ideas** mode brainstorms 6 ideas with a **Picture this** button on each
- Everything you make is saved in the browser's gallery, with full-size viewing and download
- **Favourites**: star your best images, filter the gallery, and **Export favourites** as a zip of images with matching `.txt` prompt captions, the layout LoRA training tools expect
