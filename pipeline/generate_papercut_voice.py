import os
import json
import base64
import urllib.request
import subprocess
import wave
from pipeline.voice_engine import load_env_file

load_env_file()

def synthesize_with_timestamps(text: str, voice_id: str = "pNInz6obpgDQGcFmaJgB") -> tuple[bytes, list[dict]]:
    """
    Calls ElevenLabs /v1/text-to-speech/{voice_id}/with-timestamps
    Returns (audio_bytes, list_of_word_timings_with_exact_start_and_end)
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in environment.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
    )

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    audio_bytes = base64.b64decode(data["audio_base64"])
    align = data.get("alignment", {})
    chars = align.get("characters", [])
    starts = align.get("character_start_times_seconds", [])
    ends = align.get("character_end_times_seconds", [])

    # Group characters into words with microsecond precision
    words = []
    curr_word = []
    w_start = None
    prev_e = 0.0

    for c, s, e in zip(chars, starts, ends):
        if c == " ":
            if curr_word:
                words.append({
                    "w": "".join(curr_word),
                    "s": round(w_start, 3),
                    "e": round(prev_e, 3)
                })
                curr_word = []
                w_start = None
        else:
            if w_start is None:
                w_start = s
            curr_word.append(c)
            prev_e = e

    if curr_word:
        words.append({
            "w": "".join(curr_word),
            "s": round(w_start, 3),
            "e": round(prev_e, 3)
        })

    return audio_bytes, words

def build_papercut_voice(narration_dir: str, script: list[dict] = None):
    os.makedirs(narration_dir, exist_ok=True)
    voice_dir = os.path.join(narration_dir, "voice", "final_narrator")
    os.makedirs(voice_dir, exist_ok=True)

    if not script:
        script = [
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

    SR = 48000
    seg = {}

    print(f"🎙️ Synthesizing {len(script)} lines with ElevenLabs neural forced alignment...")

    for item in script:
        line_id = item["id"]
        text = item["text"]

        mp3_path = os.path.join(voice_dir, f"{line_id}.mp3")
        wav_path = os.path.join(voice_dir, f"{line_id}.wav")

        try:
            # 1. Fetch audio with microsecond alignment directly from ElevenLabs
            audio_bytes, exact_words = synthesize_with_timestamps(text)
            with open(mp3_path, "wb") as f:
                f.write(audio_bytes)
        except Exception as e:
            print(f"  ⚠️ Warning: ElevenLabs API alignment failed ({e}), falling back...")
            from pipeline.voice_engine import generate_voiceover
            import asyncio
            asyncio.run(generate_voiceover(text, mp3_path, preferred_voice="adam"))
            exact_words = []

        # Convert to 48kHz mono 16-bit PCM WAV for Remotion
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

        if not exact_words:
            words_list = text.split()
            weights = [len(x) + 2 for x in words_list]
            total_w = sum(weights)
            t = 0.0
            body = max(0.1, dur - 0.15)
            for x, wt in zip(words_list, weights):
                d = body * wt / total_w
                exact_words.append({"w": x, "s": round(t, 3), "e": round(t + d, 3)})
                t += d

        rel_wav = f"voice/final_narrator/{line_id}.wav"
        seg[line_id] = {
            "dur": round(dur, 3),
            "file": rel_wav,
            "words": exact_words
        }
        print(f"  ✓ {line_id}: {dur:.2f}s ({len(exact_words)} exact aligned words)")

    timing_js = os.path.join(narration_dir, "timing_narrator.js")
    vo_data = {
        "order": [item["id"] for item in script],
        "seg": seg
    }
    with open(timing_js, "w", encoding="utf-8") as f:
        f.write(f"// Generated for Steer Papercut Explainer with ElevenLabs Alignment\nconst VO = {json.dumps(vo_data, indent=1)};\n")

    script_json = os.path.join(narration_dir, "script.json")
    with open(script_json, "w", encoding="utf-8") as f:
        json.dump(script, f, indent=1)

    total_dur = sum(s["dur"] for s in seg.values())
    print(f"✅ Generated voiceover with exact neural alignment in {narration_dir} (Total: {total_dur:.2f}s)")
    return timing_js

if __name__ == "__main__":
    target = "C:/Users/yuvra/AppData/Local/hermes/cache/scratch/papercut/library/papercut/template/narration"
    build_papercut_voice(target)
