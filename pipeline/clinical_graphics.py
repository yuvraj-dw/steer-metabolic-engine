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

def draw_vector_check(draw, x, y, color="#235937"):
    draw.line([(x, y + 8), (x + 6, y + 15)], fill=color, width=3)
    draw.line([(x + 6, y + 15), (x + 16, y)], fill=color, width=3)

def draw_tofi_dexa_diagram(w=840, h=360) -> Image.Image:
    """Renders dual DEXA body scan comparison in Steer calm editorial aesthetic."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Left Column: European Control (Subcutaneous)
    # Right Column: South Asian TOFI (Ectopic Visceral)
    col_w = (w - 60) // 2
    
    # 1. Left Card
    x1, y1 = 20, 20
    draw.rounded_rectangle([x1, y1, x1 + col_w, y1 + h - 40], radius=12, fill="#EFE8DE", outline="#DCD3C7", width=1)
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
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

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
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

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
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.text((24, 18), "STEP-1 TRIAL EXTENSION (n=327)", fill=PALETTE["clay"], font=get_font(13, bold=True))
    draw.text((24, 38), "The Neuro-Endocrine Rebound Alarm", fill=PALETTE["oxblood"], font=get_font(22, bold=True, serif=True))

    # Center Fulcrum & Balance Beam
    cx = w // 2
    beam_y = 115
    # Angled beam tilting down on Ghrelin side
    draw.line([(cx - 240, beam_y + 25), (cx + 240, beam_y - 25)], fill=PALETTE["clay"], width=5)
    # Triangular fulcrum
    draw.polygon([(cx, beam_y), (cx - 20, beam_y + 42), (cx + 20, beam_y + 42)], fill=PALETTE["oxblood"])

    # Left Pan (Heavy: Ghrelin Surge)
    pan1_x, pan1_y = cx - 220, beam_y + 48
    draw.line([(cx - 220, beam_y + 25), (pan1_x, pan1_y)], fill=PALETTE["clay"], width=2)
    draw.rounded_rectangle([pan1_x - 90, pan1_y, pan1_x + 90, pan1_y + 80], radius=12, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=2)
    draw.text((pan1_x - 75, pan1_y + 10), "GHRELIN (HUNGER)", fill=PALETTE["rust"], font=get_font(14, bold=True))
    draw.text((pan1_x - 75, pan1_y + 30), "+240% Surge", fill=PALETTE["oxblood"], font=get_font(20, bold=True, serif=True))
    draw.text((pan1_x - 75, pan1_y + 56), "Urgent Food Noise", fill=PALETTE["clay"], font=get_font(13))

    # Right Pan (Light: Leptin Crash)
    pan2_x, pan2_y = cx + 220, beam_y - 8
    draw.line([(cx + 220, beam_y - 25), (pan2_x, pan2_y)], fill=PALETTE["clay"], width=2)
    draw.rounded_rectangle([pan2_x - 90, pan2_y, pan2_x + 90, pan2_y + 80], radius=12, fill=PALETTE["teal_light"], outline=PALETTE["teal"], width=2)
    draw.text((pan2_x - 75, pan2_y + 10), "LEPTIN (SATIETY)", fill=PALETTE["teal"], font=get_font(14, bold=True))
    draw.text((pan2_x - 75, pan2_y + 30), "-40% Crash", fill=PALETTE["teal"], font=get_font(20, bold=True, serif=True))
    draw.text((pan2_x - 75, pan2_y + 56), "Starvation Alarm", fill=PALETTE["clay"], font=get_font(13))

    # Bottom Takeaway Slab (Positioned with 30px clear space below pans)
    ban_y = 275
    draw.rounded_rectangle([24, ban_y, w - 24, ban_y + 60], radius=10, fill="#FAF3EB", outline=PALETTE["border"], width=1)
    draw.text((44, ban_y + 20), "Unmonitored stopping regains 67% of weight. Steer's planned off-ramp recalibrates the thermostat.", fill=PALETTE["oxblood"], font=get_font(14, bold=True))

    return img

def draw_narayan_diagram(w=840, h=360) -> Image.Image:
    """Renders South Asian BMI 22.0 threshold vs Western 25.0 benchmark diagram."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

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

