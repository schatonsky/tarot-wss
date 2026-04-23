#!/usr/bin/env python3
"""Génère les icônes PNG pour la PWA Tarot WSS."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
BG = (139, 92, 246, 255)  # violet --primary
BG_DARK = (15, 23, 42, 255)  # --bg

def rounded_square(size, radius, color):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=color)
    return img

def draw_card_tee(img, size, text_color=(255, 255, 255, 255)):
    """Dessine un 'T' stylisé de grande taille au centre."""
    draw = ImageDraw.Draw(img)
    font_path = '/System/Library/Fonts/Supplemental/Futura.ttc'
    if not os.path.exists(font_path):
        font_path = '/System/Library/Fonts/HelveticaNeue.ttc'
    try:
        font = ImageFont.truetype(font_path, int(size * 0.62))
    except Exception:
        font = ImageFont.load_default()
    text = 'T'
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1] - size * 0.02
    draw.text((x, y), text, font=font, fill=text_color)
    # Petit 'wss' en bas
    try:
        small_font = ImageFont.truetype(font_path, int(size * 0.12))
    except Exception:
        small_font = font
    sub = 'WSS'
    sb = draw.textbbox((0, 0), sub, font=small_font)
    sw = sb[2] - sb[0]
    draw.text(((size - sw) / 2 - sb[0], size * 0.78), sub, font=small_font, fill=text_color)

def make_icon(size, maskable=False):
    if maskable:
        # Safe zone: 80% centré. On étend le fond sur toute la zone.
        img = Image.new('RGBA', (size, size), BG)
        safe = int(size * 0.8)
        inner = Image.new('RGBA', (safe, safe), (0, 0, 0, 0))
        draw_card_tee(inner, safe)
        img.paste(inner, ((size - safe) // 2, (size - safe) // 2), inner)
    else:
        img = rounded_square(size, int(size * 0.22), BG)
        draw_card_tee(img, size)
    return img

for size, name in [(180, 'icon-180.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
    img = make_icon(size)
    img.save(os.path.join(OUT_DIR, name))
    print(f'Généré : {name}')

maskable = make_icon(512, maskable=True)
maskable.save(os.path.join(OUT_DIR, 'icon-maskable-512.png'))
print('Généré : icon-maskable-512.png')

# Favicon 32x32
fav = make_icon(32)
fav.save(os.path.join(OUT_DIR, 'favicon-32.png'))
print('Généré : favicon-32.png')
