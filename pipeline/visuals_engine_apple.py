import os
import sys
from PIL import Image, ImageDraw, ImageFont

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
    if not study or not study.key_findings:
        return get_default_slides()
    
    f0 = study.key_findings[0]
    f1 = study.key_findings[1] if len(study.key_findings) > 1 else f0

    s1_title = f"{study.study_id}: Clinical Evidence"
    if "tirzepatide" in study.title.lower():
        s1_title = "SURPASS-2: Dual Incretin (Tirzepatide) Trial."
    elif "rebound" in f0.claim.lower() or "regain" in f0.claim.lower() or "withdrawal" in study.title.lower():
        s1_title = "STEP-1 Extension: The Rebound Truth."
    elif "cardiovascular" in study.title.lower() or "mace" in study.title.lower():
        s1_title = "STEER Study: 57% Lower Heart Risk."
    elif "tofi" in study.title.lower() or "south asian" in study.title.lower():
        s1_title = "The 70 kg Paradox: Indian TOFI Phenotype."

    journal_clean = study.journal.replace("The ", "").upper()

    slides = [
        # Slide 1: Study Hero
        {
            "tag": f"{journal_clean} EVIDENCE",
            "title": s1_title,
            "subtitle": f"Peer-reviewed clinical trial published in {study.journal} ({study.year}, n={study.sample_size:,}).",
            "type": "rebound_hero",
            "stat": f0.metric,
            "stat_label": f0.claim,
            "stat_sub": f"Statistically significant trial outcome (p {f0.p_value})",
            "p1": f"In a rigorous clinical study of {study.sample_size:,} individuals published in {study.journal}, researchers investigated metabolic regulation and medical intervention.",
            "p2": f0.clinical_interpretation or f0.claim,
            "takeaway": "Evidence proves that sustained metabolic success demands clinical supervision.",
            "citation": f"Source: {study.journal} {study.year}; DOI: {study.doi}"
        },
        # Slide 2: Neuro-Endocrine Set-Point
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
        # Slide 3: Secondary Clinical Finding
        {
            "tag": "CLINICAL EFFICACY & SAFETY",
            "title": "Targeting the root biology.",
            "subtitle": f"Key secondary endpoint from {study.journal} ({study.year}).",
            "type": "rebound_hero",
            "stat": f1.metric,
            "stat_label": f1.claim,
            "stat_sub": f"Evidence-based efficacy (p {f1.p_value})",
            "p1": f1.claim,
            "p2": f1.clinical_interpretation or "Metabolic health requires comprehensive biomarker diagnostics and muscle preservation rather than unmonitored crash dieting.",
            "takeaway": "True health is measured in visceral fat reduction and biomarker health, not bathroom scale numbers.",
            "citation": f"Source: {study.title} ({study.year}) • {study.journal}"
        },
        # Slide 4: Steer Architecture
        {
            "tag": "THE STEER ARCHITECTURE",
            "title": "Doctor-led care with a planned exit.",
            "subtitle": "How Steer sustains long-term metabolic health after medication.",
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
    return slides

def generate_apple_carousel(output_dir: str, study=None) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
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
        arena_top = y_text + 35
        card_w = width - 180

        if slide["type"] == "rebound_hero":
            card_h = 780
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            
            # Narrative paragraphs
            font_body = get_sans(22)
            y_p = arena_top + 45
            for p in [slide["p1"], slide["p2"]]:
                plines = wrap_text(p, font_body, card_w - 80, draw)
                for pl in plines:
                    draw.text((130, y_p), pl, fill=PALETTE["ink"], font=font_body)
                    y_p += 33
                y_p += 18

            # Highlight Stat Card inside (Dynamic metric measurement & word-wrapped labels)
            stat_top = y_p + 15
            stat_h = 175
            draw.rounded_rectangle([130, stat_top, 130 + card_w - 80, stat_top + stat_h], radius=18, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            
            font_stat = get_serif(76, bold=True)
            stat_bbox = draw.textbbox((0, 0), slide["stat"], font=font_stat)
            stat_w = stat_bbox[2] - stat_bbox[0]
            draw.text((160, stat_top + 38), slide["stat"], fill=PALETTE["rust"], font=font_stat)
            
            # Stat labels dynamically placed with ample gutter
            lbl_x = 160 + stat_w + 35
            max_lbl_w = (130 + card_w - 80) - lbl_x - 20
            
            lbl_lines = wrap_text(slide["stat_label"], get_sans(23, bold=True), max_lbl_w, draw)
            y_lbl = stat_top + 30
            for ll in lbl_lines:
                draw.text((lbl_x, y_lbl), ll, fill=PALETTE["deep_maroon"], font=get_sans(23, bold=True))
                y_lbl += 28
            draw.text((lbl_x, y_lbl + 6), slide["stat_sub"], fill=PALETTE["clay"], font=get_sans(18))

            # Doctor note callout
            note_top = stat_top + stat_h + 30
            draw.rounded_rectangle([130, note_top, 130 + card_w - 80, note_top + 70], radius=12, fill="#EDF5F0")
            draw.text((155, note_top + 22), "✓  " + slide["takeaway"], fill=PALETTE["teal_calm"], font=get_sans(22, bold=True))

            # Citation
            draw.text((130, arena_top + card_h - 45), slide["citation"], fill=PALETTE["clay"], font=get_sans(18))

        elif slide["type"] == "hormone_scales":
            card_h = 780
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            
            font_body = get_sans(24)
            y_p = arena_top + 45
            for p in [slide["p1"], slide["p2"]]:
                plines = wrap_text(p, font_body, card_w - 80, draw)
                for pl in plines:
                    draw.text((130, y_p), pl, fill=PALETTE["ink"], font=font_body)
                    y_p += 36
                y_p += 22

            # Visual Dual Scales (Ghrelin vs Leptin)
            sc_top = y_p + 15
            # Scale 1: Ghrelin Spike
            draw.rounded_rectangle([130, sc_top, 130 + card_w - 80, sc_top + 105], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            draw.text((160, sc_top + 22), "GHRELIN (HUNGER HORMONE)", fill=PALETTE["deep_maroon"], font=get_sans(19, bold=True))
            draw.text((160, sc_top + 58), "Triggers urgent food noise & 4 PM cravings", fill=PALETTE["clay"], font=get_sans(19))
            
            draw_vector_arrow(draw, width - 295, sc_top + 38, direction="up", color=PALETTE["rust"])
            draw.text((width - 270, sc_top + 28), "+240%", fill=PALETTE["rust"], font=get_serif(38, bold=True))

            # Scale 2: Leptin Crash
            sc2_top = sc_top + 128
            draw.rounded_rectangle([130, sc2_top, 130 + card_w - 80, sc2_top + 105], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            draw.text((160, sc2_top + 22), "LEPTIN (SATIETY SIGNAL)", fill=PALETTE["deep_maroon"], font=get_sans(19, bold=True))
            draw.text((160, sc2_top + 58), "Signals fullness & regulates metabolic burn", fill=PALETTE["clay"], font=get_sans(19))
            
            draw_vector_arrow(draw, width - 275, sc2_top + 42, direction="down", color=PALETTE["deep_maroon"])
            draw.text((width - 250, sc2_top + 28), "-40%", fill=PALETTE["deep_maroon"], font=get_serif(38, bold=True))

            # Takeaway Box (Warm Cream & Deep Maroon Accent, Clean Wrapped Text)
            note_top = sc2_top + 138
            note_h = 100
            draw.rounded_rectangle([130, note_top, 130 + card_w - 80, note_top + note_h], radius=14, fill="#F2E6DC", outline="#DEC3B5", width=1)
            draw_vector_check(draw, 155, note_top + 26, color=PALETTE["deep_maroon"])
            
            font_note = get_sans(21, bold=True)
            note_lines = wrap_text(slide["takeaway"], font_note, card_w - 140, draw)
            y_note = note_top + 20
            for nl in note_lines:
                draw.text((185, y_note), nl, fill=PALETTE["deep_maroon"], font=font_note)
                y_note += 28

            # Citation
            draw.text((130, arena_top + card_h - 45), slide["citation"], fill=PALETTE["clay"], font=get_sans(18))

        elif slide["type"] == "tofi_breakdown":
            card_h = 780
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            
            font_body = get_sans(22)
            y_p = arena_top + 45
            for p in [slide["p1"], slide["p2"]]:
                plines = wrap_text(p, font_body, card_w - 80, draw)
                for pl in plines:
                    draw.text((130, y_p), pl, fill=PALETTE["ink"], font=font_body)
                    y_p += 33
                y_p += 18

            # Highlight card (Dynamic measurement)
            stat_top = y_p + 15
            stat_h = 175
            draw.rounded_rectangle([130, stat_top, 130 + card_w - 80, stat_top + stat_h], radius=18, fill=PALETTE["white"], outline=PALETTE["rust"], width=2)
            
            font_stat = get_serif(76, bold=True)
            stat_bbox = draw.textbbox((0, 0), slide["stat"], font=font_stat)
            stat_w = stat_bbox[2] - stat_bbox[0]
            draw.text((160, stat_top + 38), slide["stat"], fill=PALETTE["rust"], font=font_stat)
            
            lbl_x = 160 + stat_w + 35
            max_lbl_w = (130 + card_w - 80) - lbl_x - 20
            lbl_lines = wrap_text(slide["stat_label"], get_sans(23, bold=True), max_lbl_w, draw)
            y_lbl = stat_top + 30
            for ll in lbl_lines:
                draw.text((lbl_x, y_lbl), ll, fill=PALETTE["deep_maroon"], font=get_sans(23, bold=True))
                y_lbl += 28
            draw.text((lbl_x, y_lbl + 6), slide["stat_sub"], fill=PALETTE["clay"], font=get_sans(18))

            note_top = stat_top + stat_h + 30
            draw.rounded_rectangle([130, note_top, 130 + card_w - 80, note_top + 70], radius=12, fill="#FAF0EB", outline="#F0C5B4")
            draw.text((155, note_top + 22), "⚠️  " + slide["takeaway"], fill=PALETTE["rust"], font=get_sans(21, bold=True))

            draw.text((130, arena_top + card_h - 45), slide["citation"], fill=PALETTE["clay"], font=get_sans(18))

        else:
            # Slide 4: Clean Apple Keynote 4-Pillar Slabs
            card_h = 780
            draw.rounded_rectangle([90, arena_top, 90 + card_w, arena_top + card_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
            
            draw.text((130, arena_top + 45), "THE 4-PILLAR CLINICAL OFF-RAMP", fill=PALETTE["clay"], font=get_sans(18, bold=True))

            slab_y = arena_top + 95
            for title, desc in slide["pillars"]:
                draw.rounded_rectangle([130, slab_y, 130 + card_w - 80, slab_y + 115], radius=16, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
                draw.text((160, slab_y + 20), title, fill=PALETTE["deep_maroon"], font=get_sans(24, bold=True))
                draw.text((160, slab_y + 62), desc, fill=PALETTE["ink"], font=get_sans(20))
                slab_y += 135

            draw.text((130, arena_top + card_h - 45), slide["citation"], fill=PALETTE["clay"], font=get_sans(18))

        # 5. Footer
        draw_footer(draw, idx, total, width, height)

        out_path = os.path.join(output_dir, f"carousel_slide_{idx}.png")
        img.save(out_path, quality=95)
        out_files.append(out_path)
        print(f"✅ Generated Apple-Crafted Slide {idx}: {out_path}")

    return out_files

if __name__ == "__main__":
    generate_apple_carousel("output/carousel")
