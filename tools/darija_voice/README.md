# Snay3i Darija Voice Factory

This folder contains a GitHub Actions proof of concept for generating Moroccan Darija voiceovers with the open HADRA model (`Jip7e/habibi-tts-doda-darija`).

## Why this setup

- Uses a model fine-tuned specifically for Moroccan Darija.
- Uses Habibi-TTS's bundled Moroccan reference voice (`MAR.mp3`) instead of storing a voice sample in this repository.
- Runs on GitHub Actions so the first prototype does not require a dedicated server.
- Produces a WAV artifact that can later be fed into the Snay3i Shorts/video pipeline.

## Test text

The initial workflow test uses:

> واش كتقلب على بلومبي مزيان فكازا وما عارفش منين تبدا؟ دخل لسنّايعي دوت ما، وقلب على الحرفي اللي قريب ليك.

## Workflow

`Darija Voice Factory Test` runs automatically when this test branch changes and can later be triggered manually with custom Darija text.

The generated audio is uploaded as the `snay3i-darija-voice` workflow artifact.

## Live-site safety

This work lives on the `darija-voice-factory` branch while it is being tested. It does not change or deploy the live Snay3i backend unless deliberately merged into `main` later.
