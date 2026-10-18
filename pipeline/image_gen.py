"""
Steer AI Image Generation Engine
Integrates Pollinations and Nano-Banana MCP / API engines for high-status clinical visuals.
Formats images strictly for Instagram standards:
  - 4:5 Portrait Carousel: 1080 x 1350 px
  - 1:1 Square Feed Asset: 1080 x 1080 px (or 800 x 800 in-card)
  - 9:16 Vertical Story / Reel: 1080 x 1920 px
"""

import os
import urllib.parse
import subprocess
import json
from typing import Optional, Dict, Any
from PIL import Image

STUDY_PROMPTS: Dict[str, Dict[str, str]] = {
    "LANCET-TOFI-2021": {
        "carousel": (
            "Minimalist tactile layered papercraft art of human abdominal anatomy, showing visceral organ fat "
            "surrounding liver and pancreas, warm oatmeal taupe background (#E4D7C8), Steer rust (#C04E2A) "
            "and deep oxblood accents, clean paper cut-out layers, soft studio shadows, elegant medical editorial design"
        ),
        "reel": (
            "Tactile papercut diorama cut-out of human abdomen showing hidden yellow visceral ectopic fat "
            "wrapped around deep red organs, matte cardstock texture, clean paper edges, studio lighting, beige background"
        ),
    },
    "SURPASS-2-2021": {
        "carousel": (
            "Minimalist tactile layered papercraft illustration of dual incretin receptor signaling GLP-1 and GIP "
            "molecular synergy, interlocking paper cut-out shapes, calm taupe background, calm teal (#235937) and "
            "Steer rust cardstock, studio drop shadows, modern medical editorial style"
        ),
        "reel": (
            "Tactile papercut diorama of dual hormone receptor lock and key mechanism, GLP-1 and GIP molecular synergy, "
            "warm oatmeal cardstock, clean layered paper cut-outs, soft drop shadows"
        ),
    },
    "STEER-MACE-2026": {
        "carousel": (
            "Minimalist tactile layered papercraft of human cardiovascular anatomy, heart and healthy open blood vessels, "
            "arterial decompression, calm oatmeal background (#E4D7C8), warm terracotta and oxblood cut-out cardstock, "
            "elegant medical science aesthetic, soft shadows"
        ),
        "reel": (
            "Tactile papercut diorama cut-out of human heart and branching arterial vessels, clean blood flow, "
            "matte paper layers in terracotta and oxblood, calm taupe backdrop, studio lighting"
        ),
    },
    "STEP-1-EXT-2022": {
        "carousel": (
            "Minimalist tactile layered papercraft of neuro-endocrine hunger hormone balance scales, ghrelin surge and "
            "leptin crash, hypothalamic metabolic set-point, clean paper cut-out layers, calm oatmeal taupe background, "
            "subtle rust and blush cardstock, studio lighting, medical editorial"
        ),
        "reel": (
            "Tactile papercut diorama of balance scale weighing hunger hormones ghrelin and leptin, hypothalamic thermostat, "
            "layered cardstock cut-outs, soft shadows, warm neutral palette"
        ),
    },
    "BMJ-NARAYAN-2021": {
        "carousel": (
            "Minimalist tactile layered papercraft of DEXA body composition scan silhouette showing hidden ectopic visceral "
            "adipose tissue at normal body mass index, clean paper cut-out layers, warm oatmeal background, deep oxblood "
            "and calm teal paper layers, editorial medical journal illustration"
        ),
        "reel": (
            "Tactile papercut diorama of DEXA scan dual silhouette comparison, lean exterior with hidden internal visceral fat, "
            "layered papercraft in oatmeal and oxblood, soft studio lighting"
        ),
    },
}

def get_study_prompt(study_id: str, format_type: str = "carousel") -> str:
    """Resolve tailored aesthetic prompt for a given study ID and format."""
    sid = (study_id or "").upper()
    for key, prompts in STUDY_PROMPTS.items():
        if key in sid or key.split("-")[0] in sid:
            return prompts.get(format_type, prompts["carousel"])
    
    # Clean clinical default
    return (
        "Minimalist tactile layered papercraft medical illustration of metabolic endocrine signaling, "
        "calm oatmeal taupe background (#E4D7C8), Steer rust (#C04E2A) and calm teal accents, "
        "clean paper cut-out layers, studio lighting, editorial medical journal aesthetic"
    )

