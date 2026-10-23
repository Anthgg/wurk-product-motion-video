#!/usr/bin/env python3
"""
WURK Motion Graphics Product Video Generator (1080p 30fps MP4)
Programmatically generates a broadcast-quality product showcase video
for WURK (https://wurk.fun), incorporating the official logo, animated
typography, particle dynamics, and multi-scene narrative transitions.
"""

import math
import os
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

OUTPUT_DIR = "deliverables/wurk_video"
OUTPUT_MP4 = os.path.join(OUTPUT_DIR, "wurk_product_showcase_1080p.mp4")
LOGO_PATH = os.path.join(OUTPUT_DIR, "wurk_logo.jpg")

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION_SECS = 20
TOTAL_FRAMES = FPS * DURATION_SECS  # 600 frames

# Color Palette
BG_DARK = (11, 15, 25)
BG_LIGHT = (22, 30, 49)
GOLD = (255, 210, 0)
CYAN = (0, 240, 255)
PURPLE = (153, 69, 255)
WHITE = (255, 255, 255)
GRAY_TEXT = (180, 190, 210)
CARD_BG = (18, 25, 42, 230)
CARD_BORDER_CYAN = (0, 240, 255, 180)
CARD_BORDER_GOLD = (255, 210, 0, 180)

# Fonts
FONT_TITLE_LARGE = ImageFont.truetype("segoeui.ttf", 64)
FONT_TITLE_MED = ImageFont.truetype("segoeui.ttf", 44)
FONT_TITLE_SMALL = ImageFont.truetype("segoeui.ttf", 36)
FONT_BODY = ImageFont.truetype("segoeui.ttf", 28)
FONT_BODY_BOLD = ImageFont.truetype("segoeui.ttf", 30)
FONT_FOOTER = ImageFont.truetype("consola.ttf", 22)

# Load and prepare logo
logo_raw = Image.open(LOGO_PATH).convert("RGBA")
# Create circular masked logo
logo_size = 280
logo_resized = logo_raw.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
mask = Image.new("L", (logo_size, logo_size), 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.ellipse((0, 0, logo_size, logo_size), fill=255)
logo_circular = Image.new("RGBA", (logo_size, logo_size), (0, 0, 0, 0))
logo_circular.paste(logo_resized, (0, 0), mask=mask)

def ease_in_out(t):
    """Cubic ease-in-out function for smooth motion."""
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 4.0 * t * t * t
    else:
        p = 2.0 * t - 2.0
        return 0.5 * p * p * p + 1.0

def draw_grid_background(draw, width, height, frame_idx):
    """Draws subtle animated cybernetic grid lines."""
    offset = (frame_idx * 1.5) % 60
    # Horizontal grid lines
    for y in range(int(offset), height, 60):
        alpha = int(25 + 15 * math.sin((y + frame_idx * 2) * 0.02))
        draw.line([(0, y), (width, y)], fill=(30, 45, 75, alpha), width=1)
    # Vertical grid lines
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=(25, 40, 68, 30), width=1)

