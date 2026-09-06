#!/usr/bin/env python3
# Snay3i Moroccan Darija voice factory test runner.
import argparse
from contextlib import nullcontext
from importlib.resources import files
from pathlib import Path

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
    parser.add_argument("--speed", type=float, default=0.93, help="Speech speed")
    parser.add_argument("--nfe", type=int, default=16, help="Flow-matching inference steps")
    return parser.parse_args()


def main():
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Downloading HADRA model weights and vocabulary...")
    ckpt_path = hf_hub_download(repo_id=MODEL_REPO, filename="model_ema.safetensors")
    vocab_path = hf_hub_download(repo_id=MODEL_REPO, filename="vocab.txt")

    # Habibi-TTS ships a clean Moroccan/Darija reference clip. Using a bundled
    # reference keeps the workflow self-contained and avoids storing voice files
    # in the Snay3i repository.
    ref_audio = files("habibi_tts").joinpath("assets/MAR.mp3")
    if not ref_audio.is_file():
        raise FileNotFoundError(f"Bundled Moroccan reference audio not found: {ref_audio}")

    print(f"Using Moroccan reference voice: {ref_audio}")
    print("Loading HADRA model...")
    cfg = dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4)
    model = load_model(DiT, cfg, ckpt_path, vocab_file=vocab_path)
    vocoder = load_vocoder("vocos")

    ra, rt = preprocess_ref_audio_text(str(ref_audio), MAR_REF_TEXT)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running inference on {device}...")
    ctx = torch.autocast(device_type="cuda", dtype=torch.float16) if device == "cuda" else nullcontext()
    with ctx:
        wav, sr, _ = infer_process(
            ra,
            rt,
            args.text,
            model,
            vocoder,
            speed=args.speed,
            nfe_step=args.nfe,
            cfg_strength=2.0,
            sway_sampling_coef=-1.0,
        )

    sf.write(output_path, wav, sr)
    print(f"Generated {output_path} at {sr} Hz")


if __name__ == "__main__":
    main()
