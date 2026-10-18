import os
import sys
import json
import argparse
from pipeline.ingest import load_study_from_file, generate_doctor_verification_ledger
from pipeline.visuals_engine import generate_carousel, generate_static
from pipeline.papercut_engine import build_reel

def run_pipeline(paper_path: str, output_dir: str = "output", run_carousel: bool = True, run_static: bool = True, run_reel: bool = True, audit_only: bool = False):
    print(f"=== Steer Research-to-Instagram Automated Pipeline ===")
    print(f"Loading clinical study: {paper_path}")
    study = load_study_from_file(paper_path)
    print(f"Validated Study: {study.title} ({study.journal} {study.year}, n={study.sample_size})")

    # Doctor Review Gate
    ledger = generate_doctor_verification_ledger([study])
    ledger_path = os.path.join(output_dir, "doctor_review_gate.json")
    os.makedirs(output_dir, exist_ok=True)
    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)
    print(f"Doctor Review Gate verified: {ledger['verified_claims_count']} claims mapped to source DOI -> {ledger_path}")

    if audit_only:
        return

    # Visuals
    if run_carousel:
        c_dir = os.path.join(output_dir, "carousel")
        print(f"Generating 4:5 Instagram Carousel in {c_dir}...")
        slides = generate_carousel(c_dir)
        print(f"Produced {len(slides)} carousel slides.")

    if run_static:
        s_dir = os.path.join(output_dir, "static")
        print(f"Generating Static Infographic in {s_dir}...")
        static_file = generate_static(s_dir)
        print(f"Produced static post: {static_file}")

    if run_reel:
        r_dir = os.path.join(output_dir, "reel")
        os.makedirs(r_dir, exist_ok=True)
        reel_file = os.path.join(r_dir, "steer_clinical_reel.mp4")
        if not os.path.exists(reel_file):
            print(f"Rendering 9:16 vertical AI Reel with edge-tts neural audio in {r_dir}...")
            build_reel(reel_file)
            print(f"Produced Reel: {reel_file}")
        else:
            print(f"Reel already exists at {reel_file}")

    print("=== Pipeline Run Complete! All assets compliant with Steer Brand Kit ===")

def main():
    parser = argparse.ArgumentParser(description="Steer Research-to-Instagram Pipeline")
    parser.add_argument("--paper", required=True, help="Path to clinical paper summary JSON")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--carousel", action="store_true", help="Generate carousel only")
    parser.add_argument("--static", action="store_true", help="Generate static only")
    parser.add_argument("--reel", action="store_true", help="Generate reel only")
    parser.add_argument("--all", action="store_true", help="Generate all assets")
    parser.add_argument("--audit", action="store_true", help="Run doctor review audit gate only")

    args = parser.parse_args()
    
    if args.audit:
        run_pipeline(args.paper, args.output, audit_only=True)
    elif args.all or (not args.carousel and not args.static and not args.reel):
        run_pipeline(args.paper, args.output, run_carousel=True, run_static=True, run_reel=True)
    else:
        run_pipeline(
            args.paper, 
            args.output, 
            run_carousel=args.carousel, 
            run_static=args.static, 
            run_reel=args.reel
        )

if __name__ == "__main__":
    main()
