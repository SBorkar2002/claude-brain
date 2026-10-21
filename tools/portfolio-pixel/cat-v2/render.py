"""Preview Cat v2: sheet (both colourways, every frame), a 1x strip, animated GIFs per state, JSON export.
Usage: python3 render.py [out_dir]   (defaults to ./preview)
Colours are the Figma variable values (Portfolio · Color, cat/*), so the preview matches Dark and Light modes.
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sprites import FRAMES, TIMINGS, W, H
from PIL import Image, ImageDraw

THEMES = {
    'light': {'bg': (243, 240, 250), '#': (23, 20, 31), 'f': (66, 59, 84), 'l': (58, 52, 74), 's': (217, 211, 232), 'g': (217, 248, 96), 'Y': (255, 212, 59), 'p': (23, 20, 31), 'w': (255, 255, 255),
              'm': (255, 143, 177), 'M': (196, 69, 110), 'z': (143, 123, 255), 'h': (255, 111, 156),
              'H': (91, 61, 208), 'b': (167, 139, 250), 'k': (242, 239, 250)},
    'dark':  {'bg': (21, 19, 28), '#': (242, 239, 250), 'f': (190, 183, 210), 'l': (255, 255, 255), 's': (11, 10, 16), 'g': (217, 248, 96), 'Y': (255, 212, 59), 'p': (21, 19, 28), 'w': (255, 255, 255),
              'm': (255, 143, 177), 'M': (196, 69, 110), 'z': (195, 181, 255), 'h': (255, 143, 177),
              'H': (91, 61, 208), 'b': (167, 139, 250), 'k': (23, 20, 31)},
}


def frame_img(g, pal, scale):
    img = Image.new('RGB', (W, H), pal['bg'])
    px = img.load()
    for r in range(H):
        for c in range(W):
            k = g[r][c]
            if k != '.':
                px[c, r] = pal[k]
    return img.resize((W * scale, H * scale), Image.NEAREST)


def sheet(out, scale=4):
    pad, label = 12, 18
    maxn = max(len(v) for v in FRAMES.values())
    cw, ch = W * scale + pad, H * scale + pad + label
    img = Image.new('RGB', (pad + 2 * maxn * cw + 40, pad + len(FRAMES) * ch), (60, 60, 60))
    d = ImageDraw.Draw(img)
    for ti, (tname, pal) in enumerate(THEMES.items()):
        ox = pad + ti * (maxn * cw + 40)
        for si, (state, frames) in enumerate(FRAMES.items()):
            for fi, g in enumerate(frames):
                x0, y0 = ox + fi * cw, pad + si * ch
                img.paste(frame_img(g, pal, scale), (x0, y0 + label))
                d.text((x0, y0 + 2), f"{state} {fi + 1}  {TIMINGS[state][fi]}s", fill=(230, 230, 230))
    img.save(out)


def strip(out, scale=1):
    frames = [g for st in FRAMES.values() for g in st]
    img = Image.new('RGB', (len(frames) * (W + 4), 2 * (H + 4)), (128, 128, 128))
    for row, pal in enumerate(THEMES.values()):
        for i, g in enumerate(frames):
            img.paste(frame_img(g, pal, 1), (i * (W + 4) + 2, row * (H + 4) + 2))
    img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    img.save(out)


def gifs(out_dir, scale=4):
    for tname, pal in THEMES.items():
        for state, frames in FRAMES.items():
            imgs = [frame_img(g, pal, scale) for g in frames]
            durs = [int(t * 1000) for t in TIMINGS[state]]
            imgs[0].save(os.path.join(out_dir, f"{state.lower()}-{tname}.gif"), save_all=True,
                         append_images=imgs[1:], duration=durs, loop=0, disposal=2)


def export(out):
    data = {state: [["".join(r) for r in g] for g in frames] for state, frames in FRAMES.items()}
    import accessories
    json.dump(accessories.export_into({'size': W, 'frames': data, 'timings': TIMINGS}), open(out, 'w'))


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'preview')
    os.makedirs(out_dir, exist_ok=True)
    sheet(os.path.join(out_dir, 'sheet-4x.png'))
    strip(os.path.join(out_dir, 'strip-1x.png'), 1)
    strip(os.path.join(out_dir, 'strip-2x.png'), 2)
    gifs(out_dir)
    export(os.path.join(out_dir, 'frames.json'))
    print('ok', sum(len(v) for v in FRAMES.values()), 'frames')
