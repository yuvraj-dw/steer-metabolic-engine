import os
import json
import asyncio
import subprocess
import wave
from pipeline.voice_engine import generate_voiceover, load_env_file

load_env_file()

SCRIPT = [
    {
        "id": "l1_hook",
        "text": "Two people. Both 70 kilos. Both normal BMI. So why does one carry diabetic risk?"
    },
    {
        "id": "l2_tofi",
        "text": "The scale is a trap. In India, researchers call it the TOFI phenotype: thin outside, fat inside."
    },
    {
        "id": "l3_visceral",
        "text": "Indian biology stores up to 80% more toxic visceral fat around the liver and pancreas."
    },
    {
        "id": "l4_noise",
        "text": "This hidden organ fat physically blocks satiety receptors, triggering constant food noise."
    },
    {
        "id": "l5_steer",
        "text": "It's biology, not lack of willpower. Steer starts with DEXA scans and 55 biomarkers before any medicine."
    },
    {
        "id": "l6_cta",
        "text": "Stop guessing your metabolic health. Talk to a real doctor at steerclub.com."
    }
]

def build_papercut_voice(narration_dir: str):
    os.makedirs(narration_dir, exist_ok=True)
    voice_dir = os.path.join(narration_dir, "voice", "final_narrator")
    os.makedirs(voice_dir, exist_ok=True)

    SR = 48000
    seg = {}

    print(f"🎙️ Synthesizing {len(SCRIPT)} lines of narration for Papercut Explainer...")

    for item in SCRIPT:
        line_id = item["id"]
        text = item["text"]
        words = text.split()

        mp3_path = os.path.join(voice_dir, f"{line_id}.mp3")
        wav_path = os.path.join(voice_dir, f"{line_id}.wav")

        # Synthesize audio with ElevenLabs Adam voice (or edge-tts fallback)
        asyncio.run(generate_voiceover(text, mp3_path, preferred_voice="adam"))

        # Convert to 48kHz mono 16-bit WAV for Remotion audio mixer
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-i", mp3_path,
            "-ar", str(SR),
            "-ac", "1",
            "-c:a", "pcm_s16le",
            wav_path
        ]
        subprocess.run(cmd, check=True)

        with wave.open(wav_path, "rb") as w:
            dur = w.getnframes() / w.getframerate()

        weights = [len(x) + 2 for x in words]
        total_w = sum(weights)
        t = 0.0
        out_words = []
        body = max(0.1, dur - 0.15)
        for x, wt in zip(words, weights):
            d = body * wt / total_w
            out_words.append({"w": x, "s": round(t, 3), "e": round(t + d, 3)})
            t += d

        rel_wav = f"voice/final_narrator/{line_id}.wav"
        seg[line_id] = {
            "dur": round(dur, 3),
            "file": rel_wav,
            "words": out_words
        }
        print(f"  ✓ {line_id}: {dur:.2f}s ({len(words)} words)")

    timing_js = os.path.join(narration_dir, "timing_narrator.js")
    vo_data = {
        "order": [item["id"] for item in SCRIPT],
        "seg": seg
    }
    with open(timing_js, "w", encoding="utf-8") as f:
        f.write(f"// Generated for Steer Papercut Explainer\nconst VO = {json.dumps(vo_data, indent=1)};\n")

    script_json = os.path.join(narration_dir, "script.json")
    with open(script_json, "w", encoding="utf-8") as f:
        json.dump(SCRIPT, f, indent=1)

    total_dur = sum(s["dur"] for s in seg.values())
    print(f"✅ Generated voiceover and word timing in {narration_dir} (Total: {total_dur:.2f}s)")
    return timing_js

if __name__ == "__main__":
    target = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/papercut/template/narration"
    build_papercut_voice(target)
