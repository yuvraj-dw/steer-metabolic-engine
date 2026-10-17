import os
import math
import asyncio
import functools
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from pipeline.voice_engine import generate_voiceover, load_env_file

load_env_file()

PALETTE = {
    "cream": "#F5EBDF",
    "rust": "#C04E2A",
    "deep_maroon": "#661414",
    "ink": "#351D1D",
    "clay": "#7D5246",
    "blush": "#DEC3B5",
    "soft_paper": "#FAF5EF",
    "white": "#FFFFFF",
    "card_border": "#E2CCBD",
    "teal_calm": "#235937",
    "teal_bright": "#34A853",
    "coral_alert": "#D94228"
}

WINDOWS_FONTS = "C:/Windows/Fonts"

@functools.lru_cache(maxsize=128)
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

@functools.lru_cache(maxsize=128)
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

def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1.0 - math.pow(1.0 - t, 3)

def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)

SCENES_TOFI = [
    {
        "id": 1, "start": 0.0, "end": 9.0, "dark": False,
        "tag": "THE 70 KG PARADOX",
        "title": "Two people. Both 70 kilos.",
        "subtitle": "Same height. Both normal BMI. So why does one carry diabetic risk?",
        "type": "paradox_compare"
    },
    {
        "id": 2, "start": 9.0, "end": 16.5, "dark": False,
        "tag": "LANCET CLINICAL STUDY",
        "title": "The weighing scale is a trap.",
        "subtitle": "Thin on the Outside, Fat on the Inside (The TOFI Phenotype).",
        "type": "tofi_intro"
    },
    {
        "id": 3, "start": 16.5, "end": 26.5, "dark": False,
        "tag": "DEXA SCAN TELEMETRY",
        "title": "Up to 80% more visceral fat.",
        "subtitle": "Indian genetics store ectopic fat around organs, even at normal weight.",
        "type": "organ_adiposity"
    },
    {
        "id": 4, "start": 26.5, "end": 33.5, "dark": False,
        "tag": "GUT-BRAIN SIGNALING GAP",
        "title": "Hidden fat blocks satiety.",
        "subtitle": "Visceral cytokines physically block natural GLP-1 and leptin signals.",
        "type": "hormonal_block"
    },
    {
        "id": 5, "start": 33.5, "end": 40.5, "dark": True,
        "tag": "BIOLOGY OVER WILLPOWER",
        "title": "It's biology, not willpower.",
        "subtitle": "Steer starts with DEXA scans and 55+ biomarkers before any medicine.",
        "type": "steer_dexa"
    },
    {
        "id": 6, "start": 40.5, "end": 46.8, "dark": False,
        "tag": "DOCTOR-LED HEALTH CLUB",
        "title": "Stop guessing. Ask a doctor.",
        "subtitle": "Real doctors. Comprehensive testing. Habit off-ramps that last.",
        "type": "steer_cta"
    }
]

