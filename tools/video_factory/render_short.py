#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
BG_TOP = (14, 28, 43)
BG_BOTTOM = (29, 67, 82)
CREAM = (248, 245, 237)
MINT = (77, 214, 180)
GOLD = (242, 190, 92)
DARK = (12, 23, 35)


def run(cmd):
    print('+', ' '.join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def rtl(text: str) -> str:
    if not text:
        return text
    return get_display(arabic_reshaper.reshape(text))


def find_font(patterns):
    for p in patterns:
        matches = list(Path('/usr/share/fonts').rglob(p))
        if matches:
            return str(matches[0])
    raise FileNotFoundError(f'Could not find a usable font: {patterns}')


def fit_font(draw, text, font_path, max_size, min_size, max_width):
    size = max_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size)
        box = draw.textbbox((0, 0), text, font=font)
        if box[2] - box[0] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(font_path, min_size)


def gradient():
    img = Image.new('RGB', (W, H), BG_TOP)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        color = tuple(round(BG_TOP[i] * (1-t) + BG_BOTTOM[i] * t) for i in range(3))
        draw.line((0, y, W, y), fill=color)
    return img


def draw_brand(draw, font):
    draw.rounded_rectangle((62, 72, 344, 150), radius=38, fill=CREAM)
    draw.text((203, 112), 'SNAY3I.MA', font=font, fill=DARK, anchor='mm')
    draw.rounded_rectangle((875, 78, 1015, 140), radius=28, fill=MINT)
    draw.text((945, 109), 'MA', font=font, fill=DARK, anchor='mm')


def icon_drop(draw, box):
    x1, y1, x2, y2 = box
    cx = (x1+x2)//2
    pts = [(cx, y1+20), (x2-25, y1+145), (x2-8, y1+230), (cx, y2-15), (x1+8, y1+230), (x1+25, y1+145)]
    draw.polygon(pts, fill=MINT)
    draw.ellipse((x1+28, y1+170, x2-28, y2-22), fill=MINT)
    draw.ellipse((cx-38, y1+188, cx+8, y1+236), fill=(230,255,249))


def icon_pin(draw, box):
    x1, y1, x2, y2 = box
    cx = (x1+x2)//2
    draw.ellipse((x1+38, y1+30, x2-38, y2-90), fill=GOLD)
    draw.polygon([(cx-70, y2-140), (cx+70, y2-140), (cx, y2-12)], fill=GOLD)
    draw.ellipse((cx-38, y1+92, cx+38, y1+168), fill=DARK)


def icon_check(draw, box):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1+18, y1+18, x2-18, y2-18), radius=65, fill=MINT)
    draw.line((x1+75, y1+175, x1+135, y1+235), fill=DARK, width=26)
    draw.line((x1+130, y1+235, x2-70, y1+92), fill=DARK, width=26)


