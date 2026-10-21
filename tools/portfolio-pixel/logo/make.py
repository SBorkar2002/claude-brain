from PIL import Image, ImageDraw
S=[".####","#....","#....",".###.","....#","....#","####."]
B=["####.","#...#","#...#","####.","#...#","#...#","####."]
def letters(ox,oy):
    px={}
    for y,r in enumerate(S):
        for x,c in enumerate(r):
            if c=='#': px[(ox+x,oy+y)]='ink'
    for y,r in enumerate(B):
        for x,c in enumerate(r):
            if c=='#': px[(ox+6+x,oy+y)]='ink'
    return px
def A():  # cat ears on top
    p=letters(1,3); W,H=13,11
    for e in [(1,1),(1,2),(2,2),(9,1),(9,2),(8,2)]: p[e]='ink'
    p[(10,2)]='ink'; p[(10,1)]='ink'; p[(2,1)]=None
    for k in [k for k,v in p.items() if v is None]: del p[k]
    return W,H,p,None
def Bd(): # lime badge
    p=letters(2,2); return 15,11,p,'lime'
def C():  # B counters = yellow eyes, ears
    p=letters(1,3)
    p[(9,5)]='eye'; p[(9,8)]='eye'
    for e in [(7,1),(7,2),(8,2),(11,1),(11,2),(10,2)]: p[e]='ink'
    return 13,11,p,None
def render(spec,ink,bg,scale=14):
    W,H,p,badge=spec
    im=Image.new('RGB',(W*scale,H*scale),bg); d=ImageDraw.Draw(im)
    if badge: d.rectangle([scale,0,(W-1)*scale-1,H*scale-1],fill=(0xD9,0xF8,0x60)); d.rectangle([0,scale,W*scale-1,(H-1)*scale-1],fill=(0xD9,0xF8,0x60)); ink=(14,14,20)
    for (x,y),v in p.items():
        col={'ink':ink,'eye':(255,200,40)}[v]
        d.rectangle([x*scale,y*scale,(x+1)*scale-1,(y+1)*scale-1],fill=col)
    return im
specs=[('A ears',A()),('B lime badge',Bd()),('C cat-eye B',C())]
dark=(14,14,20); light=(246,244,252)
rows=[]
out=Image.new('RGB',(3*260,2*200+40),(40,40,48)); d=ImageDraw.Draw(out)
for i,(n,s) in enumerate(specs):
    for j,(ink,bg) in enumerate([((246,244,252),dark),((14,14,20),light)]):
        im=render(s,ink,bg); bgim=Image.new('RGB',(240,180),bg); bgim.paste(im,((240-im.width)//2,(180-im.height)//2))
        out.paste(bgim,(i*260+10,j*200+10))
    d.text((i*260+14,2*200+14),n,fill=(220,220,230))
out.save('options.png'); print('ok')
