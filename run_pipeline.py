#!/usr/bin/env python3
"""
Steer Metabolic Engine - Master Universal Runner
Unified entrypoint to run the Research-to-Instagram & Playable Arcade Engine anywhere.
"""

import os
import sys
import argparse
import subprocess
import zipfile
import http.server
import socketserver
import webbrowser

def run_study(paper_file: str, out_name: str = "", make_reel: bool = True):
    from pipeline.ingest import load_study_from_file
    from pipeline.editorial_carousel_engine import render_editorial_carousel
    from pipeline.runner import generate_study_caption
    from pipeline.hinglish import get_hinglish_social_caption
    
    if not os.path.exists(paper_file):
        print(f"❌ Paper file not found: {paper_file}")
        return
        
    study = load_study_from_file(paper_file)
    folder = out_name or (study.study_id.lower().replace("-", "_") + "_post")
    base_dir = os.path.join("output", "posts", folder)
    carousel_dir = os.path.join(base_dir, "carousel")
    os.makedirs(carousel_dir, exist_ok=True)
    
    print(f"\n==================================================")
    print(f"🔬 INGESTING: {study.title}")
    print(f"   Journal: {study.journal} ({study.year}) | n={study.sample_size:,}")
    print(f"   Destination: {base_dir}")
    print(f"==================================================")
    
    # 1. 1080x1080 Square Instagram Carousel
    print("🎨 [1/3] Generating 1080x1080 Square Instagram Carousel...")
    slides = render_editorial_carousel(carousel_dir, study=study)
    print(f"   ✅ {len(slides)} Apple-grade square slides generated in {carousel_dir}")
    
    # 2. Hinglish Copy & Social Captions
    print("✍️ [2/3] Generating Hinglish Script & Instagram Caption...")
    caption = generate_study_caption(study)
    hinglish = get_hinglish_social_caption()
    script_path = os.path.join(base_dir, "hinglish_script.md")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(f"# Steer Social Copy: {study.title}\n\n")
        f.write(f"**DOI:** https://doi.org/{study.doi}\n\n")
        f.write("## 📸 Instagram Feed Caption\n\n")
        f.write(caption + "\n\n")
        f.write("## 🇮🇳 Hinglish Copy\n\n")
        f.write(hinglish + "\n")
    print(f"   ✅ Social copy saved to {script_path}")
    
    # 3. Packaging Doctor Verification Gate
    print("🩺 [3/3] Auditing Doctor Verification Gate...")
    from pipeline.verify_claims import verify_all_claims
    res = verify_all_claims()
    passed, total = res["verified_count"], res["verified_count"] + res["failed_count"]
    print(f"   ✅ {passed}/{total} claims confirmed against source DOI.")
    print(f"🎉 Completed pipeline run for: {study.study_id}\n")

def run_pmid_live(pmid: str):
    print(f"\n🌐 Live PubMed Ingestion for PMID: {pmid}...")
    from pipeline.fetcher import fetch_pubmed_metadata, distill_clinical_findings
    from pipeline.schema import validate_study
    
    meta = fetch_pubmed_metadata(pmid)
    if not meta or not meta.get("title"):
        print(f"❌ Failed to fetch abstract for PMID {pmid} from NCBI.")
        return
        
    study_dict = distill_clinical_findings(meta['title'], meta['abstract'], meta['doi'], meta['journal'], meta['year'])
    study = validate_study(study_dict)
    
    out_dir = os.path.join("output", "posts", f"pubmed_{pmid}")
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join("papers", f"pubmed_{pmid}.json")
    
    import json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(study_dict, f, indent=2)
    print(f"✅ Ingested PubMed abstract saved to {json_path}")
    
    run_study(json_path, out_name=f"pubmed_{pmid}")