def get_study_reel_spec(study=None):
    if not study:
        script = '''Two people. Same height. Both 70 kilos. Both normal BMI.
So why does one have the metabolic risk of a diabetic?
Because in India, the weighing scale is a trap.
Lancet researchers call it the TOFI phenotype: Thin on the Outside, Fat on the Inside.
Indian bodies store up to 80% more visceral fat around internal organs, even at a normal weight.
This hidden fat blocks your gut's natural satiety signals, triggering chronic food noise and cravings.
You don't lack discipline. You're fighting unseen biology.
Steer starts with DEXA scans and 55 biomarkers before any medicine.
Stop Googling. Ask a doctor at steerclub.com.'''
        return script, SCENES_TOFI

    sid = study.study_id.lower()
    stitle = study.title.lower()
    f0 = study.key_findings[0] if study.key_findings else None
    f1 = study.key_findings[1] if len(study.key_findings) > 1 else f0

    if "tofi" in sid or "tofi" in stitle:
        return get_study_reel_spec(None)

    elif "tirzepatide" in stitle or "surpass" in sid:
        script = f"""Can targeting two hunger hormones produce superior weight loss?
In the landmark SURPASS-2 trial published in the New England Journal of Medicine, researchers tested dual GIP and GLP-1 therapy.
Patients achieved an average 11.2 kilo weight reduction at the highest dose.
Dual receptor agonism simultaneously quiets hypothalamic food noise and restores peripheral insulin sensitivity.
But medical care cannot be unmonitored. Steer pairs doctor-guided dosing with DEXA lean muscle defense.
Stop guessing your health. Ask a doctor at steerclub.com."""

        scenes = [
            {
                "id": 1, "start": 0.0, "end": 7.5, "dark": False,
                "tag": "NEJM CLINICAL TRIAL",
                "title": "Dual Hormone Activation.",
                "subtitle": "Targeting two satiety receptors outperforms single GLP-1 therapy.",
                "type": "clinical_hero",
                "card_title": "SURPASS-2 HEAD-TO-HEAD TRIAL (n=1,879)",
                "stat": "-11.2 kg",
                "stat_label": "Superior Dose-Dependent Weight Loss",
                "stat_sub": "Statistically significant vs semaglutide (p <0.001)",
                "slabs": [
                    ("01  Dual Receptor Synergy", "Simultaneously activates GIP & GLP-1 pathways to quiet hunger."),
                    ("02  Superior Lipid Clearance", "Accelerates peripheral insulin sensitivity and visceral fat reduction."),
                    ("03  Mandatory Clinical Care", "Doctor-supervised titration eliminates GI symptoms and protects muscle.")
                ]
            },
            {
                "id": 2, "start": 7.5, "end": 15.0, "dark": False,
                "tag": "PRIMARY TRIAL OUTCOME",
                "title": "-11.2 kg at 40 Weeks.",
                "subtitle": "Dual incretin therapy demonstrated superior dose-dependent clearance.",
                "type": "clinical_hero",
                "card_title": "NEJM TRIAL TELEMETRY (n=1,879)",
                "stat": "-11.2 kg",
                "stat_label": "Average Weight Reduction Achieved",
                "stat_sub": "Highest dose cohort at 40 weeks (NEJM 2021)",
                "slabs": [
                    ("01  Deep Glycemic Control", "Significantly greater HbA1c reduction across diverse patient cohorts."),
                    ("02  Visceral Adipose Defense", "Targeted reduction in ectopic visceral fat surrounding internal organs."),
                    ("03  Structured Titration", "Gradual clinical titration eliminates standard gastrointestinal discomfort.")
                ]
            },
            {
                "id": 3, "start": 15.0, "end": 23.0, "dark": False,
                "tag": "GUT-BRAIN PATHOPHYSIOLOGY",
                "title": "Why Dual Incretins Work.",
                "subtitle": "GIP and GLP-1 receptors synergistically silence food noise.",
                "type": "hormonal_block"
            },
            {
                "id": 4, "start": 23.0, "end": 31.0, "dark": False,
                "tag": "CLINICAL SAFETY GATE",
                "title": "Titration is Mandatory.",
                "subtitle": "Medical supervision avoids unmonitored side effects and muscle loss.",
                "type": "organ_adiposity"
            },
            {
                "id": 5, "start": 31.0, "end": 38.0, "dark": True,
                "tag": "BIOLOGY OVER WILLPOWER",
                "title": "It's biology, not willpower.",
                "subtitle": "Steer starts with DEXA scans and 55+ biomarkers before any medicine.",
                "type": "steer_dexa"
            },
            {
                "id": 6, "start": 38.0, "end": 44.0, "dark": False,
                "tag": "DOCTOR-LED HEALTH CLUB",
                "title": "Stop guessing. Ask a doctor.",
                "subtitle": "Real doctors. Comprehensive testing. Habit off-ramps that last.",
                "type": "steer_cta"
            }
        ]
        return script, scenes

    elif "mace" in sid or "cardiovascular" in stitle:
        script = f"""Why is GLP-1 heart medicine, not just a weight loss shortcut?
In the real-world STEER study of 24,800 patients published in Diabetes, Obesity and Metabolism, continuous care delivered a 57% lower rate of cardiovascular events.
Heart attacks, strokes, and cardiovascular mortality dropped significantly.
Reducing visceral organ fat directly decreases systemic arterial inflammation and insulin burden.
Vanity weight loss fades. Long-term cardiovascular protection lasts.
Stop guessing your health. Ask a doctor at steerclub.com."""

        scenes = [
            {
                "id": 1, "start": 0.0, "end": 7.5, "dark": False,
                "tag": "DOM REAL-WORLD EVIDENCE",
                "title": "GLP-1 is Heart Medicine.",
                "subtitle": "Why metabolic therapy protects your cardiovascular system.",
                "type": "clinical_hero",
                "card_title": "REAL-WORLD STEER COHORT (n=24,800)",
                "stat": "57% Lower",
                "stat_label": "Major Adverse Cardiovascular Events (MACE)",
                "stat_sub": "Statistically significant cardiovascular risk reduction",
                "slabs": [
                    ("01  Heart Attack & Stroke Defense", "Continuous clinical therapy significantly lowers acute arterial events."),
                    ("02  Vascular Decompression", "Visceral fat reduction directly relieves systemic pressure on arterial walls."),
                    ("03  Continuous Care Mandate", "Sporadic or off-label use fails to achieve cardiac and endothelial defense.")
                ]
            },
            {
                "id": 2, "start": 7.5, "end": 15.0, "dark": False,
                "tag": "CARDIOVASCULAR TELEMETRY",
                "title": "57% Lower Heart Risk.",
                "subtitle": "Clinical evidence confirms systemic arterial protection.",
                "type": "clinical_hero",
                "card_title": "CARDIOMETABOLIC RISK REDUCTION",
                "stat": "57%",
                "stat_label": "Reduction in Heart Attacks & Strokes",
                "stat_sub": "Diabetes, Obesity and Metabolism 2026",
                "slabs": [
                    ("01  Arterial Inflammation Drops", "Substantial decrease in systemic endothelial and vascular inflammation."),
                    ("02  Restores Microvascular Flow", "Improves cellular oxygen delivery and peripheral vascular sensitivity."),
                    ("03  Cardiometabolic Sanctuary", "Protects cardiac tissue while accelerating toxic visceral fat clearance.")
                ]
            },
            {
                "id": 3, "start": 15.0, "end": 23.0, "dark": False,
                "tag": "ENDOTHELIAL HEALTH",
                "title": "Visceral Fat Inflames Arteries.",
                "subtitle": "Organ fat releases inflammatory cytokines directly into blood vessels.",
                "type": "organ_adiposity"
            },
            {
                "id": 4, "start": 23.0, "end": 31.0, "dark": False,
                "tag": "CONTINUOUS CARE MANDATE",
                "title": "Consistency Saves Lives.",
                "subtitle": "Cardiovascular benefits require doctor-guided ongoing adherence.",
                "type": "hormonal_block"
            },
            {
                "id": 5, "start": 31.0, "end": 38.0, "dark": True,
                "tag": "BIOLOGY OVER WILLPOWER",
                "title": "It's biology, not willpower.",
                "subtitle": "Steer starts with DEXA scans and 55+ biomarkers before any medicine.",
                "type": "steer_dexa"
            },
            {
                "id": 6, "start": 38.0, "end": 44.0, "dark": False,
                "tag": "DOCTOR-LED HEALTH CLUB",
                "title": "Stop guessing. Ask a doctor.",
                "subtitle": "Real doctors. Comprehensive testing. Habit off-ramps that last.",
                "type": "steer_cta"
            }
        ]
        return script, scenes

    else:
        # STEP-1 Extension Rebound Reel
        script = f"""Why does two-thirds of lost weight return after stopping GLP-1?
In the official STEP-1 trial extension, participants regained 67% of lost weight within 12 months without structured tapering.
Not because they lacked willpower, but because the brain defends its metabolic set-point.
When medication stops abruptly, ghrelin surges and the body fights to rebound.
Medicine is the jumpstart. Maintenance is the goal.
Stop guessing your health. Ask a doctor at steerclub.com."""

        scenes = [
            {
                "id": 1, "start": 0.0, "end": 7.5, "dark": False,
                "tag": "STEP-1 TRIAL EXTENSION",
                "title": "The Rebound Trap.",
                "subtitle": "Why does two-thirds of lost weight return after stopping?",
                "type": "clinical_hero",
                "card_title": "NEJM / DOM TRIAL EXTENSION",
                "stat": "67%",
                "stat_label": "Weight Regained Without Lifestyle Tapering",
                "stat_sub": "Clinical data confirms set-point hormonal defense",
                "slabs": [
                    ("01  Famine Survival Alarm", "Abrupt medication cessation triggers primitive starvation defense."),
                    ("02  Hypothalamic Weight Rebound", "Brain forcefully pulls hormonal levers to restore prior fat reserves."),
                    ("03  Structured Off-Ramp Required", "Doctor-led tapering allows metabolic set-point to recalibrate permanently.")
                ]
            },
            {
                "id": 2, "start": 7.5, "end": 15.0, "dark": False,
                "tag": "SET-POINT DEFENSE",
                "title": "Your Body Fights Back.",
                "subtitle": "Calorie restriction alone triggers ancient famine alarms.",
                "type": "clinical_hero",
                "card_title": "HYPOTHALAMIC SET-POINT CRISIS",
                "stat": "+240%",
                "stat_label": "Ghrelin Surge Upon Abrupt Cessation",
                "stat_sub": "Forces intense cravings and weight regain",
                "slabs": [
                    ("01  Leptin Satiety Crash", "Circulating satiety signals drop by 40% within weeks of stopping."),
                    ("02  Ghrelin Hunger Alarms", "Hunger hormones surge violently to force rapid caloric consumption."),
                    ("03  Metabolic Adaptation", "Resting energy expenditure drops without targeted resistance and protein.")
                ]
            },
            {
                "id": 3, "start": 15.0, "end": 23.0, "dark": False,
                "tag": "HORMONAL SET-POINT",
                "title": "The Weight Thermostat.",
                "subtitle": "Your brain defends its weight unless biologically reset.",
                "type": "hormonal_block"
            },
            {
                "id": 4, "start": 23.0, "end": 31.0, "dark": False,
                "tag": "THE EXIT OFF-RAMP",
                "title": "Medicine is the Jumpstart.",
                "subtitle": "Maintenance is the goal. Steer builds the planned exit.",
                "type": "organ_adiposity"
            },
            {
                "id": 5, "start": 31.0, "end": 38.0, "dark": True,
                "tag": "BIOLOGY OVER WILLPOWER",
                "title": "It's biology, not willpower.",
                "subtitle": "Steer starts with DEXA scans and 55+ biomarkers before any medicine.",
                "type": "steer_dexa"
            },
            {
                "id": 6, "start": 38.0, "end": 44.0, "dark": False,
                "tag": "DOCTOR-LED HEALTH CLUB",
                "title": "Stop guessing. Ask a doctor.",
                "subtitle": "Real doctors. Comprehensive testing. Habit off-ramps that last.",
                "type": "steer_cta"
            }
        ]
        return script, scenes

