#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 30
WHITE = (255, 255, 255)
MINT = (60, 210, 171)
GOLD = (246, 185, 74)
DARK = (7, 18, 27)


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
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    px = ov.load()
    for y in range(H):
        if y < 720:
            a = int(45 * (1 - y / 720))
        elif y > 900:
            a = int(205 * min(1, (y - 900) / 800))
        else:
            a = 30
        for x in range(W):
            px[x, y] = (3, 12, 18, a)
    return Image.alpha_composite(img.convert('RGBA'), ov)


def wrap_rtl(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], []
    for word in words:
        test = ' '.join(cur + [word])
        if draw.textbbox((0, 0), test, font=font)[2] > max_width and cur:
            lines.append(' '.join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(' '.join(cur))
    return lines


def render_scene(scene, idx, assets, logo, out_path, arabic_regular, arabic_bold, latin_bold):
    bg_path = assets / scene['background']
    if not bg_path.exists():
        raise FileNotFoundError(bg_path)
    bg = Image.open(bg_path).convert('RGB')
    bg = cover_crop(bg, focus_x=scene.get('focus_x', 0.5), focus_y=scene.get('focus_y', 0.5))
    bg = ImageEnhance.Contrast(bg).enhance(1.05)
    bg = ImageEnhance.Color(bg).enhance(0.94)
    canvas = overlay_gradient(bg)
    draw = ImageDraw.Draw(canvas)

    # Real brand mark top-left.
    mark = logo.copy().convert('RGBA')
    mark.thumbnail((150, 150), Image.Resampling.LANCZOS)
    badge = Image.new('RGBA', (196, 196), (255, 255, 255, 235))
    badge = badge.filter(ImageFilter.GaussianBlur(0.25))
    mask = Image.new('L', badge.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, 195, 195), radius=44, fill=255)
    canvas.alpha_composite(Image.composite(badge, Image.new('RGBA', badge.size), mask), (58, 58))
    canvas.alpha_composite(mark, (58 + (196 - mark.width)//2, 58 + (196 - mark.height)//2))

    # City / category pill.
    pill_text = rtl(scene.get('eyebrow', ''))
    pill_font = ImageFont.truetype(arabic_bold, 44)
    pill_box = draw.textbbox((0, 0), pill_text, font=pill_font)
    pw = min(760, max(260, pill_box[2] - pill_box[0] + 90))
    draw.rounded_rectangle((58, 305, 58 + pw, 392), radius=43, fill=(8, 20, 28, 210))
    draw.text((58 + pw/2, 348), pill_text, font=pill_font, fill=MINT, anchor='mm')

    # Main copy is pushed into lower third for image visibility.
    headline = scene.get('headline', '')
    is_ar = any('\u0600' <= ch <= '\u06ff' for ch in headline)
    htxt = rtl(headline) if is_ar else headline
    hpath = arabic_bold if is_ar else latin_bold
    hfont = fit_font(draw, htxt, hpath, 104, 64, 920)
    draw.text((540, 1260), htxt, font=hfont, fill=WHITE, anchor='mm', stroke_width=3, stroke_fill=(0,0,0,140))

    body = rtl(scene.get('body', ''))
    bfont = fit_font(draw, body, arabic_regular, 58, 38, 900)
    lines = wrap_rtl(draw, body, bfont, 860)
    y = 1395
    for line in lines[:3]:
        draw.text((540, y), line, font=bfont, fill=(238, 244, 244), anchor='mm', stroke_width=2, stroke_fill=(0,0,0,120))
        y += 74

    # Branded CTA rail.
    draw.rounded_rectangle((58, 1650, 1022, 1812), radius=50, fill=(6, 17, 24, 228))
    num_font = ImageFont.truetype(latin_bold, 40)
    brand_font = ImageFont.truetype(latin_bold, 56)
    draw.text((104, 1732), f'{idx+1:02d}', font=num_font, fill=GOLD, anchor='lm')
    draw.text((540, 1732), 'Snay3i.ma', font=brand_font, fill=WHITE, anchor='mm')
    draw.rounded_rectangle((862, 1680, 970, 1785), radius=52, fill=MINT)
    draw.text((916, 1732), '›', font=ImageFont.truetype(latin_bold, 74), fill=DARK, anchor='mm')

    canvas.convert('RGB').save(out_path, quality=95)


def duration(audio):
    p = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(audio)], capture_output=True, text=True, check=True)
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

    ar_reg = find_font(['NotoSansArabic-Regular.ttf','NotoNaskhArabic-Regular.ttf'])
    ar_bold = find_font(['NotoSansArabic-Bold.ttf','NotoNaskhArabic-Bold.ttf'])
    lat_bold = find_font(['NotoSans-Bold.ttf','DejaVuSans-Bold.ttf'])

    frames=[]
    for i, scene in enumerate(data['scenes']):
        p=work/f'scene_{i+1}.jpg'
        render_scene(scene, i, assets, logo, p, ar_reg, ar_bold, lat_bold)
        frames.append(p)

    total=max(duration(Path(args.audio))+1.0, 12.0)
    fade=0.30
    weights=[0.22,0.28,0.27,0.23]
    durs=[total*w for w in weights]
    clips=[]
    for i,(frame,dur) in enumerate(zip(frames,durs)):
        clip=work/f'clip_{i+1}.mp4'
        # Slow Ken Burns motion on actual photography.
        if i % 2 == 0:
            z="zoompan=z='min(zoom+0.0008,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        else:
            z="zoompan=z='if(lte(zoom,1.0),1.08,max(1.0,zoom-0.0007))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        run(['ffmpeg','-y','-loop','1','-i',str(frame),'-vf',z,'-t',f'{dur:.3f}','-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(clip)])
        clips.append(clip)

    o1=durs[0]-fade
    o2=durs[0]+durs[1]-2*fade
    o3=durs[0]+durs[1]+durs[2]-3*fade
    filt=(f'[0:v][1:v]xfade=transition=fade:duration={fade}:offset={o1:.3f}[v1];'
          f'[v1][2:v]xfade=transition=slideleft:duration={fade}:offset={o2:.3f}[v2];'
          f'[v2][3:v]xfade=transition=fade:duration={fade}:offset={o3:.3f}[v3]')
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y']
    for c in clips: cmd += ['-i',str(c)]
    cmd += ['-i',args.audio,'-filter_complex',filt,'-map','[v3]','-map','4:a','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-pix_fmt','yuv420p','-shortest','-movflags','+faststart',str(out)]
    run(cmd)
    print(f'Rendered premium v2: {out}')

if __name__=='__main__':
    main()
