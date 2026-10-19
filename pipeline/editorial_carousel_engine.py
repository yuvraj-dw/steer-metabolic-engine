import os
import math
from PIL import Image, ImageDraw, ImageFont
from pipeline.fonts import get_cross_platform_serif as get_serif, get_cross_platform_sans as get_sans
from pipeline.carousel_motifs import (
    draw_cellular_pattern,
    draw_stethoscope,
    draw_caring_hands,
    draw_cardiac_monitor
)
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
    "cream": "#F3ECE2",
    "oxblood": "#5C181A",
    "charcoal": "#241E1C",
    "rust": "#B85338",
    "slate": "#8E8277",
    "white": "#FAF7F2",
    "cream_border": "#241E1C",
    "oxblood_border": "#FAF7F2"
}

# Cross-platform fonts imported from pipeline.fonts

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

def draw_pill_badge(draw, text="draft · pending doctor review", width=1080, is_dark=False):
    font_badge = get_sans(15, bold=False)
    bbox = draw.textbbox((0, 0), text, font=font_badge)
    tw = bbox[2] - bbox[0]
    badge_w = tw + 28
    badge_h = 32
    bx2 = width - 50
    bx1 = bx2 - badge_w
    by1 = 48
    by2 = by1 + badge_h
    
    border_col = (170, 90, 95) if is_dark else PALETTE["slate"]
    text_col = PALETTE["white"] if is_dark else PALETTE["slate"]
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=16, outline=border_col, width=1)
    draw.text((bx1 + 14, by1 + 6), text, fill=text_col, font=font_badge)

def draw_slide_chrome(draw, idx, total, width=1080, height=1080, is_dark=False):
    # 1. Outer 1.5px Border Frame
    border_col = (160, 80, 85) if is_dark else PALETTE["cream_border"]
    draw.rectangle([28, 28, width - 28, height - 28], outline=border_col, width=2)
    
    # 2. Pill Badge
    draw_pill_badge(draw, text="draft · pending doctor review", width=width, is_dark=is_dark)
    
    # 3. Footer Elements
    font_logo = get_serif(30, bold=True)
    font_counter = get_sans(19, bold=False)
    
    logo_col = PALETTE["white"] if is_dark else PALETTE["rust"]
    counter_col = (190, 130, 135) if is_dark else PALETTE["slate"]
    
    # Lower-left wordmark
    draw.text((65, height - 68), "steer", fill=logo_col, font=font_logo)
    
    # Lower-right counter
    counter_text = f"{idx}/{total}"
    c_bbox = draw.textbbox((0, 0), counter_text, font=font_counter)
    cw = c_bbox[2] - c_bbox[0]
    draw.text((width - 65 - cw, height - 64), counter_text, fill=counter_col, font=font_counter)

