#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

W, H = 1080, 1920
FPS = 30
WHITE = (255, 255, 255)
NAVY = (13, 27, 42)          # live Snay3i header
TERRACOTTA = (196, 98, 45)   # live Snay3i accent
GOLD = (212, 168, 67)        # live Snay3i gold
CREAM = (250, 246, 239)      # live Snay3i background


def run(cmd):
    print('+', ' '.join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def rtl(text):
    return get_display(arabic_reshaper.reshape(text)) if text else text


def find_font(patterns):
    for p in patterns:
        matches = list(Path('/usr/share/fonts').rglob(p))
        if matches:
            return str(matches[0])
    raise FileNotFoundError(patterns)


def fit_font(draw, text, path, max_size, min_size, max_width):
    for size in range(max_size, min_size - 1, -2):
        font = ImageFont.truetype(path, size)
        box = draw.textbbox((0, 0), text, font=font)
        if box[2] - box[0] <= max_width:
            return font
    return ImageFont.truetype(path, min_size)


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
    """Protect readability while leaving most of the real photography visible."""
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    px = ov.load()
    for y in range(H):
        if y < 520:
            a = int(82 * (1 - y / 520))
        elif y < 930:
            a = 12
        else:
            a = int(220 * min(1, (y - 930) / 760))
        for x in range(W):
            px[x, y] = (*NAVY, a)
    return Image.alpha_composite(img.convert('RGBA'), ov)


def wrap_original_arabic(draw, text, font, max_width):
    """Wrap before bidi shaping so Arabic word order remains correct."""
    words = text.split()
    lines, cur = [], []
    for word in words:
        candidate = ' '.join(cur + [word])
        display = rtl(candidate)
        box = draw.textbbox((0, 0), display, font=font)
        if box[2] - box[0] > max_width and cur:
            lines.append(' '.join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(' '.join(cur))
    return lines


def draw_brand_lockup(canvas, draw, logo, arabic_bold, latin_bold):
    """Use the same visual identity as the live Snay3i frontend."""
    draw.rounded_rectangle((50, 48, 750, 238), radius=48, fill=(13, 27, 42, 238))

    mark = logo.copy().convert('RGBA')
    mark.thumbnail((118, 118), Image.Resampling.LANCZOS)
    draw.rounded_rectangle((74, 82, 208, 216), radius=32, fill=CREAM)
    canvas.alpha_composite(mark, (74 + (134 - mark.width)//2, 82 + (134 - mark.height)//2))

    lat = ImageFont.truetype(latin_bold, 55)
    ar = ImageFont.truetype(arabic_bold, 35)
    draw.text((240, 119), 'SNAY3I.MA', font=lat, fill=CREAM, anchor='lm')
    draw.text((242, 185), rtl('صنايعي'), font=ar, fill=GOLD, anchor='lm')
    draw.rounded_rectangle((655, 86, 706, 200), radius=24, fill=TERRACOTTA)


def render_scene(scene, idx, assets, logo, out_path, arabic_regular, arabic_bold, latin_bold):
    bg_path = assets / scene['background']
    if not bg_path.exists():
        raise FileNotFoundError(bg_path)

    bg = Image.open(bg_path).convert('RGB')
    bg = cover_crop(bg, focus_x=scene.get('focus_x', 0.5), focus_y=scene.get('focus_y', 0.5))
    bg = ImageEnhance.Contrast(bg).enhance(1.06)
    bg = ImageEnhance.Color(bg).enhance(0.96)
    canvas = overlay_gradient(bg)
    draw = ImageDraw.Draw(canvas, 'RGBA')

    draw_brand_lockup(canvas, draw, logo, arabic_bold, latin_bold)

    eyebrow_raw = scene.get('eyebrow', '')
    eyebrow = rtl(eyebrow_raw)
    pill_font = ImageFont.truetype(arabic_bold, 43)
    pill_box = draw.textbbox((0, 0), eyebrow, font=pill_font)
    pw = min(700, max(250, pill_box[2] - pill_box[0] + 90))
    draw.rounded_rectangle((60, 300, 60 + pw, 390), radius=44, fill=(*TERRACOTTA, 238))
    draw.text((60 + pw/2, 345), eyebrow, font=pill_font, fill=CREAM, anchor='mm')

    # Lower-third copy leaves the upper ~60% for the high-resolution photograph.
    headline = scene.get('headline', '')
    is_ar = any('\u0600' <= ch <= '\u06ff' for ch in headline)
    htxt = rtl(headline) if is_ar else headline
    hpath = arabic_bold if is_ar else latin_bold
    hfont = fit_font(draw, htxt, hpath, 104, 60, 930)
    draw.text((540, 1255), htxt, font=hfont, fill=WHITE, anchor='mm', stroke_width=4, stroke_fill=(*NAVY, 220))

    body_raw = scene.get('body', '')
    body_display = rtl(body_raw)
    bfont = fit_font(draw, body_display, arabic_regular, 57, 38, 880)
    lines = wrap_original_arabic(draw, body_raw, bfont, 850)
    y = 1395
    for raw_line in lines[:3]:
        draw.text((540, y), rtl(raw_line), font=bfont, fill=CREAM, anchor='mm', stroke_width=2, stroke_fill=(*NAVY, 210))
        y += 76

    # Strong Snay3i footer/CTA, using the website palette.
    draw.rounded_rectangle((58, 1648, 1022, 1818), radius=50, fill=(*NAVY, 245))
    num_font = ImageFont.truetype(latin_bold, 40)
    brand_font = ImageFont.truetype(latin_bold, 58)
    draw.text((106, 1733), f'{idx+1:02d}', font=num_font, fill=GOLD, anchor='lm')
    draw.text((525, 1733), 'Snay3i.ma', font=brand_font, fill=CREAM, anchor='mm')
    draw.rounded_rectangle((850, 1681, 972, 1790), radius=52, fill=TERRACOTTA)
    draw.text((911, 1735), '›', font=ImageFont.truetype(latin_bold, 76), fill=CREAM, anchor='mm')

    canvas.convert('RGB').save(out_path, quality=96)


def duration(audio):
    p = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(audio)
    ], capture_output=True, text=True, check=True)
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

    data = json.loads(Path(args.script).read_text(encoding='utf-8'))
    assets = Path(args.assets)
    logo = Image.open(args.logo).convert('RGBA')
    work = Path('output/video_factory_v2')
    work.mkdir(parents=True, exist_ok=True)

    ar_reg = find_font(['NotoSansArabic-Regular.ttf', 'NotoNaskhArabic-Regular.ttf'])
    ar_bold = find_font(['NotoSansArabic-Bold.ttf', 'NotoNaskhArabic-Bold.ttf'])
    lat_bold = find_font(['NotoSans-Bold.ttf', 'DejaVuSans-Bold.ttf'])

    frames = []
    for i, scene in enumerate(data['scenes']):
        p = work / f'scene_{i+1}.jpg'
        render_scene(scene, i, assets, logo, p, ar_reg, ar_bold, lat_bold)
        frames.append(p)

    total = max(duration(Path(args.audio)) + 1.2, 13.0)
    fade = 0.30
    weights = [0.22, 0.28, 0.27, 0.23]
    durs = [total * w for w in weights]
    clips = []

    for i, (frame, dur) in enumerate(zip(frames, durs)):
        clip = work / f'clip_{i+1}.mp4'
        if i % 2 == 0:
            motion = "zoompan=z='min(zoom+0.00075,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        else:
            motion = "zoompan=z='if(lte(zoom,1.0),1.07,max(1.0,zoom-0.00065))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        run([
            'ffmpeg', '-y', '-loop', '1', '-i', str(frame), '-vf', motion,
            '-t', f'{dur:.3f}', '-r', str(FPS), '-c:v', 'libx264',
            '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', str(clip)
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
        '-i', args.audio, '-filter_complex', filt,
        '-map', '[v3]', '-map', '4:a',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '17',
        '-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p',
        '-shortest', '-movflags', '+faststart', str(out)
    ]
    run(cmd)
    print(f'Rendered Snay3i branded v2.1: {out}')


if __name__ == '__main__':
    main()
