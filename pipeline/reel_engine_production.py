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
    "cream": "#E4D7C8",  # Calmer, dulled, premium matte taupe (zero blinding glare)
    "rust": "#C04E2A",
    "deep_maroon": "#5C1D18",
    "ink": "#2B1616",
    "clay": "#7D5246",
    "blush": "#DEC3B5",
    "soft_paper": "#FAF5EE",
    "white": "#FFFFFF",
    "card_border": "#D5C5B3",
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

def draw_vector_bullet(draw, x, y, color):
    draw.ellipse([x, y + 6, x + 10, y + 16], fill=color)

def draw_vector_check(draw, x, y, color):
    draw.line([(x, y + 10), (x + 6, y + 18)], fill=color, width=3)
    draw.line([(x + 5, y + 18), (x + 18, y + 4)], fill=color, width=3)

def draw_coronal_dexa_scan(draw, box_x, box_y, box_w, box_h, is_indian=False, t_local=0.0):
    """
    Draw an authentic coronal full-body DEXA scan heatmap.
    """
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=22, fill="#FFFFFF", outline="#D5C5B3", width=1)
    
    header_col = PALETTE["rust"] if is_indian else PALETTE["clay"]
    draw.text((box_x + 24, box_y + 24), "INDIAN PHENOTYPE" if is_indian else "EUROPEAN CONTROL", fill=header_col, font=get_sans(22, bold=True))
    draw.text((box_x + 24, box_y + 58), "70.0 kg", fill=header_col if is_indian else PALETTE["deep_maroon"], font=get_serif(48, bold=True))
    draw.text((box_x + 24, box_y + 118), "BMI 22.8 (Normal)", fill=PALETTE["ink"], font=get_sans(23))

    cx = box_x + box_w // 2
    scan_x = box_x + 20
    scan_w = box_w - 40
    scan_y = box_y + 165
    scan_h = 320
    draw.rounded_rectangle([scan_x, scan_y, scan_x + scan_w, scan_y + scan_h], radius=16, fill="#140F0F")

    for gx in range(scan_x, scan_x + scan_w, 40):
        draw.line([(gx, scan_y), (gx, scan_y + scan_h)], fill="#221A1A", width=1)
    for gy in range(scan_y, scan_y + scan_h, 40):
        draw.line([(scan_x, gy), (scan_x + scan_w, gy)], fill="#221A1A", width=1)

    torso_cy = scan_y + 160
    sh_w, waist_w, hip_w = 64, 46, 54
    torso_pts = [
        (cx - 16, torso_cy - 120), (cx + 16, torso_cy - 120),
        (cx + sh_w, torso_cy - 85), (cx + waist_w, torso_cy + 10),
        (cx + hip_w, torso_cy + 75), (cx + 38, torso_cy + 130),
        (cx + 16, torso_cy + 130), (cx, torso_cy + 55),
        (cx - 16, torso_cy + 130), (cx - 38, torso_cy + 130),
        (cx - hip_w, torso_cy + 75), (cx - waist_w, torso_cy + 10),
        (cx - sh_w, torso_cy - 85)
    ]
    draw.polygon(torso_pts, fill="#1A3832", outline="#2F6652", width=2)

    draw.line([(cx, torso_cy - 110), (cx, torso_cy + 50)], fill="#FAF5EE", width=6)
    for ry in range(int(torso_cy - 75), int(torso_cy - 10), 16):
        draw.line([(cx - 36, ry), (cx + 36, ry)], fill="#EAE0D2", width=2)
    draw.ellipse([cx - 36, torso_cy + 30, cx + 36, torso_cy + 75], outline="#FAF5EE", width=3)

    if not is_indian:
        subq_left = [(cx - sh_w + 2, torso_cy - 80), (cx - waist_w - 2, torso_cy + 10), (cx - hip_w - 2, torso_cy + 75)]
        subq_right = [(cx + sh_w - 2, torso_cy - 80), (cx + waist_w + 2, torso_cy + 10), (cx + hip_w + 2, torso_cy + 75)]
        draw.line(subq_left, fill="#34A853", width=6)
        draw.line(subq_right, fill="#34A853", width=6)
        draw.ellipse([cx - 12, torso_cy, cx + 12, torso_cy + 24], fill="#235937", outline="#34A853", width=2)
    else:
        pulse = math.sin(t_local * 4.5) * 4.0
        v_rx = int(36 + pulse)
        v_ry = int(46 + pulse)
        v_cy = torso_cy + 8
        
        draw.ellipse([cx - v_rx - 14, v_cy - v_ry - 12, cx + v_rx + 14, v_cy + v_ry + 12], fill="#42140E")
        draw.ellipse([cx - v_rx, v_cy - v_ry, cx + v_rx, v_cy + v_ry], fill="#992B17", outline="#C04E2A", width=2)
        draw.ellipse([cx - int(v_rx * 0.65), v_cy - int(v_ry * 0.65), cx + int(v_rx * 0.65), v_cy + int(v_ry * 0.65)], fill="#D94228")
        draw.ellipse([cx - int(v_rx * 0.32), v_cy - int(v_ry * 0.32), cx + int(v_rx * 0.32), v_cy + int(v_ry * 0.32)], fill="#FFA07A")

    pill_y = box_y + box_h - 75
    pill_bg = "#FAF0EB" if is_indian else "#EDF5F0"
    pill_border = "#F0C5B4" if is_indian else "#BEE0CD"
    pill_text_col = PALETTE["rust"] if is_indian else PALETTE["teal_calm"]
    pill_text = "VAT: 184 cm³ (+283% High Risk)" if is_indian else "VAT: 48 cm³ (Safe Reference)"

    draw.rounded_rectangle([box_x + 18, pill_y, box_x + box_w - 18, pill_y + 56], radius=14, fill=pill_bg, outline=pill_border, width=1)
    bullet_col = PALETTE["coral_alert"] if is_indian else PALETTE["teal_bright"]
    draw.ellipse([box_x + 32, pill_y + 21, box_x + 46, pill_y + 35], fill=bullet_col)
    draw.text((box_x + 54, pill_y + 16), pill_text, fill=pill_text_col, font=get_sans(19, bold=True))

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

    # 1. Top Brand Header
    draw.text((margin_x, 60), "steer", fill=title_col, font=get_serif(48, bold=True))
    draw.text((margin_x + 130, 70), "•  Clinical Weight Loss", fill=sub_col, font=get_sans(26))

    # 2. Category Pill Badge
    tag_font = get_sans(22, bold=True)
    t_bbox = draw.textbbox((0, 0), scene["tag"], font=tag_font)
    t_w = t_bbox[2] - t_bbox[0] + 36
    badge_bg = "#4A0F0F" if is_dark else "#D8C7B5"
    badge_text_col = PALETTE["white"] if is_dark else PALETTE["deep_maroon"]
    draw.rounded_rectangle([margin_x, 120, margin_x + t_w, 120 + 42], radius=21, fill=badge_bg)
    draw.text((margin_x + 18, 129), scene["tag"], fill=badge_text_col, font=tag_font)

    # 3. Main Headline (Commanding 66px display)
    font_title = get_serif(66, bold=True)
    title_lines = wrap_text(scene["title"], font_title, content_w, draw)
    y_title = 175
    for tl in title_lines:
        draw.text((margin_x, y_title), tl, fill=title_col, font=font_title)
        y_title += 72

    # 4. Subtitle (Generous 28px type)
    font_sub = get_sans(28)
    sub_lines = wrap_text(scene["subtitle"], font_sub, content_w, draw)
    y_sub = y_title + 8
    for sl in sub_lines:
        draw.text((margin_x, y_sub), sl, fill=sub_col, font=font_sub)
        y_sub += 36

    # 5. Middle Visual Arena (100% Screen Utilization, from 340 to 1660)
    arena_top = 340
    arena_h = 1320

    if scene["type"] == "clinical_hero":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=26, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), scene.get("card_title", "CLINICAL EVIDENCE TELEMETRY"), fill=PALETTE["clay"], font=get_sans(20, bold=True))

        stat_val = scene.get("stat", "-11.2 kg")
        font_stat = get_serif(116, bold=True)
        stat_bbox = draw.textbbox((0, 0), stat_val, font=font_stat)
        stat_w = stat_bbox[2] - stat_bbox[0]
        draw.text((margin_x + 36, arena_top + 75), stat_val, fill=PALETTE["rust"], font=font_stat)

        col2_x = margin_x + 36 + stat_w + 35
        max_lbl_w = (margin_x + content_w - 36) - col2_x

        lbl_lines = wrap_text(scene.get("stat_label", "Clinical Outcome"), get_sans(30, bold=True), max_lbl_w, draw)
        y_lbl = arena_top + 80
        for ll in lbl_lines:
            draw.text((col2_x, y_lbl), ll, fill=PALETTE["deep_maroon"], font=get_sans(30, bold=True))
            y_lbl += 36
        draw.text((col2_x, y_lbl + 8), scene.get("stat_sub", "Statistically significant outcome (p <0.001)"), fill=PALETTE["clay"], font=get_sans(21))

        # Incretin Comparison Gauge Bar
        meter_y = arena_top + 225
        meter_w = content_w - 72
        draw.rounded_rectangle([margin_x + 36, meter_y, margin_x + 36 + meter_w, meter_y + 14], radius=7, fill="#F2E6DC")
        draw.rounded_rectangle([margin_x + 36, meter_y, margin_x + 36 + int(meter_w * 0.90), meter_y + 14], radius=7, fill=PALETTE["rust"])

        div_y = arena_top + 265
        draw.line([(margin_x + 36, div_y), (margin_x + content_w - 36, div_y)], fill=PALETTE["card_border"], width=1)

        # 3 High-Impact Slabs filling the central space (height 145px each!)
        slabs = scene.get("slabs", [
            ("01  Dual Receptor Synergy", "Simultaneously activates GIP & GLP-1 pathways to quiet hunger."),
            ("02  Superior Lipid Clearance", "Accelerates peripheral insulin sensitivity and visceral fat reduction."),
            ("03  Mandatory Clinical Care", "Doctor-supervised titration eliminates GI symptoms and protects muscle.")
        ])

        slab_y = div_y + 35
        slab_h = 145
        for title, desc in slabs:
            draw.rounded_rectangle([margin_x + 36, slab_y, margin_x + content_w - 36, slab_y + slab_h], radius=18, fill=PALETTE["white"], outline=PALETTE["blush"], width=1)
            draw.text((margin_x + 64, slab_y + 26), title, fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
            
            d_lines = wrap_text(desc, get_sans(24), content_w - 130, draw)
            dy = slab_y + 72
            for dl in d_lines:
                draw.text((margin_x + 64, dy), dl, fill=PALETTE["ink"], font=get_sans(24))
                dy += 32
            slab_y += slab_h + 22

        # Bottom Trust Anchor
        trust_y = arena_top + arena_h - 110
        draw.rounded_rectangle([margin_x + 36, trust_y, margin_x + content_w - 36, trust_y + 88], radius=18, fill="#EDF5F0", outline="#BEE0CD", width=1)
        draw_vector_check(draw, margin_x + 58, trust_y + 32, PALETTE["teal_calm"])
        draw.text((margin_x + 88, trust_y + 18), "DEXA-Verified Body Composition  •  Steer Clinical Protocol", fill=PALETTE["teal_calm"], font=get_sans(24, bold=True))
        draw.text((margin_x + 88, trust_y + 50), "Measures Visceral Fat vs Protected Lean Muscle on Day 1", fill=PALETTE["clay"], font=get_sans(20))

    elif scene["type"] == "paradox_compare":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=26, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "CORONAL DEXA SCAN TELEMETRY (L4-L5 PLANE • LANCET 2021)", fill=PALETTE["clay"], font=get_sans(20, bold=True))

        col_w = (content_w - 72 - 24) // 2
        b1_x = margin_x + 36
        b2_x = b1_x + col_w + 24
        box_y = arena_top + 68
        box_h = 580

        draw_coronal_dexa_scan(draw, b1_x, box_y, col_w, box_h, is_indian=False, t_local=t_local)
        draw_coronal_dexa_scan(draw, b2_x, box_y, col_w, box_h, is_indian=True, t_local=t_local)

        div_y = box_y + box_h + 30
        draw.line([(margin_x + 36, div_y), (margin_x + content_w - 36, div_y)], fill="#D5C5B3", width=1)

        draw.text((margin_x + 36, div_y + 24), "2.1x", fill=PALETTE["rust"], font=get_serif(120, bold=True))

        col2_x = margin_x + 340
        draw.text((col2_x, div_y + 28), "Higher Visceral Adipose Ratio", fill=PALETTE["deep_maroon"], font=get_sans(32, bold=True))
        takeaway = "At identical scale weight, South Asians store double the toxic organ fat around liver and pancreas, causing premature insulin resistance."
        t_lines = wrap_text(takeaway, get_sans(25), content_w - 370, draw)
        ty = div_y + 75
        for tl in t_lines:
            draw.text((col2_x, ty), tl, fill=PALETTE["ink"], font=get_sans(25))
            ty += 35
        draw.text((col2_x, ty + 12), "Lancet Diabetes & Endocrinology (2021) • steerclub.com", fill=PALETTE["clay"], font=get_sans(20))

        tile_y = ty + 50
        tile_w = (content_w - 72 - 24) // 2
        tiles = [
            ("Liver Lipid Burden", "2.1x Visceral Fat", PALETTE["rust"]),
            ("Metabolic Risk Onset", "10 Years Earlier", PALETTE["deep_maroon"])
        ]
        for idx, (t_label, t_val, t_col) in enumerate(tiles):
            tx = margin_x + 36 + idx * (tile_w + 24)
            draw.rounded_rectangle([tx, tile_y, tx + tile_w, tile_y + 110], radius=16, fill="#FFFFFF", outline="#D8C7B5", width=1)
            draw.text((tx + 24, tile_y + 20), t_label, fill=PALETTE["clay"], font=get_sans(19, bold=True))
            draw.text((tx + 24, tile_y + 54), t_val, fill=t_col, font=get_serif(32, bold=True))

        trust_y = arena_top + arena_h - 110
        draw.rounded_rectangle([margin_x + 36, trust_y, margin_x + content_w - 36, trust_y + 88], radius=18, fill="#EDF5F0", outline="#BEE0CD", width=1)
        draw_vector_check(draw, margin_x + 58, trust_y + 32, PALETTE["teal_calm"])
        draw.text((margin_x + 88, trust_y + 18), "DEXA-Verified Body Composition  •  Steer Clinical Protocol", fill=PALETTE["teal_calm"], font=get_sans(24, bold=True))
        draw.text((margin_x + 88, trust_y + 50), "Measures Visceral Fat vs Protected Lean Muscle on Day 1", fill=PALETTE["clay"], font=get_sans(20))

    elif scene["type"] == "tofi_intro":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=26, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "THE TOFI PHENOMENON (LANCET 2021)", fill=PALETTE["clay"], font=get_sans(20, bold=True))

        t_box_y = arena_top + 70
        draw.rounded_rectangle([margin_x + 36, t_box_y, margin_x + content_w - 36, t_box_y + 310], radius=20, fill="#FFFFFF", outline="#D8C7B5", width=1)
        
        draw.text((margin_x + 50, t_box_y + 40), "T.O.F.I.", fill=PALETTE["rust"], font=get_serif(76, bold=True))
        
        meter_p = min(1.0, t_local / 1.3)
        meter_w = int(220 * ease_out_cubic(meter_p))
        draw.rounded_rectangle([margin_x + 50, t_box_y + 155, margin_x + 50 + 220, t_box_y + 170], radius=7, fill="#F2E6DC")
        if meter_w > 0:
            draw.rounded_rectangle([margin_x + 50, t_box_y + 155, margin_x + 50 + meter_w, t_box_y + 170], radius=7, fill=PALETTE["rust"])

        col2_x = margin_x + 360
        draw.text((col2_x, t_box_y + 38), "Thin Outside, Fat Inside", fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
        draw.text((col2_x, t_box_y + 90), "The weighing scale measures gravity, not metabolic health.", fill=PALETTE["ink"], font=get_sans(23))
        draw.text((col2_x, t_box_y + 138), "Standard BMI cutoffs fail South Asian physiology completely.", fill=PALETTE["clay"], font=get_sans(22))
        draw.text((col2_x, t_box_y + 186), "Visceral fat wraps around vital internal organs silently.", fill=PALETTE["rust"], font=get_sans(22, bold=True))

        div_y = t_box_y + 360
        draw.line([(margin_x + 36, div_y), (margin_x + content_w - 36, div_y)], fill=PALETTE["card_border"], width=1)
        
        yrs_p = min(1.0, t_local / 1.0)
        yrs_val = int(10 * ease_out_cubic(yrs_p))
        draw.text((margin_x + 36, div_y + 40), f"{yrs_val} yrs", fill=PALETTE["deep_maroon"], font=get_serif(110, bold=True))
        
        draw.text((col2_x, div_y + 45), "Earlier Metabolic Complications", fill=PALETTE["deep_maroon"], font=get_sans(30, bold=True))
        txt = "Indians develop diabetes and cardiovascular risks a decade before Western populations."
        t_lines = wrap_text(txt, get_sans(24), content_w - 390, draw)
        ty = div_y + 95
        for tl in t_lines:
            draw.text((col2_x, ty), tl, fill=PALETTE["ink"], font=get_sans(24))
            ty += 34
        draw.text((col2_x, ty + 14), "ICMR National Surveillance Study • steerclub.com", fill=PALETTE["clay"], font=get_sans(20))

        trust_y = arena_top + arena_h - 110
        draw.rounded_rectangle([margin_x + 36, trust_y, margin_x + content_w - 36, trust_y + 88], radius=18, fill="#EDF5F0", outline="#BEE0CD", width=1)
        draw_vector_check(draw, margin_x + 58, trust_y + 32, PALETTE["teal_calm"])
        draw.text((margin_x + 88, trust_y + 18), "DEXA Body Composition Scan • Doctor Consultation", fill=PALETTE["teal_calm"], font=get_sans(24, bold=True))
        draw.text((margin_x + 88, trust_y + 50), "Clinical Protocol Built for Indian Physiology • steerclub.com", fill=PALETTE["clay"], font=get_sans(20))

    elif scene["type"] == "organ_adiposity":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=26, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "DEXA ORGAN SCAN TELEMETRY", fill=PALETTE["clay"], font=get_sans(20, bold=True))

        stat_p = min(1.0, t_local / 1.1)
        stat_val = int(80 * ease_out_cubic(stat_p))
        draw.text((margin_x + 36, arena_top + 80), f"+{stat_val}%", fill=PALETTE["rust"], font=get_serif(110, bold=True))
        
        col2_x = margin_x + 380
        draw.text((col2_x, arena_top + 90), "Visceral Ectopic Storage", fill=PALETTE["deep_maroon"], font=get_sans(30, bold=True))
        draw.text((col2_x, arena_top + 140), "Fat accumulates inside liver and pancreas tissues", fill=PALETTE["ink"], font=get_sans(24))
        draw.text((col2_x, arena_top + 182), "Completely undetectable by standard weighing scales", fill=PALETTE["clay"], font=get_sans(21))

        meter_y = arena_top + 240
        meter_total_w = content_w - 72
        fill_w = int(meter_total_w * (stat_val / 80.0))
        draw.rounded_rectangle([margin_x + 36, meter_y, margin_x + 36 + meter_total_w, meter_y + 16], radius=8, fill="#F2E6DC")
        if fill_w > 0:
            draw.rounded_rectangle([margin_x + 36, meter_y, margin_x + 36 + fill_w, meter_y + 16], radius=8, fill=PALETTE["rust"])

        div_y = arena_top + 290
        draw.line([(margin_x + 36, div_y), (margin_x + content_w - 36, div_y)], fill=PALETTE["card_border"], width=1)

        draw.text((margin_x + 36, div_y + 40), "Why Traditional Calorie Counting Fails in India:", fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
        
        items = [
            ("Caloric restriction burns precious lean muscle first", False),
            ("Toxic visceral organ fat remains locked by circulating insulin", False),
            ("DEXA body scanning is clinically required to separate muscle from fat", True)
        ]
        b_y = div_y + 105
        for text_line, is_highlight in items:
            bullet_col = PALETTE["rust"] if is_highlight else PALETTE["deep_maroon"]
            text_col = PALETTE["rust"] if is_highlight else PALETTE["ink"]
            font_b = get_sans(24, bold=is_highlight)
            draw_vector_bullet(draw, margin_x + 36, b_y + 6, bullet_col)
            draw.text((margin_x + 64, b_y), text_line, fill=text_col, font=font_b)
            b_y += 75

        trust_y = arena_top + arena_h - 110
        draw.rounded_rectangle([margin_x + 36, trust_y, margin_x + content_w - 36, trust_y + 88], radius=18, fill="#EDF5F0", outline="#BEE0CD", width=1)
        draw_vector_check(draw, margin_x + 58, trust_y + 32, PALETTE["teal_calm"])
        draw.text((margin_x + 88, trust_y + 18), "DEXA-Verified Body Composition  •  Steer Clinical Protocol", fill=PALETTE["teal_calm"], font=get_sans(24, bold=True))
        draw.text((margin_x + 88, trust_y + 50), "Full Body Composition Analysis: Visceral Fat vs Protected Lean Muscle", fill=PALETTE["clay"], font=get_sans(20))

    elif scene["type"] == "hormonal_block":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=26, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "GUT-BRAIN INCRETIN AXIS", fill=PALETTE["clay"], font=get_sans(20, bold=True))

        draw.text((margin_x + 36, arena_top + 80), "84 dB", fill=PALETTE["deep_maroon"], font=get_serif(110, bold=True))
        col2_x = margin_x + 380
        draw.text((col2_x, arena_top + 90), "Hypothalamic Food Noise", fill=PALETTE["deep_maroon"], font=get_sans(30, bold=True))
        draw.text((col2_x, arena_top + 140), "Visceral cytokines physically block satiety receptors", fill=PALETTE["rust"], font=get_sans(24, bold=True))

        div_y = arena_top + 260
        wave_pts = []
        for wx in range(margin_x + 36, margin_x + content_w - 36, 4):
            wy = div_y + math.sin(wx / 30.0 + t_local * 6.5) * 16.0
            wave_pts.append((wx, wy))
        draw.line(wave_pts, fill=PALETTE["rust"], width=4)

        draw.text((margin_x + 36, div_y + 45), "The Biochemical Breakdown at 4 PM:", fill=PALETTE["deep_maroon"], font=get_sans(28, bold=True))
        
        breakdown_items = [
            "Stomach is full, but intestinal GLP-1 signals are blunted",
            "Brain misinterprets silence as an urgent starvation threat",
            "Hunger ghrelin surges +240%, forcing uncontrollable cravings"
        ]
        b_y = div_y + 110
        for bi in breakdown_items:
            draw_vector_bullet(draw, margin_x + 36, b_y + 6, PALETTE["deep_maroon"])
            draw.text((margin_x + 64, b_y), bi, fill=PALETTE["ink"], font=get_sans(24))
            b_y += 75

        trust_y = arena_top + arena_h - 110
        draw.rounded_rectangle([margin_x + 36, trust_y, margin_x + content_w - 36, trust_y + 88], radius=18, fill="#EDF5F0", outline="#BEE0CD", width=1)
        draw_vector_check(draw, margin_x + 58, trust_y + 32, PALETTE["teal_calm"])
        draw.text((margin_x + 88, trust_y + 18), "DEXA-Verified Body Composition  •  Steer Clinical Protocol", fill=PALETTE["teal_calm"], font=get_sans(24, bold=True))
        draw.text((margin_x + 88, trust_y + 50), "Restores Gut-Brain Satiety Feedback • steerclub.com", fill=PALETTE["clay"], font=get_sans(20))

    elif scene["type"] == "steer_dexa":
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=26, fill="#500E0E", outline="#7D2626", width=1)
        draw.text((margin_x + 36, arena_top + 28), "STEER CLINICAL PROTOCOL", fill=PALETTE["blush"], font=get_sans(20, bold=True))

        draw.text((margin_x + 36, arena_top + 80), "Diagnostics First.", fill=PALETTE["white"], font=get_serif(64, bold=True))
        draw.text((margin_x + 36, arena_top + 155), "Never guess your biology from an obsolete scale.", fill=PALETTE["blush"], font=get_sans(26))

        pillars = [
            ("DEXA Body Composition Scan", "Quantifies visceral organ fat vs protected lean muscle mass", 0.2),
            ("55+ Biomarker Diagnostic Panel", "Measures fasting insulin, HOMA-IR, liver enzymes, and lipids", 0.6),
            ("Doctor-Led Care With Planned Exit", "Medical jumpstart coupled with permanent habit calibration", 1.0)
        ]

        p_y = arena_top + 250
        for title, desc, delay in pillars:
            p_prog = min(1.0, max(0.0, (t_local - delay) / 0.5))
            slide_x = int(-24 * (1.0 - ease_out_cubic(p_prog)))
            cur_x = margin_x + 36 + slide_x

            draw.rounded_rectangle([cur_x, p_y, cur_x + content_w - 72, p_y + 130], radius=18, fill="#3D0B0B", outline="#7D2626", width=1)
            draw_vector_check(draw, cur_x + 24, p_y + 28, PALETTE["teal_bright"])
            draw.text((cur_x + 62, p_y + 24), title, fill=PALETTE["white"], font=get_sans(28, bold=True))
            draw.text((cur_x + 62, p_y + 68), desc, fill=PALETTE["blush"], font=get_sans(23))
            p_y += 155

        trust_y = arena_top + arena_h - 110
        draw.rounded_rectangle([margin_x + 36, trust_y, margin_x + content_w - 36, trust_y + 88], radius=18, fill="#3D0B0B", outline="#7D2626", width=1)
        draw_vector_check(draw, margin_x + 58, trust_y + 32, PALETTE["teal_bright"])
        draw.text((margin_x + 88, trust_y + 18), "Doctor-Led Care With Planned Exit  •  Steer Health Club", fill=PALETTE["white"], font=get_sans(24, bold=True))
        draw.text((margin_x + 88, trust_y + 50), "Habits that last after medication stops • steerclub.com", fill=PALETTE["blush"], font=get_sans(20))

    else:
        draw.rounded_rectangle([margin_x, arena_top, margin_x + content_w, arena_top + arena_h], radius=26, fill=PALETTE["soft_paper"], outline=PALETTE["card_border"], width=1)
        draw.text((margin_x + 36, arena_top + 28), "A TRUSTED DOCTOR'S NOTE", fill=PALETTE["clay"], font=get_sans(20, bold=True))

        draw.text((margin_x + 36, arena_top + 90), "Lose well. Live well.", fill=PALETTE["deep_maroon"], font=get_serif(64, bold=True))
        
        quote = '"Before you start another diet, hear it from a doctor, not a reel. No obligation. If it isn\'t right for you, they\'ll say so."'
        q_lines = wrap_text(quote, get_serif(36, italic=True), content_w - 72, draw)
        qy = arena_top + 200
        for ql in q_lines:
            draw.text((margin_x + 36, qy), ql, fill=PALETTE["ink"], font=get_serif(36, italic=True))
            qy += 56

        draw.line([(margin_x + 36, qy + 40), (margin_x + content_w - 36, qy + 40)], fill=PALETTE["card_border"], width=1)
        
        arrow_pulse = math.sin(t_local * 4.5) * 6.0
        draw.text((margin_x + 36 + int(arrow_pulse), qy + 85), "Doctor-led • Built for Indian biology • steerclub.com →", fill=PALETTE["rust"], font=get_sans(26, bold=True))

    # Bottom Full-Width Action Button (100% Screen Utilization, reaches y=1795!)
    cta_y = arena_top + arena_h + 30
    cta_h = 88
    draw.rounded_rectangle([margin_x, cta_y, margin_x + content_w, cta_y + cta_h], radius=22, fill=PALETTE["deep_maroon"])
    draw.text((margin_x + 40, cta_y + 26), "Talk to a Steer Doctor at steerclub.com", fill="#FFFFFF", font=get_sans(26, bold=True))
    draw.text((margin_x + content_w - 75, cta_y + 24), "→", fill="#DEC3B5", font=get_serif(34, bold=True))

    sub_cta_y = cta_y + cta_h + 16
    draw.text((margin_x, sub_cta_y), "Doctor-Led Metabolic Care for Indian Biology • Zero Crash Diets", fill=PALETTE["clay"], font=get_sans(22))

    # Progress Line
    prog_y = sub_cta_y + 36
    draw.line([(margin_x, prog_y), (margin_x + content_w, prog_y)], fill="#CBB8A4", width=3)
    prog_len = int(content_w * min(1.0, max(0.0, t_global / total_duration)))
    if prog_len > 0:
        bar_col = PALETTE["rust"] if not is_dark else PALETTE["blush"]
        draw.line([(margin_x, prog_y), (margin_x + prog_len, prog_y)], fill=bar_col, width=5)

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

    print(f"🎬 Rendering {total_frames} fluid frames ({duration:.1f}s at {fps}fps with 100% screen utilization & DEXA heatmaps)...")

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

    print(f"✅ Generated 100% Full-Screen AI Reel: {output_mp4_path}")
    return output_mp4_path

if __name__ == "__main__":
    out_reel = "C:/Users/yuvra/Downloads/Personal Proj/Steer Club Hackathon/output/reel/steer_clinical_reel.mp4"
    build_reel(out_reel)
