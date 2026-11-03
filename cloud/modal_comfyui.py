"""Daydream cloud GPU: ComfyUI on Modal, so Daydream can make images and videos with your PC off.

- Starts by itself when Daydream sends a job and shuts down after a few idle minutes
  (Modal bills by the second; the free Starter plan includes monthly credit).
- Model files are downloaded once into a Modal Volume ("daydream-models").
- A password gate (daydream_proxy.py) sits in front of ComfyUI. Your Daydream address is:
      https://<your-workspace>--daydream-comfy.modal.run/k/<your password>

Deploy from GitHub: Actions -> "Cloud GPU (Modal)" -> Run workflow.
Or from a computer: `modal deploy cloud/modal_comfyui.py`, then
`modal run cloud/modal_comfyui.py::download_models --sets images,video14b`.
"""
import os
import subprocess
import sys
from pathlib import Path

import modal

GPU = os.environ.get("DAYDREAM_GPU", "L40S")
IDLE_MINUTES = int(os.environ.get("DAYDREAM_IDLE_MINUTES", "5"))
MODELS_DIR = "/models"
COMFY_DIR = "/root/comfy/ComfyUI"

WAN22 = "Comfy-Org/Wan_2.2_ComfyUI_Repackaged"
WAN21 = "Comfy-Org/Wan_2.1_ComfyUI_repackaged"
ZIMG = "Comfy-Org/z_image_turbo"
# (Hugging Face repo, file in the repo, ComfyUI models folder) - the same files Daydream asks for on a PC.
MODEL_SETS = {
    "images": [
        (ZIMG, "split_files/diffusion_models/z_image_turbo_bf16.safetensors", "diffusion_models"),
        (ZIMG, "split_files/text_encoders/qwen_3_4b.safetensors", "text_encoders"),
        (ZIMG, "split_files/vae/ae.safetensors", "vae"),
    ],
    "video14b": [
        (WAN21, "split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors", "text_encoders"),
        (WAN22, "split_files/vae/wan_2.1_vae.safetensors", "vae"),
        (WAN22, "split_files/diffusion_models/wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "diffusion_models"),
        (WAN22, "split_files/diffusion_models/wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "diffusion_models"),
        (WAN22, "split_files/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "loras"),
        (WAN22, "split_files/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "loras"),
        (WAN22, "split_files/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors", "diffusion_models"),
        (WAN22, "split_files/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors", "diffusion_models"),
        (WAN22, "split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors", "loras"),
        (WAN22, "split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors", "loras"),
    ],
    "video5b": [
        (WAN21, "split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors", "text_encoders"),
        (WAN22, "split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors", "diffusion_models"),
        (WAN22, "split_files/vae/wan2.2_vae.safetensors", "vae"),
    ],
}

EXTRA_PATHS = f"""daydream:
  base_path: {MODELS_DIR}
  diffusion_models: diffusion_models
  text_encoders: text_encoders
  vae: vae
  loras: loras
"""

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git", "ffmpeg", "libgl1", "libglib2.0-0")
    .uv_pip_install("comfy-cli", "aiohttp", "huggingface_hub[hf_xet]")
    .run_commands("comfy --skip-prompt install --fast-deps --nvidia")
    .env({"HF_XET_HIGH_PERFORMANCE": "1"})
    .add_local_file(Path(__file__).parent / "daydream_proxy.py", "/root/daydream_proxy.py")
)

app = modal.App("daydream", image=image)
models = modal.Volume.from_name("daydream-models", create_if_missing=True)


@app.function(volumes={MODELS_DIR: models}, timeout=3 * 60 * 60, cpu=4, memory=4096)
def download_models(sets: str = "images,video14b"):
    """Downloads the model files into the Modal Volume (skips any already there). Runs on a cheap CPU machine."""
    from huggingface_hub import hf_hub_download

    wanted = []
    for name in [s.strip() for s in sets.split(",") if s.strip() and s.strip() != "none"]:
        if name not in MODEL_SETS:
            sys.exit(f"Unknown model set {name!r}. Use any of: {', '.join(MODEL_SETS)}")
        wanted += [m for m in MODEL_SETS[name] if m not in wanted]
    for repo, file, folder in wanted:
        dest = Path(MODELS_DIR) / folder / Path(file).name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"already there: {folder}/{dest.name}")
            continue
        print(f"downloading {folder}/{dest.name} ...", flush=True)
        staging = Path(MODELS_DIR) / "_downloading"
        got = Path(hf_hub_download(repo, file, local_dir=staging))
        dest.parent.mkdir(parents=True, exist_ok=True)
        got.rename(dest)
        models.commit()
        print(f"  done ({dest.stat().st_size / 1e9:.1f} GB)", flush=True)
    subprocess.run(["rm", "-rf", f"{MODELS_DIR}/_downloading"])
    models.commit()
    print("All model files are ready.")


@app.function(
    gpu=GPU,
    volumes={MODELS_DIR: models},
    secrets=[modal.Secret.from_name("daydream-key")],
    scaledown_window=IDLE_MINUTES * 60,
    timeout=60 * 60,
    max_containers=1,
    memory=24576,
)
@modal.concurrent(max_inputs=100)
@modal.web_server(8000, startup_timeout=300, label="daydream-comfy")
def comfy():
    Path(COMFY_DIR, "extra_model_paths.yaml").write_text(EXTRA_PATHS)
    # ComfyUI listens only inside the container; the password gate is the public door.
    subprocess.Popen(
        [sys.executable, "main.py", "--listen", "127.0.0.1", "--port", "8188", "--enable-cors-header", "*", "--disable-auto-launch"],
        cwd=COMFY_DIR,
    )
    subprocess.Popen([sys.executable, "/root/daydream_proxy.py"])
