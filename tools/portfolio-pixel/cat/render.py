import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from sprites import FRAMES, W, H
from PIL import Image, ImageDraw
THEMES = {
    'light': {'bg': (243, 240, 250), '#': (23, 20, 31), 'Y': (255, 212, 59), 'p': (23, 20, 31), 'w': (255, 255, 255), 'm': (255, 143, 177), 'M': (196, 69, 110), 'z': (157, 140, 255), 'h': (255, 120, 160)},
    'dark':  {'bg': (21, 19, 28), '#': (242, 239, 250), 'Y': (255, 212, 59), 'p': (21, 19, 28), 'w': (255, 255, 255), 'm': (255, 143, 177), 'M': (196, 69, 110), 'z': (195, 181, 255), 'h': (255, 143, 177)},
}
S = 6; PAD = 12; LABEL = 18
def render(out):
    maxn = max(len(v) for v in FRAMES.values())
    cw = W * S + PAD; ch = H * S + PAD + LABEL
    img = Image.new('RGB', (PAD + 2 * maxn * cw + 40, PAD + len(FRAMES) * ch), (60, 60, 60))
    d = ImageDraw.Draw(img)
    for ti, (tname, pal) in enumerate(THEMES.items()):
        ox = PAD + ti * (maxn * cw + 40)
        for si, (state, frames) in enumerate(FRAMES.items()):
            for fi, g in enumerate(frames):
                x0 = ox + fi * cw; y0 = PAD + si * ch
                d.rectangle([x0, y0 + LABEL, x0 + W * S - 1, y0 + LABEL + H * S - 1], fill=pal['bg'])
                for r in range(H):
                    for c in range(W):
                        k = g[r][c]
                        if k != '.':
                            d.rectangle([x0 + c * S, y0 + LABEL + r * S, x0 + c * S + S - 1, y0 + LABEL + r * S + S - 1], fill=pal[k])
                d.text((x0, y0 + 2), f"{state} {fi+1}", fill=(230, 230, 230))
    img.save(out)
def export(out):
    data = {state: [["".join(r) for r in g] for g in frames] for state, frames in FRAMES.items()}
    json.dump(data, open(out, 'w'))
if __name__ == '__main__':
    render(sys.argv[1]); export(sys.argv[2])
