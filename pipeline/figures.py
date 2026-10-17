import math
from PIL import Image, ImageDraw, ImageFont

def draw_medical_figure(
    draw: ImageDraw.ImageDraw, 
    cx: int, 
    cy: int, 
    is_indian: bool = False, 
    t_local: float = 0.0,
    width_scale: float = 1.0
):
    """
    Draw a clean, medical-grade anatomical body silhouette.
    Both European and Indian figures share the exact identical outward morphology (70.0 kg, normal BMI).
    The Indian figure reveals the hidden visceral ectopic fat deposit suffocating liver and pancreas.
    """
    skin_fill = "#FAF5EF"
    skin_outline = "#8C6A5E"
    scale = width_scale

    def pt(dx, dy):
        return (int(cx + dx * scale), int(cy + dy * scale))

    # 1. Smooth Head (Anatomical oval)
    hw, hh = int(32 * scale), int(42 * scale)
    head_cy = int(cy - 165 * scale)
    draw.ellipse([cx - hw, head_cy - hh, cx + hw, head_cy + hh], fill=skin_fill, outline=skin_outline, width=2)

    # 2. Smooth Contoured Torso & Limbs Polygon
    body_points = [
        # Neck & Shoulders
        pt(-14, -125), pt(-35, -115), pt(-82, -90), pt(-95, -75),
        # Arms & Chest
        pt(-88, -20), pt(-78, 40),
        # Waist indentation
        pt(-55, 60),
        # Hip contour
        pt(-66, 110),
        # Left Leg outer contour
        pt(-52, 180), pt(-42, 250),
        # Feet / Inseam
        pt(-22, 250), pt(-20, 180), pt(-8, 125),
        # Crotch center
        pt(0, 115),
        # Right Inseam
        pt(8, 125), pt(20, 180), pt(22, 250),
        # Right Leg outer contour
        pt(42, 250), pt(52, 180),
        # Right Hip contour
        pt(66, 110),
        # Right Waist indentation
        pt(55, 60),
        # Right Chest & Arm
        pt(78, 40), pt(88, -20),
        # Right Shoulder & Neck
        pt(95, -75), pt(82, -90), pt(35, -115), pt(14, -125)
    ]
    draw.polygon(body_points, fill=skin_fill, outline=skin_outline)

    # Chest & Clavicle subtle clinical line
    draw.line([pt(-35, -78), pt(0, -68), pt(35, -78)], fill="#D8C7B5", width=2)
    draw.line([pt(0, -65), pt(0, 15)], fill="#E4D7C8", width=1)

    if not is_indian:
        # European body: Subcutaneous fat safely stored beneath peripheral skin layer
        subq_left = [pt(-80, -15), pt(-53, 60), pt(-64, 110), pt(-50, 180)]
        subq_right = [pt(80, -15), pt(53, 60), pt(64, 110), pt(50, 180)]
        draw.line(subq_left, fill="#34A853", width=4)
        draw.line(subq_right, fill="#34A853", width=4)
        
        core_cy = int(cy + 45 * scale)
        draw.ellipse([cx - 14, core_cy - 14, cx + 14, core_cy + 14], fill="#EDF5F0", outline="#34A853", width=2)
    else:
        # Indian body: Visceral ectopic fat suffocating internal organs (Liver, Pancreas, Mesentery)
        pulse = math.sin(t_local * 4.5) * 3.5
        core_cx = cx
        core_cy = int(cy + 45 * scale)

        r1_x = int((38 + pulse) * scale)
        r1_y = int((48 + pulse) * scale)
        
        draw.ellipse([core_cx - r1_x - 14, core_cy - r1_y - 14, core_cx + r1_x + 14, core_cy + r1_y + 14], fill="#FDEEE8")
        draw.ellipse([core_cx - r1_x, core_cy - r1_y, core_cx + r1_x, core_cy + r1_y], fill="#F0A892", outline="#C04E2A", width=2)
        
        draw.ellipse([core_cx - 24, core_cy - 20, core_cx + 20, core_cy + 22], fill="#C04E2A")
        draw.ellipse([core_cx - 10, core_cy + 12, core_cx + 18, core_cy + 36], fill="#8B1E0F")

        draw.line([pt(30, 45), pt(75, 45)], fill="#C04E2A", width=2)
        draw.ellipse([pt(28, 43)[0], pt(28, 43)[1], pt(32, 47)[0], pt(32, 47)[1]], fill="#C04E2A")

def draw_gut_brain_diagram(draw: ImageDraw.ImageDraw, cx: int, cy: int, t_local: float = 0.0):
    """
    Draw a gut-brain incretin signaling pathway diagram.
    Shows stomach producing satiety signal, but visceral cytokines blocking receptors at brain.
    """
    # 1. Brain / Hypothalamus (Top)
    brain_y = cy - 130
    draw.rounded_rectangle([cx - 110, brain_y, cx + 110, brain_y + 70], radius=18, fill="#FFFFFF", outline="#7D5246", width=2)
    draw.text((cx - 80, brain_y + 12), "HYPOTHALAMUS", fill="#661414", font=ImageFont.load_default())
    draw.text((cx - 95, brain_y + 38), "Hunger / Satiety Center", fill="#7D5246", font=ImageFont.load_default())

    # 2. Gut / Incretin Origin (Bottom)
    gut_y = cy + 110
    draw.rounded_rectangle([cx - 110, gut_y, cx + 110, gut_y + 70], radius=18, fill="#FFFFFF", outline="#34A853", width=2)
    draw.text((cx - 75, gut_y + 12), "INTESTINAL L-CELLS", fill="#235937", font=ImageFont.load_default())
    draw.text((cx - 95, gut_y + 38), "Produces natural GLP-1", fill="#7D5246", font=ImageFont.load_default())

    # 3. Signaling Channel
    draw.line([(cx, gut_y), (cx, brain_y + 70)], fill="#DEC3B5", width=4)

    # 4. Animated Incretin Signal rising
    sig_offset = int((t_local * 120) % 170)
    sig_y = gut_y - sig_offset
    draw.ellipse([cx - 10, sig_y - 10, cx + 10, sig_y + 10], fill="#34A853")

    # 5. Inflammatory Visceral Cytokine Blockade (Middle Barrier)
    bar_y = cy
    draw.rounded_rectangle([cx - 130, bar_y - 25, cx + 130, bar_y + 25], radius=12, fill="#FAF0EB", outline="#C04E2A", width=2)
    draw.text((cx - 105, bar_y - 10), "⚠️ VISCERAL FAT BLOCKADE", fill="#C04E2A", font=ImageFont.load_default())
