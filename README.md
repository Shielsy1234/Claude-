# Daydream Studio

Type what you're picturing and get a realistic image, a video, or a page of ideas.

Everything is in one file, `index.html`. Host it with GitHub Pages (recommended) or any static web server. The **This PC** engine needs the page to be opened from a web address (`https://…` or `http://localhost`), not by double-clicking the file.

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
