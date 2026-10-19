import os
import math
from PIL import Image, ImageDraw, ImageFont
from pipeline.fonts import get_cross_platform_serif as get_serif, get_cross_platform_sans as get_sans
from pipeline.study_themes import get_study_theme
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

def draw_slide_chrome(draw, idx, total, width, height, palette, is_dark=False):
    # Outer 1.5px Border Frame (No draft badge)
    border_col = palette.border_dark if is_dark else palette.border_light
    draw.rectangle([28, 28, width - 28, height - 28], outline=border_col, width=2)
    
    # Footer Elements
    font_logo = get_serif(30, bold=True)
    font_counter = get_sans(19, bold=False)
    
    logo_col = palette.text_light if is_dark else palette.accent
    counter_col = palette.text_muted_on_dark if is_dark else palette.text_muted
    
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
    
    study_id = getattr(study, "study_id", "") or (study.title if study and hasattr(study, "title") else "LANCET-TOFI-2021")
    theme = get_study_theme(study_id)
    pal = theme.color_palette
    
    slides_data = build_study_slides(study)
    total = len(slides_data)
    out_files = []
    
    hero_idx = theme.hero_slide_index  # Varies dynamically per study (e.g. 2 or 3)
    
    for idx, slide in enumerate(slides_data, start=1):
        is_dark = (idx == hero_idx)
        bg_col = pal.hero_bg if is_dark else pal.cream_bg
        
        img = Image.new("RGB", (width, height), bg_col)
        draw = ImageDraw.Draw(img)
        
        # Chrome (Frame, Logo, Counter — zero draft badge)
        draw_slide_chrome(draw, idx, total, width, height, pal, is_dark=is_dark)
        
        if is_dark:
            # -----------------------------------------------------------------
            # HERO CONTRAST SLIDE (Varied per study: deep oxblood, pine, navy, clay, rust, teal)
            # -----------------------------------------------------------------
            # Primary vector motif top center
            if theme.primary_motif == "cardiac_monitor":
                draw_cardiac_monitor(draw, width // 2, 185, scale=1.22, color=pal.text_light, stroke_w=2)
            elif theme.primary_motif == "cellular":
                draw_cellular_pattern(draw, width // 2, 175, radius=48, color=pal.text_light)
            elif theme.primary_motif == "stethoscope":
                draw_stethoscope(draw, width // 2, 130, scale=0.85, color=pal.text_light, stroke_w=2)
            else:
                draw_cellular_pattern(draw, width // 2, 175, radius=48, color=pal.text_light)
                
            # Study-Tailored Hero Italic Pull-Quote
            font_hero_quote = get_serif(50, bold=True, italic=True)
            quote_text = f'"{theme.hero_quote}"'
            q_lines = wrap_text(quote_text, font_hero_quote, width - 160, draw)[:3]
            y_hq = 320
            for ql in q_lines:
                draw.text((80, y_hq), ql, fill=pal.text_light, font=font_hero_quote)
                y_hq += 60
                
            draw.line([(80, y_hq + 10), (220, y_hq + 10)], fill=pal.accent, width=4)
            
            # Clinical Caveat / Reality Paragraph
            font_caveat = get_sans(22, bold=False)
            p1 = slide.get("p1", "")
            p2 = slide.get("p2", "")
            body_text = f"{p1} {p2}".strip() or theme.study_directive
            y_cav = y_hq + 30
            c_lines = wrap_text(body_text, font_caveat, width - 160, draw)[:3]
            for cl in c_lines:
                draw.text((80, y_cav), cl, fill=pal.text_light, font=font_caveat)
                y_cav += 32
                
            # Key Clinical Stat or Takeaway on dark
            stat_val = slide.get("stat", "") or theme.metadata.get("stat", "")
            stat_lbl = slide.get("stat_label", "") or theme.metadata.get("stat_label", "")
            if stat_val:
                y_ds = y_cav + 20
                draw.line([(80, y_ds), (80, y_ds + 75)], fill=pal.accent, width=5)
                draw.text((102, y_ds - 4), stat_val, fill=pal.accent, font=get_serif(54, bold=True))
                s_bbox = draw.textbbox((0, 0), stat_val, font=get_serif(54, bold=True))
                sw = s_bbox[2] - s_bbox[0]
                draw.text((120 + sw, y_ds + 12), stat_lbl, fill=pal.text_light, font=get_sans(21, bold=True))
                
            # Bottom Directive line
            draw.text((80, height - 120), theme.study_directive, fill=pal.text_muted_on_dark, font=get_sans(17, bold=True))
            
            font_cit = get_sans(15, italic=True)
            draw.text((80, height - 90), slide.get("citation", ""), fill=pal.text_muted_on_dark, font=font_cit)

        elif idx == 1:
            # -----------------------------------------------------------------
            # SLIDE 1: COVER / HOOK (Square 1080x1080)
            # -----------------------------------------------------------------
            # Tailored Motif top-left
            if theme.primary_motif == "cardiac_monitor":
                draw_cardiac_monitor(draw, 120, 105, scale=0.85, color=pal.text_dark, stroke_w=2)
            elif theme.primary_motif == "stethoscope":
                draw_stethoscope(draw, 120, 75, scale=0.72, color=pal.text_dark, stroke_w=2)
            else:
                draw_cellular_pattern(draw, 115, 105, radius=48, color=pal.text_dark)
            
            title_text = slide.get("title", "")
            font_italic = get_serif(48, bold=True, italic=True)
            font_title = get_serif(48, bold=True, italic=False)
            
            t_lines = wrap_text(title_text, font_title, width - 150, draw)
            y_title = 168
            for i, tl in enumerate(t_lines[:2]):
                if i == 0 and (":" in tl or len(t_lines) > 1):
                    parts = tl.split(":")
                    if len(parts) == 2:
                        draw.text((75, y_title), parts[0] + ":", fill=pal.accent, font=font_italic)
                        bbox0 = draw.textbbox((0, 0), parts[0] + ": ", font=font_italic)
                        draw.text((75 + (bbox0[2] - bbox0[0]), y_title), parts[1].strip(), fill=pal.text_dark, font=font_title)
                    else:
                        draw.text((75, y_title), tl, fill=pal.accent, font=font_italic)
                else:
                    draw.text((75, y_title), tl, fill=pal.text_dark, font=font_title)
                y_title += 56
                
            draw.line([(75, y_title + 6), (200, y_title + 6)], fill=pal.accent, width=4)
            
            font_body = get_sans(23, bold=False)
            p1 = slide.get("p1", "")
            y_body = y_title + 24
            b_lines = wrap_text(p1, font_body, width - 150, draw)[:2]
            for bl in b_lines:
                draw.text((75, y_body), bl, fill=pal.text_dark, font=font_body)
                y_body += 32
                
            stat_val = slide.get("stat", "") or theme.metadata.get("stat", "")
            stat_lbl = slide.get("stat_label", "") or theme.metadata.get("stat_label", "")
            stat_sub = slide.get("stat_sub", "") or theme.metadata.get("stat_sub", "")
            
            y_stat = y_body + 18
            bar_h = 110
            draw.line([(75, y_stat), (75, y_stat + bar_h)], fill=pal.accent, width=6)
            
            font_big_stat = get_serif(72, bold=True)
            draw.text((95, y_stat - 8), stat_val, fill=pal.accent, font=font_big_stat)
            
            s_bbox = draw.textbbox((0, 0), stat_val, font=font_big_stat)
            sw = s_bbox[2] - s_bbox[0]
            
            y_lbl = y_stat + 6
            lbl_lines = wrap_text(stat_lbl, get_sans(21, bold=True), width - (115 + sw + 30), draw)[:2]
            for ll in lbl_lines:
                draw.text((115 + sw, y_lbl), ll, fill=pal.text_dark, font=get_sans(21, bold=True))
                y_lbl += 28
            draw.text((115 + sw, y_lbl + 4), stat_sub, fill=pal.text_muted, font=get_sans(16))
            
            # Embedded Telemetry Chart in lower area
            sid = (study.study_id if study else "LANCET-TOFI-2021").upper()
            telem_img = draw_slide1_telemetry(sid, width - 150, 310)
            if telem_img:
                img.paste(telem_img, (75, y_stat + bar_h + 16), telem_img if telem_img.mode == "RGBA" else None)
                
            font_cit = get_sans(15, italic=True)
            draw.text((75, height - 90), slide.get("citation", ""), fill=pal.text_muted, font=font_cit)

        elif idx == 2 and not is_dark:
            # -----------------------------------------------------------------
            # SLIDE 2: PATHOPHYSIOLOGY / MECHANISM (When not dark hero)
            # -----------------------------------------------------------------
            font_title = get_serif(46, bold=True)
            title_text = slide.get("title", "")
            t_lines = wrap_text(title_text, font_title, width - 150, draw)[:2]
            y_title = 95
            for tl in t_lines:
                draw.text((75, y_title), tl, fill=pal.text_dark, font=font_title)
                y_title += 52
            draw.line([(75, y_title + 6), (195, y_title + 6)], fill=pal.accent, width=4)
            
            dkey = slide.get("diagram_key", "")
            diag_w = width - 150
            diag_h = 350
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
                
            y_diag = y_title + 20
            img.paste(diag_img, (75, y_diag), diag_img if diag_img.mode == "RGBA" else None)
            
            y_takeaway = y_diag + diag_h + 20
            draw.line([(75, y_takeaway), (75, y_takeaway + 120)], fill=pal.accent, width=6)
            
            p1 = slide.get("p1", "")
            takeaway = slide.get("takeaway", "")
            
            font_quote = get_serif(23, italic=True)
            q_lines = wrap_text(f'"{p1}"', font_quote, width - 180, draw)[:3]
            y_q = y_takeaway + 2
            for ql in q_lines:
                draw.text((100, y_q), ql, fill=pal.text_dark, font=font_quote)
                y_q += 30
                
            font_t_bold = get_sans(19, bold=True)
            draw.text((100, y_q + 6), f"Key Protocol: {takeaway}", fill=pal.accent, font=font_t_bold)
            
            draw.text((75, y_takeaway + 145), theme.study_directive, fill=pal.text_dark, font=get_sans(17, bold=True))
            font_cit = get_sans(15, italic=True)
            draw.text((75, height - 90), slide.get("citation", ""), fill=pal.text_muted, font=font_cit)

        elif idx == 3 and not is_dark:
            # -----------------------------------------------------------------
            # SLIDE 3: SECONDARY CLINICAL DATA (When not dark hero)
            # -----------------------------------------------------------------
            font_title = get_serif(46, bold=True)
            title_text = slide.get("title", "")
            t_lines = wrap_text(title_text, font_title, width - 150, draw)[:2]
            y_title = 95
            for tl in t_lines:
                draw.text((75, y_title), tl, fill=pal.text_dark, font=font_title)
                y_title += 52
            draw.line([(75, y_title + 6), (195, y_title + 6)], fill=pal.accent, width=4)
            
            # Secondary Telemetry / Biomarker Panels
            sid = (study.study_id if study else "LANCET-TOFI-2021").upper()
            telem_img = draw_slide3_telemetry(sid, width - 150, 260)
            y_telem = y_title + 24
            if telem_img:
                img.paste(telem_img, (75, y_telem), telem_img if telem_img.mode == "RGBA" else None)
                
            y_narrative = y_telem + 280
            p1 = slide.get("p1", "")
            p2 = slide.get("p2", "")
            narrative = f"{p1} {p2}".strip()
            font_body = get_sans(21)
            n_lines = wrap_text(narrative, font_body, width - 160, draw)[:3]
            for nl in n_lines:
                draw.text((75, y_narrative), nl, fill=pal.text_dark, font=font_body)
                y_narrative += 30
                
            draw.text((75, y_narrative + 14), theme.study_directive, fill=pal.accent, font=get_sans(17, bold=True))
            font_cit = get_sans(15, italic=True)
            draw.text((75, height - 90), slide.get("citation", ""), fill=pal.text_muted, font=font_cit)

        elif idx == 4:
            # -----------------------------------------------------------------
            # SLIDE 4: STEER CLINICAL ARCHITECTURE & CALL TO ACTION
            # -----------------------------------------------------------------
            # Secondary motif (stethoscope, caring hands, or tailored icon)
            if theme.secondary_motif == "stethoscope":
                draw_stethoscope(draw, 740, 290, scale=0.92, color=pal.text_dark, stroke_w=3)
            elif theme.secondary_motif == "caring_hands":
                draw_caring_hands(draw, 750, 420, scale=0.95, color=pal.text_dark, stroke_w=2)
            else:
                draw_stethoscope(draw, 740, 290, scale=0.92, color=pal.text_dark, stroke_w=3)
            
            font_cta_title = get_serif(46, bold=True, italic=True)
            draw.text((75, 90), "Talk to a Steer doctor.", fill=pal.accent, font=font_cta_title)
            draw.line([(75, 148), (200, 148)], fill=pal.accent, width=4)
            
            font_sub = get_sans(22)
            draw.text((75, 168), "Doctor-led metabolic care built for Indian biology.", fill=pal.text_dark, font=font_sub)
            
            # 3 Tailored Protocol Pillars from STUDY_THEMES
            y_p = 235
            pillars = theme.protocol_pillars
            
            for p_title, p_desc in pillars[:3]:
                draw.line([(75, y_p), (75, y_p + 68)], fill=pal.accent, width=5)
                draw.text((95, y_p), p_title, fill=pal.text_dark, font=get_sans(21, bold=True))
                d_lines = wrap_text(p_desc, get_sans(17), 460, draw)[:2]
                yd = y_p + 26
                for dl in d_lines:
                    draw.text((95, yd), dl, fill=pal.text_muted, font=get_sans(17))
                    yd += 22
                y_p += 105
                
            # Caring hands illustration anchoring lower-left if secondary motif was stethoscope
            if theme.secondary_motif == "stethoscope":
                draw_caring_hands(draw, 190, 680, scale=0.78, color=pal.text_dark, stroke_w=2)
            
            # Study-Tailored CTA Box & URL
            draw.text((75, 790), f"Visit steerclub.com → {theme.cta_headline}", fill=pal.accent, font=get_sans(23, bold=True))
            draw.text((75, 830), theme.cta_subtext, fill=pal.text_muted, font=get_sans(15))
            draw.text((75, 865), "Doctor-led consultations • Continuous metabolic monitoring across India", fill=pal.text_dark, font=get_sans(16, bold=True))
            
            font_cit = get_sans(15, italic=True)
            draw.text((75, height - 90), slide.get("citation", "Steer Clinical Care Protocol 2026 • steerclub.com"), fill=pal.text_muted, font=font_cit)
            
        out_path = os.path.normpath(os.path.join(abs_dir, f"carousel_slide_{idx}.png"))
        img.save(out_path, quality=95)
        out_files.append(out_path)
        print(f"✅ Generated Study-Tailored Square Slide {idx}: {out_path}")
        
    return out_files

if __name__ == "__main__":
    from pipeline.ingest import load_study_from_file
    study = load_study_from_file("papers/lancet_tofi_2021.json")
    render_editorial_carousel("output/test_editorial_carousel", study=study)
