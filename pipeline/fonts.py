import os
import sys
from PIL import ImageFont

# Candidate system font directories across Windows, macOS, and Linux
FONT_DIRS = [
    # Windows
    "C:/Windows/Fonts",
    os.path.expandvars("%WINDIR%/Fonts"),
    # macOS
    "/System/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "/Library/Fonts",
    os.path.expanduser("~/Library/Fonts"),
    # Linux / Debian / Ubuntu / Alpine / Arch
    "/usr/share/fonts",
    "/usr/share/fonts/truetype",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/opentype",
    "/usr/local/share/fonts",
    os.path.expanduser("~/.fonts"),
    os.path.expanduser("~/.local/share/fonts"),
    # Local fallback directory inside the repo
    os.path.join(os.path.dirname(__file__), "fonts"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")
]

SERIF_NAMES = {
    "regular": ["georgia.ttf", "DejaVuSerif.ttf", "LiberationSerif-Regular.ttf", "times.ttf", "Times.ttc", "Sitka.ttc"],
    "bold": ["georgiab.ttf", "DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf", "timesbd.ttf"],
    "italic": ["georgiai.ttf", "DejaVuSerif-Italic.ttf", "LiberationSerif-Italic.ttf", "timesi.ttf"],
    "bold_italic": ["georgiaz.ttf", "DejaVuSerif-BoldItalic.ttf", "LiberationSerif-BoldItalic.ttf", "timesbi.ttf"]
}

SANS_NAMES = {
    "regular": ["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Helvetica.ttc", "segoeui.ttf", "SF-Pro.ttf"],
    "bold": ["arialbd.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "segoeuib.ttf", "Helvetica-Bold.ttf"],
    "italic": ["ariali.ttf", "DejaVuSans-Oblique.ttf", "LiberationSans-Italic.ttf", "segoeuii.ttf"],
    "bold_italic": ["arialbi.ttf", "DejaVuSans-BoldOblique.ttf", "LiberationSans-BoldItalic.ttf", "segoeuiz.ttf"]
}

_FONT_CACHE = {}

def find_font_file(name_list):
    cache_key = tuple(name_list)
    if cache_key in _FONT_CACHE:
        return _FONT_CACHE[cache_key]

    for d in FONT_DIRS:
        if not d or not os.path.exists(d):
            continue
        for name in name_list:
            fp = os.path.join(d, name)
            if os.path.exists(fp):
                _FONT_CACHE[cache_key] = fp
                return fp
            # Case-insensitive search on Linux
            if os.path.isdir(d):
                try:
                    for f in os.listdir(d):
                        if f.lower() == name.lower():
                            full = os.path.join(d, f)
                            _FONT_CACHE[cache_key] = full
                            return full
                except:
                    pass
    return None

def get_cross_platform_serif(size, bold=False, italic=False):
    if bold and italic:
        names = SERIF_NAMES["bold_italic"] + SERIF_NAMES["bold"] + SERIF_NAMES["regular"]
    elif italic:
        names = SERIF_NAMES["italic"] + SERIF_NAMES["regular"]
    elif bold:
        names = SERIF_NAMES["bold"] + SERIF_NAMES["regular"]
    else:
        names = SERIF_NAMES["regular"]

    font_path = find_font_file(names)
    if font_path:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass

    try:
        return ImageFont.load_default(size=size)
    except:
        return ImageFont.load_default()

def get_cross_platform_sans(size, bold=False, italic=False):
    if bold and italic:
        names = SANS_NAMES["bold_italic"] + SANS_NAMES["bold"] + SANS_NAMES["regular"]
    elif italic:
        names = SANS_NAMES["italic"] + SANS_NAMES["regular"]
    elif bold:
        names = SANS_NAMES["bold"] + SANS_NAMES["regular"]
    else:
        names = SANS_NAMES["regular"]

    font_path = find_font_file(names)
    if font_path:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass

    try:
        return ImageFont.load_default(size=size)
    except:
        return ImageFont.load_default()