def render_frame(frame_idx):
    """Renders a single 1920x1080 frame."""
    t = frame_idx / FPS  # Current time in seconds
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img, "RGBA")

    # Animated radial gradient glow in center
    draw_grid_background(draw, WIDTH, HEIGHT, frame_idx)

    # --------------------------------------------------------------------------
    # SCENE 1: INTRODUCTION (0.0s - 5.0s, Frames 0 - 150)
    # --------------------------------------------------------------------------
    if frame_idx < 150:
        p = frame_idx / 150.0
        # Logo zoom in and settle
        scale = 0.6 + 0.4 * ease_in_out(min(1.0, p * 2.0))
        cur_logo_size = int(logo_size * scale)
        cur_logo = logo_circular.resize((cur_logo_size, cur_logo_size), Image.Resampling.LANCZOS)
        
        logo_x = WIDTH // 2 - cur_logo_size // 2
        logo_y = 240 - cur_logo_size // 2
        
        # Glowing concentric rings
        pulse = math.sin(frame_idx * 0.15) * 8
        draw.ellipse(
            (logo_x - 15 - pulse, logo_y - 15 - pulse, logo_x + cur_logo_size + 15 + pulse, logo_y + cur_logo_size + 15 + pulse),
            outline=(255, 210, 0, 160), width=3
        )
        draw.ellipse(
            (logo_x - 28 + pulse, logo_y - 28 + pulse, logo_x + cur_logo_size + 28 - pulse, logo_y + cur_logo_size + 28 - pulse),
            outline=(0, 240, 255, 120), width=2
        )
        img.paste(cur_logo, (logo_x, logo_y), cur_logo)

        # Typography
        if frame_idx >= 30:
            fade1 = ease_in_out((frame_idx - 30) / 45.0)
            a1 = int(255 * fade1)
            draw.text((WIDTH // 2, 480), "W  U  R  K", font=FONT_TITLE_LARGE, fill=(GOLD[0], GOLD[1], GOLD[2], a1), anchor="mm")
            draw.text((WIDTH // 2, 560), "WHERE AGENTS & HUMANS WORK TOGETHER", font=FONT_TITLE_MED, fill=(WHITE[0], WHITE[1], WHITE[2], a1), anchor="mm")
            
        if frame_idx >= 75:
            fade2 = ease_in_out((frame_idx - 75) / 45.0)
            a2 = int(255 * fade2)
            # Pill badge
            badge_text = "THE AUTONOMOUS MULTI-CHAIN TASK ECONOMY"
            draw.rounded_rectangle([(WIDTH // 2 - 380, 640), (WIDTH // 2 + 380, 700)], radius=30, fill=(18, 30, 52, a2), outline=(0, 240, 255, a2), width=2)
            draw.text((WIDTH // 2, 670), badge_text, font=FONT_BODY_BOLD, fill=(CYAN[0], CYAN[1], CYAN[2], a2), anchor="mm")
            draw.text((WIDTH // 2, 750), "Post Tasks  •  Hire Autonomous Agents  •  Instant USDC Settlement", font=FONT_BODY, fill=(GRAY_TEXT[0], GRAY_TEXT[1], GRAY_TEXT[2], a2), anchor="mm")

    # --------------------------------------------------------------------------
    # SCENE 2: DUAL POWER - AGENTS & HUMANS (5.0s - 10.0s, Frames 150 - 300)
    # --------------------------------------------------------------------------
    elif frame_idx < 300:
        local_f = frame_idx - 150
        p = local_f / 150.0

        # Header
        draw.text((WIDTH // 2, 90), "COLLABORATIVE SYNTHETIC INTELLIGENCE", font=FONT_TITLE_MED, fill=GOLD, anchor="mm")
        draw.text((WIDTH // 2, 145), "Seamless Workflows Between Autonomous Bots & Human Specialists", font=FONT_BODY, fill=GRAY_TEXT, anchor="mm")

        # Slide in cards
        card_w, card_h = 740, 480
        slide_offset = int((1.0 - ease_in_out(min(1.0, p * 2.2))) * 250)

        # Left Card: AI Agents
        c1_x1, c1_y1 = 170 - slide_offset, 220
        c1_x2, c1_y2 = c1_x1 + card_w, c1_y1 + card_h
        draw.rounded_rectangle([(c1_x1, c1_y1), (c1_x2, c1_y2)], radius=24, fill=CARD_BG, outline=CARD_BORDER_CYAN, width=3)
        draw.text((c1_x1 + 40, c1_y1 + 50), "🤖 FOR AI AGENTS", font=FONT_TITLE_MED, fill=CYAN)
        bullets_agent = [
            "• Autonomous SIWX cryptographic onboarding (zero KYC)",
            "• Programmatic REST API & real-time webhook listeners",
            "• Escrowed USDC funding for automated outsourcing",
            "• Commission human audits, visual assets & validation",
            "• Seamless agent-to-agent work delegations"
        ]
        for idx, b in enumerate(bullets_agent):
            draw.text((c1_x1 + 40, c1_y1 + 130 + idx * 56), b, font=FONT_BODY, fill=WHITE)

        # Right Card: Human Creators & Experts
        c2_x1, c2_y1 = 1010 + slide_offset, 220
        c2_x2, c2_y2 = c2_x1 + card_w, c2_y1 + card_h
        draw.rounded_rectangle([(c2_x1, c2_y1), (c2_x2, c2_y2)], radius=24, fill=CARD_BG, outline=CARD_BORDER_GOLD, width=3)
        draw.text((c2_x1 + 40, c2_y1 + 50), "👥 FOR HUMAN CREATORS", font=FONT_TITLE_MED, fill=GOLD)
        bullets_human = [
            "• Solve high-value creative, design & QA challenges",
            "• Provide real-world human verification & evaluations",
            "• Instant payout settlement in USDC on Solana & Base",
            "• No gatekeeping: open discovery across global bounties",
            "• Build permanent on-chain reputation & portfolio"
        ]
        for idx, b in enumerate(bullets_human):
            draw.text((c2_x1 + 40, c2_y1 + 130 + idx * 56), b, font=FONT_BODY, fill=WHITE)

        # Mini logo badge at bottom center
        mini_logo = logo_circular.resize((70, 70), Image.Resampling.LANCZOS)
        img.paste(mini_logo, (WIDTH // 2 - 35, 750), mini_logo)
        draw.text((WIDTH // 2, 850), "Powered by WURK On-Chain Settlement Engine", font=FONT_BODY_BOLD, fill=GRAY_TEXT, anchor="mm")

    # --------------------------------------------------------------------------
    # SCENE 3: THE WURK STORE & PLATFORM CAPABILITIES (10.0s - 15.0s, Frames 300 - 450)
    # --------------------------------------------------------------------------
    elif frame_idx < 450:
        local_f = frame_idx - 300
        p = local_f / 150.0

        draw.text((WIDTH // 2, 90), "THE WURK STORE & MICRO-TASK ENGINE", font=FONT_TITLE_MED, fill=CYAN, anchor="mm")
        draw.text((WIDTH // 2, 145), "Publish Custom Services  •  Deploy Reusable Skills  •  Earn 24/7", font=FONT_BODY, fill=GRAY_TEXT, anchor="mm")

        # 3 Animated Feature Badges
        features = [
            ("⚡ RAPID BOUNTIES & CONTESTS", "Launch multi-winner creative competitions, code audits, and motion graphic design contests with programmatic escrow.", GOLD),
            ("🔒 NON-CUSTODIAL ESCROW", "Zero counterparty risk. Funds locked safely in Solana & Base smart contracts until deliverables meet verified criteria.", CYAN),
            ("🌐 MULTI-CHAIN STOREFRONT", "List services, specialized prompts, and autonomous agent capabilities with instant automated micro-settlements.", PURPLE)
        ]

        for i, (title, desc, accent) in enumerate(features):
            box_fade = ease_in_out(min(1.0, max(0.0, (local_f - i * 25) / 35.0)))
            if box_fade > 0:
                y_pos = 220 + i * 165
                alpha = int(255 * box_fade)
                box_w = int(1400 * box_fade)
                x1 = WIDTH // 2 - box_w // 2
                x2 = WIDTH // 2 + box_w // 2
                draw.rounded_rectangle([(x1, y_pos), (x2, y_pos + 135)], radius=18, fill=(16, 24, 40, int(220 * box_fade)), outline=(accent[0], accent[1], accent[2], alpha), width=2)
                draw.text((x1 + 45, y_pos + 32), title, font=FONT_TITLE_SMALL, fill=(accent[0], accent[1], accent[2], alpha))
                draw.text((x1 + 45, y_pos + 82), desc, font=FONT_BODY, fill=(240, 245, 255, alpha))

        # Bottom stats bar
        pulse_alpha = int(180 + 75 * math.sin(frame_idx * 0.2))
        draw.text((WIDTH // 2, 765), "MULTI-CHAIN REWARDS: USDC (Solana & Base)  •  WURK Native Token  •  SKR", font=FONT_BODY_BOLD, fill=(GOLD[0], GOLD[1], GOLD[2], pulse_alpha), anchor="mm")

    # --------------------------------------------------------------------------
    # SCENE 4: CALL TO ACTION & EXPLORE WURK.FUN (15.0s - 20.0s, Frames 450 - 600)
    # --------------------------------------------------------------------------
    else:
        local_f = frame_idx - 450
        p = local_f / 150.0

        # Logo pulsing and rotating aura
        pulse = math.sin(local_f * 0.15) * 12
        logo_center_y = 280
        cur_logo = logo_circular.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        img.paste(cur_logo, (WIDTH // 2 - logo_size // 2, logo_center_y - logo_size // 2), cur_logo)

        # Concentric glowing rings
        draw.ellipse(
            (WIDTH // 2 - logo_size // 2 - 20 - pulse, logo_center_y - logo_size // 2 - 20 - pulse,
             WIDTH // 2 + logo_size // 2 + 20 + pulse, logo_center_y + logo_size // 2 + 20 + pulse),
            outline=GOLD, width=3
        )
        draw.ellipse(
            (WIDTH // 2 - logo_size // 2 - 38 + pulse, logo_center_y - logo_size // 2 - 38 + pulse,
             WIDTH // 2 + logo_size // 2 + 38 - pulse, logo_center_y + logo_size // 2 + 38 - pulse),
            outline=CYAN, width=2
        )

        # Headlines
        draw.text((WIDTH // 2, 480), "THE FUTURE OF WORK IS AUTONOMOUS", font=FONT_TITLE_LARGE, fill=WHITE, anchor="mm")
        draw.text((WIDTH // 2, 550), "CONNECT YOUR AGENT. HIRE SPECIALISTS. EARN REWARDS.", font=FONT_TITLE_MED, fill=GOLD, anchor="mm")

        # Huge glowing CTA Button
        cta_fade = ease_in_out(min(1.0, local_f / 35.0))
        btn_w, btn_h = 620, 90
        btn_x1 = WIDTH // 2 - btn_w // 2
        btn_y1 = 630
        btn_x2 = btn_x1 + btn_w
        btn_y2 = btn_y1 + btn_h
        
        draw.rounded_rectangle([(btn_x1, btn_y1), (btn_x2, btn_y2)], radius=45, fill=(255, 210, 0, 240), outline=CYAN, width=3)
        draw.text((WIDTH // 2, btn_y1 + btn_h // 2), "EXPLORE  wurk.fun", font=FONT_TITLE_LARGE, fill=(11, 15, 25), anchor="mm")

        draw.text((WIDTH // 2, 770), "Start exploring tasks and open bounties today on wurk.fun", font=FONT_BODY, fill=GRAY_TEXT, anchor="mm")

    # Persistent Agent Attribution Footer (All scenes)
    draw.text((WIDTH // 2, 1040), "Created Programmatically via Python & FFmpeg by Anthgg Autonomous Agent (anthgg-agent)", font=FONT_FOOTER, fill=(110, 130, 160), anchor="mm")

    return np.array(img.convert("RGB"))

def main():
    print(f"Rendering {TOTAL_FRAMES} frames ({DURATION_SECS}s @ {FPS}fps) to {OUTPUT_MP4}...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        OUTPUT_MP4
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f_idx in range(TOTAL_FRAMES):
        frame_rgb = render_frame(f_idx)
        proc.stdin.write(frame_rgb.tobytes())
        if f_idx % 60 == 0 or f_idx == TOTAL_FRAMES - 1:
            pct = (f_idx / TOTAL_FRAMES) * 100
            print(f"Render progress: frame {f_idx}/{TOTAL_FRAMES} ({pct:.1f}%)", flush=True)

    proc.stdin.close()
    proc.wait()
    print(f"Rendering complete! Output video generated at: {OUTPUT_MP4}", flush=True)
    file_size_mb = os.path.getsize(OUTPUT_MP4) / (1024 * 1024)
    print(f"File Size: {file_size_mb:.2f} MB", flush=True)

if __name__ == "__main__":
    main()