def render_editorial_carousel(output_dir: str, study=None) -> list[str]:
    from pipeline.visuals_engine_apple import build_study_slides
    
    abs_dir = os.path.abspath(output_dir)
    os.makedirs(abs_dir, exist_ok=True)
    # Native Instagram Square dimensions (1080 x 1080 px, 1:1 Aspect Ratio)
    width, height = 1080, 1080
    
    slides_data = build_study_slides(study)
    total = len(slides_data)
    out_files = []
    
    for idx, slide in enumerate(slides_data, start=1):
        # Slide 3 is the deep oxblood burgundy pattern interrupt slide
        is_dark = (idx == 3)
        bg_col = PALETTE["oxblood"] if is_dark else PALETTE["cream"]
        
        img = Image.new("RGB", (width, height), bg_col)
        draw = ImageDraw.Draw(img)
        
        # Chrome (Frame, Badge, Logo, Counter)
        draw_slide_chrome(draw, idx, total, width, height, is_dark=is_dark)
        
        if idx == 1:
            # SLIDE 1: COVER / HOOK (Square 1080x1080)
            # Monoline Cellular / Biological Motif top-left
            draw_cellular_pattern(draw, 115, 105, radius=48, color=PALETTE["charcoal"])
            
            # Title with Italic Serif Accent
            title_text = slide.get("title", "")
            font_italic = get_serif(52, bold=True, italic=True)
            font_title = get_serif(52, bold=True, italic=False)
            
            t_lines = wrap_text(title_text, font_title, width - 150, draw)
            y_title = 165
            for i, tl in enumerate(t_lines[:2]):
                if i == 0 and (":" in tl or len(t_lines) > 1):
                    parts = tl.split(":")
                    if len(parts) == 2:
                        draw.text((75, y_title), parts[0] + ":", fill=PALETTE["rust"], font=font_italic)
                        bbox0 = draw.textbbox((0, 0), parts[0] + ": ", font=font_italic)
                        draw.text((75 + (bbox0[2] - bbox0[0]), y_title), parts[1].strip(), fill=PALETTE["charcoal"], font=font_title)
                    else:
                        draw.text((75, y_title), tl, fill=PALETTE["rust"], font=font_italic)
                else:
                    draw.text((75, y_title), tl, fill=PALETTE["charcoal"], font=font_title)
                y_title += 52
                
            # Short horizontal accent underline rule
            draw.line([(75, y_title + 6), (175, y_title + 6)], fill=PALETTE["rust"], width=3)
            
            # Narrative Body (directly on cream, no box!)
            font_body = get_sans(24, bold=False)
            p1 = slide.get("p1", "")
            y_body = y_title + 24
            b_lines = wrap_text(p1, font_body, width - 150, draw)[:2]
            for bl in b_lines:
                draw.text((75, y_body), bl, fill=PALETTE["charcoal"], font=font_body)
                y_body += 34
                
            # Stat Highlight with Vertical Terracotta Bar (NO WHITE BOX!)
            stat_val = slide.get("stat", "")
            stat_lbl = slide.get("stat_label", "")
            stat_sub = slide.get("stat_sub", "")
            
            y_stat = y_body + 20
            bar_h = 115
            draw.line([(75, y_stat), (75, y_stat + bar_h)], fill=PALETTE["rust"], width=6)
            
            font_big_stat = get_serif(76, bold=True)
            draw.text((95, y_stat - 4), stat_val, fill=PALETTE["rust"], font=font_big_stat)
            
            s_bbox = draw.textbbox((0, 0), stat_val, font=font_big_stat)
            sw = s_bbox[2] - s_bbox[0]
            
            y_lbl = y_stat + 4
            lbl_lines = wrap_text(stat_lbl, get_sans(22, bold=True), width - (115 + sw + 30), draw)[:2]
            for ll in lbl_lines:
                draw.text((110 + sw, y_lbl), ll, fill=PALETTE["charcoal"], font=get_sans(18, bold=True))
                y_lbl += 30
            draw.text((115 + sw, y_lbl + 4), stat_sub, fill=PALETTE["slate"], font=get_sans(17))
            
            sid = (study.study_id if study else "lancet_tofi").upper()
            telem_img = draw_slide1_telemetry(sid, width - 150, 230)
            if telem_img:
                img.paste(telem_img, (75, y_stat + bar_h + 18), telem_img if telem_img.mode == "RGBA" else None)
                
            font_cit = get_sans(14, italic=True)
            draw.text((75, height - 90), slide.get("citation", ""), fill=PALETTE["slate"], font=font_cit)
            
        elif idx == 2:
            # SLIDE 2: PATHOPHYSIOLOGY / MECHANISM (Square 1080x1080, Direct Cream)
            font_title = get_serif(48, bold=True)
            title_text = slide.get("title", "")
            t_lines = wrap_text(title_text, font_title, width - 150, draw)[:2]
            y_title = 110
            for tl in t_lines:
                draw.text((75, y_title), tl, fill=PALETTE["charcoal"], font=font_title)
                y_title += 50
            draw.line([(75, y_title + 6), (175, y_title + 6)], fill=PALETTE["rust"], width=3)
            
            # Clinical Vector Diagram rendered transparently directly on canvas
            dkey = slide.get("diagram_key", "")
            diag_w = width - 150
            diag_h = 360
            if "SURPASS" in dkey:
                diag_img = draw_surpass_diagram(diag_w, diag_h)
            elif "MACE" in dkey or "STEER" in dkey:
                diag_img = draw_mace_diagram(diag_w, diag_h)
            elif "STEP" in dkey:
                diag_img = draw_step1_diagram(diag_w, diag_h)
            elif "NARAYAN" in dkey:
                diag_img = draw_narayan_diagram(diag_w, diag_h)
            else:
                diag_img = draw_tofi_dexa_diagram(diag_w, diag_h)
                
            y_diag = y_title + 24
            img.paste(diag_img, (75, y_diag), diag_img if diag_img.mode == "RGBA" else None)
            
            # Clinical Finding with Vertical Terracotta Bar (Directly on cream!)
            y_takeaway = y_diag + diag_h + 24
            draw.line([(75, y_takeaway), (75, y_takeaway + 135)], fill=PALETTE["rust"], width=6)
            
            p1 = slide.get("p1", "")
            takeaway = slide.get("takeaway", "")
            
            font_quote = get_serif(25, italic=True)
            q_lines = wrap_text(f'"{p1}"', font_quote, width - 180, draw)[:3]
            y_q = y_takeaway + 2
            for ql in q_lines:
                draw.text((95, y_q), ql, fill=PALETTE["charcoal"], font=font_quote)
                y_q += 34
                
            font_t_bold = get_sans(20, bold=True)
            draw.text((95, y_q + 6), f"Key Protocol: {takeaway}", fill=PALETTE["rust"], font=font_t_bold)
            
            # Citation
            font_cit = get_sans(14, italic=True)
            draw.text((75, height - 90), slide.get("citation", ""), fill=PALETTE["slate"], font=font_cit)
            
        elif idx == 3:
            # SLIDE 3: PATTERN INTERRUPT (Square 1080x1080, Deep Oxblood Maroon `#5C181A`)
            draw_cardiac_monitor(draw, width // 2, 185, scale=1.22, color=PALETTE["white"], stroke_w=2)
            
            font_hero_quote = get_serif(52, bold=True, italic=True)
            quote_text = "Before you start, hear it from a doctor, not a reel."
            q_lines = wrap_text(quote_text, font_hero_quote, width - 160, draw)[:2]
            y_hq = 350
            for ql in q_lines:
                draw.text((80, y_hq), ql, fill=PALETTE["white"], font=font_hero_quote)
                y_hq += 62
                
            draw.line([(80, y_hq + 10), (190, y_hq + 10)], fill=PALETTE["rust"], width=3)
            
            font_caveat = get_sans(23, bold=False)
            p1 = slide.get("p1", "")
            p2 = slide.get("p2", "")
            body_text = f"{p1} {p2}".strip()
            y_cav = y_hq + 32
            c_lines = wrap_text(body_text, font_caveat, width - 160, draw)[:3]
            for cl in c_lines:
                draw.text((80, y_cav), cl, fill=(245, 238, 230), font=font_caveat)
                y_cav += 32
                
            # Key Clinical Stat or Takeaway on dark
            stat_val = slide.get("stat", "")
            stat_lbl = slide.get("stat_label", "")
            if stat_val:
                y_ds = y_cav + 20
                draw.line([(80, y_ds), (80, y_ds + 82)], fill=PALETTE["rust"], width=5)
                draw.text((102, y_ds - 4), stat_val, fill=PALETTE["rust"], font=get_serif(56, bold=True))
                s_bbox = draw.textbbox((0, 0), stat_val, font=get_serif(44, bold=True))
                sw = s_bbox[2] - s_bbox[0]
                draw.text((120 + sw, y_ds + 12), stat_lbl, fill=PALETTE["white"], font=get_sans(21, bold=True))
                
            # Citation
            font_cit = get_sans(14, italic=True)
            draw.text((80, height - 95), slide.get("citation", ""), fill=(200, 150, 155), font=font_cit)
            
        elif idx == 4:
            # SLIDE 4: THE STEER ARCHITECTURE / DOCTOR CONSULTATION (Square 1080x1080)
            draw_stethoscope(draw, 740, 310, scale=0.96, color=PALETTE["charcoal"], stroke_w=3)
            
            font_cta_title = get_serif(50, bold=True, italic=True)
            draw.text((75, 105), "Talk to a Steer doctor.", fill=PALETTE["rust"], font=font_cta_title)
            draw.line([(75, 160), (175, 160)], fill=PALETTE["rust"], width=3)
            
            font_sub = get_sans(23)
            draw.text((75, 178), "Doctor-led metabolic care built for Indian biology.", fill=PALETTE["charcoal"], font=font_sub)
            
            # Steer 3 Pillars
            y_p = 250
            pillars = slide.get("pillars", [
                ("01  DEXA Muscle Tracking", "Quantifies fat loss vs lean mass preservation every 8 weeks."),
                ("02  Doctor-Led Titration", "Physician micro-dosing to eliminate nausea and GI symptoms."),
                ("03  Structured Off-Ramp", "Gradual tapering protocol to maintain set-point permanently.")
            ])
            
            for p_title, p_desc in pillars[:3]:
                draw.line([(75, y_p), (75, y_p + 68)], fill=PALETTE["rust"], width=5)
                draw.text((95, y_p), p_title, fill=PALETTE["charcoal"], font=get_sans(22, bold=True))
                d_lines = wrap_text(p_desc, get_sans(18), 450, draw)[:2]
                yd = y_p + 24
                for dl in d_lines:
                    draw.text((95, yd), dl, fill=PALETTE["slate"], font=get_sans(18))
                    yd += 24
                y_p += 105
                
            # Caring hands illustration anchoring lower-left
            draw_caring_hands(draw, 200, 680, scale=0.82, color=PALETTE["charcoal"], stroke_w=2)
            
            # CTA Box & URL
            draw.text((75, 800), "Visit steerclub.com to check eligibility →", fill=PALETTE["rust"], font=get_sans(25, bold=True))
            draw.text((75, 840), "Comprehensive blood panel • Doctor consult • Continuous monitoring", fill=PALETTE["slate"], font=get_sans(16))
            draw.text((75, 875), "Doctor-led consultations • Continuous metabolic monitoring across India", fill=PALETTE["charcoal"], font=get_sans(17, bold=True))
            
            # Citation
            font_cit = get_sans(14, italic=True)
            draw.text((75, height - 95), slide.get("citation", "Steer Clinical Care Protocol 2026 • steerclub.com"), fill=PALETTE["slate"], font=font_cit)
            
        out_path = os.path.normpath(os.path.join(abs_dir, f"carousel_slide_{idx}.png"))
        img.save(out_path, quality=95)
        out_files.append(out_path)
        print(f"✅ Generated Apple Editorial Slide {idx}: {out_path}")
        
    return out_files

if __name__ == "__main__":
    from pipeline.ingest import load_study_from_file
    study = load_study_from_file("papers/lancet_tofi_2021.json")
    render_editorial_carousel("output/test_editorial_carousel", study=study)
