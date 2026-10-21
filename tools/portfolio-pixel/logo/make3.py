from PIL import Image, ImageDraw
exec(open('make2.py').read().split('opts=')[0])
LAV=(0xA7,0x8B,0xFA); DEEP=(0x6D,0x4B,0xE0)
def deco(g,collar=None,ears=None):
    W=len(g[0])
    if ears:
        for (x,y) in [(1,0),(13,0)]: g[y][x]=ears
    if collar:
        for x in range(1,W-1): g[11][x]=collar
    return g
opts=[('A lavender cat, lime collar',lambda:deco(grid(True,INK,LAV),collar=LIME)),
      ('B ink cat, lavender SB, lime ear tips',lambda:deco(grid(True,LAV,INK),ears=LIME)),
      ('C deep purple cat, lime SB',lambda:grid(True,LIME,DEEP))]
out=Image.new('RGB',(3*260,2*220+30),(40,40,48)); d=ImageDraw.Draw(out)
for i,(n,f) in enumerate(opts):
    for j,page in enumerate([INK,PAPER]):
        g=f()
        if n.startswith('B') and page==INK: g=deco(grid(True,DEEP,LAV),ears=LIME)
        out.paste(render(g,page),(i*260+10,j*220+10))
    d.text((i*260+14,2*220+10),n,fill=(220,220,230))
out.save('options3.png')
