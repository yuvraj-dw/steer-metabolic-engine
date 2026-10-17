import os
import sys
import shutil
import subprocess

PAPERCUT_DIR = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/papercut/template"
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def build_papercut_video(output_mp4: str = "output/reel/steer_papercut_explainer.mp4") -> str:
    """
    Renders the Steer Clinical Papercut Explainer video using Remotion,
    tactile paper dioramas, Web Audio sound effects, and ElevenLabs neural narration.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)
    abs_out = os.path.abspath(output_mp4)

    print("🎨 Preparing Steer Papercut Explainer generation...")

    # 1. Synthesize audio lines & word timings
    print("🎙️ Step 1/4: Synthesizing ElevenLabs neural narration & word-cue timestamps...")
    sys.path.insert(0, os.path.abspath("."))
    from pipeline.generate_papercut_voice import build_papercut_voice
    narration_dir = os.path.join(PAPERCUT_DIR, "narration")
    build_papercut_voice(narration_dir)

    # 2. Build voiceover WAV, plan.json, and captions.json
    print("📦 Step 2/4: Building scene cut plan & word-tag captions...")
    build_vo_tool = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/tools/build_vo.py"
    subprocess.run([sys.executable, build_vo_tool], cwd=PAPERCUT_DIR, check=True)

    # 3. Generate SFX cues & render procedural audio bed
    print("🎵 Step 3/4: Synthesizing marimba music bed & tactile paper sound effects in headless Chrome...")
    cues_tool = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/tools/cues.py"
    subprocess.run([sys.executable, cues_tool], cwd=PAPERCUT_DIR, check=True)

    render_audio_tool = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/audio/render.mjs"
    env = os.environ.copy()
    env["CHROME_PATH"] = CHROME_PATH
    subprocess.run(["node", render_audio_tool], cwd=PAPERCUT_DIR, env=env, check=True)

    # 4. Render Remotion Composition to MP4
    print("🎬 Step 4/4: Rendering 1,312 frames with Remotion headless browser...")
    cmd = [
        "bun", "x", "remotion", "render",
        "SteerPapercut",
        abs_out,
        "--gl=angle"
    ]
    subprocess.run(cmd, cwd=PAPERCUT_DIR, env=env, check=True)

    print(f"✅ Generated Steer Papercut Explainer: {abs_out}")
    return abs_out

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/reel/steer_papercut_explainer.mp4"
    build_papercut_video(out)
