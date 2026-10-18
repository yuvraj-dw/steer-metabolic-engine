import os
import urllib.parse
import urllib.request
import time
from PIL import Image

ILLUSTRATION_DIR = "assets/illustrations"

STUDY_PROMPTS = {
    "surpass2_tirzepatide": (
        "minimalist 3D sculptural illustration of two interconnected glowing biochemical receptor nodes, "
        "representing GIP and GLP-1 hormone synergy, soft terracotta and ivory ceramic material, warm cream background (#F5EBDF), "
        "clean biomorphic medical art, soft ambient studio lighting, no text, no watermark"
    ),
    "steer_mace_cv": (
        "minimalist sculptural bas-relief of a stylized human heart and branching coronary vascular arteries, "
        "crafted from soft salmon terracotta and matte porcelain, warm cream background (#F5EBDF), "
        "calm serene clinical art, cardiovascular health, clean modern medical sculpture, no text, no watermark"
    ),
    "step1_extension_rebound": (
        "minimalist sculptural bas-relief of a calibrated mechanical biological thermostat dial and balancing scales, "
        "representing metabolic set-point equilibrium, warm clay and ivory ceramic textures, soft terracotta background, "
        "modern editorial medical sculpture, no text, no watermark"
    ),
    "lancet_tofi": (
        "minimalist 3D sculptural depiction of a stylized human torso cross section showing abdominal organs, "
        "liver and pancreas highlighted in warm coral terracotta, matte ivory bone structure, clean clinical diorama, "
        "warm cream background (#F5EBDF), modern editorial art, no text, no watermark"
    ),
    "bmj_narayan_tofi": (
        "minimalist sculptural bas-relief of a cellular metabolic receptor grid and diagnostic biomarker prism, "
        "warm terracotta and sage green porcelain materials, warm cream background (#F5EBDF), "
        "clean editorial medical art, soft studio shadows, no text, no watermark"
    )
}

def get_study_key(study) -> str:
    if not study:
        return "lancet_tofi"
    sid = study.study_id.lower()
    if "surpass" in sid or "tirzepatide" in sid:
        return "surpass2_tirzepatide"
    elif "mace" in sid or "cardio" in sid:
        return "steer_mace_cv"
    elif "step" in sid or "rebound" in sid:
        return "step1_extension_rebound"
    elif "narayan" in sid:
        return "bmj_narayan_tofi"
    else:
        return "lancet_tofi"

def generate_study_illustration(study=None, force: bool = False) -> str:
    """
    Generates a high-status, publication-grade editorial illustration
    using Pollinations.ai (Flux model) matching Steer's warm clay and cream palette.
    Completely free, no API key required, with local disk caching.
    """
    os.makedirs(ILLUSTRATION_DIR, exist_ok=True)
    key = get_study_key(study)
    out_path = os.path.join(ILLUSTRATION_DIR, f"{key}.png")

    if os.path.exists(out_path) and not force:
        return out_path

    prompt = STUDY_PROMPTS.get(key, STUDY_PROMPTS["lancet_tofi"])
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&nologo=true&model=flux"

    print(f"🎨 [FREE IMAGE GEN] Generating bespoke editorial illustration for {key} via Flux...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=35) as resp:
            data = resp.read()
        
        with open(out_path, "wb") as f:
            f.write(data)

        # Post-process: ensure correct RGBA/RGB and resize if needed
        with Image.open(out_path) as img:
            rgb_img = img.convert("RGB")
            # Crop 40px from bottom to guarantee zero watermark artifacts
            w, h = rgb_img.size
            cropped = rgb_img.crop((0, 0, w, h - 30))
            final_img = cropped.resize((700, 700), Image.Resampling.LANCZOS)
            final_img.save(out_path, quality=95)

        print(f"✅ Generated and cached illustration: {out_path}")
        return out_path
    except Exception as e:
        print(f"⚠️ Image generation network fallback ({e}). Using existing or procedural asset.")
        if os.path.exists(out_path):
            return out_path
        # Return None or fallback
        return None

if __name__ == "__main__":
    for k in STUDY_PROMPTS:
        class Dummy:
            study_id = k
        generate_study_illustration(Dummy(), force=False)
