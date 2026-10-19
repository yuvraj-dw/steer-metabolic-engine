import math
from PIL import Image, ImageDraw

def get_bezier_curve(p0, p1, p2, p3, steps=40):
    curve = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = (u**3)*p0[0] + 3*(u**2)*t*p1[0] + 3*u*(t**2)*p2[0] + (t**3)*p3[0]
        y = (u**3)*p0[1] + 3*(u**2)*t*p1[1] + 3*u*(t**2)*p2[1] + (t**3)*p3[1]
        curve.append((x, y))
    return curve

def draw_cellular_pattern(draw, cx, cy, radius=80, color="#241E1C"):
    """
    Renders minimalist biological line art:
    Concentric rings, overlapping cell membranes, floating receptor droplets.
    """
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=color, width=3)
    draw.ellipse([cx - radius * 0.65, cy - radius * 0.75, cx + radius * 0.75, cy + radius * 0.65], outline=color, width=2)
    draw.ellipse([cx - radius * 0.35, cy - radius * 0.35, cx + radius * 0.35, cy + radius * 0.35], outline=color, width=2)
    
    satellites = [
        (cx - radius * 1.15, cy - radius * 0.4, 6),
        (cx + radius * 1.1, cy - radius * 0.6, 5),
        (cx + radius * 0.9, cy + radius * 0.85, 8),
        (cx - radius * 0.8, cy + radius * 1.05, 5),
        (cx - radius * 0.2, cy - radius * 1.25, 7),
        (cx + radius * 0.4, cy + radius * 1.2, 6)
    ]
    for sx, sy, sr in satellites:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=color)
        
    draw.arc([cx - radius * 1.35, cy - radius * 1.35, cx + radius * 1.35, cy + radius * 1.35], start=30, end=90, fill=color, width=2)
    draw.arc([cx - radius * 1.35, cy - radius * 1.35, cx + radius * 1.35, cy + radius * 1.35], start=210, end=270, fill=color, width=2)

def draw_stethoscope(draw, ox, oy, scale=1.0, color="#241E1C", stroke_w=3):
    """
    Renders refined monoline stethoscope with perfectly tensioned, smooth parabolic loop.
    """
    left_ear = (ox - 42 * scale, oy)
    right_ear = (ox + 42 * scale, oy)
    
    draw.ellipse([left_ear[0] - 6 * scale, left_ear[1] - 4 * scale, left_ear[0] + 6 * scale, left_ear[1] + 4 * scale], fill=color)
    draw.ellipse([right_ear[0] - 6 * scale, right_ear[1] - 4 * scale, right_ear[0] + 6 * scale, right_ear[1] + 4 * scale], fill=color)
    
    y_joint = (ox, oy + 85 * scale)
    
    # Binaural arches
    left_pts = [left_ear, (ox - 50 * scale, oy + 30 * scale), (ox - 30 * scale, oy + 65 * scale), y_joint]
    right_pts = [right_ear, (ox + 50 * scale, oy + 30 * scale), (ox + 30 * scale, oy + 65 * scale), y_joint]
    
    draw.line(get_bezier_curve(left_pts[0], left_pts[1], left_pts[2], left_pts[3]), fill=color, width=int(stroke_w * scale))
    draw.line(get_bezier_curve(right_pts[0], right_pts[1], right_pts[2], right_pts[3]), fill=color, width=int(stroke_w * scale))
    
    # Perfectly tensioned, smooth continuous loop
    c1 = get_bezier_curve(y_joint, (ox, oy + 170 * scale), (ox - 140 * scale, oy + 250 * scale), (ox - 90 * scale, oy + 360 * scale))
    c2 = get_bezier_curve((ox - 90 * scale, oy + 360 * scale), (ox - 30 * scale, oy + 460 * scale), (ox + 160 * scale, oy + 440 * scale), (ox + 175 * scale, oy + 280 * scale))
    c3 = get_bezier_curve((ox + 175 * scale, oy + 280 * scale), (ox + 180 * scale, oy + 170 * scale), (ox + 210 * scale, oy + 120 * scale), (ox + 260 * scale, oy + 140 * scale))
    
    draw.line(c1, fill=color, width=int(stroke_w * scale))
    draw.line(c2, fill=color, width=int(stroke_w * scale))
    draw.line(c3, fill=color, width=int(stroke_w * scale))
    
    # Chest piece (bell and diaphragm)
    cx, cy = (ox + 260 * scale, oy + 140 * scale)
    r_outer = 32 * scale
    r_inner = 22 * scale
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=color, width=int(stroke_w * scale))
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], outline=color, width=int(max(1, stroke_w - 1) * scale))
    draw.ellipse([cx - 5 * scale, cy - 5 * scale, cx + 5 * scale, cy + 5 * scale], fill=color)