def download_and_clean_image(url: str, output_path: str, target_w: int, target_h: int, max_retries: int = 4) -> str:
    """
    Downloads image via curl with automated rate-limit retry,
    removes any bottom watermark (cropping bottom 45px),
    and resamples cleanly with Lanczos interpolation.
    """
    abs_out = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)
    temp_path = abs_out + ".raw"

    import re
    import time

    for attempt in range(max_retries):
        res = subprocess.run(
            ["curl", "-s", "-L", "-w", "%{http_code}", "-o", temp_path, url],
            capture_output=True,
            text=True,
            timeout=60
        )
        code = res.stdout.strip()

        if code == "200" and os.path.exists(temp_path) and os.path.getsize(temp_path) > 3000:
            try:
                with Image.open(temp_path) as im:
                    w, h = im.size
                    cropped = im.crop((0, 0, w, max(h - 45, int(h * 0.9))))
                    cleaned = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    cleaned.save(abs_out, format="PNG", quality=95)
                return abs_out
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        wait_sec = 18
        if os.path.exists(temp_path):
            try:
                with open(temp_path, "r", encoding="utf-8") as f:
                    err_json = json.load(f)
                    msg = err_json.get("error", {}).get("message", "")
                    m = re.search(r"Retry after (\d+)s", msg)
                    if m:
                        wait_sec = int(m.group(1)) + 2
            except Exception:
                pass
            if os.path.exists(temp_path):
                os.remove(temp_path)

        if attempt < max_retries - 1:
            print(f"⏳ Pollinations rate limit active. Waiting {wait_sec}s (retry {attempt + 1}/{max_retries})...")
            time.sleep(wait_sec)

    raise RuntimeError(f"Failed to fetch image via curl from {url} after {max_retries} attempts")

def generate_image(
    prompt: str,
    output_path: str,
    width: int = 800,
    height: int = 800,
    seed: Optional[int] = 42,
    force: bool = False
) -> str:
    """
    Generate an image using Pollinations / Nano-Banana with watermark removal and caching.
    """
    abs_out = os.path.abspath(output_path)
    if os.path.exists(abs_out) and not force and os.path.getsize(abs_out) > 5000:
        return abs_out

    encoded = urllib.parse.quote(prompt)
    fetch_w = 768
    fetch_h = 768
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={fetch_w}&height={fetch_h}"
    if seed:
        url += f"&seed={seed}"

    print(f"🎨 Synthesizing clinical visual ({width}x{height}) -> {os.path.basename(abs_out)}")
    return download_and_clean_image(url, abs_out, width, height)

def get_study_slug(study_id: str) -> str:
    sid = (study_id or "").lower()
    if "tofi" in sid or "lancet" in sid:
        return "lancet_tofi_70kg"
    elif "surpass" in sid or "tirzepatide" in sid:
        return "surpass2_tirzepatide"
    elif "mace" in sid or "cv" in sid or "cardio" in sid:
        return "steer_mace_cv"
    elif "step" in sid or "rebound" in sid:
        return "step1_extension_rebound"
    elif "narayan" in sid:
        return "bmj_narayan_tofi"
    return sid.replace("-", "_")

def generate_all_study_visuals(study_id: str, base_output_dir: str = "output/posts", force: bool = False) -> Dict[str, str]:
    """
    Generates study-tailored visuals:
      - card_graphic: 800x800 square for Carousel Slide 2
      - reel_graphic: 800x800 square for Remotion Diorama
      - instagram_hero: 1080x1350 (4:5 portrait) standalone carousel hero
    """
    slug = get_study_slug(study_id)
    vis_dir = os.path.join(base_output_dir, slug, "visuals")
    os.makedirs(vis_dir, exist_ok=True)

    c_prompt = get_study_prompt(study_id, "carousel")
    r_prompt = get_study_prompt(study_id, "reel")

    # 1. Carousel Card Graphic (800x800)
    card_path = os.path.join(vis_dir, "clinical_illustration_card.png")
    generate_image(c_prompt, card_path, 800, 800, seed=101, force=force)

    # 2. Instagram 4:5 Portrait Feed Hero (1080x1350)
    hero_path = os.path.join(vis_dir, "instagram_hero_4x5.png")
    generate_image(c_prompt + ", full-bleed vertical editorial framing, high resolution", hero_path, 1080, 1350, seed=202, force=force)

    # 3. Reel Diorama Graphic (800x800)
    reel_path = os.path.join(vis_dir, "reel_diorama_graphic.png")
    generate_image(r_prompt, reel_path, 800, 800, seed=303, force=force)

    # Also copy reel graphic to Remotion public dir so video renders with it!
    remotion_public = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/papercut/template/public/assets"
    if os.path.exists(remotion_public):
        target_reel_asset = os.path.join(remotion_public, f"graphic_{slug}.png")
        try:
            with open(reel_path, "rb") as rf, open(target_reel_asset, "wb") as wf:
                wf.write(rf.read())
        except Exception:
            pass

    return {
        "card_graphic": card_path,
        "instagram_hero": hero_path,
        "reel_graphic": reel_path
    }

if __name__ == "__main__":
    print("Testing generate_all_study_visuals for LANCET-TOFI-2021...")
    res = generate_all_study_visuals("LANCET-TOFI-2021", force=True)
    print("Done:", res)
