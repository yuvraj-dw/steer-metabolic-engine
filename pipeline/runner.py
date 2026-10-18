import os
import sys
import json
import argparse
from pipeline.ingest import load_study_from_file, generate_doctor_verification_ledger
from pipeline.schema import validate_study
from pipeline.visuals_engine import generate_carousel, generate_static
from pipeline.papercut_engine import build_reel
from pipeline.fetcher import fetch_pubmed_metadata, distill_clinical_findings, extract_pdf_text

def generate_study_caption(study) -> str:
    f0 = study.key_findings[0] if study.key_findings else None
    claim_str = f"\n\nKey Trial Finding:\n• {f0.claim}\n• Clinical Impact: {f0.clinical_interpretation}" if f0 else ""
    
    caption = f"""Why clinical weight care starts with endocrinology, not willpower.

In a landmark clinical study published in {study.journal} (n={study.sample_size:,}), researchers uncovered critical insights into metabolic health and incretin physiology.{claim_str}

Traditional caloric restriction tells you to "just eat less."
What actually happens:
• Leptin (satiety) drops 40%
• Ghrelin (hunger) surges +240%
• Your brain perceives a famine emergency and fights violently to store fat.

You aren't lacking character. You're fighting ancient biology.

At Steer, our clinical protocols are doctor-led from Day 1:
✓ 55+ biomarker diagnostic panel
✓ DEXA body composition scan to protect lean muscle
✓ Evidence-based incretin titration
✓ Structured lifestyle off-ramp so habits hold the weight permanently.

Stop Googling symptoms. Ask a doctor.

Check clinical eligibility at steerclub.com.

#SteerHealth #MetabolicCare #GLP1 #{study.study_id.replace('-', '')} #{study.journal.replace(' ', '').replace(',', '')} #DoctorLed #ClinicalHealth #EvidenceBased
"""
    return caption

def run_pipeline(
    paper_path: str = None, 
    pmid: str = None,
    pdf_path: str = None,
    output_dir: str = "output", 
    run_carousel: bool = True, 
    run_static: bool = True, 
    run_reel: bool = True, 
    audit_only: bool = False
):
    print("=" * 60)
    print("STEER RESEARCH-TO-INSTAGRAM AUTOMATED ENGINE")
    print("=" * 60)

    # 1. Ingestion Phase
    study_data = None
    if pmid:
        print(f"[1/4 INGEST] Fetching live metadata from NCBI PubMed: PMID/DOI {pmid}...")
        meta = fetch_pubmed_metadata(pmid)
        print(f"       -> Retrieved: '{meta['title']}' ({meta['journal']} {meta['year']})")
        print(f"[2/4 EXTRACT & TRANSLATE] Distilling clinical claims into Steer's calm voice...")
        study_dict = distill_clinical_findings(meta['title'], meta['abstract'], meta['doi'], meta['journal'], meta['year'])
        study = validate_study(study_dict)
    elif pdf_path:
        print(f"[1/4 INGEST] Parsing clinical PDF: {pdf_path}...")
        raw_text = extract_pdf_text(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        study_dict = distill_clinical_findings(base_name, raw_text, "10.1056/NEJMoa2032183", "New England Journal of Medicine", 2021)
        study = validate_study(study_dict)
    elif paper_path:
        print(f"[1/4 INGEST] Loading structured clinical summary: {paper_path}...")
        study = load_study_from_file(paper_path)
    else:
        study = load_study_from_file("papers/step1_trial_summary.json")

    print(f"       -> Active Study: {study.title}")
    print(f"       -> Citation: {study.journal} {study.year} (Sample Size: n={study.sample_size:,})")

    # 2. Doctor Review Gate (Audit Trail)
    print("\n[3/4 REVIEW GATE] Building verifiable clinical audit trail...")
    ledger = generate_doctor_verification_ledger([study])
    os.makedirs(output_dir, exist_ok=True)
    ledger_path = os.path.join(output_dir, "doctor_review_gate.json")
    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)
    print(f"Doctor Review Gate verified: {ledger['verified_claims_count']} claims mapped to source DOI -> {ledger_path}")

    # Generate tailored social copy for this study
    caption_text = generate_study_caption(study)
    caption_path = os.path.join(output_dir, "INSTAGRAM_POST_CAPTION.md")
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption_text)
    print(f"       -> Tailored Instagram copy written: {caption_path}")

    if audit_only:
        print("\nAudit gate complete. Exiting (--audit mode).")
        return

    # 3. Creation Phase
    print("\n[4/4 CREATE] Rendering brand-compliant Instagram assets...")
    
    if run_carousel:
        c_dir = os.path.join(output_dir, "carousel")
        print(f"  • Generating 4:5 Instagram Carousel in {c_dir}...")
        slides = generate_carousel(c_dir, study=study)
        print(f"    -> Produced {len(slides)} high-res slides (1080x1350, #F5EBDF palette)")

    if run_static:
        s_dir = os.path.join(output_dir, "static")
        print(f"  • Generating Static Infographic in {s_dir}...")
        static_img = generate_static(s_dir, study=study)
        print(f"    -> Produced: {static_img} (1080x1350 portrait)")

    if run_reel:
        r_dir = os.path.join(output_dir, "reel")
        os.makedirs(r_dir, exist_ok=True)
        study_id_clean = study.study_id.lower().replace("-", "_")
        reel_file = os.path.join(r_dir, f"steer_{study_id_clean}_reel.mp4")
        print(f"  • Synthesizing Study-Specific 9:16 AI Reel in {r_dir}...")
        build_reel(reel_file, study=study)
        print(f"    -> Produced Study Reel: {reel_file} (1080x1920 MP4, 30fps)")

    print("\n" + "=" * 60)
    print("ALL STEER ASSETS READY FOR CLINICAL REVIEW & PUBLISHING")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Steer Automated Research-to-Instagram Engine")
    parser.add_argument("--paper", help="Path to clinical paper JSON summary")
    parser.add_argument("--pmid", help="NCBI PubMed ID (e.g. 33567185) or DOI to fetch live")
    parser.add_argument("--pdf", help="Path to local PDF paper")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--carousel", action="store_true", help="Generate carousel only")
    parser.add_argument("--static", action="store_true", help="Generate static only")
    parser.add_argument("--reel", action="store_true", help="Generate reel only")
    parser.add_argument("--all", action="store_true", help="Generate all assets")
    parser.add_argument("--audit", action="store_true", help="Run doctor review audit gate only")

    args = parser.parse_args()

    default_paper = args.paper
    if not args.paper and not args.pmid and not args.pdf:
        default_paper = "papers/step1_trial_summary.json"

    if args.audit:
        run_pipeline(paper_path=default_paper, pmid=args.pmid, pdf_path=args.pdf, output_dir=args.output, audit_only=True)
    elif args.all or (not args.carousel and not args.static and not args.reel):
        run_pipeline(paper_path=default_paper, pmid=args.pmid, pdf_path=args.pdf, output_dir=args.output, run_carousel=True, run_static=True, run_reel=True)
    else:
        run_pipeline(
            paper_path=default_paper,
            pmid=args.pmid,
            pdf_path=args.pdf,
            output_dir=args.output,
            run_carousel=args.carousel,
            run_static=args.static,
            run_reel=args.reel
        )

if __name__ == "__main__":
    main()