def draw_caring_hands(draw, ox, oy, scale=1.0, color="#241E1C", stroke_w=3):
    """
    Renders refined, anatomically graceful continuous-line illustration of two hands reaching out.
    """
    w = int(stroke_w * scale)
    
    # Patient Hand (Lower left, palm open upwards in need of support)
    p_wrist_top = (ox - 160 * scale, oy + 80 * scale)
    p_wrist_bot = (ox - 170 * scale, oy + 125 * scale)
    
    # Wrist contours
    draw.line(get_bezier_curve(p_wrist_top, (ox - 120 * scale, oy + 65 * scale), (ox - 90 * scale, oy + 60 * scale), (ox - 60 * scale, oy + 55 * scale)), fill=color, width=w)
    draw.line(get_bezier_curve(p_wrist_bot, (ox - 130 * scale, oy + 115 * scale), (ox - 90 * scale, oy + 105 * scale), (ox - 50 * scale, oy + 95 * scale)), fill=color, width=w)
    
    # Thumb arching out gracefully
    thumb_tip = (ox - 10 * scale, oy + 25 * scale)
    draw.line(get_bezier_curve((ox - 60 * scale, oy + 55 * scale), (ox - 45 * scale, oy + 40 * scale), (ox - 30 * scale, oy + 28 * scale), thumb_tip), fill=color, width=w)
    draw.line(get_bezier_curve(thumb_tip, (ox - 5 * scale, oy + 32 * scale), (ox - 15 * scale, oy + 52 * scale), (ox - 25 * scale, oy + 62 * scale)), fill=color, width=w)
    
    # Index finger reaching forward
    index_tip = (ox + 45 * scale, oy + 32 * scale)
    draw.line(get_bezier_curve((ox - 25 * scale, oy + 62 * scale), (ox - 5 * scale, oy + 45 * scale), (ox + 20 * scale, oy + 32 * scale), index_tip), fill=color, width=w)
    draw.line(get_bezier_curve(index_tip, (ox + 48 * scale, oy + 42 * scale), (ox + 25 * scale, oy + 52 * scale), (ox + 10 * scale, oy + 58 * scale)), fill=color, width=w)
    
    # Middle & ring finger tips extending
    mid_tip = (ox + 50 * scale, oy + 54 * scale)
    draw.line(get_bezier_curve((ox + 10 * scale, oy + 58 * scale), (ox + 28 * scale, oy + 50 * scale), (ox + 42 * scale, oy + 50 * scale), mid_tip), fill=color, width=w)
    draw.line(get_bezier_curve(mid_tip, (ox + 50 * scale, oy + 64 * scale), (ox + 25 * scale, oy + 72 * scale), (ox + 5 * scale, oy + 75 * scale)), fill=color, width=w)
    
    # Pinky and bottom of palm
    draw.line(get_bezier_curve((ox + 5 * scale, oy + 75 * scale), (ox + 20 * scale, oy + 76 * scale), (ox + 35 * scale, oy + 78 * scale), (ox + 35 * scale, oy + 86 * scale)), fill=color, width=w)
    draw.line(get_bezier_curve((ox + 35 * scale, oy + 86 * scale), (ox + 15 * scale, oy + 90 * scale), (ox - 10 * scale, oy + 94 * scale), (ox - 50 * scale, oy + 95 * scale)), fill=color, width=w)

    # Doctor Hand (Upper right, reaching downward with reassurance & care)
    dx, dy = ox + 40 * scale, oy - 40 * scale
    
    # Arm & wrist entering from upper right
    d_arm_top = (dx + 160 * scale, dy - 50 * scale)
    d_arm_bot = (dx + 180 * scale, dy - 10 * scale)
    
    draw.line(get_bezier_curve(d_arm_top, (dx + 120 * scale, dy - 35 * scale), (dx + 80 * scale, dy - 20 * scale), (dx + 40 * scale, dy - 5 * scale)), fill=color, width=w)
    draw.line(get_bezier_curve(d_arm_bot, (dx + 130 * scale, dy + 15 * scale), (dx + 90 * scale, dy + 25 * scale), (dx + 50 * scale, dy + 30 * scale)), fill=color, width=w)
    
    # Downward sheltering thumb
    d_thumb_tip = (dx + 10 * scale, dy + 28 * scale)
    draw.line(get_bezier_curve((dx + 50 * scale, dy + 30 * scale), (dx + 35 * scale, dy + 32 * scale), (dx + 20 * scale, dy + 32 * scale), d_thumb_tip), fill=color, width=w)
    draw.line(get_bezier_curve(d_thumb_tip, (dx + 8 * scale, dy + 18 * scale), (dx + 20 * scale, dy + 10 * scale), (dx + 30 * scale, dy + 5 * scale)), fill=color, width=w)
    
    # Reassuring index finger pointing down towards patient's hand
    d_index_tip = (dx - 15 * scale, dy + 15 * scale)
    draw.line(get_bezier_curve((dx + 40 * scale, dy - 5 * scale), (dx + 20 * scale, dy - 2 * scale), (dx + 2 * scale, dy + 5 * scale), d_index_tip), fill=color, width=w)
    draw.line(get_bezier_curve(d_index_tip, (dx - 18 * scale, dy + 25 * scale), (dx - 5 * scale, dy + 28 * scale), (dx + 12 * scale, dy + 22 * scale)), fill=color, width=w)
    
    # Second protective finger
    d_mid_tip = (dx - 10 * scale, dy + 35 * scale)
    draw.line(get_bezier_curve((dx + 12 * scale, dy + 22 * scale), (dx + 2 * scale, dy + 30 * scale), (dx - 5 * scale, dy + 32 * scale), d_mid_tip), fill=color, width=w)
    draw.line(get_bezier_curve(d_mid_tip, (dx - 8 * scale, dy + 42 * scale), (dx + 8 * scale, dy + 40 * scale), (dx + 20 * scale, dy + 35 * scale)), fill=color, width=w)

