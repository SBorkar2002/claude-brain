import sys; sys.path.insert(0, '.')
from PIL import Image, ImageDraw
import accessories as A, sprites as S, render as R
base, cells, clash = A.compute()
combos = [[], ['hat'], ['tie'], ['glasses'], ['bow'], ['tie', 'glasses', 'bow'], ['tie', 'glasses', 'hat']]
theme = sys.argv[2]; pal = R.THEMES[theme]

states = [s for s in base if s != 'Shadow']
sc = 3; cw = 48 * sc + 4
frames = [(st, i) for st in states for i in range(len(base[st]))]
img = Image.new('RGB', (len(combos) * cw + 90, len(frames) * cw), (60, 60, 60))
d = ImageDraw.Draw(img)
for fi, (st, i) in enumerate(frames):
    d.text((2, fi * cw + 4), f"{st} {i+1}", fill=(230, 230, 230))
    for ci, combo in enumerate(combos):
        layers = [cells[n][st][i] for n in A.NAMES if n in combo]
        g = A.composite(base[st][i], layers)
        img.paste(R.frame_img(g, pal, sc), (90 + ci * cw, fi * cw))
img.save(sys.argv[1])
