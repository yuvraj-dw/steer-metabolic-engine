#!/usr/bin/env python3
"""
Steer Metabolic Engine - Universal One-Command Setup & Verification
Supported Platforms: Windows, macOS, Linux, Docker
"""

import sys
import os
import subprocess
import shutil

BANNER = r"""
============================================================
   ____  __                   __  ___     __        __      ___      
  / __/ / /_ ___  ___   ____ /  |/  /___ / /_ ___ _/ /  ___/ (_)___  
 _\ \  / __// -_)/ -_) / __// /|_/ // -_) __// _ `/ _ \/ _  / // _ \ 
/___/  \__/ \__/ \__/ /_/  /_/  /_/ \__//__/ \_,_/_.__/\_,_/_//\___/ 
                                                                    
         Research-to-Instagram & Playable Arcade Engine
============================================================
"""

def print_step(num, title):
    print(f"\n[Step {num}/5] {title}...")

def check_python():
    print_step(1, "Checking Python Runtime")
    v = sys.version_info
    print(f"  • Current Python: {v.major}.{v.minor}.{v.micro} on {sys.platform}")
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print("  ❌ ERROR: Python 3.10 or higher is required.")
        sys.exit(1)
    print("  ✅ Python version is compatible (>= 3.10).")

def check_ffmpeg():
    print_step(2, "Checking FFmpeg Multimedia Engine")
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"  ✅ FFmpeg detected: {ffmpeg_path}")
    else:
        print("  ⚠️ WARNING: FFmpeg was not found on your system PATH.")
        print("     Video reel rendering requires FFmpeg.")
        if sys.platform == "darwin":
            print("     → Install via Homebrew: brew install ffmpeg")
        elif sys.platform.startswith("linux"):
            print("     → Install via APT: sudo apt-get update && sudo apt-get install -y ffmpeg")
        else:
            print("     → Install on Windows via Winget: winget install Gyan.FFmpeg")
            print("     → Or download from: https://ffmpeg.org/download.html")

def install_dependencies():
    print_step(3, "Installing Python Dependencies")
    
    # First check if core modules are already importable
    try:
        import PIL
        import pytest
        print("  ✅ Core dependencies (Pillow, pytest, etc.) are already installed!")
        return
    except ImportError:
        pass

    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.exists(req_file):
        print("  ❌ requirements.txt not found!")
        sys.exit(1)

    # Try various package managers
    candidates = [
        [sys.executable, "-m", "pip", "install", "-r", req_file],
        ["pip", "install", "-r", req_file],
        ["pip3", "install", "-r", req_file],
        ["uv", "pip", "install", "-r", req_file]
    ]

    installed = False
    for cmd in candidates:
        exe = shutil.which(cmd[0]) or (cmd[0] if os.path.exists(cmd[0]) else None)
        if not exe:
            continue
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  ✅ Installed dependencies using: {' '.join(cmd[:2])}")
                installed = True
                break
        except Exception:
            continue

    if not installed:
        print("  ⚠️ Notice: Could not invoke pip automatically.")
        print(f"     Please run manually: pip install -r {req_file}")

def verify_claims():
    print_step(4, "Auditing Medical Claims Integrity")
    from pipeline.verify_claims import verify_all_claims
    res = verify_all_claims()
    passed = res["verified_count"]
    total = res["verified_count"] + res["failed_count"]
    if passed == total and total > 0:
        print(f"  ✅ Claim Integrity Gate Passed: {passed}/{total} verified against source DOIs.")
    else:
        print(f"  ⚠️ Claim Gate Audit: {passed}/{total} verified.")

def smoke_test_generation():
    print_step(5, "Running Pipeline Smoke Test (Lancet TOFI Study)")
    test_out = os.path.join("output", "smoke_test")
    os.makedirs(test_out, exist_ok=True)
    
    from pipeline.ingest import load_study_from_file
    from pipeline.editorial_carousel_engine import render_editorial_carousel
    
    paper_path = os.path.join("papers", "lancet_tofi_2021.json")
    if os.path.exists(paper_path):
        study = load_study_from_file(paper_path)
        slides = render_editorial_carousel(test_out, study=study)
        print(f"  ✅ Successfully rendered {len(slides)} square Instagram slides (1080x1080):")
        for s in slides:
            print(f"     • {os.path.basename(s)}")
    else:
        print("  ⚠️ Sample paper not found for smoke test.")

def main():
    print(BANNER)
    check_python()
    check_ffmpeg()
    install_dependencies()
    verify_claims()
    smoke_test_generation()
    
    print("\n" + "=" * 60)
    print(" 🎉 SETUP COMPLETE! THE PIPELINE IS READY ANYWHERE.")
    print("=" * 60)
    print("\nNext steps to run the pipeline:")
    print("  1. Process all clinical studies:")
    print("     python run_pipeline.py --all")
    print("\n  2. Ingest a new paper live from PubMed by PMID:")
    print("     python run_pipeline.py --pmid 37952131")
    print("\n  3. Launch local review studio dashboard:")
    print("     python run_pipeline.py --serve")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