def draw_cardiac_monitor(draw, ox, oy, scale=1.0, color="#FAF7F2", stroke_w=2):
    """
    Renders clean desktop cardiac monitor with ECG pulse waveform (monoline style).
    """
    w = 200 * scale
    h = 140 * scale
    draw.rounded_rectangle([ox - w/2, oy - h/2, ox + w/2, oy + h/2], radius=int(14*scale), outline=color, width=int(stroke_w * scale))
    draw.line([(ox, oy + h/2), (ox, oy + h/2 + 25*scale)], fill=color, width=int(stroke_w * scale))
    draw.line([(ox - 35*scale, oy + h/2 + 25*scale), (ox + 35*scale, oy + h/2 + 25*scale)], fill=color, width=int(stroke_w * scale))
    
    ecg_y = oy
    start_x = ox - w/2 + 20*scale
    end_x = ox + w/2 - 20*scale
    
    ecg_pts = [
        (start_x, ecg_y),
        (start_x + 30*scale, ecg_y),
        (start_x + 40*scale, ecg_y - 8*scale),
        (start_x + 50*scale, ecg_y),
        (start_x + 60*scale, ecg_y + 6*scale),
        (start_x + 72*scale, ecg_y - 45*scale),
        (start_x + 84*scale, ecg_y + 20*scale),
        (start_x + 94*scale, ecg_y),
        (start_x + 110*scale, ecg_y - 12*scale),
        (start_x + 125*scale, ecg_y),
        (end_x, ecg_y)
    ]
    draw.line(ecg_pts, fill=color, width=int(stroke_w * scale))
    
    draw.line([(ox + w/2 - 30*scale, oy + h/2), (ox + w/2 - 30*scale, oy + h/2 + 35*scale)], fill=color, width=int(stroke_w * scale))
    bcx = ox + w/2 - 30*scale
    bcy = oy + h/2 + 55*scale
    draw.ellipse([bcx - 18*scale, bcy - 18*scale, bcx + 18*scale, bcy + 18*scale], outline=color, width=int(stroke_w * scale))
    draw.ellipse([bcx - 9*scale, bcy - 9*scale, bcx + 9*scale, bcy + 9*scale], outline=color, width=int(stroke_w * scale))
