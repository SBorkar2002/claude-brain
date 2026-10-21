from PIL import Image, ImageDraw
S=[".####","#....","#....",".###.","....#","....#","####."]
B=["####.","#...#","#...#","####.","#...#","#...#","####."]
LIME=(0xD9,0xF8,0x60); INK=(14,14,20); PAPER=(246,244,252)
def grid(ears, fg, bgc):
    W,H=15,13; g=[[None]*W for _ in range(H)]
    top=2 if ears else 0
    for y in range(top,H if ears else 11):
        for x in range(W):
            corner=(x in(0,W-1)) and (y in(top,(H if ears else 11)-1))
            if not corner: g[y][x]=bgc
    if ears:
        for (x,y) in [(1,0),(1,1),(2,1),(13,0),(13,1),(12,1)]: g[y][x]=bgc
    oy=top+2
    for y,r in enumerate(S):
        for x,c in enumerate(r):
            if c=='#': g[oy+y][2+x]=fg
    for y,r in enumerate(B):
        for x,c in enumerate(r):
            if c=='#': g[oy+y][8+x]=fg
    return g
def render(g,page,sc=12):
    H=len(g);W=len(g[0]); im=Image.new('RGB',(240,200),page); d=ImageDraw.Draw(im)
    ox=(240-W*sc)//2; oy=(200-H*sc)//2
    for y in range(H):
        for x in range(W):
            if g[y][x]: d.rectangle([ox+x*sc,oy+y*sc,ox+(x+1)*sc-1,oy+(y+1)*sc-1],fill=g[y][x])
    return im
opts=[('1 lime badge',lambda:grid(False,INK,LIME)),('2 lime cat badge',lambda:grid(True,INK,LIME)),('3 ink cat badge',lambda:grid(True,LIME,INK))]
out=Image.new('RGB',(3*260,2*220+30),(40,40,48)); d=ImageDraw.Draw(out)
for i,(n,f) in enumerate(opts):
    for j,page in enumerate([INK,PAPER]):
        g=f()
        if n.startswith('3') and page==INK:  # keep visible on dark: add lime outline
            g=grid(True,INK,PAPER)
        out.paste(render(g,page),(i*260+10,j*220+10))
    d.text((i*260+14,2*220+10),n,fill=(220,220,230))
out.save('options2.png')
