#!/bin/bash
# Installs ComfyUI v0.44.1 + Pixal3D (multi-view, INT8) the way it runs on our RTX 2080 Ti box (since 06.11.2026).
#   COMFY_BASE=~/comfy ./install.sh          (needs git, curl, uv; NVIDIA driver with CUDA 12.8 support)
# Afterwards: python3 ../img23d.py --views front.png side.png back.png --out figur.glb
set -euo pipefail
B=${COMFY_BASE:-$HOME/comfy}
mkdir -p "$B" && cd "$B"
echo "== ComfyUI v0.44.1 (we used commit 49b61c3)"
[ -d ComfyUI ] || git clone --depth 1 --branch v0.44.1 https://github.com/Comfy-Org/ComfyUI.git ComfyUI
git -C ComfyUI rev-parse HEAD
echo "== venv (Python 3.12) + torch 2.11 cu128"
[ -d venv ] || uv venv --python 3.12 venv
. venv/bin/activate
uv pip install torch==2.11.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
uv pip install -r ComfyUI/requirements.txt
echo "== models (Hugging Face Comfy-Org, about 9.3 GB)"
M=ComfyUI/models
mkdir -p $M/diffusion_models $M/vae $M/clip_vision $M/background_removal
dl() { [ -s "$2" ] && { echo "have $2"; return; }; curl -fSL -o "$2.part" "$1" && mv "$2.part" "$2" && ls -l "$2"; }
H=https://huggingface.co/Comfy-Org/Pixal3D/resolve/main
dl $H/diffusion_models/pixal3d_multiview_int8_convrot.safetensors $M/diffusion_models/pixal3d_multiview_int8_convrot.safetensors
dl $H/vae/trellis_2_shape_vae_bf16.safetensors                     $M/vae/trellis_2_shape_vae_bf16.safetensors
dl $H/vae/trellis_2_texture_vae_bf16.safetensors                   $M/vae/trellis_2_texture_vae_bf16.safetensors
dl $H/clip_vision/dino_v3_L_naf_fp32.safetensors                   $M/clip_vision/dino_v3_L_naf_fp32.safetensors
dl https://huggingface.co/Comfy-Org/BiRefNet/resolve/main/background_removal/birefnet.safetensors $M/background_removal/birefnet.safetensors
echo "== done. Expected sizes: pixal3d 5.58 GB, shape VAE 1.10 GB, texture VAE 0.95 GB, DINOv3 1.22 GB, BiRefNet 0.44 GB"
