import os
import json
import asyncio
import urllib.request
import urllib.error
import edge_tts
from typing import Optional

# Curated ElevenLabs high-realism voice library
ELEVENLABS_VOICES = {
    "adam": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "description": "Deep, calm, narrative authority (great for medical/health explainers)"
    },
    "george": {
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",
        "description": "Warm British documentary narrator, intelligent and captivating"
    },
    "rachel": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
        "description": "Calm, empathetic, natural conversational female voice"
    },
    "antoni": {
        "voice_id": "ErXwobaYiN019PkySvjV",
        "description": "Energetic, clear storytelling voice"
    }
}

def load_env_file():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ:
                        os.environ[k.strip()] = v.strip().strip("'\"")

load_env_file()

async def generate_voiceover(
    script: str, 
    output_path: str, 
    preferred_voice: str = "adam",
    api_key: Optional[str] = None
) -> str:
    """
    Generate voiceover. If ELEVENLABS_API_KEY is available, uses ElevenLabs' 
    ultra-human neural synthesis (eleven_multilingual_v2).
    Otherwise, gracefully falls back to Microsoft Edge Neural expressive voice.
    """
    eleven_key = api_key or os.environ.get("ELEVENLABS_API_KEY")

    if eleven_key:
        voice_cfg = ELEVENLABS_VOICES.get(preferred_voice.lower(), ELEVENLABS_VOICES["adam"])
        voice_id = voice_cfg["voice_id"]
        print(f"🎙️ Using ElevenLabs API (Voice: {preferred_voice.title()}, Model: eleven_multilingual_v2)...")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": eleven_key
        }
        payload = {
            "text": script,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.85,
                "style": 0.15,
                "use_speaker_boost": True
            }
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req) as resp:
                audio_bytes = resp.read()
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            print(f"✅ ElevenLabs audio generated: {output_path}")
            return output_path
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8', errors='ignore')
            print(f"⚠️ ElevenLabs API error ({e.code}): {err_msg}. Falling back to Edge-TTS neural engine...")

    # Fallback to high-quality Microsoft Edge Neural Expressive
    print("🎙️ Using Edge-TTS Expressive Neural Engine (en-IN-PrabhatNeural / NeerjaExpressive)...")
    # PrabhatNeural sounds like a grounded, credible doctor; NeerjaExpressive is conversational
    voice_name = "en-IN-PrabhatNeural"
    tts = edge_tts.Communicate(script, voice_name, rate="+2%")
    await tts.save(output_path)
    print(f"✅ Neural voiceover generated: {output_path}")
    return output_path

if __name__ == "__main__":
    test_script = "Two people. Both 70 kilos. Both normal BMI. So why does one have the metabolic risk of a diabetic?"
    asyncio.run(generate_voiceover(test_script, "output/reel/test_voice_engine.mp3"))
