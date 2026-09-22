#!/usr/bin/env python3
# Snay3i Moroccan Darija voice factory.
import argparse
import re
from contextlib import nullcontext
from importlib.resources import files
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from huggingface_hub import hf_hub_download
from f5_tts.infer.utils_infer import (
    infer_process,
    load_model,
    load_vocoder,
    preprocess_ref_audio_text,
)
from f5_tts.model import DiT

MODEL_REPO = "Jip7e/habibi-tts-doda-darija"
MAR_REF_TEXT = "إذا بغيتي شي صوت باللهجة المغربية للإعلانات ديالك هذا أحسن واحد غادي تلقاه."

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Moroccan Darija speech with HADRA")
    parser.add_argument("--text", required=True, help="Darija text to synthesize")
    parser.add_argument("--output", default="output/darija.wav", help="Output WAV path")
    parser.add_argument("--speed", type=float, default=0.98, help="Speech speed")
    parser.add_argument("--nfe", type=int, default=16, help="Flow-matching inference steps")
    parser.add_argument("--pause", type=float, default=0.10, help="Pause between spoken chunks in seconds")
    parser.add_argument("--ref-audio", default=None, help="Optional reference-speaker audio file")
    parser.add_argument("--ref-text", default=None, help="Verbatim transcript for --ref-audio")
    return parser.parse_args()

def spoken_chunks(text: str):
    # Short sentence-sized chunks give HADRA much more natural Moroccan pacing
    # than one long advertising paragraph.
    chunks = re.split(r'(?<=[.!?؟])\s+', text.strip())
    return [c.strip() for c in chunks if c.strip()]

def main():
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Downloading HADRA model weights and vocabulary...")
    ckpt_path = hf_hub_download(repo_id=MODEL_REPO, filename="model_ema.safetensors")
    vocab_path = hf_hub_download(repo_id=MODEL_REPO, filename="vocab.txt")

    if args.ref_audio:
        ref_audio = Path(args.ref_audio)
        ref_text = args.ref_text
        if not ref_text:
            raise ValueError("--ref-text is required when --ref-audio is supplied")
    else:
        ref_audio = files("habibi_tts").joinpath("assets/MAR.mp3")
        ref_text = MAR_REF_TEXT
    if not ref_audio.is_file():
        raise FileNotFoundError(f"Moroccan reference audio not found: {ref_audio}")

    print(f"Using Moroccan reference voice: {ref_audio}")
    print("Loading HADRA model...")
    cfg = dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4)
    model = load_model(DiT, cfg, ckpt_path, vocab_file=vocab_path)
    vocoder = load_vocoder("vocos")
    ra, rt = preprocess_ref_audio_text(str(ref_audio), ref_text)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    chunks = spoken_chunks(args.text)
    print(f"Running inference on {device} in {len(chunks)} conversational chunks...")
    audio_parts = []
    sr = None
    ctx = torch.autocast(device_type="cuda", dtype=torch.float16) if device == "cuda" else nullcontext()
    with ctx:
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}: {chunk}")
            wav, chunk_sr, _ = infer_process(
                ra,
                rt,
                chunk,
                model,
                vocoder,
                speed=args.speed,
                nfe_step=args.nfe,
                cfg_strength=2.0,
                sway_sampling_coef=-1.0,
            )
            sr = chunk_sr
            audio_parts.append(wav)
            if i < len(chunks) - 1:
                audio_parts.append(np.zeros(int(sr * args.pause), dtype=wav.dtype))

    if not audio_parts or sr is None:
        raise RuntimeError("No audio generated")
    wav = np.concatenate(audio_parts)
    sf.write(output_path, wav, sr)
    print(f"Generated {output_path} at {sr} Hz")

if __name__ == "__main__":
    main()
