# Voxtral Mini 4B Realtime — Model Setup

After installing the `voxtral-mini-realtime-rs` package, you need to download model weights separately.

## F32 (full precision, ~9 GB)

Requires a HuggingFace account with access to the gated model. Accept the license at
https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602 first, then:

```bash
uvx hf auth login
uvx hf download mistralai/Voxtral-Mini-4B-Realtime-2602 --local-dir ~/models/voxtral
```

### Run

```bash
voxtral-transcribe \
  --audio recording.wav \
  --safetensors ~/models/voxtral/consolidated.safetensors \
  --tokenizer ~/models/voxtral/tekken.json
```

GPU requirement: ~9.2 GB VRAM (Vulkan). Any 12 GB+ GPU works.

## Q4 GGUF (quantized, ~2.5 GB)

```bash
uvx hf download TrevorJS/voxtral-mini-realtime-gguf voxtral-q4.gguf --local-dir ~/models
```

### Run

```bash
voxtral-transcribe \
  --audio recording.wav \
  --gguf ~/models/voxtral-q4.gguf \
  --tokenizer ~/models/voxtral/tekken.json
```

GPU requirement: ~700 MB VRAM. Runs ~4x faster than f32 but slightly higher word error rate (8.5% vs 4.9%).

## Verify GPU access

```bash
vulkaninfo --summary
```

If this fails, install your GPU's Vulkan driver (`mesa-vulkan-drivers` for AMD/Intel, `nvidia-gpu-firmware` + `akmod-nvidia` for NVIDIA).
