import os
import asyncio
import edge_tts
from typing import Dict, Any

# Clinical claim translations in natural, culturally resonant conversational Hinglish
HINGLISH_CLINICAL_TRANSLATIONS = {
    "willpower_myth": {
        "headline": "Yeh weak willpower nahi, basic biology hai.",
        "subhead": "4 baje ka chai aur biscuit craving aapka character flaw nahi hai.",
        "script": """Do log. Dono ka weight 70 kilos. Dono ka BMI normal.
Phir bhi ek ko diabetes aur metabolic crash ka severe risk kyun hai?
Kyunki India mein weighing scale sach nahi batata.
Lancet researchers ise kehte hain TOFI phenotype: Thin on the Outside, Fat on the Inside.
Indian bodies normal weight par bhi liver aur pancreas ke paas 80% zyada visceral fat store karti hain.
Yeh chhipa hua fat aapke gut ke natural satiety hormones ko block kar deta hai.
Pet mein khana hai, par brain ko lagta hai ki aap bhookhe hain.
Aap mein discipline ki kami nahi hai, aap unseen biology se lad rahe hain.
Steer shuru karta hai DEXA body scans aur 55 blood biomarkers ke saath.
Health ka guess lagana band kijiye. Doctor se poochiye at steerclub.com."""
    },
    "rebound_trap": {
        "headline": "Dawaii band karne ke baad 2/3 weight wapas kyun aata hai?",
        "subhead": "Bina exit plan ke weight loss sirf aadhi science hai.",
        "takeaway": "Hypothalamic set-point ko recalibrate kiye bina body famine defense trigger karti hai. Steer doctor-led off-ramp banata hai taaki results permanently sustain ho sakein."
    }
}

async def generate_hinglish_voiceover(output_path: str, voice: str = "hi-IN-MadhurNeural") -> str:
    """Generate high-quality conversational Hinglish neural voiceover."""
    script = HINGLISH_CLINICAL_TRANSLATIONS["willpower_myth"]["script"]
    tts = edge_tts.Communicate(script, voice, rate="+2%")
    await tts.save(output_path)
    print(f"Hinglish neural voiceover generated: {output_path}")
    return output_path

def get_hinglish_social_caption() -> str:
    return """Do log. Dono 70 kilos. Dono ka normal BMI.

Phir bhi ek ka metabolic health diabetic jaisa kyun hai?

Kyunki India mein bathroom scale pura sach nahi batata.

Lancet research ise kehti hai TOFI phenotype: Thin on the Outside, Fat on the Inside.

Indian genetics mein organs ke paas 80% zyada visceral fat store hota hai, even normal scale weight par. 

Yeh chhipa hua fat aapke satiety signals ko block kar deta hai—jisse din bhar food noise aur 4 baje ka sugar crash trigger hota hai.

Aapki willpower weak nahi hai. Aap hidden biology se fight kar rahe hain.

Isi liye Steer sirf scale par rely nahi karta. Har member ka safar shuru hota hai DEXA body scan aur 55+ biomarkers ke saath.

Pehle doctor se suniye, reels se nahi.

Visit steerclub.com.

#SteerClub #MetabolicHealthIndia #TOFI #ThinFat #GLP1India #DoctorLed #HealthInHinglish #EvidenceBasedCare"""

if __name__ == "__main__":
    out_audio = "C:/Users/yuvra/Downloads/Personal Proj/Steer Club Hackathon/output/reel/voiceover_hinglish.mp3"
    asyncio.run(generate_hinglish_voiceover(out_audio))
