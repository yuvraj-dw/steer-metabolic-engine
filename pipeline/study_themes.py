"""
Steer Clinical Editorial Theme Registry
Provides publication-grade, study-tailored visual themes, distinct motifs, varied color
palettes, variable hero slide indices, custom editorial pull-quotes, and bespoke protocol
pillars across all 7 clinical research studies.
"""

from typing import Dict, List, Tuple, Any, Optional

class ThemeConfig(dict):
    """
    Dictionary subclass supporting dot-attribute access alongside dictionary indexing.
    Enables both `theme['hero_quote']` and `theme.hero_quote` seamlessly, including nested dicts.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in list(self.items()):
            if isinstance(v, dict) and not isinstance(v, ThemeConfig):
                self[k] = ThemeConfig(v)

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'ThemeConfig' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if isinstance(value, dict) and not isinstance(value, ThemeConfig):
            value = ThemeConfig(value)
        self[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'ThemeConfig' object has no attribute '{name}'")


# -----------------------------------------------------------------------------
# 7 CLINICAL STUDY THEMES DEFINITION
# -----------------------------------------------------------------------------

STUDY_THEMES: Dict[str, ThemeConfig] = {
    # 1. LANCET TOFI 2021: Indian 70kg Paradox (+80% Visceral Ectopic Fat)
    "LANCET-TOFI-2021": ThemeConfig({
        "study_id": "LANCET-TOFI-2021",
        "study_file": "papers/lancet_tofi_2021.json",
        "theme_name": "Ectopic Visceral Fat",
        "topic": "The 70 kg Paradox & Indian Ectopic Adiposity",
        "hero_slide_index": 3,
        "hero_quote": "The weighing scale is measuring gravity, not the fat causing diabetes.",
        "primary_motif": "cellular",
        "secondary_motif": "caring_hands",
        "study_directive": "Identical scale weights conceal an 80% visceral fat surplus around Indian organs. Replace standard BMI with Day-1 DEXA imaging.",
        "protocol_pillars": [
            (
                "01  Day-1 DEXA Visceral Mapping",
                "Quantify deep ectopic organ fat infiltrating liver and pancreas tissues rather than relying on bathroom scale weight."
            ),
            (
                "02  Targeted Visceral Decompression",
                "Physician-guided metabolic therapy specifically formulated to eliminate toxic ectopic cytokines before cutting calories."
            ),
            (
                "03  Sustained Set-Point Off-Ramp",
                "Gradual hormonal tapering protocol to recalibrate leptin sensitivity and lock in the new metabolic baseline."
            )
        ],
        "cta_headline": "Look beyond the scale with doctor-led DEXA care.",
        "cta_subtext": "55+ clinical biomarkers • Full DEXA visceral fat mapping • Dedicated metabolic physician access across India",
        "color_palette": {
            "hero_bg": "#5C181A",          # Deep Oxblood Burgundy
            "cream_bg": "#F5EBDF",         # Calm Editorial Warm Cream
            "accent": "#C04E2A",           # Terracotta Rust
            "accent_light": "#FDF0EB",     # Soft Terracotta Tint
            "text_dark": "#241E1C",        # Charcoal Ink
            "text_light": "#FAF7F2",       # Pure Ivory White
            "text_muted": "#8E8277",       # Warm Muted Slate
            "text_muted_on_dark": "#D4A8AA", # Soft Roseate Slate on Dark
            "border_dark": "#A05055",      # Muted Roseate Oxblood
            "border_light": "#241E1C",     # Refined Editorial Frame
            # Canonical shorthand mappings
            "oxblood": "#5C181A",
            "cream": "#F5EBDF",
            "rust": "#C04E2A",
            "charcoal": "#241E1C",
            "slate": "#8E8277",
            "white": "#FAF7F2"
        },
        "metadata": {
            "journal": "The Lancet Diabetes & Endocrinology (2021)",
            "doi": "10.1016/S2213-8587(21)00028-1",
            "sample_size": 8420,
            "stat": "+80%",
            "stat_label": "Higher Visceral Organ Fat in South Asians",
            "stat_sub": "n=8,420 Cohort (Lancet Diabetes & Endocrinol)"
        }
    }),

    # 2. BMJ NARAYAN 2021: South Asian Normal-BMI Diabetes (BMI 22.0 Threshold)
    "BMJ-NARAYAN-2021": ThemeConfig({
        "study_id": "BMJ-NARAYAN-2021",
        "study_file": "papers/bmj_narayan_tofi_2021.json",
        "theme_name": "BMI 22.0 Saturation Threshold",
        "topic": "South Asian Normal-BMI Diabetes Anomaly",
        "hero_slide_index": 2,            # Hero interruption occurs early at Slide 2
        "hero_quote": "South Asian biology saturates adipose storage 3 BMI points earlier than Western guidelines.",
        "primary_motif": "threshold_curve",
        "secondary_motif": "telemetry_curve",
        "study_directive": "Normal weight conceals a 5.3-fold diabetes risk in Indian women. Adipose overflow begins at BMI 22.0 kg/m², 3 points lower than Western guidelines.",
        "protocol_pillars": [
            (
                "01  Threshold-Calibrated Screening",
                "Clinical risk screening triggering at Indian BMI 22.0 kg/m² instead of outdated Western 25.0 benchmarks."
            ),
            (
                "02  Fasting Insulin & HOMA-IR Panel",
                "Detect beta-cell exhaustion 5 to 10 years before fasting glucose or HbA1c elevation manifests."
            ),
            (
                "03  Adipose Capacity Expansion Protocol",
                "Physician-directed resistance and nutritional programming to clear ectopic lipid overflow from vital organs."
            )
        ],
        "cta_headline": "Stop waiting for high BMI. Screen your real risk.",
        "cta_subtext": "Early-detection fasting insulin • Indian-specific metabolic cutoffs • Direct specialist physician access",
        "color_palette": {
            "hero_bg": "#4A2820",          # Deep Roasted Clay / Umber
            "cream_bg": "#F4ECE1",         # Calm Sand Cream
            "accent": "#C85A32",           # Warm Terracotta Ochre
            "accent_light": "#F7EDE6",     # Pale Clay Wash
            "text_dark": "#261C18",        # Deep Umber Ink
            "text_light": "#FBF8F3",       # Crisp Soft White
            "text_muted": "#8C7A70",       # Muted Clay Gray
            "text_muted_on_dark": "#D1BCB2", # Pale Clay Muted on Dark
            "border_dark": "#8A5E52",      # Clay Border
            "border_light": "#261C18",
            # Shorthands
            "oxblood": "#4A2820",
            "cream": "#F4ECE1",
            "rust": "#C85A32",
            "charcoal": "#261C18",
            "slate": "#8C7A70",
            "white": "#FBF8F3"
        },
        "metadata": {
            "journal": "BMJ Open Diabetes Research & Care (2021)",
            "doi": "10.1136/bmjdrc-2020-001997",
            "sample_size": 16240,
            "stat": "5.3x",
            "stat_label": "Higher Diabetes Risk in Normal-Weight Women",
            "stat_sub": "2.9x in men at normal BMI < 25 (BMJ Open 2021)"
        }
    }),

    # 3. SURPASS-2 2021: Tirzepatide Dual Incretin Co-Agonism (-11.2 kg)
    "SURPASS-2-2021": ThemeConfig({
        "study_id": "SURPASS-2-2021",
        "study_file": "papers/surpass2_tirzepatide_2021.json",
        "theme_name": "GIP + GLP-1 Incretin Synergy & Muscle Defense",
        "topic": "Dual Incretin Receptor Co-Agonism & Sarcopenia Defense",
        "hero_slide_index": 3,
        "hero_quote": "Dual co-agonism quiets hunger while restoring adipose insulin sensitivity.",
        "primary_motif": "receptor_lock",
        "secondary_motif": "progress_bars",
        "study_directive": "Co-activating GIP and GLP-1 delivers 11.2 kg weight loss with 86% reaching HbA1c <6.5%, requiring clinical DEXA scans to defend lean muscle.",
        "protocol_pillars": [
            (
                "01  Dual Incretin Precision Titration",
                "Micro-adjusted dosing schedules supervised by endocrinologists to eliminate nausea and digestive distress."
            ),
            (
                "02  DEXA Sarcopenia Defense",
                "Bi-monthly lean muscle tracking ensuring at least 75% of cleared mass is pathogenic visceral adipose tissue."
            ),
            (
                "03  Metabolic Nitrogen Preservation",
                "Dietitian-supervised amino acid and resistance protocols guarding resting metabolic rate during fat clearance."
            )
        ],
        "cta_headline": "Experience dual incretin care with active muscle defense.",
        "cta_subtext": "Dual GIP/GLP-1 clinical oversight • DEXA lean body mass tracking • High-protein metabolic architecture",
        "color_palette": {
            "hero_bg": "#1D3A29",          # Deep Forest Green / Pine
            "cream_bg": "#F2EFE9",         # Natural Flaxen Cream
            "accent": "#2D7D46",           # Botanical Emerald Green
            "accent_light": "#EAF4ED",     # Pale Mint Wash
            "text_dark": "#1B281F",        # Forest Ink
            "text_light": "#F7FAF8",       # Pristine Crisp White
            "text_muted": "#6E8074",       # Muted Sage
            "text_muted_on_dark": "#A4BEAF", # Soft Sage Mist on Dark
            "border_dark": "#4D735C",      # Sage Green Border
            "border_light": "#1B281F",
            # Shorthands
            "oxblood": "#1D3A29",
            "cream": "#F2EFE9",
            "rust": "#2D7D46",
            "charcoal": "#1B281F",
            "slate": "#6E8074",
            "white": "#F7FAF8"
        },
        "metadata": {
            "journal": "The New England Journal of Medicine (2021)",
            "doi": "10.1056/NEJMoa2107519",
            "sample_size": 1879,
            "stat": "-11.2 kg",
            "stat_label": "Superior Weight Loss at 40 Weeks",
            "stat_sub": "p <0.001 vs selective GLP-1 mono-agonist"
        }
    }),

    # 4. STEER-MACE 2026: Real-World Cardiovascular Survival (57% Lower MACE)
    "STEER-MACE-2026": ThemeConfig({
        "study_id": "STEER-MACE-2026",
        "study_file": "papers/steer_cv_outcomes_2026.json",
        "theme_name": "Cardiovascular Survival",
        "topic": "Real-World Arterial Decompression & 57% MACE Reduction",
        "hero_slide_index": 2,            # Early hero interrupt at Slide 2
        "hero_quote": "GLP-1 is direct cardiovascular medicine, not cosmetic weight loss.",
        "primary_motif": "cardiac_monitor",
        "secondary_motif": "arterial_flow",
        "study_directive": "Continuous physician-led GLP-1 care cuts major cardiac events by 57% and decompresses systolic blood pressure by 8.4 mmHg in 24,800 patients.",
        "protocol_pillars": [
            (
                "01  ApoB & Endothelial Telemetry",
                "Advanced atherogenic lipoprotein particle sizing and endothelial function monitoring beyond basic cholesterol."
            ),
            (
                "02  Continuous Hemodynamic Decompression",
                "24/7 digital blood pressure telemetry tracking vascular unloading and arterial compliance restoration."
            ),
            (
                "03  Cardioprotective Continuity Protocol",
                "Structured ongoing clinical oversight preventing the vascular rebound that follows abrupt cessation."
            )
        ],
        "cta_headline": "Protect your heart with direct cardiometabolic care.",
        "cta_subtext": "Advanced ApoB lipid profiling • Continuous arterial monitoring • Doctor-directed vascular preservation",
        "color_palette": {
            "hero_bg": "#162436",          # Deep Royal Navy / Midnight Cobalt
            "cream_bg": "#F1EDE6",         # Alabaster Paper Cream
            "accent": "#C04E2A",           # Cardiac Rust Red
            "accent_light": "#E8EEF5",     # Subtle Ice Blue Wash
            "text_dark": "#141C24",        # Navy Midnight Ink
            "text_light": "#FAF8F5",       # Ivory Star White
            "text_muted": "#6E7B8B",       # Muted Steel Slate
            "text_muted_on_dark": "#A4B8D1", # Soft Midnight Blue Mist on Dark
            "border_dark": "#3E5878",      # Midnight Blue Border
            "border_light": "#141C24",
            # Shorthands
            "oxblood": "#162436",
            "cream": "#F1EDE6",
            "rust": "#C04E2A",
            "charcoal": "#141C24",
            "slate": "#6E7B8B",
            "white": "#FAF8F5"
        },
        "metadata": {
            "journal": "Diabetes, Obesity and Metabolism (2026)",
            "doi": "10.1111/dom.70436",
            "sample_size": 24800,
            "stat": "57%",
            "stat_label": "Lower Rate of Major Cardiovascular Events",
            "stat_sub": "Major Adverse Cardiovascular Events (MACE) HR 0.43"
        }
    }),

    # 5. STEP-1 EXTENSION 2022: Neuro-Endocrine Rebound Alarm (67% Regain)
    "STEP-1-EXT-2022": ThemeConfig({
        "study_id": "STEP-1-EXT-2022",
        "study_file": "papers/step1_extension_2022.json",
        "theme_name": "Neuro-Endocrine Rebound Alarm",
        "topic": "Biological Set-Point Defense & Structured Exit Architecture",
        "hero_slide_index": 3,
        "hero_quote": "Stopping abruptly triggers a 240% primitive famine alarm.",
        "primary_motif": "hormone_scales",
        "secondary_motif": "telemetry_curve",
        "study_directive": "Stopping GLP-1 cold turkey returns 67% of lost weight within 12 months. Sustainable metabolic health requires a doctor-guided exit plan.",
        "protocol_pillars": [
            (
                "01  12-Week Structured Off-Ramp",
                "Physician-guided micro-tapering protocol preventing hypothalamic hunger surges and hormonal whiplash."
            ),
            (
                "02  Hypothalamic Set-Point Stabilization",
                "Continuous satiety hormone monitoring and biological hunger recalibration to lock in the new weight set-point."
            ),
            (
                "03  Metabolic Habit Architecture",
                "Behavioral, circadian, and nutritional habit formation designed so permanent routines hold the weight."
            )
        ],
        "cta_headline": "Never start a GLP-1 without a doctor-planned exit.",
        "cta_subtext": "12-week clinical tapering off-ramp • Set-point stabilization protocol • Permanent weight maintenance guarantee",
        "color_palette": {
            "hero_bg": "#5C181A",          # Deep Oxblood Crimson
            "cream_bg": "#F6EDE3",         # Warm Parchment Cream
            "accent": "#B84E28",           # Spiced Terracotta
            "accent_light": "#FCEFE8",     # Pale Terracotta Blush
            "text_dark": "#251B1A",        # Crimson Charcoal
            "text_light": "#FAF6F0",       # Parchment White
            "text_muted": "#8C7875",       # Muted Russet Slate
            "text_muted_on_dark": "#D2ADA8", # Roseate Parchment Slate on Dark
            "border_dark": "#964B4D",      # Crimson Border
            "border_light": "#251B1A",
            # Shorthands
            "oxblood": "#5C181A",
            "cream": "#F6EDE3",
            "rust": "#B84E28",
            "charcoal": "#251B1A",
            "slate": "#8C7875",
            "white": "#FAF6F0"
        },
        "metadata": {
            "journal": "Diabetes, Obesity and Metabolism (2022)",
            "doi": "10.1111/dom.14725",
            "sample_size": 327,
            "stat": "67%",
            "stat_label": "Weight Regained Within 12 Months",
            "stat_sub": "When medication is stopped without clinical tapering"
        }
    }),

    # 6. SURMOUNT-1 2022: Landmark 20.9% Obesity Clearance
    "SURMOUNT-1-2022": ThemeConfig({
        "study_id": "SURMOUNT-1-2022",
        "study_file": "papers/surmount1_tirzepatide_2022.json",
        "theme_name": "Landmark Obesity Clearance",
        "topic": "Unprecedented 20.9% Weight Reset & Visceral Clearing",
        "hero_slide_index": 2,            # Early hero interrupt at Slide 2
        "hero_quote": "Unprecedented 20.9% biological set-point reset.",
        "primary_motif": "dose_bars",
        "secondary_motif": "progress_bars",
        "study_directive": "91% achieved clinically significant fat clearance with a 14.6 cm waist drop. Deep weight reset requires medical supervision to protect metabolic rate.",
        "protocol_pillars": [
            (
                "01  Dose-Optimized Metabolic Escalation",
                "Bi-weekly physician titration schedules tailored to body response, maximizing fat loss while preventing gastrointestinal distress."
            ),
            (
                "02  DEXA Body Composition Auditing",
                "Precision dual-energy X-ray absorption scans every 60 days to verify visceral fat clearance and isolate lean mass."
            ),
            (
                "03  Visceral Adipose Clearance Verification",
                "Targeting pathogenic mesenteric and omental fat depots to permanently restore peripheral insulin sensitivity."
            )
        ],
        "cta_headline": "Unlock 20.9% clearance with clinical precision.",
        "cta_subtext": "Physician-led dose optimization • Full DEXA visceral auditing • Sarcopenia prevention protocol",
        "color_palette": {
            "hero_bg": "#C04E2A",          # Bold Terracotta Rust / Sedona Flame
            "cream_bg": "#F5ECE2",         # Warm Editorial Canvas Cream
            "accent": "#5C181A",           # Deep Oxblood Anchor
            "accent_light": "#FDEEE8",     # Soft Peach Wash
            "text_dark": "#221815",        # Warm Obsidian Ink
            "text_light": "#FFFBF7",       # Pure Warm Linen White
            "text_muted": "#856F67",       # Earthy Sandstone Muted
            "text_muted_on_dark": "#F4D2C7", # Soft Warm Linen Tint on Dark
            "border_dark": "#E07D5E",      # Terracotta Border Highlight
            "border_light": "#221815",
            # Shorthands
            "oxblood": "#5C181A",
            "cream": "#F5ECE2",
            "rust": "#C04E2A",
            "charcoal": "#221815",
            "slate": "#856F67",
            "white": "#FFFBF7"
        },
        "metadata": {
            "journal": "The New England Journal of Medicine (2022)",
            "doi": "10.1056/NEJMoa2206038",
            "sample_size": 2539,
            "stat": "-20.9%",
            "stat_label": "Mean Body Weight Loss at 72 Weeks",
            "stat_sub": "p <0.001 vs placebo in adults with obesity"
        }
    }),

    # 7. SELECT / STEP-1 2023: Atherosclerotic Plaque Stabilization (20% MACE Reduction)
    "SELECT-2023": ThemeConfig({
        "study_id": "SELECT-2023",
        "study_file": "papers/step1_trial_summary.json",
        "theme_name": "Atherosclerotic Plaque Stabilization",
        "topic": "Vascular Endothelial Survival & 20% MACE Reduction",
        "hero_slide_index": 3,
        "hero_quote": "Cardiovascular survival benefits occur before major weight loss.",
        "primary_motif": "survival_curve",
        "secondary_motif": "stethoscope",
        "study_directive": "Cardiovascular risk plunged 20% independent of diabetes status (n=17,604), proving GLP-1 stabilizes vulnerable arterial plaques directly.",
        "protocol_pillars": [
            (
                "01  Endothelial Micro-Inflammation Panels",
                "Serial hs-CRP, Lp-PLA2, and oxidized LDL assays measuring biological vascular inflammation resolution."
            ),
            (
                "02  Hemodynamic Wall Tension Decompression",
                "Medical blood pressure and arterial stiffness optimization guarding against micro-ischemic events."
            ),
            (
                "03  Cardiometabolic Sanctuary Program",
                "Multi-disciplinary physician protocol shielding arterial beds from cytokine-driven atherogenesis."
            )
        ],
        "cta_headline": "Stabilize vascular health with evidence-backed care.",
        "cta_subtext": "55+ vascular inflammation biomarkers • Direct cardiologist oversight • Complete cardiometabolic protection",
        "color_palette": {
            "hero_bg": "#1E2F2F",          # Deep Cypress Teal / Slate Spruce
            "cream_bg": "#F0EBE3",         # Oatmeal Cream Canvas
            "accent": "#C85A32",           # Atheroma Rust Highlight
            "accent_light": "#E6F0EE",     # Pale Cypress Mist
            "text_dark": "#172222",        # Dark Cypress Ink
            "text_light": "#F5FAF8",       # Opal Frost White
            "text_muted": "#6F807E",       # Spruce Slate
            "text_muted_on_dark": "#A4BDBB", # Frost Spruce Mist on Dark
            "border_dark": "#426362",      # Teal Slate Border
            "border_light": "#172222",
            # Shorthands
            "oxblood": "#1E2F2F",
            "cream": "#F0EBE3",
            "rust": "#C85A32",
            "charcoal": "#172222",
            "slate": "#6F807E",
            "white": "#F5FAF8"
        },
        "metadata": {
            "journal": "New England Journal of Medicine (2023)",
            "doi": "10.1056/NEJMoa2307563",
            "sample_size": 17604,
            "stat": "20%",
            "stat_label": "Lower Rate of Major Cardiovascular Events",
            "stat_sub": "Primary composite MACE Hazard Ratio HR 0.80 (p <0.001)"
        }
    })
}

# Link alias for STEP-1 trial summary to point directly to SELECT / STEP-1 Plaque Stabilization
STUDY_THEMES["STEP-1-2021"] = STUDY_THEMES["SELECT-2023"]


# -----------------------------------------------------------------------------
# ALIAS LOOKUP TABLE
# -----------------------------------------------------------------------------

STUDY_KEY_ALIASES: Dict[str, str] = {
    # Lancet TOFI
    "tofi": "LANCET-TOFI-2021",
    "lancet": "LANCET-TOFI-2021",
    "lancet_tofi": "LANCET-TOFI-2021",
    "lancet_tofi_2021": "LANCET-TOFI-2021",
    "lancet_tofi_70kg": "LANCET-TOFI-2021",
    "70kg": "LANCET-TOFI-2021",
    "indian_tofi": "LANCET-TOFI-2021",
    "ectopic": "LANCET-TOFI-2021",

    # BMJ Narayan
    "narayan": "BMJ-NARAYAN-2021",
    "bmj": "BMJ-NARAYAN-2021",
    "bmj_narayan": "BMJ-NARAYAN-2021",
    "bmj_narayan_tofi": "BMJ-NARAYAN-2021",
    "bmj_narayan_tofi_2021": "BMJ-NARAYAN-2021",
    "bmi_22": "BMJ-NARAYAN-2021",
    "threshold": "BMJ-NARAYAN-2021",

    # SURPASS-2
    "surpass": "SURPASS-2-2021",
    "surpass2": "SURPASS-2-2021",
    "surpass_2": "SURPASS-2-2021",
    "surpass2_tirzepatide": "SURPASS-2-2021",
    "surpass2_tirzepatide_2021": "SURPASS-2-2021",
    "tirzepatide": "SURPASS-2-2021",
    "dual_incretin": "SURPASS-2-2021",

    # STEER-MACE
    "mace": "STEER-MACE-2026",
    "cardio": "STEER-MACE-2026",
    "steer_mace": "STEER-MACE-2026",
    "steer_cv": "STEER-MACE-2026",
    "steer_mace_cardio": "STEER-MACE-2026",
    "steer_cv_outcomes_2026": "STEER-MACE-2026",
    "cv_outcomes": "STEER-MACE-2026",

    # STEP-1 EXTENSION
    "step1_ext": "STEP-1-EXT-2022",
    "step_1_ext": "STEP-1-EXT-2022",
    "step1_extension": "STEP-1-EXT-2022",
    "step1_extension_rebound": "STEP-1-EXT-2022",
    "step1_extension_2022": "STEP-1-EXT-2022",
    "rebound": "STEP-1-EXT-2022",

    # SURMOUNT-1
    "surmount": "SURMOUNT-1-2022",
    "surmount1": "SURMOUNT-1-2022",
    "surmount_1": "SURMOUNT-1-2022",
    "surmount1_tirzepatide": "SURMOUNT-1-2022",
    "surmount1_tirzepatide_2022": "SURMOUNT-1-2022",

    # SELECT / STEP-1
    "select": "SELECT-2023",
    "select_trial": "SELECT-2023",
    "select_trial_cv": "SELECT-2023",
    "step1": "SELECT-2023",
    "step1_trial_summary": "SELECT-2023",
    "step1_summary": "SELECT-2023",
    "step-1": "SELECT-2023"
}


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS & SELECTORS
# -----------------------------------------------------------------------------

def resolve_study_key(study_or_id: Any) -> str:
    """
    Normalizes any study object, study_id string, filename, or alias into
    the canonical study key matching STUDY_THEMES.
    """
    if not study_or_id:
        return "LANCET-TOFI-2021"

    # Handle ClinicalStudy or object with study_id attribute
    if hasattr(study_or_id, "study_id"):
        raw_key = str(study_or_id.study_id).strip().upper()
        if raw_key in STUDY_THEMES:
            return raw_key
        # Check title if available
        title = getattr(study_or_id, "title", "").lower()
        search_str = f"{raw_key.lower()} {title}"
    else:
        search_str = str(study_or_id).strip().lower()

    # Exact canonical check
    upper_key = search_str.upper()
    if upper_key in STUDY_THEMES:
        return upper_key

    # Alias dict direct check
    clean_search = search_str.replace("-", "_").replace(" ", "_").strip("/\\")
    # Take basename if path
    if "/" in clean_search or "\\" in clean_search:
        import os
        clean_search = os.path.basename(clean_search).replace(".json", "")
    
    if clean_search in STUDY_KEY_ALIASES:
        return STUDY_KEY_ALIASES[clean_search]

    # Substring heuristic checks
    if "narayan" in search_str or "bmj" in search_str:
        return "BMJ-NARAYAN-2021"
    if "surpass" in search_str:
        return "SURPASS-2-2021"
    if "mace" in search_str or "cardio" in search_str or "steer_cv" in search_str:
        return "STEER-MACE-2026"
    if "extension" in search_str or "rebound" in search_str or "step_1_ext" in search_str:
        return "STEP-1-EXT-2022"
    if "surmount" in search_str:
        return "SURMOUNT-1-2022"
    if "select" in search_str or "plaque" in search_str:
        return "SELECT-2023"
    if "tofi" in search_str or "70kg" in search_str or "lancet" in search_str:
        return "LANCET-TOFI-2021"

    # Default fallback
    return "LANCET-TOFI-2021"


def get_study_theme(study_or_id: Any = None) -> ThemeConfig:
    """
    Returns the rich ThemeConfig dictionary for a given study or identifier.
    Guarantees all required theme attributes are present.
    """
    key = resolve_study_key(study_or_id)
    return STUDY_THEMES.get(key, STUDY_THEMES["LANCET-TOFI-2021"])


def get_color_palette(study_or_id: Any = None) -> Dict[str, str]:
    """Returns the study-specific color palette."""
    return get_study_theme(study_or_id)["color_palette"]


def get_hero_slide_index(study_or_id: Any = None) -> int:
    """Returns the study-specific hero slide index (2 or 3)."""
    return get_study_theme(study_or_id)["hero_slide_index"]


def get_hero_quote(study_or_id: Any = None) -> str:
    """Returns the publication-grade editorial hero quote."""
    return get_study_theme(study_or_id)["hero_quote"]


def get_primary_motif(study_or_id: Any = None) -> str:
    """Returns the primary illustration motif key."""
    return get_study_theme(study_or_id)["primary_motif"]


def get_secondary_motif(study_or_id: Any = None) -> str:
    """Returns the secondary illustration motif key."""
    return get_study_theme(study_or_id)["secondary_motif"]


def get_study_directive(study_or_id: Any = None) -> str:
    """Returns the unique clinical takeaway for slides 1/2."""
    return get_study_theme(study_or_id)["study_directive"]


def get_protocol_pillars(study_or_id: Any = None) -> List[Tuple[str, str]]:
    """Returns the 3 bespoke Steer clinical protocol steps."""
    return get_study_theme(study_or_id)["protocol_pillars"]


def get_cta(study_or_id: Any = None) -> Dict[str, str]:
    """Returns the paper-tailored CTA headline and subtext."""
    theme = get_study_theme(study_or_id)
    return {
        "headline": theme["cta_headline"],
        "subtext": theme["cta_subtext"]
    }


def list_all_study_themes() -> List[ThemeConfig]:
    """Returns a list of all distinct canonical study themes."""
    canonical_keys = [
        "LANCET-TOFI-2021",
        "BMJ-NARAYAN-2021",
        "SURPASS-2-2021",
        "STEER-MACE-2026",
        "STEP-1-EXT-2022",
        "SURMOUNT-1-2022",
        "SELECT-2023"
    ]
    return [STUDY_THEMES[k] for k in canonical_keys]
