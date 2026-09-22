#!/usr/bin/env python3
import argparse
from pathlib import Path

import soundfile as sf
import torch
from f5_tts.infer.utils_infer import load_model, load_vocoder, preprocess_ref_audio_text, infer_process
from f5_tts.model import DiT
from huggingface_hub import hf_hub_download

REPO_ID = "Jip7e/habibi-tts-doda-darija"

PERSONAS = {
    "amine": {
        "speaker": "M1",
        "ref_text": "يمكن ما كيعجبكش الطيران من هادشي كلو",
        "ref_file": "amine.wav",
    },
    "yassine": {
        "speaker": "M3",
        "ref_text": "يبان ليا غايجينا جواب اسرع من الناس لي فالاستقبال",
        "ref_file": "yassine.wav",
    },
    "kenza": {
        "speaker": "F3",
        "ref_text": "نستافدو من المدينة وداكشي لي تقدر تعطي",
        "ref_file": "kenza.wav",
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--refs-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--speed", type=float, default=0.92)
    ap.add_argument("--nfe", type=int, default=16)
    args = ap.parse_args()

    refs_dir = Path(args.refs_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ckpt_path = hf_hub_download(repo_id=REPO_ID, filename="model_ema.safetensors")
    vocab_path = hf_hub_download(repo_id=REPO_ID, filename="vocab.txt")

    cfg = dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4)
    model = load_model(DiT, cfg, ckpt_path, vocab_file=vocab_path)
    vocoder = load_vocoder("vocos")

    device_type = "cuda" if torch.cuda.is_available() else "cpu"

    for name, persona in PERSONAS.items():
        ref_audio = refs_dir / persona["ref_file"]
        if not ref_audio.exists():
            raise FileNotFoundError(ref_audio)

        ra, rt = preprocess_ref_audio_text(str(ref_audio), persona["ref_text"])
        print(f"Generating {name} ({persona['speaker']})...")

        autocast_ctx = torch.autocast(device_type=device_type, dtype=torch.bfloat16) if device_type == "cpu" else torch.autocast(device_type="cuda", dtype=torch.float16)
        with autocast_ctx:
            wav, sr, _ = infer_process(
                ra,
                rt,
                args.target,
                model,
                vocoder,
                speed=args.speed,
                nfe_step=args.nfe,
                cfg_strength=2.0,
                sway_sampling_coef=-1.0,
            )

        out = out_dir / f"snay3i-darija-{name}.wav"
        sf.write(out, wav, sr)
        print(f"Saved {out} @ {sr} Hz")


if __name__ == "__main__":
    main()
