import os
import sys
from PIL import Image, ImageDraw, ImageFont

PALETTE = {
    "cream": "#F5EBDF",
    "rust": "#C04E2A",
    "deep_maroon": "#661414",
    "ink": "#351D1D",
    "clay": "#7D5246",
    "blush": "#DEC3B5",
    "soft_paper": "#FAF5EF",
    "white": "#FFFFFF"
}

WINDOWS_FONTS = "C:/Windows/Fonts"

def get_serif(size, bold=False, italic=False):
    try:
        if italic and bold:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "georgiaz.ttf"), size)
        elif italic:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "georgiai.ttf"), size)
        elif bold:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "georgiab.ttf"), size)
        else:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "georgia.ttf"), size)
    except Exception:
        return ImageFont.load_default()

def get_sans(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "arialbd.ttf"), size)
        else:
            return ImageFont.truetype(os.path.join(WINDOWS_FONTS, "arial.ttf"), size)
    except Exception:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    words = text.split(" ")
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_header_badge(draw, text="CLINICAL DECONSTRUCTION", y=75, left_align=80):
    font = get_sans(19, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    badge_w = tw + 32
    badge_h = 36
    draw.rounded_rectangle([left_align, y, left_align + badge_w, y + badge_h], radius=18, fill="#E6D3C2")
    draw.text((left_align + 16, y + 8), text, fill=PALETTE["deep_maroon"], font=font)

def draw_footer(draw, current_slide, total_slides, width=1080, height=1350):
    font_brand = get_serif(30, bold=True)
    font_sub = get_sans(20)
    draw.line([(80, height - 100), (width - 80, height - 100)], fill=PALETTE["blush"], width=1)
    draw.text((80, height - 80), "steer", fill=PALETTE["deep_maroon"], font=font_brand)
    draw.text((165, height - 76), "•  steerclub.com", fill=PALETTE["clay"], font=font_sub)
    if total_slides > 1:
        tracker = f"{current_slide} / {total_slides}"
        bbox = draw.textbbox((0, 0), tracker, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text((width - 80 - tw, height - 76), tracker, fill=PALETTE["clay"], font=font_sub)

def generate_static(output_dir: str, study=None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    width, height = 1080, 1080
    img = Image.new("RGB", (width, height), PALETTE["cream"])
    draw = ImageDraw.Draw(img)
    
    badge_title = f"CLINICAL EVIDENCE • {study.study_id}" if study else "CLINICAL EVIDENCE • STEP-1 TRIAL"
    draw_header_badge(draw, badge_title, y=75, left_align=80)
    
    font_head = get_serif(62, bold=True)
    draw.text((80, 140), "It’s not weak willpower.", fill=PALETTE["deep_maroon"], font=font_head)
    
    font_sub = get_serif(56, italic=True)
    draw.text((80, 215), "It’s basic endocrinology.", fill=PALETTE["rust"], font=font_sub)
    
    font_lead = get_sans(24)
    if study:
        lead_text = f"Why Indian adults struggle with chronic cravings—and what {study.journal} ({study.year}, n={study.sample_size:,}) proves about treating the biology first."
    else:
        lead_text = "Why Indian adults struggle with chronic 4 PM food noise and weight rebound—and what happens when you treat the biology first."
    lines = wrap_text(lead_text, font_lead, width - 160, draw)
    y = 300
    for l in lines:
        draw.text((80, y), l, fill=PALETTE["ink"], font=font_lead)
        y += 34

    col_w = (width - 160 - 24) // 2
    b1_left = 80
    b2_left = 80 + col_w + 24
    box_top = y + 25
    box_h = 680
    
    draw.rounded_rectangle([b1_left, box_top, b1_left + col_w, box_top + box_h], radius=18, fill=PALETTE["soft_paper"], outline=PALETTE["blush"], width=1)
    draw.text((b1_left + 24, box_top + 24), "TRADITIONAL DIETS", fill=PALETTE["clay"], font=get_sans(17, bold=True))
    draw.text((b1_left + 24, box_top + 52), "The Willpower Trap", fill=PALETTE["ink"], font=get_serif(28, bold=True))
    draw.line([(b1_left + 24, box_top + 92), (b1_left + col_w - 24, box_top + 92)], fill=PALETTE["blush"], width=1)
    
    items_left = [
        ("Blames character", "Treats weight struggle as a personal moral failure rather than hormonal signaling."),
        ("Famine defense protocol", "Calorie cuts drop leptin 40% and spike ghrelin hunger alarms +240%."),
        ("Relentless 'food noise'", "Intrusive cravings consume daily mental bandwidth and focus."),
        ("High rebound rate", "67% of lost weight returns within 12 months without metabolic reset.")
    ]
    
    y_b1 = box_top + 115
    for title, desc in items_left:
        draw.text((b1_left + 24, y_b1), f"• {title}", fill=PALETTE["ink"], font=get_sans(19, bold=True))
        y_b1 += 28
        d_lines = wrap_text(desc, get_sans(17), col_w - 48, draw)
        for dl in d_lines:
            draw.text((b1_left + 36, y_b1), dl, fill=PALETTE["ink"], font=get_sans(17))
            y_b1 += 24
        y_b1 += 22

    draw.rounded_rectangle([b2_left, box_top, b2_left + col_w, box_top + box_h], radius=18, fill="#FFFDFB", outline=PALETTE["rust"], width=2)
    draw.text((b2_left + 24, box_top + 24), "STEER CLINICAL PROTOCOL", fill=PALETTE["rust"], font=get_sans(17, bold=True))
    draw.text((b2_left + 24, box_top + 52), "Doctor-Led Biology", fill=PALETTE["deep_maroon"], font=get_serif(28, bold=True))
    draw.line([(b2_left + 24, box_top + 92), (b2_left + col_w - 24, box_top + 92)], fill=PALETTE["blush"], width=1)
    
    if study and study.key_findings:
        f0_desc = study.key_findings[0].claim[:70] + ("..." if len(study.key_findings[0].claim) > 70 else "")
        f0_title = f"Proven efficacy ({study.key_findings[0].metric})"
    else:
        f0_title = "Restores gut satiety"
        f0_desc = "GLP-1 receptor activation calms hypothalamic food noise at the root."

    items_right = [
        ("Diagnostics first", "55+ blood biomarkers and DEXA body composition scan on Day 1."),
        (f0_title, f0_desc),
        ("Protects lean muscle", "Targeted protein and resistance plan supervised by clinical dieticians."),
        ("A planned exit off-ramp", "Doctor-guided tapering so sustainable habits hold the results.")
    ]
    
    y_b2 = box_top + 115
    for title, desc in items_right:
        draw.text((b2_left + 24, y_b2), f"• {title}", fill=PALETTE["deep_maroon"], font=get_sans(19, bold=True))
        y_b2 += 28
        d_lines = wrap_text(desc, get_sans(17), col_w - 48, draw)
        for dl in d_lines:
            draw.text((b2_left + 36, y_b2), dl, fill=PALETTE["ink"], font=get_sans(17))
            y_b2 += 24
        y_b2 += 22

    banner_top = box_top + box_h + 30
    banner_h = 76
    draw.rounded_rectangle([80, banner_top, width - 80, banner_top + banner_h], radius=14, fill=PALETTE["deep_maroon"])
    
    font_banner = get_sans(21, bold=True)
    msg = "Before you start, hear it from a doctor, not a reel. • steerclub.com"
    bbox = draw.textbbox((0, 0), msg, font=font_banner)
    bw = bbox[2] - bbox[0]
    bx = (width - bw) // 2
    draw.text((bx, banner_top + 26), msg, fill="#FFFFFF", font=font_banner)
    
    draw_footer(draw, 1, 1, width, height)
    out_file = os.path.join(output_dir, "steer_static_infographic.png")
    img.save(out_file, quality=95)
    return out_file

def generate_carousel(output_dir: str, study=None) -> list[str]:
    from pipeline.visuals_engine_apple import generate_apple_carousel
    return generate_apple_carousel(output_dir, study=study)
