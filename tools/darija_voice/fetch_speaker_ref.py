#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from datasets import load_dataset
from huggingface_hub import hf_hub_download

DATASET="abnajlae/darija-asr-corpus"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--speaker", required=True)
    p.add_argument("--audio-out", required=True)
    p.add_argument("--text-out", required=True)
    args=p.parse_args()

    ds=load_dataset(DATASET, "doda", split="train", streaming=True)
    for row in ds:
        if (row.get("speakerName") or "").strip()==args.speaker:
            text=(row.get("utteranceText") or row.get("utteranceTextArabic") or "").strip()
            audio_path=row["audioPath"]
            downloaded=hf_hub_download(repo_id=DATASET, repo_type="dataset", filename=audio_path)
            Path(args.audio_out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.audio_out).write_bytes(Path(downloaded).read_bytes())
            Path(args.text_out).write_text(text, encoding="utf-8")
            print(json.dumps({"speaker":args.speaker,"text":text,"audioPath":audio_path}, ensure_ascii=False))
            return
    raise SystemExit(f"No sample found for {args.speaker}")

if __name__=="__main__":
    main()
