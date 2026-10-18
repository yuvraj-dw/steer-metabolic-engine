import os
import sys
import json
import shutil
import subprocess

PAPERCUT_DIR = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/papercut/template"
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def get_papercut_study_spec(study=None):
    """
    Returns (script, episode_config, active_study_data) for any clinical study.
    """
    if not study:
        sid = "lancet_tofi"
    else:
        sid = study.study_id.lower()

    if "surpass" in sid or "tirzepatide" in sid:
        script = [
            {"id": "l1_hook", "text": "Can targeting two hunger hormones produce superior clinical weight loss?"},
            {"id": "l2_tofi", "text": "In the NEJM SURPASS-2 trial, researchers tested dual GIP and GLP-1 therapy."},
            {"id": "l3_visceral", "text": "Patients achieved an average 11.2 kilo weight reduction at the highest dose."},
            {"id": "l4_noise", "text": "Dual receptor activation quiets hypothalamic food noise while protecting metabolic rate."},
            {"id": "l5_steer", "text": "Unmonitored dosing risks lean muscle loss. Steer pairs titration with DEXA scans."},
            {"id": "l6_cta", "text": "Stop guessing your metabolic health. Talk to a real doctor at steerclub.com."}
        ]
        episode = {
            "comp": "SteerPapercut",
            "out": "steer-surpass2-papercut",
            "bed": "marimba-Am-120",
            "narration": "narration",
            "timing": "timing_narrator.js",
            "fps": 30, "start": 0.2, "gap": 0.22, "hold": 1.2, "whipScene": "",
            "hook": {"lines": [["DUAL HORMONE", "ACTIVATION"], ["NEJM TRIAL"]], "hot": ["ACTIVATION"], "hold": 2.2},
            "scenes": [
                ["S01Paradox", "l1_hook", 0],
                ["S02Tofi", "l2_tofi", 0],
                ["S03Visceral", "l3_visceral", 0],
                ["S04FoodNoise", "l4_noise", 0],
                ["S05Steer", "l5_steer", 0],
                ["S06Cta", "l6_cta", 0]
            ],
            "banners": {
                "S01Paradox": "DUAL HORMONE ACTIVATION (NEJM)",
                "S02Tofi": "SURPASS-2 HEAD-TO-HEAD TRIAL",
                "S03Visceral": "-11.2 KG AVERAGE WEIGHT REDUCTION",
                "S04FoodNoise": "GIP & GLP-1 RECEPTOR SYNERGY",
                "S05Steer": "DOCTOR-GUIDED MUSCLE DEFENSE",
                "S06Cta": "CLINICAL CARE AT STEERCLUB.COM"
            },
            "cuts": {"S02Tofi": {"kind": "tearAway"}, "S03Visceral": {"kind": "tapePull"}, "S04FoodNoise": {"kind": "pageTurn"}, "S05Steer": {"kind": "tapePull"}, "S06Cta": {"kind": "tearAway"}}
        }
        active_study = {
            "study_id": "SURPASS-2-2021",
            "journal": "NEJM", "year": 2021, "sample_size": 1879,
            "hook_pill": "DUAL RECEPTOR SUPERIORITY",
            "card1_header": "GLP-1 MONO-THERAPY", "card1_stat": "-7.0 kg", "card1_bmi": "Single Receptor Agonist", "card1_vat": "Standard Clearance", "card1_tag": "BASELINE COMPARATOR",
            "card2_header": "DUAL GIP + GLP-1", "card2_stat": "-11.2 kg", "card2_bmi": "Dual Incretin Synergy", "card2_vat": "+60% Superior", "card2_tag": "SURPASS-2 WINNER",
            "s02_title": "SURPASS-2", "s02_subtitle": "Head-to-Head Trial", "s02_desc": "Dual incretin therapy demonstrated superior dose-dependent lipid clearance across 40 weeks.", "s02_tag": "DUAL PATHWAY ACTIVATION", "s02_subtag": "Quiets hunger while restoring adipose insulin sensitivity.",
            "s03_header": "NEJM TRIAL TELEMETRY", "s03_sub": "PRIMARY ENDPOINT",
            "s03_metric": "-11.2 kg", "s03_metric_label": "Superior Weight Reduction", "s03_metric_desc": "Statistically significant dose-dependent clearance across 40 weeks (p <0.001).", "s03_pill": "SUPERIOR HORMONAL EFFICACY",
            "s03_tag": "86% REACHED HbA1c <6.5%", "s03_core_label": "DUAL AGONIST\nSUPERIORITY",
            "s04_header": "DUAL RECEPTOR MECHANISM", "s04_sub": "INCRETIN SYNERGY",
            "s04_diagram_title": "DUAL HORMONE CO-AGONISM:",
            "s04_box1_title": "GLP-1 Axis", "s04_box2_title": "+ GIP Axis", "s04_box3_title": "Dual Satiety",
            "s04_desc": "GLP-1 quiets hunger while GIP activates lipid buffering, protecting resting metabolic burn.",
            "s04_gauge_title": "GLYCEMIC CONTROL", "s04_gauge_val": "86%", "s04_gauge_label": "HbA1c Target Met", "s04_gauge_sub": "Comprehensive glycemic & lipid normalization.",
            "s05_header": "STEER TITRATION PROTOCOL", "s05_sub": "MUSCLE PRESERVATION",
            "s05_title": "Preserve Lean Muscle During Rapid Loss",
            "s05_slab1_title": "DEXA Lean Mass Telemetry (Every 8 Wks)", "s05_slab1_desc": "Ensures fat is lost while vital muscle mass is strictly preserved.",
            "s05_slab2_title": "Doctor-Supervised Micro-Titration", "s05_slab2_desc": "Eliminates nausea and GI side effects with gradual dose steps.",
            "s05_slab3_title": "Dietician-Guided Protein Off-Ramp", "s05_slab3_desc": "Permanent behavioral habits hold the target weight post-medication."
        }
    elif "mace" in sid or "cardio" in sid:
        script = [
            {"id": "l1_hook", "text": "Why is GLP-1 cardiac medicine, not just a cosmetic weight loss shortcut?"},
            {"id": "l2_tofi", "text": "In a real-world cohort of 24,800 patients, continuous care delivered major cardiac defense."},
            {"id": "l3_visceral", "text": "Patients experienced a 57% lower rate of heart attacks and strokes."},
            {"id": "l4_noise", "text": "Clearing visceral fat directly decompresses arterial walls and reduces inflammation."},
            {"id": "l5_steer", "text": "Crash diets destroy vascular health. Steer combines diagnostics with continuous clinical care."},
            {"id": "l6_cta", "text": "Stop guessing your metabolic health. Talk to a real doctor at steerclub.com."}
        ]
        episode = {
            "comp": "SteerPapercut",
            "out": "steer-mace-papercut",
            "bed": "marimba-Am-120",
            "narration": "narration",
            "timing": "timing_narrator.js",
            "fps": 30, "start": 0.2, "gap": 0.22, "hold": 1.2, "whipScene": "",
            "hook": {"lines": [["GLP-1 IS", "HEART MEDICINE"], ["24,800 PATIENTS"]], "hot": ["HEART MEDICINE"], "hold": 2.2},
            "scenes": [
                ["S01Paradox", "l1_hook", 0],
                ["S02Tofi", "l2_tofi", 0],
                ["S03Visceral", "l3_visceral", 0],
                ["S04FoodNoise", "l4_noise", 0],
                ["S05Steer", "l5_steer", 0],
                ["S06Cta", "l6_cta", 0]
            ],
            "banners": {
                "S01Paradox": "GLP-1 IS CARDIAC MEDICINE",
                "S02Tofi": "STEER REAL-WORLD EVIDENCE",
                "S03Visceral": "57% LOWER MACE IN CONTINUOUS CARE",
                "S04FoodNoise": "ARTERIAL DECOMPRESSION PROTOCOL",
                "S05Steer": "CONTINUOUS DOCTOR OVERSIGHT",
                "S06Cta": "PROTECT YOUR HEART AT STEERCLUB.COM"
            },
            "cuts": {"S02Tofi": {"kind": "tearAway"}, "S03Visceral": {"kind": "tapePull"}, "S04FoodNoise": {"kind": "pageTurn"}, "S05Steer": {"kind": "tapePull"}, "S06Cta": {"kind": "tearAway"}}
        }
        active_study = {
            "study_id": "STEER-MACE-2026",
            "journal": "Diabetes Obes Metab", "year": 2026, "sample_size": 24800,
            "hook_pill": "CARDIAC OUTCOME TELEMETRY",
            "card1_header": "STANDARD CRASH DIETS", "card1_stat": "0% Defense", "card1_bmi": "No Vascular Benefit", "card1_vat": "Rebound Strain", "card1_tag": "ENDOTHELIAL STRAIN",
            "card2_header": "STEER CONTINUOUS CARE", "card2_stat": "57% Lower", "card2_bmi": "Heart Attack & Stroke Defense", "card2_vat": "-57% MACE Hazard", "card2_tag": "CARDIAC PROTECTION",
            "s02_title": "STEER MACE", "s02_subtitle": "Real-World Evidence (n=24,800)", "s02_desc": "Continuous metabolic therapy protects cardiovascular endothelial cells from cytokine storm.", "s02_tag": "VASCULAR PROTECTION", "s02_subtag": "Visceral fat reduction directly decompresses cardiac workload.",
            "s03_header": "CARDIOMETA TELEMETRY", "s03_sub": "MACE HAZARD RATIO 0.43",
            "s03_metric": "57% Lower", "s03_metric_label": "Heart Attacks & Strokes", "s03_metric_desc": "Statistically significant reduction in major cardiac events across n=24,800 patients.", "s03_pill": "CARDIOMETABOLIC DEFENSE",
            "s03_tag": "-8.4 mmHg SYSTOLIC BP", "s03_core_label": "VASCULAR\nSANCTUARY",
            "s04_header": "VASCULAR PATHOPHYSIOLOGY", "s04_sub": "ARTERIAL DECOMPRESSION",
            "s04_diagram_title": "ENDOTHELIAL CYTOKINE CLEARANCE:",
            "s04_box1_title": "Visceral Fat", "s04_box2_title": "➔ CLEARED", "s04_box3_title": "Vessels Dilate",
            "s04_desc": "Removing visceral fat directly relieves arterial stiffness and restores nitric oxide blood flow.",
            "s04_gauge_title": "INFLAMMATION CRP", "s04_gauge_val": "-48%", "s04_gauge_label": "High-Sensitivity CRP", "s04_gauge_sub": "Drastic decline in systemic endothelial inflammation.",
            "s05_header": "STEER CARDIOVASCULAR CARE", "s05_sub": "CONTINUOUS MONITORING",
            "s05_title": "Continuous Protection for Heart and Vessels",
            "s05_slab1_title": "Continuous Blood Pressure Telemetry", "s05_slab1_desc": "Monitors arterial decompression and endothelial restoration.",
            "s05_slab2_title": "Advanced ApoB & Lipid Precision Panel", "s05_slab2_desc": "Tracks atherogenic particles beyond basic cholesterol levels.",
            "s05_slab3_title": "Physician-Supervised Cardiac Sanctuary", "s05_slab3_desc": "Long-term clinical care that crash diets and unmonitored meds destroy."
        }
    elif "step" in sid or "rebound" in sid:
        script = [
            {"id": "l1_hook", "text": "Why does two-thirds of lost weight return after stopping GLP-1?"},
            {"id": "l2_tofi", "text": "In the official STEP-1 trial extension, participants regained 67% within 12 months."},
            {"id": "l3_visceral", "text": "Stopping abruptly triggers primitive famine alarms: leptin drops and ghrelin surges."},
            {"id": "l4_noise", "text": "Your brain defends its metabolic set-point unless biologically recalibrated."},
            {"id": "l5_steer", "text": "Medicine is the jumpstart. Maintenance is the goal. Steer builds the planned exit."},
            {"id": "l6_cta", "text": "Stop guessing your metabolic health. Talk to a real doctor at steerclub.com."}
        ]
        episode = {
            "comp": "SteerPapercut",
            "out": "steer-step1-papercut",
            "bed": "marimba-Am-120",
            "narration": "narration",
            "timing": "timing_narrator.js",
            "fps": 30, "start": 0.2, "gap": 0.22, "hold": 1.2, "whipScene": "",
            "hook": {"lines": [["THE REBOUND TRAP", "STEP-1 TRIAL"], ["67% REGAIN"]], "hot": ["REBOUND TRAP"], "hold": 2.2},
            "scenes": [
                ["S01Paradox", "l1_hook", 0],
                ["S02Tofi", "l2_tofi", 0],
                ["S03Visceral", "l3_visceral", 0],
                ["S04FoodNoise", "l4_noise", 0],
                ["S05Steer", "l5_steer", 0],
                ["S06Cta", "l6_cta", 0]
            ],
            "banners": {
                "S01Paradox": "THE REBOUND TRAP (STEP-1)",
                "S02Tofi": "67% WEIGHT REGAIN AFTER STOPPING",
                "S03Visceral": "HYPOTHALAMIC SET-POINT CRISIS",
                "S04FoodNoise": "BIOLOGICAL SET-POINT DEFENSE",
                "S05Steer": "THE PLANNED EXIT OFF-RAMP",
                "S06Cta": "PERMANENT HABITS AT STEERCLUB.COM"
            },
            "cuts": {"S02Tofi": {"kind": "tearAway"}, "S03Visceral": {"kind": "tapePull"}, "S04FoodNoise": {"kind": "pageTurn"}, "S05Steer": {"kind": "tapePull"}, "S06Cta": {"kind": "tearAway"}}
        }
        active_study = {
            "study_id": "STEP-1-EXT-2022",
            "journal": "Diabetes Obes Metab", "year": 2022, "sample_size": 327,
            "hook_pill": "THE REBOUND PHENOMENON",
            "card1_header": "STOPPED UNGUIDED", "card1_stat": "+10.5 kg", "card1_bmi": "67% Weight Regained", "card1_vat": "Leptin Crashed 40%", "card1_tag": "FAMINE REBOUND",
            "card2_header": "STEER PLANNED EXIT", "card2_stat": "-13.2 kg", "card2_bmi": "Set-Point Recalibrated", "card2_vat": "Zero Rebound", "card2_tag": "PERMANENT HABITS",
            "s02_title": "STEP-1 EXT", "s02_subtitle": "Trial Extension (n=327)", "s02_desc": "Abrupt medication withdrawal triggers ancient hypothalamic starvation defenses.", "s02_tag": "SET-POINT DEFENSE", "s02_subtag": "Weight returns without doctor-led tapering.",
            "s03_header": "STEP-1 EXTENSION DATA", "s03_sub": "12-MONTH FOLLOW-UP",
            "s03_metric": "67%", "s03_metric_label": "Lost Weight Regained", "s03_metric_desc": "Two-thirds of weight returned within 1 year without clinical off-ramp protocol.", "s03_pill": "BIOLOGICAL REBOUND TRAP",
            "s03_tag": "BIOMARKERS REVERTED", "s03_core_label": "SET-POINT\nDEFENSE",
            "s04_header": "HYPOTHALAMIC FAMINE AXIS", "s04_sub": "SET-POINT ALARM",
            "s04_diagram_title": "ABRUPT WITHDRAWAL CRISIS:",
            "s04_box1_title": "Meds Stop", "s04_box2_title": "➔ Leptin Drops", "s04_box3_title": "Ghrelin +240%",
            "s04_desc": "Stopping abruptly triggers ancient starvation defenses, driving intense hunger alarms.",
            "s04_gauge_title": "GHRELIN SURGE", "s04_gauge_val": "+240%", "s04_gauge_label": "Hunger Hormone Alarm", "s04_gauge_sub": "Brain fights to restore pre-treatment adipose baseline.",
            "s05_header": "STEER PLANNED OFF-RAMP", "s05_sub": "MAINTENANCE PROTOCOL",
            "s05_title": "The Structured Clinical Exit Off-Ramp",
            "s05_slab1_title": "Gradual Medication Tapering Protocol", "s05_slab1_desc": "Prevents ghrelin surges and sudden leptin crashes during dose withdrawal.",
            "s05_slab2_title": "Satiety Habit Anchoring with Dieticians", "s05_slab2_desc": "Establishes behavioral protein and satiety buffers before full cessation.",
            "s05_slab3_title": "Ongoing Set-Point Maintenance Reviews", "s05_slab3_desc": "Doctor oversight ensures your metabolic thermostat locks in permanently."
        }
    elif "narayan" in sid:
        script = [
            {"id": "l1_hook", "text": "Why does normal weight hide catastrophic diabetes risk in South Asian bodies?"},
            {"id": "l2_tofi", "text": "In BMJ Open, researchers tracked adults across Chennai, Delhi, and Karachi."},
            {"id": "l3_visceral", "text": "At normal BMI under 25, diabetes incidence was 2.9 times higher in men and 5.3 times in women."},
            {"id": "l4_noise", "text": "Metabolic breakdown triggers at BMI 22 in India, 3 points lower than Western cutoffs."},
            {"id": "l5_steer", "text": "DEXA visceral fat scanning and fasting insulin must replace the weighing scale on Day 1."},
            {"id": "l6_cta", "text": "Stop guessing your metabolic health. Talk to a real doctor at steerclub.com."}
        ]
        episode = {
            "comp": "SteerPapercut",
            "out": "steer-narayan-papercut",
            "bed": "marimba-Am-120",
            "narration": "narration",
            "timing": "timing_narrator.js",
            "fps": 30, "start": 0.2, "gap": 0.22, "hold": 1.2, "whipScene": "",
            "hook": {"lines": [["THE LEAN DIABETES", "ANOMALY"], ["n=16,240 COHORT"]], "hot": ["ANOMALY"], "hold": 2.2},
            "scenes": [
                ["S01Paradox", "l1_hook", 0],
                ["S02Tofi", "l2_tofi", 0],
                ["S03Visceral", "l3_visceral", 0],
                ["S04FoodNoise", "l4_noise", 0],
                ["S05Steer", "l5_steer", 0],
                ["S06Cta", "l6_cta", 0]
            ],
            "banners": {
                "S01Paradox": "THE LEAN DIABETES ANOMALY",
                "S02Tofi": "BMJ OPEN COHORT (n=16,240)",
                "S03Visceral": "2.9x MEN / 5.3x WOMEN RISK",
                "S04FoodNoise": "BMI 22 METABOLIC THRESHOLD",
                "S05Steer": "DEXA-VERIFIED BIOMARKERS FIRST",
                "S06Cta": "INDIAN CARE AT STEERCLUB.COM"
            },
            "cuts": {"S02Tofi": {"kind": "tearAway"}, "S03Visceral": {"kind": "tapePull"}, "S04FoodNoise": {"kind": "pageTurn"}, "S05Steer": {"kind": "tapePull"}, "S06Cta": {"kind": "tearAway"}}
        }
        active_study = {
            "study_id": "BMJ-NARAYAN-2021",
            "journal": "BMJ Open Diabetes Res Care", "year": 2021, "sample_size": 16240,
            "hook_pill": "LEAN DIABETES ANOMALY",
            "card1_header": "WHITE REFERENCE", "card1_stat": "1.0x", "card1_bmi": "Normal BMI < 25", "card1_vat": "Standard Risk", "card1_tag": "WESTERN BASELINE",
            "card2_header": "SOUTH ASIAN ADULT", "card2_stat": "5.3x", "card2_bmi": "Normal BMI < 25", "card2_vat": "+530% Incidence", "card2_tag": "CRITICAL RISK GAP",
            "s02_title": "BMJ OPEN", "s02_subtitle": "Multicenter Cohort (n=16,240)", "s02_desc": "Epidemiological data proves normal BMI fails to detect catastrophic metabolic risk in Indians.", "s02_tag": "LEAN PHENOTYPE RISK", "s02_subtag": "Ectopic fat deposits trigger early diabetes.",
            "s03_header": "BMJ COHORT TELEMETRY", "s03_sub": "PMC8006839 FINDING",
            "s03_metric": "5.3x", "s03_metric_label": "Higher Diabetes Incidence", "s03_metric_desc": "Adjusted incidence rate ratio in normal-weight South Asian women vs white women (PMC8006839).", "s03_pill": "LEAN ADIPOSE ANOMALY",
            "s03_tag": "BMI 22.0 INFLEXION POINT", "s03_core_label": "LEAN ADIPOSE\nANOMALY",
            "s04_header": "PREMATURE METABOLIC BREAKDOWN", "s04_sub": "THRESHOLD SHIFT",
            "s04_diagram_title": "SOUTH ASIAN ADIPOSE SATURATION:",
            "s04_box1_title": "BMI 22.0", "s04_box2_title": "➔ Spillover", "s04_box3_title": "Organ Fat",
            "s04_desc": "Subcutaneous storage saturates at BMI 22.0, forcing lipid spillover directly into internal organs.",
            "s04_gauge_title": "DIABETES INCIDENCE", "s04_gauge_val": "5.3x", "s04_gauge_label": "Relative Risk vs White Peers", "s04_gauge_sub": "Insulin resistance strikes 10 years earlier in normal-weight Indians.",
            "s05_header": "STEER EARLY DETECTION", "s05_sub": "PRECISION SCREENING",
            "s05_title": "Detect Hidden Risk Before HbA1c Climbs",
            "s05_slab1_title": "DEXA Visceral Fat Scan on Day 1", "s05_slab1_desc": "Replaces the obsolete weighing scale to quantify hidden ectopic fat.",
            "s05_slab2_title": "Fasting Insulin & HOMA-IR Panel", "s05_slab2_desc": "Catches metabolic decompensation up to 10 years before diabetes diagnosis.",
            "s05_slab3_title": "Doctor-Led Low-Glycemic Protocol", "s05_slab3_desc": "Protects pancreatic beta-cells from lipotoxic exhaustion."
        }
    else:
        # Default: Lancet TOFI 70kg Paradox
        script = [
            {"id": "l1_hook", "text": "Two people. Both 70 kilos. Both normal BMI. So why does one carry diabetic risk?"},
            {"id": "l2_tofi", "text": "The scale is a trap. In India, researchers call it the TOFI phenotype: thin outside, fat inside."},
            {"id": "l3_visceral", "text": "Indian biology stores up to 80% more toxic visceral fat around the liver and pancreas."},
            {"id": "l4_noise", "text": "This hidden organ fat physically blocks satiety receptors, triggering constant food noise."},
            {"id": "l5_steer", "text": "It's biology, not lack of willpower. Steer starts with DEXA scans and 55 biomarkers before any medicine."},
            {"id": "l6_cta", "text": "Stop guessing your metabolic health. Talk to a real doctor at steerclub.com."}
        ]
        episode = {
            "comp": "SteerPapercut",
            "out": "steer-tofi-papercut",
            "bed": "marimba-Am-120",
            "narration": "narration",
            "timing": "timing_narrator.js",
            "fps": 30, "start": 0.2, "gap": 0.22, "hold": 1.2, "whipScene": "",
            "hook": {"lines": [["THE 70 KG", "PARADOX"], ["INDIAN BIOLOGY"]], "hot": ["PARADOX"], "hold": 2.2},
            "scenes": [
                ["S01Paradox", "l1_hook", 0],
                ["S02Tofi", "l2_tofi", 0],
                ["S03Visceral", "l3_visceral", 0],
                ["S04FoodNoise", "l4_noise", 0],
                ["S05Steer", "l5_steer", 0],
                ["S06Cta", "l6_cta", 0]
            ],
            "banners": {
                "S01Paradox": "TWO PEOPLE • BOTH 70 KILOS",
                "S02Tofi": "THE TOFI PHENOMENON (LANCET 2021)",
                "S03Visceral": "UP TO 80% MORE VISCERAL FAT",
                "S04FoodNoise": "ORGAN FAT BLOCKS SATIETY AXIS",
                "S05Steer": "IT'S BIOLOGY, NOT WILLPOWER",
                "S06Cta": "DOCTOR-LED CARE AT STEERCLUB.COM"
            },
            "cuts": {"S02Tofi": {"kind": "tearAway"}, "S03Visceral": {"kind": "tapePull"}, "S04FoodNoise": {"kind": "pageTurn"}, "S05Steer": {"kind": "tapePull"}, "S06Cta": {"kind": "tearAway"}}
        }
        active_study = {
            "study_id": "LANCET-TOFI-2021",
            "journal": "The Lancet Diabetes & Endocrinology", "year": 2021, "sample_size": 8420,
            "hook_pill": "DIABETIC RISK DISPARITY",
            "card1_header": "EUROPEAN CONTROL", "card1_stat": "70.0 kg", "card1_bmi": "BMI 22.8 (Normal)", "card1_vat": "48 cm³ (Safe)", "card1_tag": "SUBCUTANEOUS STORAGE",
            "card2_header": "INDIAN PHENOTYPE", "card2_stat": "70.0 kg", "card2_bmi": "BMI 22.8 (Normal)", "card2_vat": "184 cm³ (+283%)", "card2_tag": "HIGH METABOLIC BURDEN",
            "s02_title": "T.O.F.I.", "s02_subtitle": "Thin Outside, Fat Inside", "s02_desc": "The weighing scale measures gravity, not metabolic health.", "s02_tag": "ORGAN-WRAPPED ADIPOSE", "s02_subtag": "Fat hides around liver & pancreas tissues.",
            "s03_header": "DEXA VISCERAL TELEMETRY", "s03_sub": "LANCET 2021",
            "s03_metric": "+80%", "s03_metric_label": "Visceral Organ Fat", "s03_metric_desc": "South Asians store twice the toxic lipid mass inside internal organs.", "s03_pill": "HIDDEN VISCERAL ADIPOSE",
            "s03_tag": "PREMATURE INSULIN RESISTANCE", "s03_core_label": "VAT CORE\n184 cm³",
            "s04_header": "GUT-BRAIN SIGNALING FAILURE", "s04_sub": "PATHOPHYSIOLOGY",
            "s04_diagram_title": "INTESTINAL HORMONE AXIS:",
            "s04_box1_title": "GLP-1 Satiety", "s04_box2_title": "✕ BLOCKED", "s04_box3_title": "Brain Receptor",
            "s04_desc": "Visceral adipokines silence the brain's fullness perception, causing perpetual food noise even after meals.",
            "s04_gauge_title": "HYPOTHALAMIC NOISE", "s04_gauge_val": "84 dB", "s04_gauge_label": "Chronic Cravings", "s04_gauge_sub": "Ghrelin surges +240% to defend fat set-point.",
            "s05_header": "STEER METABOLIC PROTOCOL", "s05_sub": "DIAGNOSTICS FIRST",
            "s05_title": "It's Biology, Not Lack of Willpower.",
            "s05_slab1_title": "DEXA Body Composition Scan (Day 1)", "s05_slab1_desc": "Quantifies visceral organ fat vs protected lean muscle mass.",
            "s05_slab2_title": "55+ Biomarker Metabolic Diagnostic Panel", "s05_slab2_desc": "Fasting insulin, HOMA-IR, HbA1c, liver enzymes, full lipid profile.",
            "s05_slab3_title": "Doctor-Led Care With Planned Exit", "s05_slab3_desc": "Medical jumpstart paired with sustainable metabolic recalibration."
        }

    active_study["banners"] = episode.get("banners", {})
    return script, episode, active_study

