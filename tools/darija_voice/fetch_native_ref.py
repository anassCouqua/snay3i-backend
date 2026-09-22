#!/usr/bin/env python3
import argparse
from pathlib import Path

from datasets import load_dataset
from huggingface_hub import hf_hub_download

DATASET = "abnajlae/darija-asr-corpus"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True)
    p.add_argument("--speaker", default="M2")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    ds = load_dataset(DATASET, "doda", split="train", streaming=True)
    match = None
    for row in ds:
        text = (row.get("utteranceText") or row.get("utteranceTextArabic") or "").strip()
        speaker = (row.get("speakerName") or "").strip()
        if text == args.text.strip() and speaker == args.speaker:
            match = row
            break

    if match is None:
        raise SystemExit(f"No exact {args.speaker} reference found for: {args.text}")

    audio_path = match["audioPath"]
    print("Found reference:", match.get("fileName"), match.get("speakerName"), audio_path)
    downloaded = hf_hub_download(
        repo_id=DATASET,
        repo_type="dataset",
        filename=audio_path,
    )
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(Path(downloaded).read_bytes())
    print("Saved:", out)

if __name__ == "__main__":
    main()
