from PIL import Image, ImageDraw
S=[".####","#....","#....",".###.","....#","....#","####."]
B=["####.","#...#","#...#","####.","#...#","#...#","####."]
LIME=(0xD9,0xF8,0x60); INK=(14,14,20); PAPER=(246,244,252); LAV=(0xA7,0x8B,0xFA); DEEP=(0x5B,0x3D,0xD0); YEL=(255,200,40)
M=4  # side margin for whiskers
def build(body,letter,earin,whisk,style,bell=False):
    W,H=15+2*M,15; g=[[None]*W for _ in range(H)]
    for y in range(2,13):
        for x in range(15):
            if (x in(0,14)) and (y in(2,12)): continue
            g[y][x+M]=body
    for (x,y) in [(1,0),(1,1),(2,1),(13,0),(13,1),(12,1)]: g[y][x+M]=body
    if earin:  # inner ear pixel
        g[1][1+M]=earin; g[1][13+M]=earin
    for y,r in enumerate(S):
        for x,c in enumerate(r):
            if c=='#': g[4+y][2+x+M]=letter
    for y,r in enumerate(B):
        for x,c in enumerate(r):
            if c=='#': g[4+y][8+x+M]=letter
    # whiskers
    if style=='flat':
        for y in (6,8):
            for x in range(0,M-1): g[y][x]=whisk; g[y][W-1-x]=whisk
    else:  # fanned
        for x,y in [(2,6),(1,5),(0,5),(2,8),(1,9),(0,9),(2,7),(1,7),(0,7)]:
            g[y][x]=whisk; g[y][W-1-x]=whisk
    if bell:
        g[13][7+M]=YEL; g[13][8+M]=YEL if False else YEL; g[14][7+M]=YEL
    return g
def render(g,page,sc=11):
    H=len(g);W=len(g[0]); im=Image.new('RGB',(260,200),page); d=ImageDraw.Draw(im)
    ox=(260-W*sc)//2; oy=(200-H*sc)//2
    for y in range(H):
        for x in range(W):
            if g[y][x]: d.rectangle([ox+x*sc,oy+y*sc,ox+(x+1)*sc-1,oy+(y+1)*sc-1],fill=g[y][x])
    return im
# (name, light-page version, dark-page version)
opts=[('B1 flat whiskers',build(INK,LAV,LIME,INK,'flat'),build(LAV,DEEP,LIME,LAV,'flat')),
      ('B2 fanned whiskers',build(INK,LAV,LIME,INK,'fan'),build(LAV,DEEP,LIME,LAV,'fan')),
      ('B3 fanned, lime whiskers + bell',build(INK,LAV,LIME,LIME,'fan',bell=True),build(LAV,DEEP,LIME,LIME,'fan',bell=True))]
out=Image.new('RGB',(3*280,2*220+30),(40,40,48)); d=ImageDraw.Draw(out)
for i,(n,lg,dg) in enumerate(opts):
    out.paste(render(dg,INK),(i*280+10,10)); out.paste(render(lg,PAPER),(i*280+10,230))
    d.text((i*280+14,450),n,fill=(220,220,230))
out.save('options4.png')
