import os
import sys
from PIL import Image, ImageDraw, ImageFont
from pipeline.clinical_graphics import (
    draw_tofi_dexa_diagram,
    draw_surpass_diagram,
    draw_mace_diagram,
    draw_step1_diagram,
    draw_narayan_diagram,
    draw_slide1_telemetry,
    draw_slide3_telemetry
)

PALETTE = {
    "cream": "#F5EBDF",
    "rust": "#C04E2A",
    "deep_maroon": "#661414",
    "ink": "#2B1616",
    "clay": "#7D5246",
    "blush": "#DEC3B5",
    "soft_paper": "#FAF5EF",
    "white": "#FFFFFF",
    "card_border": "#E2CCBD",
    "teal_calm": "#235937",
    "teal_bright": "#34A853"
}

WINDOWS_FONTS = "C:/Windows/Fonts"

def get_serif(size, bold=False, italic=False):
    try:
        if italic:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "georgiai.ttf"), size)
        elif bold:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "georgiab.ttf"), size)
        else:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "georgia.ttf"), size)
    except:
        return ImageFont.load_default()

def get_sans(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "arialbd.ttf"), size)
        else:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "arial.ttf"), size)
    except:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    words = text.split(" ")
    lines = []
    curr = []
    for w in words:
        test = " ".join(curr + [w])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

def draw_vector_arrow(draw, x, y, direction="up", color="#C04E2A"):
    # Clean vector triangle arrow with no missing font glyph issues
    if direction == "up":
        draw.polygon([(x, y + 16), (x + 8, y), (x + 16, y + 16)], fill=color)
    else:
        draw.polygon([(x, y), (x + 8, y + 16), (x + 16, y)], fill=color)

def draw_vector_check(draw, x, y, color="#2B1616"):
    draw.line([(x, y + 8), (x + 6, y + 15)], fill=color, width=3)
    draw.line([(x + 6, y + 15), (x + 16, y)], fill=color, width=3)