def icon_phone(draw, box):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1+62, y1+20, x2-62, y2-20), radius=38, outline=CREAM, width=18)
    draw.rounded_rectangle((x1+102, y1+62, x2-102, y2-92), radius=26, fill=(28, 56, 70))
    draw.ellipse(((x1+x2)//2-14, y2-62, (x1+x2)//2+14, y2-34), fill=MINT)


def draw_icon(draw, kind, box):
    {'drop': icon_drop, 'pin': icon_pin, 'check': icon_check, 'phone': icon_phone}.get(kind, icon_check)(draw, box)


def wrap_arabic(draw, logical_text, font, max_width):
    words = logical_text.split()
    lines, current = [], []
    for word in words:
        candidate = ' '.join(current + [word])
        shaped = rtl(candidate)
        box = draw.textbbox((0, 0), shaped, font=font)
        if box[2] - box[0] > max_width and current:
            lines.append(rtl(' '.join(current)))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(rtl(' '.join(current)))
    return lines


def render_scene(scene, idx, out_path, arabic_regular_path, arabic_bold_path, latin_bold_path):
    img = gradient()
    draw = ImageDraw.Draw(img)
    brand_font = ImageFont.truetype(latin_bold_path, 38)
    footer_font = ImageFont.truetype(latin_bold_path, 44)
    draw_brand(draw, brand_font)

    draw.ellipse((-170, 1350, 430, 1950), fill=(21, 81, 92))
    draw.ellipse((790, 210, 1190, 610), fill=(31, 92, 97))
    draw.rounded_rectangle((72, 315, 1008, 1510), radius=62, fill=CREAM)
    draw_icon(draw, scene.get('icon', 'check'), (390, 380, 690, 680))

    eyebrow = rtl(scene.get('eyebrow', ''))
    headline = scene.get('headline', '')
    body_logical = scene.get('body', '')

    eyebrow_font = fit_font(draw, eyebrow, arabic_bold_path, 58, 38, 780)
    draw.rounded_rectangle((190, 740, 890, 835), radius=44, fill=(230, 242, 239))
    draw.text((540, 787), eyebrow, font=eyebrow_font, fill=(17, 73, 77), anchor='mm')

    if any('\u0600' <= ch <= '\u06ff' for ch in headline):
        headline_text = rtl(headline)
        headline_font = fit_font(draw, headline_text, arabic_bold_path, 104, 66, 820)
    else:
        headline_text = headline
        headline_font = fit_font(draw, headline_text, latin_bold_path, 104, 66, 820)
    draw.text((540, 990), headline_text, font=headline_font, fill=DARK, anchor='mm', align='center')

    body_probe = rtl(body_logical)
    body_font = fit_font(draw, body_probe, arabic_regular_path, 58, 40, 780)
    y = 1165
    for line in wrap_arabic(draw, body_logical, body_font, 760)[:3]:
        draw.text((540, y), line, font=body_font, fill=(71, 91, 100), anchor='mm')
        y += 78

    draw.rounded_rectangle((92, 1580, 988, 1760), radius=52, fill=(14, 31, 42))
    draw.text((160, 1668), f'{idx+1:02d}', font=footer_font, fill=MINT, anchor='lm')
    draw.text((540, 1660), 'Snay3i.ma', font=footer_font, fill=CREAM, anchor='mm')
    draw.rounded_rectangle((780, 1622, 936, 1708), radius=40, fill=GOLD)
    draw.text((858, 1665), '→', font=footer_font, fill=DARK, anchor='mm')

    img.save(out_path, quality=95)


def probe_duration(audio_path):
    p = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
    ], text=True, capture_output=True, check=True)
    return float(p.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--script', required=True)
    ap.add_argument('--audio', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('ffmpeg/ffprobe required')

    data = json.loads(Path(args.script).read_text(encoding='utf-8'))
    work = Path('output/video_factory')
    work.mkdir(parents=True, exist_ok=True)

    arabic_regular = find_font(['NotoSansArabic-Regular.ttf', 'NotoNaskhArabic-Regular.ttf'])
    arabic_bold = find_font(['NotoSansArabic-Bold.ttf', 'NotoNaskhArabic-Bold.ttf'])
    latin_bold = find_font(['NotoSans-Bold.ttf', 'DejaVuSans-Bold.ttf'])

    frames = []
    for i, scene in enumerate(data['scenes']):
        frame = work / f'scene_{i+1}.png'
        render_scene(scene, i, frame, arabic_regular, arabic_bold, latin_bold)
        frames.append(frame)

    audio = Path(args.audio)
    audio_dur = probe_duration(audio)
    total = max(audio_dur + 1.2, 12.0)
    fade = 0.35
    weights = [0.20, 0.27, 0.28, 0.25]
    durs = [total*w for w in weights]

    clips = []
    for i, (frame, dur) in enumerate(zip(frames, durs)):
        clip = work / f'clip_{i+1}.mp4'
        zoom = "zoompan=z='min(zoom+0.0007,1.06)':d=1:s=1080x1920:fps=30"
        run(['ffmpeg', '-y', '-loop', '1', '-i', str(frame), '-vf', zoom, '-t', f'{dur:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', str(clip)])
        clips.append(clip)

    offsets = []
    cumulative = durs[0]
    offsets.append(cumulative - fade)
    cumulative += durs[1] - fade
    offsets.append(cumulative - fade)
    cumulative += durs[2] - fade
    offsets.append(cumulative - fade)

    filt = (
        f'[0:v][1:v]xfade=transition=slideleft:duration={fade}:offset={offsets[0]:.3f}[v1];'
        f'[v1][2:v]xfade=transition=fade:duration={fade}:offset={offsets[1]:.3f}[v2];'
        f'[v2][3:v]xfade=transition=slideup:duration={fade}:offset={offsets[2]:.3f}[v3]'
    )
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg', '-y']
    for clip in clips:
        cmd += ['-i', str(clip)]
    cmd += ['-i', str(audio), '-filter_complex', filt, '-map', '[v3]', '-map', '4:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-shortest', '-movflags', '+faststart', str(out)]
    run(cmd)
    print(f'Rendered {out} ({W}x{H})')


if __name__ == '__main__':
    main()