def draw_vector_bullet(draw, x, y, color):
    draw.ellipse([x, y + 6, x + 8, y + 14], fill=color)

def draw_vector_check(draw, x, y, color):
    draw.line([(x, y + 8), (x + 5, y + 15)], fill=color, width=3)
    draw.line([(x + 4, y + 15), (x + 16, y + 3)], fill=color, width=3)

def render_scene_frame(
    scene: dict, 
    t_local: float, 
    t_global: float, 
    total_duration: float, 
    width: int = 1080, 
    height: int = 1920
) -> Image.Image:
    is_dark = scene["dark"]
    bg_col = PALETTE["deep_maroon"] if is_dark else PALETTE["cream"]
    title_col = PALETTE["white"] if is_dark else PALETTE["deep_maroon"]
    sub_col = PALETTE["blush"] if is_dark else PALETTE["clay"]

    img = Image.new("RGB", (width, height), bg_col)
    draw = ImageDraw.Draw(img)

    margin_x = 80
    margin_right = 140
    content_w = width - margin_x - margin_right

    # 1. Top Brand Header (Large, legible)
    draw.text((margin_x, 65), "steer", fill=title_col, font=get_serif(44, bold=True))
    draw.text((margin_x + 125, 75), "•  Clinical Weight Loss", fill=sub_col, font=get_sans(24))

    # 2. Category Pill Badge
    tag_font = get_sans(20, bold=True)
    t_bbox = draw.textbbox((0, 0), scene["tag"], font=tag_font)
    t_w = t_bbox[2] - t_bbox[0] + 34
    badge_bg = "#4A0F0F" if is_dark else "#E6D3C2"
    badge_text_col = PALETTE["white"] if is_dark else PALETTE["deep_maroon"]
    draw.rounded_rectangle([margin_x, 125, margin_x + t_w, 125 + 40], radius=20, fill=badge_bg)
    draw.text((margin_x + 17, 134), scene["tag"], fill=badge_text_col, font=tag_font)

    # 3. Main Headline (Bold 60px display)
    font_title = get_serif(60, bold=True)
    title_lines = wrap_text(scene["title"], font_title, content_w, draw)
    y_title = 185
    for tl in title_lines:
        draw.text((margin_x, y_title), tl, fill=title_col, font=font_title)
        y_title += 68

    # 4. Subtitle (Generous 26px type, strictly finishing above y=320)
    font_sub = get_sans(26)
    sub_lines = wrap_text(scene["subtitle"], font_sub, content_w, draw)
    y_sub = y_title + 10
    for sl in sub_lines:
        draw.text((margin_x, y_sub), sl, fill=sub_col, font=font_sub)
        y_sub += 34

    # 5. Middle Visual Arena (Starts safely at y=360, leaving 50px clean buffer)
    arena_top = 360
    arena_h = 1020  # Ends at y=1380

    if scene["type"] == "clinical_hero":
        arena_h = 860  # Perfectly hugs content with 40px bottom padding (zero dead space!)
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 30), scene.get("card_title", "CLINICAL EVIDENCE TELEMETRY"), fill=PALETTE["clay"], font=get_sans(20, bold=True))

        stat_val = scene.get("stat", "-11.2 kg")
        font_stat = get_serif(104, bold=True)
        stat_bbox = draw.textbbox((0, 0), stat_val, font=font_stat)
        stat_w = stat_bbox[2] - stat_bbox[0]
        draw.text((margin_x + 36, arena_top + 75), stat_val, fill=PALETTE["rust"], font=font_stat)

        col2_x = margin_x + 36 + stat_w + 35
        max_lbl_w = (margin_x + content_w - 36) - col2_x

        lbl_lines = wrap_text(scene.get("stat_label", "Clinical Outcome"), get_sans(28, bold=True), max_lbl_w, draw)
        y_lbl = arena_top + 80
        for ll in lbl_lines:
            draw.text((col2_x, y_lbl), ll, fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
            y_lbl += 34
        draw.text((col2_x, y_lbl + 6), scene.get("stat_sub", "Statistically significant outcome (p <0.001)"), fill=PALETTE["clay"], font=get_sans(20))

        # Incretin Comparison Gauge Bar
        meter_y = arena_top + 215
        meter_w = content_w - 72
        draw.rounded_rectangle([margin_x + 36, meter_y, margin_x + 36 + meter_w, meter_y + 14], radius=7, fill="#F2E6DC")
        draw.rounded_rectangle([margin_x + 36, meter_y, margin_x + 36 + int(meter_w * 0.90), meter_y + 14], radius=7, fill=PALETTE["rust"])

        div_y = arena_top + 255
        draw.line([(margin_x + 36, div_y), (margin_x + content_w - 36, div_y)], fill=PALETTE["card_border"], width=1)

        # 3 High-Impact Slabs filling the central space
        slabs = scene.get("slabs", [
            ("01  Dual Receptor Synergy", "Simultaneously activates GIP & GLP-1 pathways to quiet hunger."),
            ("02  Superior Lipid Clearance", "Accelerates peripheral insulin sensitivity and visceral fat reduction."),
            ("03  Mandatory Clinical Care", "Doctor-supervised titration eliminates GI symptoms and protects muscle.")
        ])

        slab_y = div_y + 30
        slab_h = 130
        for title, desc in slabs:
            draw.rounded_rectangle([margin_x + 36, slab_y, margin_x + content_w - 36, slab_y + slab_h], radius=18, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            draw.text((margin_x + 64, slab_y + 24), title, fill=PALETTE["deep_maroon"], font=get_sans(26, bold=True))
            
            d_lines = wrap_text(desc, get_sans(22), content_w - 130, draw)
            dy = slab_y + 68
            for dl in d_lines:
                draw.text((margin_x + 64, dy), dl, fill=PALETTE["ink"], font=get_sans(22))
                dy += 30
            slab_y += slab_h + 20

        # Bottom Trust Anchor Pill Box inside card (Even spacing, zero dead space!)
        trust_y = slab_y + 10
        draw.rounded_rectangle([margin_x + 36, trust_y, margin_x + content_w - 36, trust_y + 90], radius=16, fill="#EDF5F0", outline="#BEE0CD", width=1)
        draw_vector_check(draw, margin_x + 58, trust_y + 36, PALETTE["teal_calm"])
        draw.text((margin_x + 88, trust_y + 22), "Doctor-Led Clinical Protocol • Built for Indian Biology", fill=PALETTE["teal_calm"], font=get_sans(22, bold=True))
        draw.text((margin_x + 88, trust_y + 54), "Diagnostics First: 55+ Biomarkers • DEXA Scan • Exit Off-Ramp", fill=PALETTE["clay"], font=get_sans(19))

        # Bottom Invitation Hook below card in thumb zone
        call_y = arena_top + arena_h + 35
        draw.text((margin_x, call_y), "Doctor-Led Metabolic Care for Indian Biology • steerclub.com →", fill=PALETTE["rust"], font=get_sans(22, bold=True))

    elif scene["type"] == "paradox_compare":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "SOUTH ASIAN PHENOTYPE SCAN", fill=PALETTE["clay"], font=get_sans(19, bold=True))
        
        col_w = (content_w - 72 - 20) // 2
        b1_x = margin_x + 36
        b2_x = b1_x + col_w + 20
        box_y = arena_top + 65
        box_h = 370

        # European Card
        draw.rounded_rectangle([b1_x, box_y, b1_x + col_w, box_y + box_h], radius=18, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
        draw.text((b1_x + 24, box_y + 24), "EUROPEAN BODY", fill=PALETTE["clay"], font=get_sans(18, bold=True))
        draw.text((b1_x + 24, box_y + 62), "70.0 kg", fill=PALETTE["deep_maroon"], font=get_serif(44, bold=True))
        draw.text((b1_x + 24, box_y + 124), "BMI 22.8 (Normal)", fill=PALETTE["ink"], font=get_sans(21))

        draw.rounded_rectangle([b1_x + 24, box_y + 170, b1_x + col_w - 24, box_y + 258], radius=12, fill="#EDF5F0", outline="#BEE0CD")
        draw.ellipse([b1_x + 38, box_y + 195, b1_x + 52, box_y + 209], fill=PALETTE["teal_bright"])
        draw.text((b1_x + 62, box_y + 192), "SUBCUTANEOUS", fill=PALETTE["teal_calm"], font=get_sans(17, bold=True))
        draw.text((b1_x + 38, box_y + 226), "Stored safely under skin", fill=PALETTE["clay"], font=get_sans(15))

        draw_vector_bullet(draw, b1_x + 24, box_y + 285, PALETTE["teal_bright"])
        draw.text((b1_x + 44, box_y + 280), "Low ectopic organ fat", fill=PALETTE["teal_calm"], font=get_sans(19, bold=True))
        draw_vector_bullet(draw, b1_x + 24, box_y + 322, PALETTE["teal_bright"])
        draw.text((b1_x + 44, box_y + 317), "Normal insulin sensitivity", fill=PALETTE["teal_calm"], font=get_sans(19, bold=True))

        # Indian Card
        pulse = math.sin(t_local * 4.5) * 0.5 + 0.5
        border_r = int(192 + 35 * pulse)
        border_g = int(78 + 20 * pulse)
        border_b = int(42 + 20 * pulse)
        pulse_col = f"#{border_r:02x}{border_g:02x}{border_b:02x}"

        draw.rounded_rectangle([b2_x, box_y, b2_x + col_w, box_y + box_h], radius=18, fill=PALETTE["white"], outline=pulse_col, width=2)
        draw.text((b2_x + 24, box_y + 24), "INDIAN BODY", fill=PALETTE["rust"], font=get_sans(18, bold=True))
        draw.text((b2_x + 24, box_y + 62), "70.0 kg", fill=PALETTE["rust"], font=get_serif(44, bold=True))
        draw.text((b2_x + 24, box_y + 124), "BMI 22.8 (Normal)", fill=PALETTE["ink"], font=get_sans(21))

        draw.rounded_rectangle([b2_x + 24, box_y + 170, b2_x + col_w - 24, box_y + 258], radius=12, fill="#FAF0EB", outline="#F0C5B4")
        draw.ellipse([b2_x + 38, box_y + 195, b2_x + 52, box_y + 209], fill=PALETTE["coral_alert"])
        draw.text((b2_x + 62, box_y + 192), "VISCERAL BURDEN", fill=PALETTE["rust"], font=get_sans(17, bold=True))
        draw.text((b2_x + 38, box_y + 226), "Suffocates liver & organs", fill=PALETTE["deep_maroon"], font=get_sans(15, bold=True))

        draw_vector_bullet(draw, b2_x + 24, box_y + 285, PALETTE["coral_alert"])
        draw.text((b2_x + 44, box_y + 280), "Severe hepatic lipid fat", fill=PALETTE["rust"], font=get_sans(19, bold=True))
        draw_vector_bullet(draw, b2_x + 24, box_y + 322, PALETTE["coral_alert"])
        draw.text((b2_x + 44, box_y + 317), "Early insulin resistance", fill=PALETTE["rust"], font=get_sans(19, bold=True))

        div_y = box_y + box_h + 30
        draw.line([(margin_x + 36, div_y), (margin_x + content_w - 36, div_y)], fill=PALETTE["card_border"], width=1)
        
        stat_p = min(1.0, t_local / 1.1)
        stat_val = 1.0 + 1.1 * ease_out_cubic(stat_p)
        draw.text((margin_x + 36, div_y + 28), f"{stat_val:.1f}x", fill=PALETTE["rust"], font=get_serif(104, bold=True))
        
        col2_x = margin_x + 310
        draw.text((col2_x, div_y + 35), "Higher Visceral Adipose Ratio", fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
        takeaway = "At identical scale weight, South Asians carry double the visceral organ fat, accelerating pre-diabetes."
        t_lines = wrap_text(takeaway, get_sans(21), content_w - 340, draw)
        ty = div_y + 78
        for tl in t_lines:
            draw.text((col2_x, ty), tl, fill=PALETTE["ink"], font=get_sans(21))
            ty += 30
        draw.text((col2_x, ty + 10), "Source: Lancet Diabetes & Endocrinology 2021", fill=PALETTE["clay"], font=get_sans(18))

        trust_y = arena_top + arena_h - 75
        draw.rounded_rectangle([margin_x + 36, trust_y, margin_x + content_w - 36, trust_y + 54], radius=14, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
        draw_vector_check(draw, margin_x + 58, trust_y + 16, PALETTE["deep_maroon"])
        draw.text((margin_x + 88, trust_y + 16), "DEXA-Verified Body Composition  •  Steer Clinical Protocol", fill=PALETTE["deep_maroon"], font=get_sans(18, bold=True))

    elif scene["type"] == "tofi_intro":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "THE TOFI PHENOMENON (LANCET 2021)", fill=PALETTE["clay"], font=get_sans(19, bold=True))

        t_box_y = arena_top + 70
        draw.rounded_rectangle([margin_x + 36, t_box_y, margin_x + content_w - 36, t_box_y + 250], radius=18, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
        
        draw.text((margin_x + 50, t_box_y + 35), "T.O.F.I.", fill=PALETTE["rust"], font=get_serif(68, bold=True))
        
        meter_p = min(1.0, t_local / 1.3)
        meter_w = int(200 * ease_out_cubic(meter_p))
        draw.rounded_rectangle([margin_x + 50, t_box_y + 135, margin_x + 50 + 200, t_box_y + 147], radius=6, fill="#F2E6DC")
        if meter_w > 0:
            draw.rounded_rectangle([margin_x + 50, t_box_y + 135, margin_x + 50 + meter_w, t_box_y + 147], radius=6, fill=PALETTE["rust"])

        col2_x = margin_x + 350
        draw.text((col2_x, t_box_y + 36), "Thin Outside, Fat Inside", fill=PALETTE["deep_maroon"], font=get_sans(26, bold=True))
        draw.text((col2_x, t_box_y + 84), "The weighing scale measures gravity, not health.", fill=PALETTE["ink"], font=get_sans(21))
        draw.text((col2_x, t_box_y + 128), "Standard BMI fails South Asian physiology.", fill=PALETTE["clay"], font=get_sans(20))
        draw.text((col2_x, t_box_y + 172), "Visceral fat wraps vital organs silently.", fill=PALETTE["rust"], font=get_sans(20, bold=True))

        div_y = t_box_y + 290
        draw.line([(margin_x + 36, div_y), (margin_x + content_w - 36, div_y)], fill=PALETTE["card_border"], width=1)
        
        yrs_p = min(1.0, t_local / 1.0)
        yrs_val = int(10 * ease_out_cubic(yrs_p))
        draw.text((margin_x + 36, div_y + 40), f"{yrs_val} yrs", fill=PALETTE["deep_maroon"], font=get_serif(96, bold=True))
        
        draw.text((col2_x, div_y + 45), "Earlier Metabolic Complications", fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
        txt = "Indians develop diabetes and cardiovascular risks a decade before Western populations."
        t_lines = wrap_text(txt, get_sans(21), content_w - 380, draw)
        ty = div_y + 92
        for tl in t_lines:
            draw.text((col2_x, ty), tl, fill=PALETTE["ink"], font=get_sans(21))
            ty += 30
        draw.text((col2_x, ty + 12), "ICMR National Surveillance Study • steerclub.com", fill=PALETTE["clay"], font=get_sans(18))

    elif scene["type"] == "organ_adiposity":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "DEXA ORGAN SCAN TELEMETRY", fill=PALETTE["clay"], font=get_sans(19, bold=True))

        stat_p = min(1.0, t_local / 1.1)
        stat_val = int(80 * ease_out_cubic(stat_p))
        draw.text((margin_x + 36, arena_top + 80), f"+{stat_val}%", fill=PALETTE["rust"], font=get_serif(96, bold=True))
        
        col2_x = margin_x + 370
        draw.text((col2_x, arena_top + 90), "Visceral Ectopic Storage", fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
        draw.text((col2_x, arena_top + 136), "Fat accumulates inside liver and pancreas tissues", fill=PALETTE["ink"], font=get_sans(22))
        draw.text((col2_x, arena_top + 174), "Completely undetectable by standard weighing scales", fill=PALETTE["clay"], font=get_sans(19))

        meter_y = arena_top + 225
        meter_total_w = content_w - 72
        fill_w = int(meter_total_w * (stat_val / 80.0))
        draw.rounded_rectangle([margin_x + 36, meter_y, margin_x + 36 + meter_total_w, meter_y + 14], radius=7, fill="#F2E6DC")
        if fill_w > 0:
            draw.rounded_rectangle([margin_x + 36, meter_y, margin_x + 36 + fill_w, meter_y + 14], radius=7, fill=PALETTE["rust"])

        div_y = arena_top + 270
        draw.line([(margin_x + 36, div_y), (margin_x + content_w - 36, div_y)], fill=PALETTE["card_border"], width=1)

        draw.text((margin_x + 36, div_y + 40), "Why Traditional Calorie Counting Fails in India:", fill=PALETTE["deep_maroon"], font=get_sans(26, bold=True))
        
        items = [
            ("Caloric restriction burns precious lean muscle first", False),
            ("Toxic visceral organ fat remains locked by circulating insulin", False),
            ("DEXA body scanning is clinically required to separate muscle from fat", True)
        ]
        b_y = div_y + 95
        for text_line, is_highlight in items:
            bullet_col = PALETTE["rust"] if is_highlight else PALETTE["deep_maroon"]
            text_col = PALETTE["rust"] if is_highlight else PALETTE["ink"]
            font_b = get_sans(22, bold=is_highlight)
            draw_vector_bullet(draw, margin_x + 36, b_y + 5, bullet_col)
            draw.text((margin_x + 60, b_y), text_line, fill=text_col, font=font_b)
            b_y += 66

    elif scene["type"] == "hormonal_block":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "GUT-BRAIN INCRETIN AXIS", fill=PALETTE["clay"], font=get_sans(19, bold=True))

        draw.text((margin_x + 36, arena_top + 80), "84 dB", fill=PALETTE["deep_maroon"], font=get_serif(96, bold=True))
        col2_x = margin_x + 370
        draw.text((col2_x, arena_top + 90), "Hypothalamic Food Noise", fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
        draw.text((col2_x, arena_top + 136), "Visceral cytokines physically block satiety receptors", fill=PALETTE["rust"], font=get_sans(22, bold=True))

        div_y = arena_top + 250
        wave_pts = []
        for wx in range(margin_x + 36, margin_x + content_w - 36, 4):
            wy = div_y + math.sin(wx / 30.0 + t_local * 6.5) * 14.0
            wave_pts.append((wx, wy))
        draw.line(wave_pts, fill=PALETTE["rust"], width=4)

        draw.text((margin_x + 36, div_y + 40), "The Biochemical Breakdown at 4 PM:", fill=PALETTE["deep_maroon"], font=get_sans(26, bold=True))
        
        breakdown_items = [
            "Stomach is full, but intestinal GLP-1 signals are blunted",
            "Brain misinterprets silence as an urgent starvation threat",
            "Hunger ghrelin surges +240%, forcing uncontrollable cravings"
        ]
        b_y = div_y + 95
        for bi in breakdown_items:
            draw_vector_bullet(draw, margin_x + 36, b_y + 5, PALETTE["deep_maroon"])
            draw.text((margin_x + 60, b_y), bi, fill=PALETTE["ink"], font=get_sans(22))
            b_y += 66

    elif scene["type"] == "steer_dexa":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=24, fill="#500E0E", outline="#7D2626", width=1)
        draw.text((margin_x + 36, arena_top + 28), "STEER CLINICAL PROTOCOL", fill=PALETTE["blush"], font=get_sans(19, bold=True))

        draw.text((margin_x + 36, arena_top + 80), "Diagnostics First.", fill=PALETTE["white"], font=get_serif(60, bold=True))
        draw.text((margin_x + 36, arena_top + 150), "Never guess your biology from an obsolete scale.", fill=PALETTE["blush"], font=get_sans(24))

        pillars = [
            ("DEXA Body Composition Scan", "Quantifies visceral organ fat vs protected lean muscle mass", 0.2),
            ("55+ Biomarker Diagnostic Panel", "Measures fasting insulin, HOMA-IR, liver enzymes, and lipids", 0.6),
            ("Doctor-Led Care With Planned Exit", "Medical jumpstart coupled with permanent habit calibration", 1.0)
        ]

        p_y = arena_top + 245
        for title, desc, delay in pillars:
            p_prog = min(1.0, max(0.0, (t_local - delay) / 0.5))
            slide_x = int(-24 * (1.0 - ease_out_cubic(p_prog)))
            cur_x = margin_x + 36 + slide_x

            draw.rounded_rectangle([cur_x, p_y, cur_x + content_w - 72, p_y + 115], radius=16, fill="#3D0B0B", outline="#7D2626", width=1)
            draw_vector_check(draw, cur_x + 24, p_y + 24, PALETTE["teal_bright"])
            draw.text((cur_x + 58, p_y + 20), title, fill=PALETTE["white"], font=get_sans(26, bold=True))
            draw.text((cur_x + 58, p_y + 60), desc, fill=PALETTE["blush"], font=get_sans(21))
            p_y += 135

    else:
        # Steer Doctor CTA
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=24, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "A TRUSTED DOCTOR'S NOTE", fill=PALETTE["clay"], font=get_sans(19, bold=True))

        draw.text((margin_x + 36, arena_top + 85), "Lose well. Live well.", fill=PALETTE["deep_maroon"], font=get_serif(60, bold=True))
        
        quote = '"Before you start another diet, hear it from a doctor, not a reel. No obligation. If it isn\'t right for you, they\'ll say so."'
        q_lines = wrap_text(quote, get_serif(34, italic=True), content_w - 72, draw)
        qy = arena_top + 185
        for ql in q_lines:
            draw.text((margin_x + 36, qy), ql, fill=PALETTE["ink"], font=get_serif(34, italic=True))
            qy += 52

        draw.line([(margin_x + 36, qy + 35), (margin_x + content_w - 36, qy + 35)], fill=PALETTE["card_border"], width=1)
        
        arrow_pulse = math.sin(t_local * 4.5) * 6.0
        draw.text((margin_x + 36 + int(arrow_pulse), qy + 75), "Doctor-led • Built for Indian biology • steerclub.com →", fill=PALETTE["rust"], font=get_sans(24, bold=True))

    prog_y = 1415
    draw.line([(margin_x, prog_y), (margin_x + content_w, prog_y)], fill="#DEC3B5" if not is_dark else "#500E0E", width=2)
    prog_len = int(content_w * min(1.0, max(0.0, t_global / total_duration)))
    if prog_len > 0:
        bar_col = PALETTE["rust"] if not is_dark else PALETTE["blush"]
        draw.line([(margin_x, prog_y), (margin_x + prog_len, prog_y)], fill=bar_col, width=4)

    return img

def get_audio_duration(audio_path: str) -> float:
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True, check=True
        )
        return float(res.stdout.strip())
    except Exception:
        return 44.0

def build_reel(output_mp4_path: str, study=None, duration_limit: float = None) -> str:
    fps = 30
    width, height = 1080, 1920

    work_dir = os.path.dirname(os.path.abspath(output_mp4_path))
    reel_basename = os.path.splitext(os.path.basename(output_mp4_path))[0]
    frames_dir = os.path.join(work_dir, f"temp_{reel_basename}_frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    study_suffix = f"_{study.study_id.lower().replace('-', '_')}" if study else "_tofi"
    audio_path = os.path.join(work_dir, f"voiceover{study_suffix}.mp3")

    script, scenes = get_study_reel_spec(study)

    if not os.path.exists(audio_path) or bool(os.environ.get("ELEVENLABS_API_KEY")):
        print(f"🎙️ Synthesizing study-specific voiceover ({len(script)} chars)...")
        asyncio.run(generate_voiceover(script, audio_path, preferred_voice="adam"))

    actual_duration = get_audio_duration(audio_path)
    duration = duration_limit if duration_limit else actual_duration
    total_frames = int(fps * duration)

    orig_total = scenes[-1]["end"]
    scale_factor = duration / orig_total if orig_total > 0 else 1.0

    scaled_scenes = []
    for sc in scenes:
        sc_copy = dict(sc)
        sc_copy["start"] = sc["start"] * scale_factor
        sc_copy["end"] = sc["end"] * scale_factor
        scaled_scenes.append(sc_copy)

    print(f"🎬 Rendering {total_frames} fluid frames ({duration:.1f}s at {fps}fps with big mobile-friendly typography)...")

    trans_duration = 0.4
    half_trans = trans_duration / 2.0

    for f in range(total_frames):
        time_sec = f / fps

        in_transition = False
        trans_idx = -1
        trans_prog = 0.0

        for i in range(len(scaled_scenes) - 1):
            boundary = scaled_scenes[i]["end"]
            if abs(time_sec - boundary) <= half_trans:
                in_transition = True
                trans_idx = i
                trans_prog = (time_sec - (boundary - half_trans)) / trans_duration
                break

        if in_transition:
            sc_A = scaled_scenes[trans_idx]
            sc_B = scaled_scenes[trans_idx + 1]
            t_loc_A = max(0.0, time_sec - sc_A["start"])
            t_loc_B = max(0.0, time_sec - sc_B["start"])

            img_A = render_scene_frame(sc_A, t_loc_A, time_sec, duration, width, height)
            img_B = render_scene_frame(sc_B, t_loc_B, time_sec, duration, width, height)

            ease = smoothstep(trans_prog)
            bg_target = PALETTE["deep_maroon"] if sc_B["dark"] else PALETTE["cream"]
            frame_img = Image.new("RGB", (width, height), bg_target)
            
            offset_A = int(-ease * width)
            offset_B = int((1.0 - ease) * width)
            
            frame_img.paste(img_A, (offset_A, 0))
            frame_img.paste(img_B, (offset_B, 0))
        else:
            scene_idx = len(scaled_scenes) - 1
            for idx, sc in enumerate(scaled_scenes):
                if sc["start"] <= time_sec < sc["end"]:
                    scene_idx = idx
                    break
            sc = scaled_scenes[scene_idx]
            t_loc = max(0.0, time_sec - sc["start"])
            frame_img = render_scene_frame(sc, t_loc, time_sec, duration, width, height)

        frame_img.save(os.path.join(frames_dir, f"frame_{f:05d}.jpg"), quality=88)

    print("Muxing video & neural audio with FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        output_mp4_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    os.rmdir(frames_dir)

    print(f"✅ Generated High-Readability Mobile AI Reel: {output_mp4_path}")
    return output_mp4_path

if __name__ == "__main__":
    out_reel = "C:/Users/yuvra/Downloads/Personal Proj/Steer Club Hackathon/output/reel/steer_clinical_reel.mp4"
    build_reel(out_reel)
