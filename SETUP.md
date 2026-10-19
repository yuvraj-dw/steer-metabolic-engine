# 🚀 Steer Metabolic Engine — Quick Setup Guide

Set up and run the Steer Metabolic Engine anywhere (macOS, Windows, Linux, or Docker) in under **60 seconds**.

---

## ⚡ Option 1: Universal 1-Command Setup (Recommended)

### **On macOS / Linux:**
```bash
git clone https://github.com/yuvraj-dw/steer-metabolic-engine.git
cd steer-metabolic-engine

chmod +x setup.sh && ./setup.sh
```

### **On Windows:**
Double-click `setup.bat` or run:
```cmd
git clone https://github.com/yuvraj-dw/steer-metabolic-engine.git
cd steer-metabolic-engine

python setup_pipeline.py
```

`setup_pipeline.py` automatically:
1. Verifies Python runtime ($\ge 3.10$).
2. Detects or guides FFmpeg installation.
3. Installs all required packages via `pip`.
4. Audits 19/19 medical claims against source DOIs.
5. Runs a smoke test generating a complete 1080×1080 Instagram carousel.

---

## 🐳 Option 2: Run via Docker (Zero Environment Friction)

If you have Docker installed, you don't even need Python or FFmpeg installed on your host:

```bash
# Build & run dashboard on http://localhost:8000
docker-compose up --build
```
Or with standard Docker CLI:
```bash
docker build -t steer-engine .
docker run -p 8000:8000 -v $(pwd)/output:/app/output steer-engine
```

Open `http://localhost:8000/doctor_review_board.html` in your browser.

---

## 🎯 Running the Pipeline

Use the unified master runner `run_pipeline.py`:

```bash
# 1. Ingest a paper live from NCBI PubMed by PMID:
python run_pipeline.py --pmid 37952131

# 2. Process all pre-loaded clinical studies in batch:
python run_pipeline.py --all

# 3. Process a specific landmark study:
python run_pipeline.py --study lancet_tofi
python run_pipeline.py --study surpass2
python run_pipeline.py --study step1_ext

# 4. Package 1-click social publishing ZIP bundles:
python run_pipeline.py --zip

# 5. Launch the visual Doctor Review Board & Content Dashboard locally:
python run_pipeline.py --serve
```

---

## 🎨 Asset Outputs & Dimensions

Every run produces publication-ready assets inside `output/posts/<study_slug>/`:
* **Instagram Carousel:** `carousel/carousel_slide_{1-4}.png` (**1080 × 1080 px Square format**, 1:1 Aspect Ratio).
* **Social Copy & Captions:** `hinglish_script.md` (English feed caption + Hinglish viral reel copy).
* **Doctor Review Gate:** `doctor_review_gate.json` (19 verified claims mapped to sentence coordinates and DOIs).
* **Social Publishing Bundle:** `output/steer-<study>-publishing-bundle.zip` (1-click archive containing all slides, scripts, and receipts).

---

## 🧪 Testing & Verification

Run the automated test suite anywhere:
```bash
pytest
python -m pipeline.verify_claims
```