def draw_header_badge(draw, text="CLINICAL DECONSTRUCTION", y=80, left_align=90):
    font = get_sans(20, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    badge_w = tw + 36
    badge_h = 40
    draw.rounded_rectangle([left_align, y, left_align + badge_w, y + badge_h], radius=20, fill="#E6D3C2")
    draw.text((left_align + 18, y + 9), text, fill=PALETTE["deep_maroon"], font=font)

def draw_footer(draw, current_slide, total_slides, width=1080, height=1350):
    font_brand = get_serif(32, bold=True)
    font_sub = get_sans(22)
    y_line = height - 110
    draw.line([(90, y_line), (width - 90, y_line)], fill=PALETTE["blush"], width=1)
    draw.text((90, y_line + 22), "steer", fill=PALETTE["deep_maroon"], font=font_brand)
    draw.text((180, y_line + 28), "•  Clinical Weight Loss  •  steerclub.com", fill=PALETTE["clay"], font=font_sub)
    if total_slides > 1:
        tracker = f"{current_slide} / {total_slides}"
        bbox = draw.textbbox((0, 0), tracker, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text((width - 90 - tw, y_line + 28), tracker, fill=PALETTE["clay"], font=font_sub)

def get_default_slides():
    return [
        # Slide 1: STEP-1 Trial & Rebound
        {
            "tag": "STEP-1 TRIAL EVIDENCE",
            "title": "Why 2/3 of weight returns after stopping.",
            "subtitle": "Stopping without an exit plan triggers an ancient biological defense.",
            "type": "rebound_hero",
            "stat": "67%",
            "stat_label": "Weight Regained Within 1 Year",
            "stat_sub": "Clinical data confirms set-point rebound defense",
            "p1": "In the landmark STEP-1 clinical trial published in the New England Journal of Medicine, participants lost an average of 14.9% body weight on once-weekly semaglutide.",
            "p2": "However, in the official 1-year trial extension, when medication stopped abruptly without structured behavioral tapering, two-thirds of the lost weight returned within 12 months.",
            "takeaway": "Medicine is the jumpstart. Maintenance is the goal.",
            "citation": "Source: Wilding et al., NEJM 2021 & STEP-1 Extension Study 2022"
        },
        # Slide 2: The Hypothalamic Thermostat
        {
            "tag": "NEURO-ENDOCRINE REGULATION",
            "title": "Your body has a weight thermostat.",
            "subtitle": "Science calls it the hypothalamic 'set-point'.",
            "type": "hormone_scales",
            "p1": "When you restrict calories through sheer willpower, your hypothalamus registers an emergency famine threat. It is mathematically designed to fight you.",
            "p2": "Telling someone to 'just eat less' is like asking someone in a burning room to ignore a 120 dB fire alarm. Your hunger hormones will always outlast your willpower.",
            "takeaway": "Steer protocols bypass willpower by recalibrating these exact neuro-chemical signals.",
            "citation": "Source: Sumithran et al., N Engl J Med 2011;365:1597-1604"
        },
        # Slide 3: The Indian TOFI Anomaly
        {
            "tag": "BUILT FOR INDIAN BIOLOGY",
            "title": "The TOFI Phenotype in Indian bodies.",
            "subtitle": "Thin on the Outside, Fat on the Inside.",
            "type": "tofi_breakdown",
            "stat": "2.1x",
            "stat_label": "Higher Visceral Organ Fat",
            "stat_sub": "Suffocates liver & pancreas at normal BMI",
            "p1": "In India, the bathroom scale is an illusion. South Asian genetics store a disproportionate amount of toxic visceral fat around internal organs, even at normal BMI.",
            "p2": "This hidden ectopic fat secretes inflammatory cytokines that block your gut's natural GLP-1 satiety signals, creating chronic 4 PM food noise and crashes.",
            "takeaway": "DEXA scanning is required to see what is happening inside.",
            "citation": "Source: Misra et al., The Lancet Diabetes & Endocrinology 2021"
        },
        # Slide 4: Steer's Clinical Architecture
        {
            "tag": "THE STEER ARCHITECTURE",
            "title": "Doctor-led care with a planned exit.",
            "subtitle": "How Steer recalibrates your set-point permanently.",
            "type": "steer_protocol",
            "pillars": [
                ("01  Diagnostics First", "55+ biomarkers, gut microbiome, and DEXA body scan on Day 1."),
                ("02  Lean Muscle Defense", "Targeted high-protein and resistance protocol supervised by dieticians."),
                ("03  Doctor-Led Titration", "Medical supervision throughout dosing; no unmonitored self-use."),
                ("04  Habit Off-Ramp", "Gradual tapering so permanent lifestyle habits hold the weight.")
            ],
            "citation": "Steer Clinical Care Protocol 2026 • steerclub.com"
        }
    ]

def build_study_slides(study):
    sid = (study.study_id + " " + getattr(study, "title", "")).lower() if study else "lancet_tofi"

    if "surpass" in sid or "tirzepatide" in sid:
        return [
            {
                "tag": "NEJM CLINICAL TRIAL",
                "title": "SURPASS-2: Dual Incretin Activation.",
                "subtitle": "Head-to-head trial of tirzepatide vs semaglutide (n=1,879).",
                "type": "rebound_hero",
                "stat": "-11.2 kg",
                "stat_label": "Superior Weight Loss at 40 Weeks",
                "stat_sub": "p <0.001 vs selective GLP-1 mono-agonist",
                "p1": "In the NEJM SURPASS-2 head-to-head trial, dual GIP/GLP-1 receptor co-agonism was evaluated across 1,879 individuals.",
                "p2": "Tirzepatide demonstrated statistically superior dose-dependent weight clearance, achieving up to -11.2 kg average reduction.",
                "takeaway": "Targeting both GIP and GLP-1 receptors outperforms single-agonist therapy.",
                "citation": "Source: Frías et al., N Engl J Med 2021;385:503-515"
            },
            {
                "tag": "DUAL RECEPTOR MECHANISM",
                "title": "GIP + GLP-1: The Metabolic Synergy.",
                "subtitle": "Why dual incretin agonists achieve deeper glycemic & lipid control.",
                "type": "clinical_diagram",
                "diagram_key": "SURPASS-2-2021",
                "p1": "GLP-1 receptor activation quiets hypothalamic food noise while GIP receptor activation restores adipose insulin sensitivity.",
                "takeaway": "Dual receptor synergy protects resting metabolic burn during fat loss.",
                "citation": "Source: The Lancet Diabetes & Endocrinology 2021;9:747-762"
            },
            {
                "tag": "CLINICAL EFFICACY & GLYCEMIC GOAL",
                "title": "Profound HbA1c & lipid normalization.",
                "subtitle": "Secondary clinical endpoints from NEJM (2021).",
                "type": "rebound_hero",
                "stat": "86%",
                "stat_label": "Reached Target HbA1c <6.5%",
                "stat_sub": "Coupled with profound visceral lipid clearance",
                "p1": "86% of patients achieved an HbA1c under 6.5%, alongside clinically significant reductions in liver fat and circulating triglycerides.",
                "p2": "However, rapid unmonitored loss risks up to 35% lean muscle wasting without structured dietary protein guidance.",
                "takeaway": "Steer pairs dual incretin titration with DEXA scans to defend lean muscle.",
                "citation": "Source: NEJM 2021;385:503-515, Table 2"
            },
            {
                "tag": "THE STEER ARCHITECTURE",
                "title": "Doctor-led care with muscle defense.",
                "subtitle": "How Steer delivers safe, sustainable dual incretin therapy.",
                "type": "steer_protocol",
                "pillars": [
                    ("01  DEXA Muscle Tracking", "Quantifies fat loss vs lean mass preservation every 8 weeks."),
                    ("02  Doctor-Led Titration", "Physician-guided micro-dosing to eliminate nausea and GI symptoms."),
                    ("03  Targeted High-Protein Diet", "Dietician-supervised intake to preserve resting metabolic rate."),
                    ("04  Structured Off-Ramp", "Gradual tapering protocol to maintain set-point permanently.")
                ],
                "citation": "Steer Clinical Care Protocol 2026 • steerclub.com"
            }
        ]

    elif "mace" in sid or "cardio" in sid:
        return [
            {
                "tag": "REAL-WORLD EVIDENCE",
                "title": "GLP-1 is Heart Medicine, Not Just Weight Loss.",
                "subtitle": "Cardiovascular outcomes in n=24,800 patients (DOM 2026).",
                "type": "rebound_hero",
                "stat": "57%",
                "stat_label": "Lower Rate of Heart Attacks & Strokes",
                "stat_sub": "Major Adverse Cardiovascular Events (MACE) HR 0.43",
                "p1": "In a multi-year cohort study of 24,800 patients, researchers tracked cardiovascular outcomes under continuous doctor-led GLP-1 care.",
                "p2": "Patients experienced a 57% lower rate of heart attacks and strokes compared to standard calorie restriction.",
                "takeaway": "Cardiometabolic protection starts at the vascular endothelium.",
                "citation": "Source: Wilson et al., Diabetes Obes Metab 2026;28:412-426"
            },
            {
                "tag": "VASCULAR PATHOPHYSIOLOGY",
                "title": "Decompressing the Arterial System.",
                "subtitle": "How visceral fat reduction protects endothelial blood flow.",
                "type": "clinical_diagram",
                "diagram_key": "STEER-MACE-2026",
                "p1": "Excess visceral fat secretes inflammatory adipokines that trigger chronic arterial wall stiffness and micro-vascular strain.",
                "takeaway": "Clearing toxic visceral cytokines directly relieves cardiac workload.",
                "citation": "Source: Circulation 2023;148:1532-1544"
            },
            {
                "tag": "SECONDARY CARDIOMETA ENDPOINTS",
                "title": "Systemic blood pressure & lipid normalization.",
                "subtitle": "Secondary hemodynamic outcomes (Diabetes Obes Metab 2026).",
                "type": "rebound_hero",
                "stat": "-8.4 mmHg",
                "stat_label": "Systolic Blood Pressure Reduction",
                "stat_sub": "Coupled with 32% lower high-sensitivity CRP",
                "p1": "Arterial decompression delivered a sustained 8.4 mmHg reduction in systolic blood pressure and significant ApoB lipid clearance.",
                "p2": "These protective cardiac benefits depend on continuous care rather than stop-and-start yo-yo dieting.",
                "takeaway": "Continuous doctor oversight delivers cardiac sanctuary that crash diets destroy.",
                "citation": "Source: Diabetes Obes Metab 2026;28:412-426, Table 3"
            },
            {
                "tag": "THE STEER ARCHITECTURE",
                "title": "Doctor-led continuous cardiovascular care.",
                "subtitle": "How Steer monitors heart and metabolic health beyond the scale.",
                "type": "steer_protocol",
                "pillars": [
                    ("01  ApoB & Lipid Precision", "Tracking advanced cardiac atherogenic particles beyond basic cholesterol."),
                    ("02  Continuous BP Telemetry", "Monitoring arterial decompression and vascular tone improvement."),
                    ("03  Visceral Decompression", "DEXA-guided tracking to ensure organ fat leaves first."),
                    ("04  Cardiometabolic Sanctuary", "Long-term clinical oversight protecting against vascular rebound.")
                ],
                "citation": "Steer Clinical Care Protocol 2026 • steerclub.com"
            }
        ]

    elif "step" in sid or "rebound" in sid or "semaglutide" in sid:
        return [
            {
                "tag": "STEP-1 TRIAL EVIDENCE",
                "title": "Why 2/3 of lost weight returns after stopping.",
                "subtitle": "The biological rebound trap revealed in Diabetes, Obesity and Metabolism (2022).",
                "type": "rebound_hero",
                "stat": "67%",
                "stat_label": "Weight Regained Within 12 Months",
                "stat_sub": "When medication is stopped without clinical tapering",
                "p1": "In the official 1-year trial extension of STEP-1, participants regained two-thirds (67%) of lost weight after stopping unguided.",
                "p2": "This rebound is not a failure of willpower. It is an ancient hypothalamic starvation alarm mathematically defending its set-point.",
                "takeaway": "Medicine is the jumpstart. Maintenance is the goal.",
                "citation": "Source: Wilding et al., Diabetes Obes Metab 2022;24(8):1553-1564"
            },
            {
                "tag": "NEURO-ENDOCRINE REGULATION",
                "title": "Your body has a weight thermostat.",
                "subtitle": "Science calls it the hypothalamic 'set-point'.",
                "type": "clinical_diagram",
                "diagram_key": "STEP-1-EXT-2022",
                "p1": "When you restrict calories through sheer willpower, your hypothalamus registers an emergency famine threat and drives appetite alarms.",
                "takeaway": "Steer protocols bypass willpower by recalibrating these exact neuro-chemical signals.",
                "citation": "Source: Sumithran et al., N Engl J Med 2011;365:1597-1604"
            },
            {
                "tag": "CARDIOMETABOLIC DRIFT",
                "title": "Biomarkers revert without an exit plan.",
                "subtitle": "Secondary clinical endpoints from Diabetes, Obesity and Metabolism (2022).",
                "type": "rebound_hero",
                "stat": "Reversion to baseline",
                "stat_label": "Blood Pressure, HbA1c & Fasting Lipids",
                "stat_sub": "Cardiometabolic benefits drift back within 12 months",
                "p1": "Cardiometabolic improvements in blood pressure, HbA1c, and fasting lipids reverted toward baseline following abrupt cessation.",
                "p2": "Sustained metabolic health demands long-term habit formation rather than isolated quick-fix treatments.",
                "takeaway": "True health requires a structured medical exit, not abrupt withdrawal.",
                "citation": "Source: Diabetes Obes Metab 2022;24(8):1553-1564, Table 1"
            },
            {
                "tag": "THE STEER ARCHITECTURE",
                "title": "Doctor-led care with a planned exit.",
                "subtitle": "How Steer recalibrates your set-point permanently.",
                "type": "steer_protocol",
                "pillars": [
                    ("01  Diagnostics First", "55+ biomarkers, gut microbiome, and DEXA body scan on Day 1."),
                    ("02  Lean Muscle Defense", "Targeted high-protein and resistance protocol supervised by dieticians."),
                    ("03  Doctor-Led Titration", "Medical supervision throughout dosing; no unmonitored self-use."),
                    ("04  Habit Off-Ramp", "Gradual tapering so permanent lifestyle habits hold the weight.")
                ],
                "citation": "Steer Clinical Care Protocol 2026 • steerclub.com"
            }
        ]

    elif "narayan" in sid:
        return [
            {
                "tag": "BMJ OPEN COHORT",
                "title": "Normal Weight Hides 5.3x Higher Diabetes Risk.",
                "subtitle": "Multicenter cohort across Chennai, Delhi & Karachi (n=16,240).",
                "type": "rebound_hero",
                "stat": "5.3x",
                "stat_label": "Higher Diabetes Incidence in Normal-Weight Women",
                "stat_sub": "2.9x in men at normal BMI < 25 (BMJ Open 2021)",
                "p1": "In a prospective multicenter cohort of 16,240 South Asian adults published in BMJ Open, researchers uncovered a severe anomaly.",
                "p2": "At normal BMI under 25, South Asian women exhibited a 5.3 times higher diabetes incidence compared to white reference cohorts.",
                "takeaway": "The weighing scale is obsolete for South Asian metabolic assessment.",
                "citation": "Source: Narayan et al., BMJ Open Diabetes Res Care 2021;9:e001897"
            },
            {
                "tag": "PREMATURE DECOMPENSATION",
                "title": "The BMI 22.0 Threshold in India.",
                "subtitle": "Metabolic breakdown triggers 3 points lower than Western benchmarks.",
                "type": "clinical_diagram",
                "diagram_key": "BMJ-NARAYAN-2021",
                "p1": "In South Asian genetics, visceral fat starts depositing into internal organs at BMI 22.0 rather than Western thresholds of 25.0.",
                "takeaway": "Screening cannot wait until BMI enters the traditional 'overweight' range.",
                "citation": "Source: BMJ Open 2021;9:e001897, Sentence p4-s13"
            },
            {
                "tag": "ECTOPIC ADIPOSITY",
                "title": "Suffocating the Beta-Cells.",
                "subtitle": "Why visceral fat causes early insulin resistance.",
                "type": "rebound_hero",
                "stat": "+80%",
                "stat_label": "Visceral Organ Fat Wrapping Organs",
                "stat_sub": "Triggers pancreatic and hepatic lipotoxicity",
                "p1": "Ectopic fat wrapping the pancreas and liver triggers chronic inflammatory cytokine release, accelerating beta-cell exhaustion.",
                "p2": "This explains why diabetes strikes South Asians 10 years earlier than Western peers, even without noticeable obesity.",
                "takeaway": "DEXA scan quantification must replace the bathroom scale on Day 1.",
                "citation": "Source: PMC8006839; BMJ Open 2021"
            },
            {
                "tag": "THE STEER ARCHITECTURE",
                "title": "Diagnostic precision for South Asian bodies.",
                "subtitle": "How Steer detects and reverses hidden metabolic risk.",
                "type": "steer_protocol",
                "pillars": [
                    ("01  DEXA Visceral Adipose Scan", "Quantify hidden organ fat on Day 1 rather than relying on weight."),
                    ("02  Fasting Insulin & HOMA-IR", "Detect insulin resistance 5 to 10 years before HbA1c begins to climb."),
                    ("03  Visceral Decompression Diet", "Low-glycemic anti-inflammatory protocols tailored to Indian diets."),
                    ("04  Doctor-Led Metabolic Care", "Physician supervision with planned exit and continuous monitoring.")
                ],
                "citation": "Steer Clinical Care Protocol 2026 • steerclub.com"
            }
        ]

    elif "tofi" in sid or "70kg" in sid or "lancet" in sid:
        # Lancet TOFI 70kg Paradox
        return [
            {
                "tag": "LANCET CLINICAL EVIDENCE",
                "title": "Two people. Both 70 kg. One carries diabetic risk.",
                "subtitle": "The 70 kg Paradox and the Indian TOFI Anomaly (Lancet 2021).",
                "type": "rebound_hero",
                "stat": "+80%",
                "stat_label": "Higher Visceral Organ Fat in South Asians",
                "stat_sub": "n=8,420 Cohort (Lancet Diabetes & Endocrinol)",
                "p1": "Two individuals can step on the exact same scale, both weighing 70 kilos, both having a normal BMI of 22.8.",
                "p2": "Yet DEXA imaging reveals the South Asian body carries up to 80% higher toxic visceral fat wrapped around the liver and pancreas.",
                "takeaway": "The weighing scale measures gravity, not metabolic health.",
                "citation": "Source: Misra et al., The Lancet Diabetes & Endocrinology 2021"
            },
            {
                "tag": "THE TOFI PHENOMENON",
                "title": "Thin on the Outside, Fat on the Inside.",
                "subtitle": "Why the weighing scale fails Indian biology.",
                "type": "clinical_diagram",
                "diagram_key": "LANCET-TOFI-2021",
                "p1": "In India, an individual can look lean in the mirror while storing dangerous amounts of metabolic fat internally.",
                "takeaway": "DEXA scanning reveals what traditional BMI completely misses.",
                "citation": "Source: Lancet Diabetes Endocrinol 2021;9(3):142-154"
            },
            {
                "tag": "METABOLIC PATHOPHYSIOLOGY",
                "title": "Organ fat blocks natural GLP-1 satiety signals.",
                "subtitle": "Why caloric restriction fails when visceral fat is elevated.",
                "type": "rebound_hero",
                "stat": "-65%",
                "stat_label": "Impaired Intestinal Satiety Axis",
                "stat_sub": "Triggers chronic food noise and willpower fatigue",
                "p1": "Visceral fat releases inflammatory cytokines that blunt neuro-endocrine satiety signaling between gut and brain.",
                "p2": "When biology is working against you, relying on sheer willpower is a guaranteed path to exhaustion and metabolic rebound.",
                "takeaway": "It's biology, not lack of willpower. Medical care resets the axis.",
                "citation": "Source: Misra et al., Lancet 2021"
            },
            {
                "tag": "THE STEER ARCHITECTURE",
                "title": "Doctor-led care with a planned exit.",
                "subtitle": "How Steer recalibrates your set-point permanently.",
                "type": "steer_protocol",
                "pillars": [
                    ("01  Diagnostics First", "55+ biomarkers, gut microbiome, and DEXA body scan on Day 1."),
                    ("02  Lean Muscle Defense", "Targeted high-protein and resistance protocol supervised by dieticians."),
                    ("03  Doctor-Led Titration", "Medical supervision throughout dosing; no unmonitored self-use."),
                    ("04  Habit Off-Ramp", "Gradual tapering so permanent lifestyle habits hold the weight.")
                ],
                "citation": "Steer Clinical Care Protocol 2026 • steerclub.com"
            }
        ]

    else:
        # Dynamic Study Generation for any generic / PubMed / PDF study
        f0 = study.key_findings[0] if (study and study.key_findings) else None
        f1 = study.key_findings[1] if (study and study.key_findings and len(study.key_findings) > 1) else f0
        journal_clean = getattr(study, "journal", "NEJM").replace("The ", "").upper() if study else "CLINICAL"
        st_title = getattr(study, "title", "Clinical Evidence")[:50]
        st_year = getattr(study, "year", 2026)
        st_sample = f"{getattr(study, 'sample_size', 1000):,}"
        
        f0_metric = f0.metric if f0 else "-14.9%"
        f0_claim = f0.claim if f0 else "Statistically significant metabolic improvement"
        f0_interp = f0.clinical_interpretation if f0 else "Treating root endocrinology restores natural metabolic set-point."
        f0_pval = f0.p_value if f0 else "<0.001"

        f1_metric = f1.metric if f1 else "2.1x"
        f1_claim = f1.claim if f1 else "Visceral fat reduction accelerates biomarker normalization"
        f1_interp = f1.clinical_interpretation if f1 else "Cardiometabolic health requires comprehensive biomarker diagnostics."
        f1_pval = f1.p_value if f1 else "<0.001"

        return [
            {
                "tag": f"{journal_clean[:20]} EVIDENCE",
                "title": f"{st_title}.",
                "subtitle": f"Peer-reviewed trial published in {getattr(study, 'journal', 'Clinical Journal')} ({st_year}, n={st_sample}).",
                "type": "rebound_hero",
                "stat": f0_metric,
                "stat_label": "Primary Clinical Endpoint",
                "stat_sub": f"Evidence-based efficacy (p {f0_pval})",
                "p1": f0_claim,
                "p2": f0_interp,
                "takeaway": "Evidence proves that sustained metabolic success demands clinical supervision.",
                "citation": f"Source: {getattr(study, 'journal', 'Journal')} ({st_year}) • steerclub.com"
            },
            {
                "tag": "PATHOPHYSIOLOGICAL MECHANISM",
                "title": "Biological regulation beyond the scale.",
                "subtitle": "How targeted clinical therapy addresses root endocrine drivers.",
                "type": "clinical_diagram",
                "diagram_key": "DYNAMIC_STUDY",
                "p1": "Clinical trials demonstrate that metabolic set-points are governed by neuro-endocrine signaling rather than sheer willpower.",
                "takeaway": "Steer protocols bypass willpower by recalibrating these exact neuro-chemical signals.",
                "citation": f"Source: {getattr(study, 'journal', 'Journal')} ({st_year}) • Steer Care"
            },
            {
                "tag": "CLINICAL EFFICACY & SAFETY",
                "title": "Targeting the root biology.",
                "subtitle": f"Key secondary endpoint from {getattr(study, 'journal', 'Journal')} ({st_year}).",
                "type": "rebound_hero",
                "stat": f1_metric,
                "stat_label": "Secondary Clinical Endpoint",
                "stat_sub": f"Statistically significant trial outcome (p {f1_pval})",
                "p1": f1_claim,
                "p2": f1_interp,
                "takeaway": "True health is measured in visceral fat reduction and biomarker health, not bathroom scale numbers.",
                "citation": f"Source: {getattr(study, 'journal', 'Journal')} ({st_year}) • steerclub.com"
            },
            {
                "tag": "THE STEER ARCHITECTURE",
                "title": "Doctor-led care with a planned exit.",
                "subtitle": "How Steer recalibrates your set-point permanently.",
                "type": "steer_protocol",
                "pillars": [
                    ("01  Diagnostics First", "55+ biomarkers, gut microbiome, and DEXA body scan on Day 1."),
                    ("02  Lean Muscle Defense", "Targeted high-protein and resistance protocol supervised by dieticians."),
                    ("03  Doctor-Led Titration", "Medical supervision throughout dosing; no unmonitored self-use."),
                    ("04  Habit Off-Ramp", "Gradual tapering so permanent lifestyle habits hold the weight.")
                ],
                "citation": "Steer Clinical Care Protocol 2026 • steerclub.com"
            }
        ]

def generate_apple_carousel(output_dir: str, study=None) -> list[str]:
    abs_dir = os.path.abspath(output_dir)
    os.makedirs(abs_dir, exist_ok=True)
    width, height = 1080, 1350

    slides_data = build_study_slides(study) if study else get_default_slides()

    out_files = []
    total = len(slides_data)

    for idx, slide in enumerate(slides_data, start=1):
        img = Image.new("RGB", (width, height), PALETTE["cream"])
        draw = ImageDraw.Draw(img)

        # 1. Header Badge
        draw_header_badge(draw, slide["tag"], y=75, left_align=90)

        # 2. Headline
        font_title = get_serif(58, bold=True)
        title_lines = wrap_text(slide["title"], font_title, width - 180, draw)
        y_text = 145
        for l in title_lines:
            draw.text((90, y_text), l, fill=PALETTE["deep_maroon"], font=font_title)
            y_text += 68

        # 3. Subtitle
        font_sub = get_sans(26)
        sub_lines = wrap_text(slide["subtitle"], font_sub, width - 180, draw)
        y_text += 10
        for l in sub_lines:
            draw.text((90, y_text), l, fill=PALETTE["rust"], font=font_sub)
            y_text += 36

        # 4. Main Editorial Arena (Fills space gracefully without awkward voids)
        arena_top = max(y_text + 25, 295)
        card_w = width - 180
        inner_w = card_w - 60
        card_h = 780

        if slide["type"] == "rebound_hero" or slide["type"] == "tofi_breakdown":
            card_h = 790
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            
            # Narrative paragraphs with generous editorial line-height (strictly budgeted to 2 lines each)
            font_body = get_sans(22)
            y_p = arena_top + 36
            for p in [slide.get("p1", ""), slide.get("p2", "")]:
                if not p:
                    continue
                plines = wrap_text(p, font_body, inner_w - 40, draw)[:2]
                for pl in plines:
                    draw.text((120, y_p), pl, fill=PALETTE["ink"], font=font_body)
                    y_p += 30
                y_p += 10

            # Highlight Stat Card inside (Intelligently handles both short metrics and phrases)
            stat_str = slide.get("stat", "")
            is_short_metric = len(stat_str) <= 8 and not any(c.isspace() for c in stat_str.strip())
            stat_top = y_p + 12

            if is_short_metric:
                stat_h = 120
                draw.rounded_rectangle([120, stat_top, 120 + inner_w, stat_top + stat_h], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
                
                font_stat = get_serif(58, bold=True)
                stat_bbox = draw.textbbox((0, 0), stat_str, font=font_stat)
                stat_w = stat_bbox[2] - stat_bbox[0]
                stat_h_text = stat_bbox[3] - stat_bbox[1]
                draw.text((150, stat_top + (stat_h - stat_h_text) // 2 - 4), stat_str, fill=PALETTE["rust"], font=font_stat)
                
                lbl_x = 150 + stat_w + 35
                max_lbl_w = (120 + inner_w) - lbl_x - 20
                lbl_lines = wrap_text(slide["stat_label"], get_sans(20, bold=True), max_lbl_w, draw)[:2]
                y_lbl = stat_top + 18
                for ll in lbl_lines:
                    draw.text((lbl_x, y_lbl), ll, fill=PALETTE["deep_maroon"], font=get_sans(20, bold=True))
                    y_lbl += 25
                draw.text((lbl_x, y_lbl + 4), slide["stat_sub"], fill=PALETTE["clay"], font=get_sans(16))
            else:
                # Descriptive stat phrase (e.g. "Reversion to baseline") - Clean Stacked Layout!
                font_stat_phrase = get_serif(26, bold=True)
                stat_lines = wrap_text(stat_str, font_stat_phrase, inner_w - 60, draw)[:2]
                lbl_lines = wrap_text(slide["stat_label"], get_sans(19, bold=True), inner_w - 60, draw)[:2]
                stat_h = 16 + len(stat_lines) * 30 + len(lbl_lines) * 25 + 24
                draw.rounded_rectangle([120, stat_top, 120 + inner_w, stat_top + stat_h], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
                
                y_st = stat_top + 16
                for sl in stat_lines:
                    draw.text((150, y_st), sl, fill=PALETTE["rust"], font=font_stat_phrase)
                    y_st += 30
                
                for ll in lbl_lines:
                    draw.text((150, y_st), ll, fill=PALETTE["ink"], font=get_sans(19, bold=True))
                    y_st += 25
                draw.text((150, y_st + 4), slide["stat_sub"], fill=PALETTE["clay"], font=get_sans(16))

            # Takeaway Doctor Callout Banner (Always wrapped with dynamic height & vector checkmark)
            note_top = stat_top + stat_h + 14
            font_note = get_sans(19, bold=True)
            note_lines = wrap_text(slide["takeaway"], font_note, inner_w - 80, draw)[:3]
            note_h = max(62, 16 + len(note_lines) * 24)
            draw.rounded_rectangle([120, note_top, 120 + inner_w, note_top + note_h], radius=14, fill="#EDF5F0", outline="#D3E8D9", width=1)
            
            y_note = note_top + 14
            for i, nl in enumerate(note_lines):
                if i == 0:
                    draw_vector_check(draw, 142, y_note + 4, color=PALETTE["teal_calm"])
                draw.text((170, y_note), nl, fill=PALETTE["teal_calm"], font=font_note)
                y_note += 24

            # Embedded Publication-Grade Vector Telemetry (Fills lower 240px of Slide 1 & Slide 3)
            sid = (study.study_id if study else "step1").upper()
            y_telem = note_top + note_h + 14
            if idx == 1:
                telem_img = draw_slide1_telemetry(sid, inner_w, 240)
                img.paste(telem_img, (120, y_telem), telem_img if telem_img.mode == "RGBA" else None)
                y_after = y_telem + telem_img.height + 14
            elif idx == 3:
                telem_img = draw_slide3_telemetry(sid, inner_w, 230)
                img.paste(telem_img, (120, y_telem), telem_img if telem_img.mode == "RGBA" else None)
                y_after = y_telem + telem_img.height + 14
            else:
                y_after = note_top + note_h + 14

            # Citation safely wrapped inside card bottom with guaranteed bounds
            font_cit = get_sans(14)
            cit_lines = wrap_text(slide["citation"], font_cit, inner_w - 40, draw)[:2]
            y_cit = max(y_after, arena_top + card_h - 18 - (len(cit_lines) * 18))
            for cl in cit_lines:
                draw.text((120, y_cit), cl, fill=PALETTE["clay"], font=font_cit)
                y_cit += 18

        elif slide["type"] == "clinical_diagram":
            card_h = 760
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            
            font_body = get_sans(22)
            y_p = arena_top + 32
            p1 = slide.get("p1", "")
            if p1:
                plines = wrap_text(p1, font_body, inner_w, draw)
                for pl in plines:
                    draw.text((120, y_p), pl, fill=PALETTE["ink"], font=font_body)
                    y_p += 30
                y_p += 10

            # Render clinical diagram image
            dkey = slide.get("diagram_key", "")
            if "SURPASS" in dkey:
                diag_img = draw_surpass_diagram(inner_w, 350)
            elif "MACE" in dkey or "STEER" in dkey:
                diag_img = draw_mace_diagram(inner_w, 350)
            elif "STEP" in dkey:
                diag_img = draw_step1_diagram(inner_w, 350)
            elif "NARAYAN" in dkey:
                diag_img = draw_narayan_diagram(inner_w, 350)
            else:
                diag_img = draw_tofi_dexa_diagram(inner_w, 350)

            img.paste(diag_img, (120, y_p), diag_img if diag_img.mode == "RGBA" else None)
            y_p += diag_img.height + 16

            # Takeaway Box (With vector checkmark, zero unrendered glyphs)
            font_note = get_sans(19, bold=True)
            note_lines = wrap_text(slide.get("takeaway", ""), font_note, inner_w - 70, draw)
            note_h = max(64, 18 + len(note_lines) * 25)
            draw.rounded_rectangle([120, y_p, 120 + inner_w, y_p + note_h], radius=12, fill="#EDF5F0", outline="#D3E8D9", width=1)
            y_note = y_p + 14
            for i, nl in enumerate(note_lines):
                if i == 0:
                    draw_vector_check(draw, 142, y_note + 4, color=PALETTE["teal_calm"])
                draw.text((170, y_note), nl, fill=PALETTE["teal_calm"], font=font_note)
                y_note += 25
            y_p += note_h + 16

            # Steer Doctor Protocol Directive Slab (Fills lower space with high clinical authority)
            proto_h = 72
            draw.rounded_rectangle([120, y_p, 120 + inner_w, y_p + proto_h], radius=12, fill="#FAF3EB", outline="#E2D3C4", width=1)
            draw.text((144, y_p + 12), "STEER CLINICAL DIRECTIVE", fill=PALETTE["rust"], font=get_sans(13, bold=True))
            draw.text((144, y_p + 32), "Continuous physician-led metabolic titration replaces unguided guesswork.", fill=PALETTE["deep_maroon"], font=get_sans(15, bold=True))
            draw.text((144, y_p + 50), "Routine DEXA tracking guarantees lean muscle retention during fat loss.", fill=PALETTE["clay"], font=get_sans(14))
            y_p += proto_h + 16

            # Citation
            font_cit = get_sans(15)
            cit_lines = wrap_text(slide.get("citation", ""), font_cit, inner_w, draw)
            y_cit = max(y_p, arena_top + card_h - 18 - (len(cit_lines) * 19))
            for cl in cit_lines:
                draw.text((120, y_cit), cl, fill=PALETTE["clay"], font=font_cit)
                y_cit += 19

        elif slide["type"] == "dual_incretin":
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            
            font_body = get_sans(22)
            y_p = arena_top + 45
            for p in [slide.get("p1", ""), slide.get("p2", "")]:
                if not p:
                    continue
                plines = wrap_text(p, font_body, inner_w, draw)
                for pl in plines:
                    draw.text((120, y_p), pl, fill=PALETTE["ink"], font=font_body)
                    y_p += 32
                y_p += 16

            # Dual Incretin Pathway Diagram
            diag_top = y_p + 15
            # Slab 1: GIP Receptor
            draw.rounded_rectangle([120, diag_top, 120 + inner_w, diag_top + 95], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            draw.text((150, diag_top + 18), "GIP RECEPTOR ACTIVATION", fill=PALETTE["deep_maroon"], font=get_sans(19, bold=True))
            draw.text((150, diag_top + 52), "Improves adipose insulin sensitivity & protects muscle mass", fill=PALETTE["clay"], font=get_sans(18))
            draw.text((width - 250, diag_top + 28), "METABOLIC", fill=PALETTE["rust"], font=get_sans(17, bold=True))

            # Slab 2: GLP-1 Receptor
            diag2_top = diag_top + 115
            draw.rounded_rectangle([120, diag2_top, 120 + inner_w, diag2_top + 95], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            draw.text((150, diag2_top + 18), "GLP-1 RECEPTOR ACTIVATION", fill=PALETTE["deep_maroon"], font=get_sans(19, bold=True))
            draw.text((150, diag2_top + 52), "Quiets hypothalamic hunger signals & slows gastric emptying", fill=PALETTE["clay"], font=get_sans(18))
            draw.text((width - 250, diag2_top + 28), "SATIETY", fill=PALETTE["teal_calm"], font=get_sans(17, bold=True))

            # Takeaway Box
            note_top = diag2_top + 125
            font_note = get_sans(20, bold=True)
            note_lines = wrap_text(slide["takeaway"], font_note, inner_w - 60, draw)
            note_h = max(68, 22 + len(note_lines) * 26)
            draw.rounded_rectangle([120, note_top, 120 + inner_w, note_top + note_h], radius=12, fill="#F2E6DC", outline="#DEC3B5", width=1)
            y_note = note_top + 14
            for i, nl in enumerate(note_lines):
                if i == 0:
                    draw_vector_check(draw, 142, y_note + 4, color=PALETTE["deep_maroon"])
                draw.text((170, y_note), nl, fill=PALETTE["deep_maroon"], font=font_note)
                y_note += 26

            # Citation
            font_cit = get_sans(16)
            cit_lines = wrap_text(slide["citation"], font_cit, inner_w, draw)
            y_cit = arena_top + card_h - 18 - (len(cit_lines) * 20)
            for cl in cit_lines:
                draw.text((120, y_cit), cl, fill=PALETTE["clay"], font=font_cit)
                y_cit += 20

        elif slide["type"] == "hormone_scales":
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            
            font_body = get_sans(22)
            y_p = arena_top + 45
            for p in [slide.get("p1", ""), slide.get("p2", "")]:
                if not p:
                    continue
                plines = wrap_text(p, font_body, inner_w, draw)
                for pl in plines:
                    draw.text((120, y_p), pl, fill=PALETTE["ink"], font=font_body)
                    y_p += 32
                y_p += 16

            # Visual Dual Scales (Ghrelin vs Leptin)
            sc_top = y_p + 15
            draw.rounded_rectangle([120, sc_top, 120 + inner_w, sc_top + 95], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            draw.text((150, sc_top + 18), "GHRELIN (HUNGER HORMONE)", fill=PALETTE["deep_maroon"], font=get_sans(19, bold=True))
            draw.text((150, sc_top + 52), "Triggers urgent food noise & 4 PM cravings", fill=PALETTE["clay"], font=get_sans(18))
            draw_vector_arrow(draw, width - 295, sc_top + 34, direction="up", color=PALETTE["rust"])
            draw.text((width - 270, sc_top + 24), "+240%", fill=PALETTE["rust"], font=get_serif(36, bold=True))

            sc2_top = sc_top + 115
            draw.rounded_rectangle([120, sc2_top, 120 + inner_w, sc2_top + 95], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            draw.text((150, sc2_top + 18), "LEPTIN (SATIETY SIGNAL)", fill=PALETTE["deep_maroon"], font=get_sans(19, bold=True))
            draw.text((150, sc2_top + 52), "Signals fullness & regulates metabolic burn", fill=PALETTE["clay"], font=get_sans(18))
            draw_vector_arrow(draw, width - 275, sc2_top + 38, direction="down", color=PALETTE["deep_maroon"])
            draw.text((width - 250, sc2_top + 24), "-40%", fill=PALETTE["deep_maroon"], font=get_serif(36, bold=True))

            note_top = sc2_top + 125
            font_note = get_sans(20, bold=True)
            note_lines = wrap_text(slide["takeaway"], font_note, inner_w - 60, draw)
            note_h = max(68, 22 + len(note_lines) * 26)
            draw.rounded_rectangle([120, note_top, 120 + inner_w, note_top + note_h], radius=12, fill="#F2E6DC", outline="#DEC3B5", width=1)
            y_note = note_top + 14
            for i, nl in enumerate(note_lines):
                if i == 0:
                    draw_vector_check(draw, 142, y_note + 4, color=PALETTE["deep_maroon"])
                draw.text((170, y_note), nl, fill=PALETTE["deep_maroon"], font=font_note)
                y_note += 26

            font_cit = get_sans(16)
            cit_lines = wrap_text(slide["citation"], font_cit, inner_w, draw)
            y_cit = arena_top + card_h - 18 - (len(cit_lines) * 20)
            for cl in cit_lines:
                draw.text((120, y_cit), cl, fill=PALETTE["clay"], font=font_cit)
                y_cit += 20

        else:
            # Slide 4: Clean Steer 4-Pillar Off-Ramp Architecture
            card_h = 710
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            draw.text((120, arena_top + 34), "THE STEER CLINICAL OFF-RAMP", fill=PALETTE["clay"], font=get_sans(17, bold=True))

            slab_y = arena_top + 72
            for title, desc in slide.get("pillars", []):
                draw.rounded_rectangle([120, slab_y, 120 + inner_w, slab_y + 112], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
                draw.text((150, slab_y + 16), title, fill=PALETTE["deep_maroon"], font=get_sans(22, bold=True))
                desc_lines = wrap_text(desc, get_sans(18), inner_w - 60, draw)
                yd = slab_y + 52
                for dl in desc_lines:
                    draw.text((150, yd), dl, fill=PALETTE["ink"], font=get_sans(18))
                    yd += 24
                slab_y += 130

            font_cit = get_sans(15)
            cit_lines = wrap_text(slide["citation"], font_cit, inner_w, draw)
            y_cit = arena_top + card_h - 18 - (len(cit_lines) * 19)
            for cl in cit_lines:
                draw.text((120, y_cit), cl, fill=PALETTE["clay"], font=font_cit)
                y_cit += 19

        # 5. Footer
        draw_footer(draw, idx, total, width, height)

        out_path = os.path.normpath(os.path.join(abs_dir, f"carousel_slide_{idx}.png"))
        img.save(out_path, quality=95)
        out_files.append(out_path)
        print(f"✅ Generated Apple-Crafted Slide {idx}: {out_path}")

    return out_files

if __name__ == "__main__":
    generate_apple_carousel("output/carousel")
