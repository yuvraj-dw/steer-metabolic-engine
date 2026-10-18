"""
Steer Clinical Editorial Graphic Engine
Renders high-status, publication-grade vector medical diagrams in Steer's calm editorial palette:
  - Lancet TOFI: Dual DEXA cross-section (Internal Visceral Ectopic Fat vs Subcutaneous)
  - SURPASS-2: Dual Incretin Co-Agonism (GLP-1 Satiety + GIP Lipid Buffering)
  - STEER MACE: Arterial Decompression & 57% Endothelial Plaque Reduction
  - STEP-1 Extension: Hypothalamic Set-Point Scales (Ghrelin +240% vs Leptin -40%)
  - BMJ Narayan: South Asian BMI 22.0 Inflexion Point vs Western 25.0 Benchmark
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

PALETTE = {
    "taupe": "#E4D7C8",
    "soft_paper": "#FAF5EE",
    "white": "#FFFFFF",
    "rust": "#C04E2A",
    "oxblood": "#5C1D18",
    "ink": "#2B1616",
    "clay": "#7D5246",
    "blush": "#DEC3B5",
    "teal": "#235937",
    "teal_light": "#EDF5F0",
    "rust_light": "#FDF0EB",
    "gold": "#D4A373",
    "border": "#E2D3C4"
}

WINDOWS_FONTS = "C:/Windows/Fonts"

def get_font(size: int, bold: bool = False, serif: bool = False):
    try:
        if serif:
            font_file = "georgiab.ttf" if bold else "georgia.ttf"
        else:
            font_file = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(os.path.join(WINDOWS_FONTS, font_file), size)
    except Exception:
        return ImageFont.load_default()

def draw_tofi_dexa_diagram(w=840, h=360) -> Image.Image:
    """Renders dual DEXA body scan comparison in Steer calm editorial aesthetic."""
    img = Image.new("RGBA", (w, h), PALETTE["soft_paper"])
    draw = ImageDraw.Draw(img)

    # Frame
    draw.rounded_rectangle([2, 2, w - 2, h - 2], radius=16, fill=PALETTE["white"], outline=PALETTE["border"], width=1)

    # Left Column: European Control (Subcutaneous)
    # Right Column: South Asian TOFI (Ectopic Visceral)
    col_w = (w - 60) // 2
    
    # 1. Left Card
    x1, y1 = 20, 20
    draw.rounded_rectangle([x1, y1, x1 + col_w, y1 + h - 40], radius=12, fill="#F9FAF8", outline="#E0E6E2", width=1)
    draw.text((x1 + 18, y1 + 16), "EUROPEAN REFERENCE", fill=PALETTE["clay"], font=get_font(15, bold=True))
    draw.text((x1 + 18, y1 + 38), "Subcutaneous Safe Buffer", fill=PALETTE["ink"], font=get_font(20, bold=True, serif=True))
    draw.text((x1 + 18, y1 + 68), "Weight: 70.0 kg  •  BMI: 22.8", fill=PALETTE["clay"], font=get_font(15))

    # Silhouette Left (Centered between BMI text and metric pill)
    cx1 = x1 + col_w // 2
    cy1 = y1 + 170
    # Head & torso outline
    draw.ellipse([cx1 - 18, cy1 - 85, cx1 + 18, cy1 - 49], fill="#EBECE8", outline="#C4C8C2", width=1)
    draw.rounded_rectangle([cx1 - 38, cy1 - 44, cx1 + 38, cy1 + 75], radius=12, fill="#EBECE8", outline="#C4C8C2", width=1)
    # Subcutaneous fat rim (Green safe border)
    draw.rounded_rectangle([cx1 - 44, cy1 - 40, cx1 - 38, cy1 + 70], radius=4, fill="#34A853")
    draw.rounded_rectangle([cx1 + 38, cy1 - 40, cx1 + 44, cy1 + 70], radius=4, fill="#34A853")
    # Low visceral fat tag
    draw.rounded_rectangle([x1 + 18, y1 + h - 85, x1 + col_w - 18, y1 + h - 55], radius=8, fill=PALETTE["teal_light"])
    draw.text((x1 + 28, y1 + h - 77), "VAT: 48 cm³ (Peripheral Storage)", fill=PALETTE["teal"], font=get_font(15, bold=True))

    # 2. Right Card
    x2 = x1 + col_w + 20
    draw.rounded_rectangle([x2, y1, x2 + col_w, y1 + h - 40], radius=12, fill=PALETTE["rust_light"], outline="#F5C7B8", width=1)
    draw.text((x2 + 18, y1 + 16), "SOUTH ASIAN PHENOTYPE", fill=PALETTE["rust"], font=get_font(15, bold=True))
    draw.text((x2 + 18, y1 + 38), "Ectopic Organ Infiltration", fill=PALETTE["oxblood"], font=get_font(20, bold=True, serif=True))
    draw.text((x2 + 18, y1 + 68), "Weight: 70.0 kg  •  BMI: 22.8", fill=PALETTE["clay"], font=get_font(15))

    # Silhouette Right (Centered between BMI text and metric pill)
    cx2 = x2 + col_w // 2
    cy2 = y1 + 170
    # Head & torso outline (Identical outward size)
    draw.ellipse([cx2 - 18, cy2 - 85, cx2 + 18, cy2 - 49], fill="#EBECE8", outline="#C4C8C2", width=1)
    draw.rounded_rectangle([cx2 - 38, cy2 - 44, cx2 + 38, cy2 + 75], radius=12, fill="#EBECE8", outline="#C4C8C2", width=1)
    # Dense visceral organ fat mass (Oxblood/Rust core)
    draw.ellipse([cx2 - 28, cy2 - 22, cx2 + 28, cy2 + 42], fill=PALETTE["rust"], outline=PALETTE["oxblood"], width=2)
    draw.ellipse([cx2 - 14, cy2 - 8, cx2 + 14, cy2 + 24], fill=PALETTE["oxblood"])
    # High visceral fat tag
    draw.rounded_rectangle([x2 + 18, y1 + h - 85, x2 + col_w - 18, y1 + h - 55], radius=8, fill="#FCECE8")
    draw.text((x2 + 28, y1 + h - 77), "VAT: 184 cm³ (+283% Toxic Organ Fat)", fill=PALETTE["oxblood"], font=get_font(15, bold=True))

    return img

def draw_surpass_diagram(w=840, h=360) -> Image.Image:
    """Renders dual incretin receptor co-agonism synergy diagram."""
    img = Image.new("RGBA", (w, h), PALETTE["soft_paper"])
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([2, 2, w - 2, h - 2], radius=16, fill=PALETTE["white"], outline=PALETTE["border"], width=1)

    # Header Tag
    draw.text((24, 20), "NEJM 2021 TRIAL MECHANISM", fill=PALETTE["clay"], font=get_font(14, bold=True))
    draw.text((24, 42), "Dual Incretin Co-Agonism Synergy", fill=PALETTE["oxblood"], font=get_font(24, bold=True, serif=True))

    # Dual Axis Cards
    box_w = (w - 70) // 2
    # 1. GLP-1 Box
    bx1, by = 24, 90
    draw.rounded_rectangle([bx1, by, bx1 + box_w, by + 160], radius=14, fill=PALETTE["teal_light"], outline="#CBE2D3", width=1)
    draw.text((bx1 + 18, by + 16), "AXIS 1: GLP-1 RECEPTOR", fill=PALETTE["teal"], font=get_font(15, bold=True))
    draw.text((bx1 + 18, by + 42), "Hypothalamic Satiety", fill=PALETTE["ink"], font=get_font(20, bold=True, serif=True))
    draw.text((bx1 + 18, by + 78), "• Quiets persistent food noise and cravings", fill=PALETTE["clay"], font=get_font(16))
    draw.text((bx1 + 18, by + 104), "• Slows gastric transit for sustained fullness", fill=PALETTE["clay"], font=get_font(16))
    draw.text((bx1 + 18, by + 130), "• Mean weight reduction: -7.0 kg", fill=PALETTE["teal"], font=get_font(15, bold=True))

    # 2. GIP Box
    bx2 = bx1 + box_w + 22
    draw.rounded_rectangle([bx2, by, bx2 + box_w, by + 160], radius=14, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
    draw.text((bx2 + 18, by + 16), "AXIS 2: GIP RECEPTOR", fill=PALETTE["rust"], font=get_font(15, bold=True))
    draw.text((bx2 + 18, by + 42), "Adipose Insulin Sensitivity", fill=PALETTE["oxblood"], font=get_font(20, bold=True, serif=True))
    draw.text((bx2 + 18, by + 78), "• Activates lipid buffering in adipose depots", fill=PALETTE["clay"], font=get_font(16))
    draw.text((bx2 + 18, by + 104), "• Protects resting energy burn and lean muscle", fill=PALETTE["clay"], font=get_font(16))
    draw.text((bx2 + 18, by + 130), "• Mean weight reduction: -11.2 kg (+60% Superior)", fill=PALETTE["oxblood"], font=get_font(15, bold=True))

    # Bottom Synergy Banner (No unrendered emoji glyphs)
    ban_y = by + 175
    draw.rounded_rectangle([24, ban_y, w - 24, ban_y + 60], radius=10, fill="#F5EFE6", outline=PALETTE["border"], width=1)
    draw.text((44, ban_y + 18), "SYNERGISTIC OUTCOME: 86% of patients normalized HbA1c <6.5% with double the weight reduction.", fill=PALETTE["oxblood"], font=get_font(15, bold=True))

    return img

def draw_mace_diagram(w=840, h=360) -> Image.Image:
    """Renders cardiovascular endothelial decompression & arterial defense diagram."""
    img = Image.new("RGBA", (w, h), PALETTE["soft_paper"])
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([2, 2, w - 2, h - 2], radius=16, fill=PALETTE["white"], outline=PALETTE["border"], width=1)

    draw.text((24, 20), "CARDIOMETABOLIC OUTCOMES (n=24,800)", fill=PALETTE["clay"], font=get_font(14, bold=True))
    draw.text((24, 42), "Arterial Decompression & Vascular Defense", fill=PALETTE["oxblood"], font=get_font(24, bold=True, serif=True))

    # Two Comparative Artery Cross-Sections
    box_w = (w - 70) // 2
    by = 90
    
    # Left: Obstructed / Inflamed Artery (Crash Diet)
    bx1 = 24
    draw.rounded_rectangle([bx1, by, bx1 + box_w, by + 230], radius=14, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
    draw.text((bx1 + 18, by + 16), "STANDARD CARE / REBOUND", fill=PALETTE["rust"], font=get_font(15, bold=True))
    draw.text((bx1 + 18, by + 40), "Arterial Stiffness & Plaque", fill=PALETTE["oxblood"], font=get_font(19, bold=True, serif=True))
    
    # Artery Cross section circle
    acx1 = bx1 + box_w // 2
    acy1 = by + 130
    draw.ellipse([acx1 - 42, acy1 - 42, acx1 + 42, acy1 + 42], fill="#EAC0B5", outline=PALETTE["oxblood"], width=4)
    # Constricted lumen
    draw.ellipse([acx1 - 14, acy1 - 14, acx1 + 14, acy1 + 14], fill="#D84B37")
    draw.text((bx1 + 18, by + 190), "• Baseline MACE Hazard (1.00x)", fill=PALETTE["clay"], font=get_font(15))
    draw.text((bx1 + 18, by + 210), "• Elevated systemic inflammation (hs-CRP)", fill=PALETTE["oxblood"], font=get_font(14, bold=True))

    # Right: Decompressed Open Artery (Steer Continuous Care)
    bx2 = bx1 + box_w + 22
    draw.rounded_rectangle([bx2, by, bx2 + box_w, by + 230], radius=14, fill=PALETTE["teal_light"], outline="#CBE2D3", width=1)
    draw.text((bx2 + 18, by + 16), "STEER CONTINUOUS CARE", fill=PALETTE["teal"], font=get_font(15, bold=True))
    draw.text((bx2 + 18, by + 40), "Restored Endothelial Flow", fill=PALETTE["teal"], font=get_font(19, bold=True, serif=True))

    acx2 = bx2 + box_w // 2
    acy2 = by + 130
    draw.ellipse([acx2 - 42, acy2 - 42, acx2 + 42, acy2 + 42], fill="#D3E8D9", outline=PALETTE["teal"], width=4)
    # Wide open lumen
    draw.ellipse([acx2 - 28, acy2 - 28, acx2 + 28, acy2 + 28], fill="#235937")
    draw.text((bx2 + 18, by + 190), "• 57% Lower Heart Attack & Stroke (HR 0.43)", fill=PALETTE["teal"], font=get_font(15, bold=True))
    draw.text((bx2 + 18, by + 210), "• Systolic blood pressure reduced by -8.4 mmHg", fill=PALETTE["clay"], font=get_font(14))

    return img

def draw_step1_diagram(w=840, h=360) -> Image.Image:
    """Renders hypothalamic set-point hunger hormone balance scales."""
    img = Image.new("RGBA", (w, h), PALETTE["soft_paper"])
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([2, 2, w - 2, h - 2], radius=16, fill=PALETTE["white"], outline=PALETTE["border"], width=1)

    draw.text((24, 20), "STEP-1 TRIAL EXTENSION (n=327)", fill=PALETTE["clay"], font=get_font(14, bold=True))
    draw.text((24, 42), "The Neuro-Endocrine Rebound Alarm", fill=PALETTE["oxblood"], font=get_font(24, bold=True, serif=True))

    # Center Fulcrum & Balance Beam
    cx = w // 2
    beam_y = 150
    # Angled beam tilting down on Ghrelin side
    draw.line([(cx - 240, beam_y + 40), (cx + 240, beam_y - 40)], fill=PALETTE["clay"], width=5)
    # Triangular fulcrum
    draw.polygon([(cx, beam_y), (cx - 22, beam_y + 50), (cx + 22, beam_y + 50)], fill=PALETTE["oxblood"])

    # Left Pan (Heavy: Ghrelin Surge)
    pan1_x, pan1_y = cx - 220, beam_y + 65
    draw.line([(cx - 220, beam_y + 40), (pan1_x, pan1_y)], fill=PALETTE["clay"], width=2)
    draw.rounded_rectangle([pan1_x - 90, pan1_y, pan1_x + 90, pan1_y + 90], radius=12, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=2)
    draw.text((pan1_x - 75, pan1_y + 12), "GHRELIN (HUNGER)", fill=PALETTE["rust"], font=get_font(15, bold=True))
    draw.text((pan1_x - 75, pan1_y + 36), "+240% Surge", fill=PALETTE["oxblood"], font=get_font(22, bold=True, serif=True))
    draw.text((pan1_x - 75, pan1_y + 66), "Urgent Food Noise", fill=PALETTE["clay"], font=get_font(14))

    # Right Pan (Light: Leptin Crash)
    pan2_x, pan2_y = cx + 220, beam_y - 15
    draw.line([(cx + 220, beam_y - 40), (pan2_x, pan2_y)], fill=PALETTE["clay"], width=2)
    draw.rounded_rectangle([pan2_x - 90, pan2_y, pan2_x + 90, pan2_y + 90], radius=12, fill=PALETTE["teal_light"], outline=PALETTE["teal"], width=2)
    draw.text((pan2_x - 75, pan2_y + 12), "LEPTIN (SATIETY)", fill=PALETTE["teal"], font=get_font(15, bold=True))
    draw.text((pan2_x - 75, pan2_y + 36), "-40% Crash", fill=PALETTE["teal"], font=get_font(22, bold=True, serif=True))
    draw.text((pan2_x - 75, pan2_y + 66), "Starvation Alarm", fill=PALETTE["clay"], font=get_font(14))

    # Bottom Takeaway Slab
    ban_y = 285
    draw.rounded_rectangle([24, ban_y, w - 24, ban_y + 55], radius=10, fill="#FAF3EB", outline=PALETTE["border"], width=1)
    draw.text((44, ban_y + 16), "Unmonitored stopping regains 67% of weight. Steer's planned off-ramp recalibrates the thermostat.", fill=PALETTE["oxblood"], font=get_font(15, bold=True))

    return img

def draw_narayan_diagram(w=840, h=360) -> Image.Image:
    """Renders South Asian BMI 22.0 threshold vs Western 25.0 benchmark diagram."""
    img = Image.new("RGBA", (w, h), PALETTE["soft_paper"])
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([2, 2, w - 2, h - 2], radius=16, fill=PALETTE["white"], outline=PALETTE["border"], width=1)

    draw.text((24, 20), "BMJ OPEN COHORT (n=16,240)", fill=PALETTE["clay"], font=get_font(14, bold=True))
    draw.text((24, 42), "The Premature Inflexion Point Anomaly", fill=PALETTE["oxblood"], font=get_font(24, bold=True, serif=True))

    box_w = (w - 70) // 2
    by = 90
    
    # Left: Western Cutoff
    bx1 = 24
    draw.rounded_rectangle([bx1, by, bx1 + box_w, by + 230], radius=14, fill=PALETTE["teal_light"], outline="#CBE2D3", width=1)
    draw.text((bx1 + 18, by + 16), "WESTERN THRESHOLD", fill=PALETTE["teal"], font=get_font(15, bold=True))
    draw.text((bx1 + 18, by + 40), "BMI 25.0 Inflexion Point", fill=PALETTE["teal"], font=get_font(20, bold=True, serif=True))
    draw.text((bx1 + 18, by + 76), "• Subcutaneous fat expands safely until BMI 25", fill=PALETTE["clay"], font=get_font(15))
    draw.text((bx1 + 18, by + 106), "• Diabetes risk baseline: 1.0x", fill=PALETTE["clay"], font=get_font(15))
    draw.text((bx1 + 18, by + 136), "• Weighing scale detects excess weight early", fill=PALETTE["clay"], font=get_font(15))
    draw.rounded_rectangle([bx1 + 18, by + 175, bx1 + box_w - 18, by + 210], radius=8, fill="#FFFFFF")
    draw.text((bx1 + 28, by + 185), "Standard Clinical Sensitivity", fill=PALETTE["teal"], font=get_font(14, bold=True))

    # Right: South Asian Anomaly
    bx2 = bx1 + box_w + 22
    draw.rounded_rectangle([bx2, by, bx2 + box_w, by + 230], radius=14, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
    draw.text((bx2 + 18, by + 16), "SOUTH ASIAN ANOMALY", fill=PALETTE["rust"], font=get_font(15, bold=True))
    draw.text((bx2 + 18, by + 40), "BMI 22.0 Saturation Point", fill=PALETTE["oxblood"], font=get_font(20, bold=True, serif=True))
    draw.text((bx2 + 18, by + 76), "• Storage saturates at BMI 22.0 (3 points lower!)", fill=PALETTE["oxblood"], font=get_font(15, bold=True))
    draw.text((bx2 + 18, by + 106), "• Normal-weight diabetes risk: 2.9x Men / 5.3x Women", fill=PALETTE["oxblood"], font=get_font(15, bold=True))
    draw.text((bx2 + 18, by + 136), "• Weighing scale completely misses internal fat", fill=PALETTE["clay"], font=get_font(15))
    draw.rounded_rectangle([bx2 + 18, by + 175, bx2 + box_w - 18, by + 210], radius=8, fill="#FFFFFF")
    draw.text((bx2 + 28, by + 185), "Requires DEXA Scan on Day 1", fill=PALETTE["rust"], font=get_font(14, bold=True))

    return img

def render_study_graphic(study_id: str, output_path: str, width=840, height=360) -> str:
    """Generate and save the vector clinical diagram for a given study."""
    sid = (study_id or "").upper()
    if "SURPASS" in sid or "TIRZEPATIDE" in sid:
        img = draw_surpass_diagram(width, height)
    elif "MACE" in sid or "CARDIO" in sid or "STEER" in sid:
        img = draw_mace_diagram(width, height)
    elif "STEP" in sid or "REBOUND" in sid:
        img = draw_step1_diagram(width, height)
    elif "NARAYAN" in sid:
        img = draw_narayan_diagram(width, height)
    else:
        # Default: Lancet TOFI 70kg paradox
        img = draw_tofi_dexa_diagram(width, height)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return output_path
