#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, features

W, H = 1080, 1920
FPS = 30
WHITE = (255, 255, 255)
CREAM = (250, 246, 239)
NAVY = (13, 27, 42)
TERRACOTTA = (196, 98, 45)
GOLD = (212, 168, 67)
RAQM = bool(features.check('raqm'))


def run(cmd):
    print('+', ' '.join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def is_arabic(text):
    return any('\u0600' <= ch <= '\u06ff' for ch in text)


def prepared_text(text):
    # Pillow wheels normally include RAQM. When RAQM is present, give Pillow
    # logical Arabic and let it shape + reorder exactly once. The old v2 path
    # reshaped/reordered first and RAQM then applied bidi again, reversing copy.
    if text and is_arabic(text) and not RAQM:
        return get_display(arabic_reshaper.reshape(text))
    return text


def text_kwargs(text):
    if text and is_arabic(text) and RAQM:
        return {'direction': 'rtl', 'language': 'ar'}
    return {}


def find_font(patterns):
    for p in patterns:
        matches = list(Path('/usr/share/fonts').rglob(p))
        if matches:
            return str(matches[0])
    raise FileNotFoundError(patterns)


def text_bbox(draw, text, font, stroke_width=0):
    t = prepared_text(text)
    return draw.textbbox((0, 0), t, font=font, stroke_width=stroke_width, **text_kwargs(text))


def text_width(draw, text, font, stroke_width=0):
    b = text_bbox(draw, text, font, stroke_width)
    return b[2] - b[0]


def fit_font(draw, text, path, max_size, min_size, max_width, stroke_width=0):
    for size in range(max_size, min_size - 1, -2):
        font = ImageFont.truetype(path, size)
        if text_width(draw, text, font, stroke_width) <= max_width:
            return font
    return ImageFont.truetype(path, min_size)


def draw_text(draw, xy, text, font, fill, anchor='mm', stroke_width=0, stroke_fill=None):
    t = prepared_text(text)
    kwargs = text_kwargs(text)
    draw.text(
        xy,
        t,
        font=font,
        fill=fill,
        anchor=anchor,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
        **kwargs,
    )


def wrap_words(draw, text, font, max_width, max_lines=3, stroke_width=0):
    words = text.split()
    if not words:
        return []
    lines, cur = [], []
    for word in words:
        candidate = ' '.join(cur + [word])
        if cur and text_width(draw, candidate, font, stroke_width) > max_width:
            lines.append(' '.join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(' '.join(cur))
    return lines[:max_lines]


def fit_wrapped(draw, text, font_path, max_size, min_size, max_width, max_lines=2, stroke_width=0):
    for size in range(max_size, min_size - 1, -2):
        font = ImageFont.truetype(font_path, size)
        lines = wrap_words(draw, text, font, max_width, max_lines=max_lines + 1, stroke_width=stroke_width)
        if len(lines) <= max_lines and all(text_width(draw, line, font, stroke_width) <= max_width for line in lines):
            return font, lines
    font = ImageFont.truetype(font_path, min_size)
    return font, wrap_words(draw, text, font, max_width, max_lines=max_lines, stroke_width=stroke_width)


def cover_crop(img, size=(W, H), focus_x=0.5, focus_y=0.5):
    sw, sh = size
    iw, ih = img.size
    scale = max(sw / iw, sh / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = int((nw - sw) * max(0, min(1, focus_x)))
    top = int((nh - sh) * max(0, min(1, focus_y)))
    left = max(0, min(left, nw - sw))
    top = max(0, min(top, nh - sh))
    return img.crop((left, top, left + sw, top + sh))


def overlay_gradient(img):
    # Preserve the photograph while creating readable top/lower safe zones.
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(H):
        if y < 430:
            alpha = int(95 * (1 - y / 520))
        elif 860 <= y <= 1640:
            alpha = int(40 + 145 * ((y - 860) / 780))
        elif y > 1640:
            alpha = 170
        else:
            alpha = 18
        d.line((0, y, W, y), fill=(4, 13, 21, max(0, min(210, alpha))))
    return Image.alpha_composite(img.convert('RGBA'), ov)


def render_scene(scene, idx, assets, logo, out_path, arabic_regular, arabic_bold, latin_bold):
    bg_path = assets / scene['background']
    if not bg_path.exists():
        raise FileNotFoundError(bg_path)

    bg = Image.open(bg_path).convert('RGB')
    bg = cover_crop(bg, focus_x=scene.get('focus_x', 0.5), focus_y=scene.get('focus_y', 0.5))
    bg = ImageEnhance.Contrast(bg).enhance(1.04)
    bg = ImageEnhance.Color(bg).enhance(0.98)
    canvas = overlay_gradient(bg)
    draw = ImageDraw.Draw(canvas)

    # Safe-area brand lockup. Kept below the top 120 px because YouTube/TikTok
    # and desktop players often overlay UI at the top edge.
    draw.rounded_rectangle((66, 145, 826, 320), radius=44, fill=(*NAVY, 238))
    draw.rounded_rectangle((92, 168, 230, 297), radius=28, fill=(*CREAM, 255))

    mark = logo.copy().convert('RGBA')
    mark.thumbnail((110, 110), Image.Resampling.LANCZOS)
    canvas.alpha_composite(mark, (161 - mark.width // 2, 232 - mark.height // 2))

    brand_font = ImageFont.truetype(latin_bold, 58)
    draw.text((270, 210), 'SNAY3I.MA', font=brand_font, fill=WHITE, anchor='lm')
    ar_brand_font = ImageFont.truetype(arabic_bold, 38)
    draw_text(draw, (724, 271), 'صنايعي', ar_brand_font, GOLD, anchor='ra')
    draw.rounded_rectangle((786, 145, 826, 320), radius=20, fill=(*TERRACOTTA, 255))

    # Category/city pill, also inside top safe area.
    eyebrow = scene.get('eyebrow', '')
    pill_font = fit_font(draw, eyebrow, arabic_bold, 42, 32, 500)
    pw = min(540, max(230, int(text_width(draw, eyebrow, pill_font) + 92)))
    draw.rounded_rectangle((70, 365, 70 + pw, 454), radius=44, fill=(*TERRACOTTA, 242))
    draw_text(draw, (70 + pw / 2, 410), eyebrow, pill_font, WHITE, anchor='mm')

    # Main copy. Leave ~170 px on the right for Shorts/TikTok action icons.
    headline = scene.get('headline', '')
    hpath = arabic_bold if is_arabic(headline) else latin_bold
    hfont, hlines = fit_wrapped(draw, headline, hpath, 82, 52, 790, max_lines=2, stroke_width=3)
    hx = 490
    hy = 1110 if len(hlines) == 1 else 1060
    for line in hlines:
        draw_text(draw, (hx, hy), line, hfont, WHITE, anchor='mm', stroke_width=3, stroke_fill=(2, 8, 13, 220))
        hy += hfont.size + 22

    body = scene.get('body', '')
    bfont = fit_font(draw, body, arabic_regular, 48, 34, 790, stroke_width=2)
    blines = wrap_words(draw, body, bfont, 790, max_lines=2, stroke_width=2)
    by = hy + 28
    for line in blines:
        draw_text(draw, (hx, by), line, bfont, CREAM, anchor='mm', stroke_width=2, stroke_fill=(2, 8, 13, 210))
        by += bfont.size + 22

    # CTA is intentionally above y=1620 so platform controls/captions do not hide it.
    draw.rounded_rectangle((66, 1450, 900, 1610), radius=48, fill=(*NAVY, 242))
    num_font = ImageFont.truetype(latin_bold, 38)
    cta_font = ImageFont.truetype(latin_bold, 50)
    draw.text((108, 1530), f'{idx + 1:02d}', font=num_font, fill=GOLD, anchor='lm')
    draw.text((485, 1530), 'Snay3i.ma', font=cta_font, fill=WHITE, anchor='mm')
    draw.rounded_rectangle((770, 1480, 858, 1570), radius=44, fill=(*TERRACOTTA, 255))
    draw.text((814, 1525), '›', font=ImageFont.truetype(latin_bold, 64), fill=WHITE, anchor='mm')

    # Keep the bottom ~300 px free of critical information for platform overlays.
    canvas.convert('RGB').save(out_path, quality=96, subsampling=0)


def duration(audio):
    p = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(p.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--script', required=True)
    ap.add_argument('--audio', required=True)
    ap.add_argument('--assets', required=True)
    ap.add_argument('--logo', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    if not shutil.which('ffmpeg'):
        raise RuntimeError('ffmpeg required')

    print('Pillow RAQM Arabic layout:', RAQM)

    data = json.loads(Path(args.script).read_text(encoding='utf-8'))
    assets = Path(args.assets)
    logo = Image.open(args.logo).convert('RGBA')
    work = Path('output/video_factory_v22')
    work.mkdir(parents=True, exist_ok=True)

    ar_reg = find_font(['NotoSansArabic-Regular.ttf', 'NotoNaskhArabic-Regular.ttf'])
    ar_bold = find_font(['NotoSansArabic-Bold.ttf', 'NotoNaskhArabic-Bold.ttf'])
    lat_bold = find_font(['NotoSans-Bold.ttf', 'DejaVuSans-Bold.ttf'])

    frames = []
    for i, scene in enumerate(data['scenes']):
        p = work / f'scene_{i + 1}.jpg'
        render_scene(scene, i, assets, logo, p, ar_reg, ar_bold, lat_bold)
        frames.append(p)

    total = max(duration(Path(args.audio)) + 1.1, 14.0)
    fade = 0.28
    weights = [0.23, 0.27, 0.27, 0.23]
    durs = [total * w for w in weights]
    clips = []

    for i, (frame, dur) in enumerate(zip(frames, durs)):
        clip = work / f'clip_{i + 1}.mp4'
        if i % 2 == 0:
            z = "zoompan=z='min(zoom+0.00055,1.055)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        else:
            z = "zoompan=z='if(lte(zoom,1.0),1.055,max(1.0,zoom-0.0005))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        run([
            'ffmpeg', '-y', '-loop', '1', '-i', str(frame), '-vf', z,
            '-t', f'{dur:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast',
            '-crf', '18', '-pix_fmt', 'yuv420p', str(clip),
        ])
        clips.append(clip)

    o1 = durs[0] - fade
    o2 = durs[0] + durs[1] - 2 * fade
    o3 = durs[0] + durs[1] + durs[2] - 3 * fade
    filt = (
        f'[0:v][1:v]xfade=transition=fade:duration={fade}:offset={o1:.3f}[v1];'
        f'[v1][2:v]xfade=transition=slideleft:duration={fade}:offset={o2:.3f}[v2];'
        f'[v2][3:v]xfade=transition=fade:duration={fade}:offset={o3:.3f}[v3]'
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg', '-y']
    for c in clips:
        cmd += ['-i', str(c)]
    cmd += [
        '-i', args.audio, '-filter_complex', filt, '-map', '[v3]', '-map', '4:a',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-c:a', 'aac', '-b:a', '192k',
        '-pix_fmt', 'yuv420p', '-shortest', '-movflags', '+faststart', str(out),
    ]
    run(cmd)
    print(f'Rendered Snay3i v2.2: {out}')


if __name__ == '__main__':
    main()