def package_all_zips():
    print("\n📦 Packaging 1-Click Social Publishing ZIP Bundles...")
    posts_dir = os.path.join("output", "posts")
    if not os.path.exists(posts_dir):
        print("❌ No output/posts directory found. Run with --all first.")
        return
        
    count = 0
    for folder in os.listdir(posts_dir):
        fp = os.path.join(posts_dir, folder)
        if os.path.isdir(fp):
            zip_filename = os.path.join("output", f"steer-{folder}-publishing-bundle.zip")
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(fp):
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, fp)
                        zf.write(full_path, arcname=rel_path)
            print(f"   ✅ Created: {zip_filename} ({os.path.getsize(zip_filename) // 1024} KB)")
            count += 1
    print(f"🎉 Packaged {count} publishing bundles!\n")

def serve_dashboard(port: int = 8000):
    print(f"\n🚀 Launching Steer Publishing Studio Dashboard on port {port}...")
    webbrowser.open(f"http://localhost:{port}/doctor_review_board.html")
    
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Quiet mode

    with socketserver.TCPServer(("", port), QuietHandler) as httpd:
        print(f"   🌐 Live Dashboard: http://localhost:{port}/doctor_review_board.html")
        print("   🎮 Playable Arcade: http://localhost:{port}/")
        print("   Press Ctrl+C to stop the server.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

def main():
    parser = argparse.ArgumentParser(description="Steer Metabolic Engine - Master Universal Runner")
    parser.add_argument("--all", action="store_true", help="Process all available clinical studies in batch")
    parser.add_argument("--study", type=str, help="Specific study to process (e.g. lancet_tofi, surpass2, step1_ext)")
    parser.add_argument("--pmid", type=str, help="Fetch live PubMed paper by PMID (e.g. 37952131, 35658024)")
    parser.add_argument("--zip", action="store_true", help="Package 1-click publishing ZIP bundles for social publishing")
    parser.add_argument("--serve", action="store_true", help="Launch local HTTP dashboard server")
    parser.add_argument("--port", type=int, default=8000, help="Port for dashboard server (default 8000)")
    
    args = parser.parse_args()
    
    mapping = {
        'lancet_tofi': ('papers/lancet_tofi_2021.json', 'lancet_tofi_70kg'),
        'bmj_narayan': ('papers/bmj_narayan_tofi_2021.json', 'bmj_narayan_tofi'),
        'surpass2': ('papers/surpass2_tirzepatide_2021.json', 'surpass2_tirzepatide'),
        'steer_mace': ('papers/steer_cv_outcomes_2026.json', 'steer_mace_cardio'),
        'step1_ext': ('papers/step1_extension_2022.json', 'step1_extension_rebound'),
        'surmount1': ('papers/surmount1_tirzepatide_2022.json', 'surmount1_tirzepatide'),
        'step1': ('papers/step1_trial_summary.json', 'step1_pubmed_live'),
        'select': ('papers/select_trial_cv_2023.json', 'select_trial_cv')
    }
    
    if args.serve:
        serve_dashboard(args.port)
        return
        
    if args.zip:
        package_all_zips()
        return
        
    if args.pmid:
        run_pmid_live(args.pmid)
        return
        
    if args.study:
        key = args.study.lower()
        if key in mapping:
            paper_path, out_name = mapping[key]
            run_study(paper_path, out_name=out_name)
        else:
            # Check if it is a raw path
            if os.path.exists(args.study):
                run_study(args.study)
            else:
                print(f"❌ Unknown study: {args.study}. Available: {list(mapping.keys())}")
        return
        
    if args.all:
        for key, (paper_path, out_name) in mapping.items():
            run_study(paper_path, out_name=out_name)
        package_all_zips()
        return
        
    # Default: Run Lancet TOFI and show help
    print("\nNo specific flags provided. Processing default landmark study: Lancet TOFI (2021)...")
    paper_path, out_name = mapping['lancet_tofi']
    run_study(paper_path, out_name=out_name)
    print("Tip: Run `python run_pipeline.py --help` to see all batch, live PubMed, and dashboard options.\n")

if __name__ == "__main__":
    main()
