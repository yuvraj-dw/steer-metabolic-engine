# Steer Metabolic Health Engine

An evidence-backed metabolic health engagement and content automation suite built for [Steer](https://steerclub.com) (October 2026).

---

## Architecture Overview

This repository solves both hackathon challenges with zero-friction, production-ready code:

### 1. The Willpower Defense Arcade (`playable_ad.html`)
* **Objective:** Replace cold lead forms with a tactile, 60fps mobile simulation illustrating why willpower fails at 4:00 PM and how incretin biology (GLP-1) restores satiety.
* **Technology:** Pure HTML5 Canvas + Web Audio API (100% client-side synthetic audio with zero external asset dependencies).
* **Viral Mechanic:** 1-click Instagram Story receipt export (`downloadStoryCard`), clinical doubt clearance accordion, and non-intrusive doctor consultation handoff.

### 2. Research-to-Social Automation Pipeline (`pipeline/`)
An end-to-end Python pipeline that ingests peer-reviewed clinical research (via local JSON schemas or live NCBI PubMed IDs) and turns them into ready-to-publish medical social assets:
* **4-Slide Apple-Grade Carousels (1080×1350):** Dynamic metric callouts, neuro-endocrine mechanisms, and Steer's 4-pillar exit off-ramp.
* **Static Editorial Infographics (1080×1350):** High-status medical journal aesthetic comparing traditional caloric restriction vs. doctor-led biomarker care.
* **AI Video Reels (1080×1920, 9:16):** Study-specific scripts, neural voiceover (ElevenLabs `eleven_multilingual_v2` / Edge Neural), 30fps fluid kinetic telemetry, and horizontal push slide transitions strictly respecting Meta Reels UI safe zones.
* **Doctor Review Gate (`doctor_review_gate.json`):** Cryptographically maps every social claim to its source DOI, p-value, and sample size for <60s clinical audit.
* **Hinglish Mode & 7-Day Batch Engine:** Generates natural conversational Indian Hinglish copy and batch-schedules weekly multi-format releases.

---

## Directory Structure

```text
├── playable_ad.html             # Standalone Meta playable ad / mobile prototype
├── pipeline/
│   ├── schema.py                # Clinical study & claim dataclass schemas
│   ├── ingest.py                # Study ingestion & doctor review gate builder
│   ├── fetcher.py               # Live NCBI PubMed API abstract fetcher
│   ├── visuals_engine_apple.py  # 1080x1350 Apple-crafted carousel generator
│   ├── visuals_engine.py        # Static infographic generator
│   ├── reel_engine_production.py# 1080x1920 9:16 safe-zone compliant video engine
│   ├── voice_engine.py          # ElevenLabs / Microsoft neural voiceover engine
│   ├── hinglish.py              # Clinical translation to conversational Hinglish
│   ├── batch_scheduler.py       # Multi-paper 7-day social release engine
│   ├── runner.py                # Unified pipeline CLI entrypoint
│   └── cli.py                   # Legacy command-line interface
└── papers/                      # Peer-reviewed study summaries (NEJM, Lancet, DOM)
```

---

## Quickstart

### Prerequisites
* Python 3.10+
* `ffmpeg` (for reel video compilation)

### Dependencies
```bash
pip install pillow edge-tts pytest
```
*(Optional: set `ELEVENLABS_API_KEY` in environment for ultra-realistic neural voiceover)*

### Running the Pipeline

**1. Run End-to-End for Any Clinical Paper:**
```bash
python -m pipeline.runner --paper papers/surpass2_tirzepatide_2021.json --output output/surpass2
```

**2. Fetch Live from NCBI PubMed by PMID:**
```bash
python -m pipeline.runner --pmid 33567185 --output output/pubmed_step1
```

**3. Generate 7-Day Batch Social Calendar:**
```bash
python -m pipeline.batch_scheduler
```

**4. Launch the Playable Ad:**
Open `playable_ad.html` directly in any modern mobile or desktop web browser.

---

## License
MIT
