# Snay3i Darija Voice Plugin

Experimental Moroccan Darija pronunciation layer for ChatGPT and TTS workflows.

## Why

Generic Arabic TTS often reads Moroccan Darija as MSA, mispronounces loanwords, or inserts unnatural vowels. This plugin separates the language layer from the voice provider.

## Tools

- `normalize_darija` — conservative spoken-Moroccan rewrites.
- `phonetic_darija` — explicit Darija-oriented tashkeel from a curated lexicon.
- `prepare_darija_for_tts` — combines both and returns TTS-ready text plus pacing hints.

## Run

```bash
pip install -r darija_plugin/requirements.txt
python darija_plugin/server.py
```

The MCP endpoint is exposed using Streamable HTTP, normally at `/mcp`.

## Development rule

Never auto-add pronunciation rules based only on spelling. Add a word to the lexicon after a Moroccan speaker has listened to the generated audio and confirmed the intended reading.