def draw_slide1_telemetry(study_id: str = "", w=840, h=240) -> Image.Image:
    """Renders publication-grade vector trajectory/telemetry for Carousel Slide 1."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    sid = (study_id or "").upper()

    if "STEP" in sid or "REBOUND" in sid:
        draw.text((24, 16), "STEP-1 REBOUND TRAJECTORY (WEEKS 0 -> 120)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        # Grid area
        gx1, gx2 = 110, w - 40
        gy_top, gy_bot = 55, 185
        
        # Y-Axis Ticks & Labels
        draw.line([(gx1, gy_top), (gx2, gy_top)], fill="#F0E8DF", width=1)
        draw.text((24, gy_top - 7), "0.0% Base", fill=PALETTE["clay"], font=get_font(12))
        
        gy_mid = gy_top + (gy_bot - gy_top) // 3
        draw.line([(gx1, gy_mid), (gx2, gy_mid)], fill="#F0E8DF", width=1)
        draw.text((24, gy_mid - 7), "-5.0% Loss", fill=PALETTE["clay"], font=get_font(12))
        
        gy_mid2 = gy_top + 2 * (gy_bot - gy_top) // 3
        draw.line([(gx1, gy_mid2), (gx2, gy_mid2)], fill="#F0E8DF", width=1)
        draw.text((24, gy_mid2 - 7), "-10.0% Loss", fill=PALETTE["clay"], font=get_font(12))

        draw.line([(gx1, gy_bot), (gx2, gy_bot)], fill="#F0E8DF", width=1)
        draw.text((24, gy_bot - 7), "-15.0% Peak", fill=PALETTE["rust"], font=get_font(12, bold=True))
        
        # Vertical axis
        draw.line([(gx1, gy_top), (gx1, gy_bot)], fill="#D8C8B8", width=2)
        
        # Timeline X Labels
        draw.text((gx1 - 10, gy_bot + 12), "Wk 0", fill=PALETTE["clay"], font=get_font(13))
        draw.text((gx1 + 250, gy_bot + 12), "Wk 68 (Medication Stop)", fill=PALETTE["oxblood"], font=get_font(13, bold=True))
        draw.text((gx2 - 50, gy_bot + 12), "Wk 120", fill=PALETTE["clay"], font=get_font(13))
        
        # Dotted line at Wk 68
        wk68_x = gx1 + 290
        for y_dash in range(gy_top, gy_bot, 7):
            draw.line([(wk68_x, y_dash), (wk68_x, y_dash + 4)], fill=PALETTE["clay"], width=1)
            
        # Curve 1: Weeks 0 to 68 Smooth sigmoidal clinical descent (-15% Peak Loss)
        descent_pts = []
        for i in range(25):
            t = i / 24.0
            curve_factor = (1.0 - math.exp(-2.8 * t)) / (1.0 - math.exp(-2.8))
            x = gx1 + t * (wk68_x - gx1)
            y = (gy_top + 8) + curve_factor * (gy_bot - (gy_top + 8))
            descent_pts.append((x, y))
        for j in range(len(descent_pts) - 1):
            draw.line([descent_pts[j], descent_pts[j + 1]], fill=PALETTE["rust"], width=4)
        
        # Callout placed cleanly at the nadir
        draw.text((wk68_x - 130, gy_bot - 20), "-15.0% Peak Loss", fill=PALETTE["rust"], font=get_font(12, bold=True))
        
        # Curve 2: Week 68 to 120 Unguided Rebound (+67% Regain)
        rebound_pts = []
        for i in range(20):
            t = i / 19.0
            rebound_factor = (1.0 - math.exp(-2.5 * t)) / (1.0 - math.exp(-2.5))
            x = wk68_x + t * (gx2 - 10 - wk68_x)
            y = gy_bot - rebound_factor * (gy_bot - gy_mid)
            rebound_pts.append((x, y))
        for j in range(len(rebound_pts) - 1):
            draw.line([rebound_pts[j], rebound_pts[j + 1]], fill=PALETTE["oxblood"], width=4)
        
        draw.rounded_rectangle([gx2 - 225, gy_mid - 24, gx2 - 5, gy_mid + 6], radius=6, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=1)
        draw.text((gx2 - 215, gy_mid - 19), "Unguided (+67% Regained)", fill=PALETTE["oxblood"], font=get_font(13, bold=True))
        
        # Curve 3: Steer Planned Exit (Plateau Defended)
        draw.line([(wk68_x, gy_bot), (gx2 - 10, gy_bot)], fill=PALETTE["teal"], width=4)
        draw.rounded_rectangle([gx2 - 225, gy_bot - 24, gx2 - 5, gy_bot + 6], radius=6, fill=PALETTE["teal_light"], outline=PALETTE["teal"], width=1)
        draw.text((gx2 - 215, gy_bot - 19), "Steer Exit (Set-Point Maintained)", fill=PALETTE["teal"], font=get_font(13, bold=True))

    elif "SURMOUNT" in sid:
        draw.text((24, 16), "SURMOUNT-1 DOSE-DEPENDENT WEIGHT CLEARANCE AT 72 WEEKS (NEJM)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        draw.text((28, 48), "Placebo: -3.1%  |  Tirzepatide 5 mg: -15.0%  |  10 mg: -19.5%", fill=PALETTE["ink"], font=get_font(13, bold=True))
        b1_w = 400
        draw.rounded_rectangle([28, 72, 28 + b1_w, 102], radius=6, fill=PALETTE["blush"], outline="#D2B5A5", width=1)
        draw.text((45, 78), "-15.0% to -19.5% Substantial Loss", fill=PALETTE["ink"], font=get_font(13, bold=True))
        
        draw.text((28, 118), "Tirzepatide 15 mg (Dual GIP/GLP-1 Co-Agonist)", fill=PALETTE["oxblood"], font=get_font(14, bold=True))
        b2_w = 540
        draw.rounded_rectangle([28, 142, 28 + b2_w, 180], radius=8, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=2)
        draw.text((45, 151), "-20.9% Average Body Weight Reduction (p < 0.001)", fill=PALETTE["oxblood"], font=get_font(15, bold=True))
        
        # Side Badge
        draw.rounded_rectangle([w - 220, 80, w - 24, 175], radius=10, fill=PALETTE["teal_light"], outline=PALETTE["teal"], width=1)
        draw.text((w - 205, 95), "91% SUCCESS", fill=PALETTE["teal"], font=get_font(14, bold=True))
        draw.text((w - 205, 119), "Achieved >5% Loss", fill=PALETTE["oxblood"], font=get_font(13, bold=True))
        draw.text((w - 205, 141), "57% Reached >20%", fill=PALETTE["clay"], font=get_font(12))
        draw.text((28, 198), "Highest degree of medical weight clearance ever recorded in a global phase 3 trial.", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    elif "SELECT" in sid:
        draw.text((24, 16), "40-MONTH COMPOSITE MACE EVENT-FREE SURVIVAL (n=17,604)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        gx1, gx2 = 100, w - 40
        gy_top, gy_bot = 55, 180
        
        draw.line([(gx1, gy_top), (gx2, gy_top)], fill="#F0E8DF", width=1)
        draw.text((24, gy_top - 7), "100%", fill=PALETTE["clay"], font=get_font(12))
        
        gy_mid = gy_top + (gy_bot - gy_top) // 2
        draw.line([(gx1, gy_mid), (gx2, gy_mid)], fill="#F5EFEB", width=1)
        draw.text((24, gy_mid - 7), "95%", fill=PALETTE["clay"], font=get_font(12))
        
        draw.line([(gx1, gy_bot), (gx2, gy_bot)], fill="#F0E8DF", width=1)
        draw.text((24, gy_bot - 7), "90%", fill=PALETTE["clay"], font=get_font(12))
        draw.line([(gx1, gy_top), (gx1, gy_bot)], fill="#D8C8B8", width=2)
        
        # Timeline X
        draw.text((gx1 - 5, gy_bot + 10), "Month 0", fill=PALETTE["clay"], font=get_font(12))
        draw.text((gx1 + 180, gy_bot + 10), "Month 20", fill=PALETTE["clay"], font=get_font(12))
        draw.text((gx2 - 50, gy_bot + 10), "Month 40", fill=PALETTE["clay"], font=get_font(12))
        
        # Survival curves
        draw.line([(gx1, gy_top + 4), (gx2 - 10, gy_top + 24)], fill=PALETTE["teal"], width=4)
        draw.rounded_rectangle([gx2 - 245, gy_top + 12, gx2 - 5, gy_top + 40], radius=6, fill=PALETTE["teal_light"], outline=PALETTE["teal"], width=1)
        draw.text((gx2 - 235, gy_top + 18), "Semaglutide 2.4mg (6.5% Event Rate)", fill=PALETTE["teal"], font=get_font(12, bold=True))
        
        draw.line([(gx1, gy_top + 4), (gx2 - 10, gy_mid + 8)], fill=PALETTE["oxblood"], width=4)
        draw.rounded_rectangle([gx2 - 245, gy_mid - 2, gx2 - 5, gy_mid + 26], radius=6, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=1)
        draw.text((gx2 - 235, gy_mid + 4), "Placebo Group (8.0% Event Rate)", fill=PALETTE["oxblood"], font=get_font(12, bold=True))
        
        draw.text((28, 206), "Hazard Ratio HR 0.80: 20% lower rate of CV death, nonfatal MI, and stroke (NEJM 2023)", fill=PALETTE["clay"], font=get_font(13, bold=True))

    elif "SURPASS" in sid or "TIRZEPATIDE" in sid:
        draw.text((24, 16), "HEAD-TO-HEAD WEIGHT CLEARANCE AT 40 WEEKS (NEJM)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        # Bar 1: Semaglutide 1.0mg
        draw.text((28, 54), "Semaglutide 1.0 mg (GLP-1 Mono-Agonist)", fill=PALETTE["ink"], font=get_font(15, bold=True))
        b1_w = 340
        draw.rounded_rectangle([28, 82, 28 + b1_w, 122], radius=8, fill=PALETTE["blush"], outline="#D2B5A5", width=1)
        draw.text((45, 92), "-7.0 kg average reduction", fill=PALETTE["ink"], font=get_font(16, bold=True))
        
        # Bar 2: Tirzepatide 15mg
        draw.text((28, 136), "Tirzepatide 15 mg (Dual GIP/GLP-1 Co-Agonist)", fill=PALETTE["oxblood"], font=get_font(15, bold=True))
        b2_w = 540
        draw.rounded_rectangle([28, 164, 28 + b2_w, 204], radius=8, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=2)
        draw.text((45, 174), "-11.2 kg average reduction (+60% Superior Clearance)", fill=PALETTE["oxblood"], font=get_font(16, bold=True))
        
        # Side Badge
        draw.rounded_rectangle([w - 220, 95, w - 24, 185], radius=10, fill=PALETTE["teal_light"], outline=PALETTE["teal"], width=1)
        draw.text((w - 205, 110), "+4.2 KG DELTA", fill=PALETTE["teal"], font=get_font(14, bold=True))
        draw.text((w - 205, 134), "p < 0.001 vs Mono", fill=PALETTE["oxblood"], font=get_font(15, bold=True))
        draw.text((w - 205, 156), "Muscle Preserved", fill=PALETTE["clay"], font=get_font(13))

    elif "MACE" in sid or "CARDIO" in sid or "STEER" in sid:
        draw.text((24, 16), "4-YEAR CARDIOVASCULAR EVENT-FREE SURVIVAL (n=24,800)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        gx1, gx2 = 100, w - 40
        gy_top, gy_bot = 55, 180
        
        draw.line([(gx1, gy_top), (gx2, gy_top)], fill="#F0E8DF", width=1)
        draw.text((24, gy_top - 7), "100%", fill=PALETTE["clay"], font=get_font(12))
        
        gy_mid = gy_top + (gy_bot - gy_top) // 2
        draw.line([(gx1, gy_mid), (gx2, gy_mid)], fill="#F5EFEB", width=1)
        draw.text((24, gy_mid - 7), "90%", fill=PALETTE["clay"], font=get_font(12))
        
        draw.line([(gx1, gy_bot), (gx2, gy_bot)], fill="#F0E8DF", width=1)
        draw.text((24, gy_bot - 7), "80%", fill=PALETTE["clay"], font=get_font(12))
        draw.line([(gx1, gy_top), (gx1, gy_bot)], fill="#D8C8B8", width=2)
        
        # Timeline X
        draw.text((gx1 - 5, gy_bot + 10), "Year 0", fill=PALETTE["clay"], font=get_font(12))
        draw.text((gx1 + 180, gy_bot + 10), "Year 2", fill=PALETTE["clay"], font=get_font(12))
        draw.text((gx2 - 50, gy_bot + 10), "Year 4", fill=PALETTE["clay"], font=get_font(12))
        
        # Survival curves
        draw.line([(gx1, gy_top + 4), (gx2 - 10, gy_top + 28)], fill=PALETTE["teal"], width=4)
        draw.rounded_rectangle([gx2 - 240, gy_top + 14, gx2 - 5, gy_top + 42], radius=6, fill=PALETTE["teal_light"], outline=PALETTE["teal"], width=1)
        draw.text((gx2 - 230, gy_top + 20), "Steer Continuous Care (94.2%)", fill=PALETTE["teal"], font=get_font(13, bold=True))
        
        draw.line([(gx1, gy_top + 4), (gx2 - 10, gy_bot - 14)], fill=PALETTE["oxblood"], width=4)
        draw.rounded_rectangle([gx2 - 240, gy_bot - 34, gx2 - 5, gy_bot - 6], radius=6, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=1)
        draw.text((gx2 - 230, gy_bot - 28), "Standard Caloric Care (86.5%)", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    elif "NARAYAN" in sid:
        draw.text((24, 16), "DIABETES INFLEXION THRESHOLD AT NORMAL WEIGHT (BMJ OPEN)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        mw = (w - 70) // 2
        # Western
        draw.rounded_rectangle([24, 52, 24 + mw, 210], radius=12, fill=PALETTE["teal_light"], outline="#CDE4D6", width=1)
        draw.text((44, 66), "WESTERN POPULATION REFERENCE", fill=PALETTE["teal"], font=get_font(13, bold=True))
        draw.text((44, 90), "BMI 25.0 Saturation Threshold", fill=PALETTE["ink"], font=get_font(18, bold=True))
        draw.text((44, 122), "• Subcutaneous adipose stores expand safely", fill=PALETTE["clay"], font=get_font(14))
        draw.text((44, 148), "• Organs protected from premature lipid spillover", fill=PALETTE["clay"], font=get_font(14))
        draw.text((44, 174), "• Low diabetes incidence at BMI 22.0", fill=PALETTE["teal"], font=get_font(14, bold=True))
        
        # South Asian
        x2 = 24 + mw + 22
        draw.rounded_rectangle([x2, 52, x2 + mw, 210], radius=12, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
        draw.text((x2 + 20, 66), "SOUTH ASIAN PHENOTYPE", fill=PALETTE["rust"], font=get_font(13, bold=True))
        draw.text((x2 + 20, 90), "BMI 22.0 Premature Inflexion", fill=PALETTE["oxblood"], font=get_font(18, bold=True))
        draw.text((x2 + 20, 122), "• Adipose saturation occurs 3 BMI points lower", fill=PALETTE["oxblood"], font=get_font(14, bold=True))
        draw.text((x2 + 20, 148), "• Ectopic fat spills into liver and pancreas", fill=PALETTE["oxblood"], font=get_font(14, bold=True))
        draw.text((x2 + 20, 174), "• 5.3x Diabetes Risk at normal scale weight!", fill=PALETTE["oxblood"], font=get_font(14, bold=True))

    else:
        # Default: Lancet TOFI Adiposity Split-Bar
        draw.text((24, 16), "INTERNAL VISCERAL VS SUBCUTANEOUS ADIPOSITY SPLIT (AT 70.0 KG)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        # Bar 1: European 70kg
        draw.text((28, 52), "European Control (70.0 kg • BMI 22.8)", fill=PALETTE["ink"], font=get_font(15, bold=True))
        draw.rounded_rectangle([28, 78, 28 + 480, 116], radius=8, fill=PALETTE["teal_light"], outline="#CBE2D3", width=1)
        draw.text((45, 88), "82% Subcutaneous Safe Buffer  •  18% Visceral (48 cm³)", fill=PALETTE["teal"], font=get_font(15, bold=True))
        
        # Bar 2: South Asian TOFI 70kg
        draw.text((28, 132), "South Asian TOFI (70.0 kg • BMI 22.8)", fill=PALETTE["oxblood"], font=get_font(15, bold=True))
        draw.rounded_rectangle([28, 158, 28 + 620, 196], radius=8, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=2)
        draw.text((45, 168), "45% Subcutaneous  •  55% Visceral (184 cm³, +283% Toxic Organ Fat)", fill=PALETTE["oxblood"], font=get_font(15, bold=True))
        
        draw.text((28, 212), "External body scale reads identical while internal visceral fat strangles organs.", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    return img

def draw_slide3_telemetry(study_id: str = "", w=840, h=230) -> Image.Image:
    """Renders publication-grade secondary biomarker panels for Carousel Slide 3."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    sid = (study_id or "").upper()

    if "STEP" in sid or "REBOUND" in sid:
        draw.text((24, 16), "SECONDARY CARDIOMETABOLIC DRIFT AT 12 MONTHS (POST-CESSATION)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        tile_w = (w - 70) // 3
        # Tile 1: Blood Pressure
        tx1 = 24
        draw.rounded_rectangle([tx1, 50, tx1 + tile_w, 205], radius=12, fill="#FAF4F0", outline="#ECDCD4", width=1)
        draw.text((tx1 + 18, 64), "BLOOD PRESSURE", fill=PALETTE["clay"], font=get_font(13, bold=True))
        draw.text((tx1 + 18, 88), "+6.2 mmHg", fill=PALETTE["oxblood"], font=get_font(26, bold=True, serif=True))
        draw.text((tx1 + 18, 130), "Systolic pressure reverted", fill=PALETTE["ink"], font=get_font(14))
        draw.text((tx1 + 18, 154), "entirely to pre-trial baseline", fill=PALETTE["ink"], font=get_font(14))
        draw.text((tx1 + 18, 180), "• Vascular Strain", fill=PALETTE["oxblood"], font=get_font(12, bold=True))

        # Tile 2: HbA1c
        tx2 = tx1 + tile_w + 11
        draw.rounded_rectangle([tx2, 50, tx2 + tile_w, 205], radius=12, fill="#FAF4F0", outline="#ECDCD4", width=1)
        draw.text((tx2 + 18, 64), "HbA1c GLYCEMIC", fill=PALETTE["clay"], font=get_font(13, bold=True))
        draw.text((tx2 + 18, 88), "+0.4% Drift", fill=PALETTE["rust"], font=get_font(26, bold=True, serif=True))
        draw.text((tx2 + 18, 130), "Glycemic improvements", fill=PALETTE["ink"], font=get_font(14))
        draw.text((tx2 + 18, 154), "lost post-discontinuation", fill=PALETTE["ink"], font=get_font(14))
        draw.text((tx2 + 18, 180), "• Insulin Resistance", fill=PALETTE["rust"], font=get_font(12, bold=True))

        # Tile 3: Fasting Lipids
        tx3 = tx2 + tile_w + 11
        draw.rounded_rectangle([tx3, 50, tx3 + tile_w, 205], radius=12, fill="#FAF4F0", outline="#ECDCD4", width=1)
        draw.text((tx3 + 18, 64), "FASTING LIPIDS", fill=PALETTE["clay"], font=get_font(13, bold=True))
        draw.text((tx3 + 18, 88), "+22 mg/dL", fill=PALETTE["oxblood"], font=get_font(26, bold=True, serif=True))
        draw.text((tx3 + 18, 130), "Circulating triglycerides", fill=PALETTE["ink"], font=get_font(14))
        draw.text((tx3 + 18, 154), "surged back to baseline", fill=PALETTE["ink"], font=get_font(14))
        draw.text((tx3 + 18, 180), "• Lipid Relapse", fill=PALETTE["oxblood"], font=get_font(12, bold=True))

    elif "SURMOUNT" in sid:
        draw.text((24, 16), "SURMOUNT-1 SECONDARY METABOLIC ENDPOINTS (NEJM 2022)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        tile_w = (w - 60) // 2
        tx1 = 24
        draw.rounded_rectangle([tx1, 50, tx1 + tile_w, 205], radius=12, fill=PALETTE["teal_light"], outline="#CBE2D3", width=1)
        draw.text((tx1 + 20, 66), "WAIST CIRCUMFERENCE", fill=PALETTE["teal"], font=get_font(14, bold=True))
        draw.text((tx1 + 20, 92), "-14.6 cm", fill=PALETTE["teal"], font=get_font(28, bold=True, serif=True))
        draw.text((tx1 + 20, 136), "Mean reduction in waist circumference at 72 weeks", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx1 + 20, 162), "reflecting deep internal visceral organ fat clearance.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx1 + 20, 184), "• Direct Visceral Decompression", fill=PALETTE["teal"], font=get_font(13, bold=True))

        tx2 = tx1 + tile_w + 12
        draw.rounded_rectangle([tx2, 50, tx2 + tile_w, 205], radius=12, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
        draw.text((tx2 + 20, 66), "DEEP WEIGHT RESPONSE", fill=PALETTE["rust"], font=get_font(14, bold=True))
        draw.text((tx2 + 20, 92), "57% Over 20%", fill=PALETTE["oxblood"], font=get_font(28, bold=True, serif=True))
        draw.text((tx2 + 20, 136), "Over half of 15mg participants lost >20% body weight.", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx2 + 20, 162), "Steer pairs titration with DEXA scans to preserve muscle.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx2 + 20, 184), "• Doctor-Supervised Muscle Defense", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    elif "SELECT" in sid:
        draw.text((24, 16), "SELECT TRIAL CARDIOVASCULAR RISK REDUCTION (NEJM 2023)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        tile_w = (w - 60) // 2
        tx1 = 24
        draw.rounded_rectangle([tx1, 50, tx1 + tile_w, 205], radius=12, fill=PALETTE["teal_light"], outline="#CBE2D3", width=1)
        draw.text((tx1 + 20, 66), "PRIMARY MACE REDUCTION", fill=PALETTE["teal"], font=get_font(14, bold=True))
        draw.text((tx1 + 20, 92), "20% Lower Risk", fill=PALETTE["teal"], font=get_font(28, bold=True, serif=True))
        draw.text((tx1 + 20, 136), "Hazard ratio HR 0.80 (p < 0.001) for composite MACE", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx1 + 20, 162), "including cardiovascular death, nonfatal MI, and stroke.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx1 + 20, 184), "• Vascular Endothelial Protection", fill=PALETTE["teal"], font=get_font(13, bold=True))

        tx2 = tx1 + tile_w + 12
        draw.rounded_rectangle([tx2, 50, tx2 + tile_w, 205], radius=12, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
        draw.text((tx2 + 20, 66), "POPULATION SIGNIFICANCE", fill=PALETTE["rust"], font=get_font(14, bold=True))
        draw.text((tx2 + 20, 92), "n = 17,604", fill=PALETTE["oxblood"], font=get_font(28, bold=True, serif=True))
        draw.text((tx2 + 20, 136), "Cardioprotection demonstrated in overweight & obesity", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx2 + 20, 162), "in the absence of diabetes across 40 months follow-up.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx2 + 20, 184), "• Incretin as Cardiovascular Medicine", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    elif "SURPASS" in sid or "TIRZEPATIDE" in sid:
        draw.text((24, 16), "SECONDARY ENDPOINTS & MUSCLE DEFENSE (NEJM)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        tile_w = (w - 60) // 2
        # Tile 1: Glycemic Remission
        tx1 = 24
        draw.rounded_rectangle([tx1, 50, tx1 + tile_w, 205], radius=12, fill=PALETTE["teal_light"], outline="#CBE2D3", width=1)
        draw.text((tx1 + 20, 66), "GLYCEMIC NORMALIZATION", fill=PALETTE["teal"], font=get_font(14, bold=True))
        draw.text((tx1 + 20, 92), "86% Under 6.5%", fill=PALETTE["teal"], font=get_font(28, bold=True, serif=True))
        draw.text((tx1 + 20, 136), "Participants achieved clinical target HbA1c <6.5%", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx1 + 20, 162), "with profound visceral lipid clearance.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx1 + 20, 184), "• Profound Metabolic Remission", fill=PALETTE["teal"], font=get_font(13, bold=True))

        # Tile 2: Lean Muscle Defense
        tx2 = tx1 + tile_w + 12
        draw.rounded_rectangle([tx2, 50, tx2 + tile_w, 205], radius=12, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
        draw.text((tx2 + 20, 66), "LEAN MUSCLE DEFENSE NEED", fill=PALETTE["rust"], font=get_font(14, bold=True))
        draw.text((tx2 + 20, 92), "Up to 35% Loss", fill=PALETTE["oxblood"], font=get_font(28, bold=True, serif=True))
        draw.text((tx2 + 20, 136), "Rapid unguided weight loss risks lean tissue wasting.", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx2 + 20, 162), "Steer monitors muscle preservation via regular DEXA.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx2 + 20, 184), "• Doctor-Supervised Protein Protocol", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    elif "MACE" in sid or "CARDIO" in sid or "STEER" in sid:
        draw.text((24, 16), "SECONDARY HEMODYNAMIC ENDPOINTS (DOM 2026)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        tile_w = (w - 60) // 2
        tx1 = 24
        draw.rounded_rectangle([tx1, 50, tx1 + tile_w, 205], radius=12, fill=PALETTE["teal_light"], outline="#CBE2D3", width=1)
        draw.text((tx1 + 20, 66), "SYSTOLIC BLOOD PRESSURE", fill=PALETTE["teal"], font=get_font(14, bold=True))
        draw.text((tx1 + 20, 92), "-8.4 mmHg", fill=PALETTE["teal"], font=get_font(28, bold=True, serif=True))
        draw.text((tx1 + 20, 136), "Direct decompression of arterial vessel wall", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx1 + 20, 162), "delivers sustained vascular pressure relief.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx1 + 20, 184), "• Endothelial Decompression", fill=PALETTE["teal"], font=get_font(13, bold=True))

        tx2 = tx1 + tile_w + 12
        draw.rounded_rectangle([tx2, 50, tx2 + tile_w, 205], radius=12, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
        draw.text((tx2 + 20, 66), "SYSTEMIC INFLAMMATION", fill=PALETTE["rust"], font=get_font(14, bold=True))
        draw.text((tx2 + 20, 92), "-32% hs-CRP", fill=PALETTE["oxblood"], font=get_font(28, bold=True, serif=True))
        draw.text((tx2 + 20, 136), "High-sensitivity CRP reduction stabilizes plaques", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx2 + 20, 162), "preventing micro-vascular ischemic rupture.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx2 + 20, 184), "• Plaque Stabilization", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    elif "NARAYAN" in sid:
        draw.text((24, 16), "RELATIVE RISK MULTIPLIER AT NORMAL BMI 22.0 (BMJ OPEN)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        tile_w = (w - 60) // 2
        tx1 = 24
        draw.rounded_rectangle([tx1, 50, tx1 + tile_w, 205], radius=12, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
        draw.text((tx1 + 20, 66), "SOUTH ASIAN MEN (BMI 22.0)", fill=PALETTE["rust"], font=get_font(14, bold=True))
        draw.text((tx1 + 20, 92), "2.9x Risk", fill=PALETTE["oxblood"], font=get_font(28, bold=True, serif=True))
        draw.text((tx1 + 20, 136), "Nearly triple the diabetes incidence rate", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx1 + 20, 162), "compared to matched European men of same weight.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx1 + 20, 184), "• Premature Metabolic Saturation", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

        tx2 = tx1 + tile_w + 12
        draw.rounded_rectangle([tx2, 50, tx2 + tile_w, 205], radius=12, fill=PALETTE["rust_light"], outline=PALETTE["oxblood"], width=2)
        draw.text((tx2 + 20, 66), "SOUTH ASIAN WOMEN (BMI 22.0)", fill=PALETTE["oxblood"], font=get_font(14, bold=True))
        draw.text((tx2 + 20, 92), "5.3x Risk", fill=PALETTE["oxblood"], font=get_font(28, bold=True, serif=True))
        draw.text((tx2 + 20, 136), "Over five times higher diabetes vulnerability", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx2 + 20, 162), "completely hidden under a normal bathroom scale reading.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx2 + 20, 184), "• Severe Ectopic Vulnerability", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    else:
        # Default: Lancet TOFI Organ Steatosis
        draw.text((24, 16), "ORGAN ECTOPIC STEATOSIS BREAKDOWN (LANCET 2021)", fill=PALETTE["clay"], font=get_font(14, bold=True))
        
        tile_w = (w - 60) // 2
        tx1 = 24
        draw.rounded_rectangle([tx1, 50, tx1 + tile_w, 205], radius=12, fill=PALETTE["rust_light"], outline="#F5C5B5", width=1)
        draw.text((tx1 + 20, 66), "HEPATIC STEATOSIS (LIVER)", fill=PALETTE["rust"], font=get_font(14, bold=True))
        draw.text((tx1 + 20, 92), "+80% Organ Fat", fill=PALETTE["oxblood"], font=get_font(28, bold=True, serif=True))
        draw.text((tx1 + 20, 136), "Severe visceral fat infiltration triggers non-alcoholic", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx1 + 20, 162), "fatty liver and fasting insulin resistance at BMI 22.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx1 + 20, 184), "• Primary Driver of Insulin Resistance", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

        tx2 = tx1 + tile_w + 12
        draw.rounded_rectangle([tx2, 50, tx2 + tile_w, 205], radius=12, fill=PALETTE["rust_light"], outline=PALETTE["rust"], width=1)
        draw.text((tx2 + 20, 66), "PANCREATIC BETA-CELL STRAIN", fill=PALETTE["oxblood"], font=get_font(14, bold=True))
        draw.text((tx2 + 20, 92), "Lipotoxicity", fill=PALETTE["oxblood"], font=get_font(28, bold=True, serif=True))
        draw.text((tx2 + 20, 136), "Fat droplets around islets directly exhaust beta-cells,", fill=PALETTE["ink"], font=get_font(15))
        draw.text((tx2 + 20, 162), "shutting down natural insulin secretion early.", fill=PALETTE["clay"], font=get_font(14))
        draw.text((tx2 + 20, 184), "• Beta-Cell Secretory Exhaustion", fill=PALETTE["oxblood"], font=get_font(13, bold=True))

    return img

def render_instagram_hero_slide(study_id: str, output_path: str) -> str:
    """
    Renders a dedicated, full-bleed 1080x1350 (4:5) Instagram Feed Hero Card
    incorporating the study's clean vector art diagram, clinical telemetry, and branding.
    100% Safe For Work, zero AI artifacts, publication-grade typography.
    """
    width, height = 1080, 1350
    img = Image.new("RGBA", (width, height), PALETTE["taupe"])
    draw = ImageDraw.Draw(img)

    # 1. Background Paper Texture Overlay
    draw.rectangle([0, 0, width, height], fill=PALETTE["taupe"])

    # 2. Main Center Card
    card_margin = 70
    card_w = width - (card_margin * 2)
    card_h = height - 160
    card_top = 80
    draw.rounded_rectangle(
        [card_margin, card_top, card_margin + card_w, card_top + card_h],
        radius=28,
        fill=PALETTE["soft_paper"],
        outline="#D8C8B8",
        width=1
    )

    # Resolve Study Metadata
    sid = (study_id or "").upper()
    if "SURMOUNT" in sid:
        tag = "NEJM 2022 OBESITY TRIAL (n=2,539)"
        title = "Up to 20.9% Deep Weight Reset."
        subtitle = "SURMOUNT-1 proves dual incretins achieve unprecedented clinical weight clearance."
        takeaway = "Dual GIP/GLP-1 co-agonism resets hypothalamic set-points with muscle defense."
        diag_img = draw_surpass_diagram(card_w - 60, 360)
    elif "SELECT" in sid:
        tag = "NEJM 2023 LANDMARK TRIAL (n=17,604)"
        title = "20% Lower Heart Attack & Stroke Risk."
        subtitle = "SELECT trial confirms semaglutide protects cardiovascular health in obesity."
        takeaway = "Cardiovascular protection operates through direct vascular endothelial relief."
        diag_img = draw_mace_diagram(card_w - 60, 360)
    elif "SURPASS" in sid or "TIRZEPATIDE" in sid:
        tag = "NEJM 2021 TRIAL EVIDENCE"
        title = "Dual Incretin Receptor Synergy."
        subtitle = "Tirzepatide co-activates GLP-1 and GIP for superior clinical weight reduction."
        takeaway = "Dual agonist synergy delivers -11.2 kg weight loss with muscle preservation."
        diag_img = draw_surpass_diagram(card_w - 60, 360)
    elif "MACE" in sid or "CARDIO" in sid or "STEER" in sid:
        tag = "REAL-WORLD EVIDENCE (n=24,800)"
        title = "GLP-1 is Cardiovascular Medicine."
        subtitle = "Visceral fat decompression protects cardiac endothelium from event storm."
        takeaway = "Continuous clinical care yields 57% lower heart attacks and strokes."
        diag_img = draw_mace_diagram(card_w - 60, 360)
    elif "STEP" in sid or "REBOUND" in sid:
        tag = "STEP-1 TRIAL EXTENSION"
        title = "The Neuro-Endocrine Rebound Trap."
        subtitle = "Why 67% of lost weight returns when treatment is abruptly stopped unguided."
        takeaway = "Medicine is the jumpstart. Maintenance is the goal with a planned exit."
        diag_img = draw_step1_diagram(card_w - 60, 360)
    elif "NARAYAN" in sid:
        tag = "BMJ OPEN COHORT (n=16,240)"
        title = "Normal Weight Hides 5.3x Diabetes Risk."
        subtitle = "Premature metabolic saturation strikes South Asians at BMI 22.0."
        takeaway = "DEXA visceral fat scanning must replace the weighing scale on Day 1."
        diag_img = draw_narayan_diagram(card_w - 60, 360)
    else:
        tag = "LANCET CLINICAL ANOMALY"
        title = "The 70 kg Paradox & Indian TOFI."
        subtitle = "Identical scale weight. 80% higher toxic visceral fat inside internal organs."
        takeaway = "It's biology, not lack of willpower. Medical care resets internal health."
        diag_img = draw_tofi_dexa_diagram(card_w - 60, 360)

    # 3. Header Section inside Card
    y_text = card_top + 45
    # Tag Pill
    draw.rounded_rectangle([card_margin + 35, y_text, card_margin + 35 + 260, y_text + 34], radius=17, fill="#E6D3C2")
    draw.text((card_margin + 50, y_text + 8), tag, fill=PALETTE["oxblood"], font=get_font(13, bold=True))
    y_text += 50

    # Title & Subtitle
    draw.text((card_margin + 35, y_text), title, fill=PALETTE["oxblood"], font=get_font(34, bold=True, serif=True))
    y_text += 48
    draw.text((card_margin + 35, y_text), subtitle, fill=PALETTE["clay"], font=get_font(18))
    y_text += 38

    # 4. Paste Vector Diagram
    img.paste(diag_img, (card_margin + 30, y_text), diag_img if diag_img.mode == "RGBA" else None)
    y_text += diag_img.height + 25

    # 5. Takeaway Box (With vector checkmark, zero tofu)
    draw.rounded_rectangle([card_margin + 30, y_text, card_margin + card_w - 30, y_text + 70], radius=14, fill=PALETTE["teal_light"], outline="#D3E8D9", width=1)
    draw_vector_check(draw, card_margin + 55, y_text + 22, color=PALETTE["teal"])
    draw.text((card_margin + 85, y_text + 22), takeaway, fill=PALETTE["teal"], font=get_font(18, bold=True))
    y_text += 95

    # 6. Lower Canvas: 3-Pillar Clinical Action Protocol (Fills space gracefully)
    draw.text((card_margin + 35, y_text), "STEER CLINICAL PROTOCOL", fill=PALETTE["clay"], font=get_font(14, bold=True))
    y_text += 26

    pillars = [
        ("01  Precision Biomarker Telemetry", "Quantify internal visceral organ fat on Day 1 with DEXA scanning."),
        ("02  Metabolic Set-Point Recalibration", "Hormonal therapy designed to quiet food noise without starvation."),
        ("03  Doctor-Guided Planned Off-Ramp", "Gradual tapering and habit anchoring so weight never rebounds.")
    ]

    for p_title, p_desc in pillars:
        draw.rounded_rectangle([card_margin + 30, y_text, card_margin + card_w - 30, y_text + 68], radius=12, fill=PALETTE["white"], outline=PALETTE["border"], width=1)
        draw.text((card_margin + 48, y_text + 12), p_title, fill=PALETTE["oxblood"], font=get_font(16, bold=True))
        draw.text((card_margin + 48, y_text + 36), p_desc, fill=PALETTE["ink"], font=get_font(15))
        y_text += 80

    # 7. Steer Footer inside Card
    foot_y = card_top + card_h - 45
    draw.text((card_margin + 35, foot_y), "steer • Clinical Metabolic Care", fill=PALETTE["oxblood"], font=get_font(16, bold=True, serif=True))
    draw.text((card_margin + card_w - 180, foot_y), "steerclub.com", fill=PALETTE["clay"], font=get_font(16))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return output_path

def render_study_graphic(study_id: str, output_path: str, width=840, height=360) -> str:
    """Generate and save the vector clinical diagram for a given study."""
    sid = (study_id or "").upper()
    if "SURMOUNT" in sid or "SURPASS" in sid or "TIRZEPATIDE" in sid:
        img = draw_surpass_diagram(width, height)
    elif "SELECT" in sid or "MACE" in sid or "CARDIO" in sid or "STEER" in sid:
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