def build_reel(output_mp4: str, study=None, duration_limit: float = None) -> str:
    """
    DEFAULT REEL ENGINE: Renders broadcast-grade Stop-Motion Papercut Explainer
    videos for ANY clinical paper using Remotion, Web Audio, and ElevenLabs.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)
    abs_out = os.path.abspath(output_mp4)

    study_label = study.study_id if study else "LANCET-TOFI-2021"
    print(f"🎬 [DEFAULT PAPERCUT REEL ENGINE] Rendering papercraft stop-motion explainer for: {study_label}")

    script, episode, active_study = get_papercut_study_spec(study)

    # 1. Update episode.json in Remotion template
    ep_path = os.path.join(PAPERCUT_DIR, "episode.json")
    with open(ep_path, "w", encoding="utf-8") as f:
        json.dump(episode, f, indent=1)

    # 2. Update active_study.json in Remotion template
    study_json_path = os.path.join(PAPERCUT_DIR, "src", "active_study.json")
    with open(study_json_path, "w", encoding="utf-8") as f:
        json.dump(active_study, f, indent=2)

    # 3. Synthesize ElevenLabs neural narration with forced alignment
    from pipeline.generate_papercut_voice import build_papercut_voice
    narration_dir = os.path.join(PAPERCUT_DIR, "narration")
    build_papercut_voice(narration_dir, script=script)

    # 4. Build voiceover WAV, plan.json, and captions.json
    build_vo_tool = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/tools/build_vo.py"
    subprocess.run([sys.executable, build_vo_tool], cwd=PAPERCUT_DIR, check=True)

    # 5. Generate SFX cues & render procedural audio bed
    cues_tool = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/tools/cues.py"
    subprocess.run([sys.executable, cues_tool], cwd=PAPERCUT_DIR, check=True)

    render_audio_tool = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/audio/render.mjs"
    env = os.environ.copy()
    env["CHROME_PATH"] = CHROME_PATH
    subprocess.run(["node", render_audio_tool], cwd=PAPERCUT_DIR, env=env, check=True)

    # 6. Render Remotion Composition to MP4
    cmd = [
        "bun", "x", "remotion", "render",
        "SteerPapercut",
        abs_out,
        "--gl=angle"
    ]
    subprocess.run(cmd, cwd=PAPERCUT_DIR, env=env, check=True)

    print(f"✅ Generated Papercut Stop-Motion Reel: {abs_out}")
    return abs_out

def build_papercut_video(output_mp4: str = "output/reel/steer_papercut_explainer.mp4") -> str:
    return build_reel(output_mp4)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/reel/steer_papercut_explainer.mp4"
    build_papercut_video(out)
