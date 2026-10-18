# Steer Metabolic Health Engine

An evidence-backed metabolic health engagement and content automation suite built for [Steer](https://steerclub.com) (October 2026).

---

## 🌐 Live Deployments

* **Playable Ad Arcade:** [https://yuvraj-dw.github.io/steer-metabolic-engine/](https://yuvraj-dw.github.io/steer-metabolic-engine/)
* **Doctor Review Board & Ingestion Studio:** [https://yuvraj-dw.github.io/steer-metabolic-engine/doctor_review_board.html](https://yuvraj-dw.github.io/steer-metabolic-engine/doctor_review_board.html)

---

## Architecture Overview

This repository solves both hackathon challenges with zero-friction, production-ready code:

### 1. The Willpower Defense Arcade (`playable_ad.html` / `index.html`)
* **Objective:** Replace cold lead forms with a tactile, 60fps mobile simulation illustrating why willpower fails at 4:00 PM and how incretin biology (GLP-1) restores satiety.
* **Technology:** Pure HTML5 Canvas + Web Audio API (100% client-side synthetic audio with zero external asset dependencies).
* **Responsive Layout:** Full-bleed `100dvh` responsive stack with zero artificial phone bezels; touch, pointer, WASD, and arrow controls.
* **Interactive Tooling:** STEP-1 Rebound Simulator, dynamic worry selector, 1-click clipboard doctor intake brief export, and Instagram Story receipt card generator.

### 2. Research-to-Social Automation Pipeline (`pipeline/`)
An end-to-end Python pipeline that ingests peer-reviewed clinical research (via local JSON schemas or live NCBI PubMed IDs) and turns them into ready-to-publish medical social assets:
* **Stop-Motion Papercut Explainer Reels (1080×1920, 9:16):** Remotion & Headless Chrome diorama engine rendering tactile papercut cutouts, dynamic trial telemetry, ElevenLabs forced word-level timestamp alignment (`/with-timestamps`), procedural foley sound effects, and strict Meta Reels safe zones.
* **Study-Tailored 4-Slide Apple Carousels (1080×1350):** Dynamic metric callouts, neuro-endocrine and vascular diagrams, and Steer's structured 4-pillar exit off-ramp.
* **Interactive Doctor Review Board (`doctor_review_board.html`):** Ingest PMID/DOI directly, audit 16 clinical claims with sentence-level coordinates, review live study reels, and inspect conversational Hinglish scripts.
* **Deterministic Claim Auditor (`pipeline/verify_claims.py`):** Cryptographically maps every social claim to its source DOI, p-value, and sample size for zero-hallucination compliance.
* **Hinglish Mode & 7-Day Batch Engine:** Generates natural conversational Indian Hinglish copy and batch-schedules weekly multi-format releases.

---

## Directory Structure

```text
├── index.html                   # Mobile-first interactive arcade (GitHub Pages root)
├── playable_ad.html             # Standalone Meta playable ad / mobile prototype
├── doctor_review_board.html     # Doctor Review Gate & Multi-Study Ingestion Studio
├── pipeline/
│   ├── schema.py                # Clinical study & claim dataclass schemas
│   ├── ingest.py                # Study ingestion & doctor review gate builder
│   ├── fetcher.py               # Live NCBI PubMed API abstract fetcher
│   ├── papercut_engine.py       # Universal Remotion stop-motion reel engine
│   ├── visuals_engine_apple.py  # 1080x1350 Apple-crafted carousel generator
│   ├── visuals_engine.py        # Static editorial infographic generator
│   ├── verify_claims.py         # Deterministic claim & citation integrity auditor
│   ├── voice_engine.py          # ElevenLabs / Microsoft neural voiceover engine
│   ├── hinglish.py              # Clinical translation to conversational Hinglish
│   ├── batch_scheduler.py       # Multi-paper 7-day social release engine
│   └── runner.py                # Unified multi-study pipeline runner
├── papers/                      # Peer-reviewed study summaries (NEJM, Lancet, BMJ, DOM)
└── tests/                       # Comprehensive pytest suite (14 passing tests)
```

---

## Quickstart

### Prerequisites
* Python 3.10+
* `ffmpeg` (for reel compilation)
* Node.js & Bun (for Remotion diorama rendering)

### Dependencies
```bash
pip install pillow edge-tts pytest requests
```
*(Optional: set `ELEVENLABS_API_KEY` in environment for neural voiceover with exact word alignments)*

### Running the Pipeline

**1. Run End-to-End for Any Clinical Paper:**
```bash
python -m pipeline.runner --paper papers/surpass2_tirzepatide_2021.json --output output/surpass2
```

**2. Fetch Live from NCBI PubMed by PMID:**
```bash
python -m pipeline.runner --pmid 33567185 --output output/pubmed_step1
```

**3. Run Deterministic Claim Audit:**
```bash
python -m pipeline.verify_claims
```

**4. Run Test Suite:**
```bash
pytest -v
```

**5. Launch the Playable Ad Arcade:**
Open `index.html` or `playable_ad.html` directly in any modern mobile or desktop web browser.

---

## License
MIT
