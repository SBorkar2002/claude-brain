"""EP003 -- build every plate the composition needs, from the raw Figma exports.

  sceneN.png        raw export, captions and SFX lettering baked in
  cleanN.png        both removed, so they can be drawn live and animated
  cleanN_open/_shut mouth variants, decided by INK not by assumption
  clean11_{oo,os,so,ss}  the two-shot, where each mouth moves independently

Re-runnable: it always starts from sceneN.png.
"""
import numpy as np, os
from PIL import Image
P = "public/rc/plates/"
L = lambda n: np.asarray(Image.open(P+n+".png").convert("L"))
RGB = lambda n: Image.open(P+n+".png").convert("RGB")

# ---- 1. dialogue captions, drawn live so they can carry the words the VO says
TXT = {1:(236,255,249,38),2:(236,255,249,38),3:(236,255,249,38),4:(96,255,529,38),
 5:(111,553,498,38),7:(120,255,481,38),8:(137,255,446,38),9:(137,255,446,38),
 10:(123,255,474,38),11:(327,255,66,38),12:(-63,543,498,38),13:(156,561,498,38),
 14:(123,255,474,38),15:(349,255,23,38),16:(349,255,23,38),17:(118,255,485,38),
 18:(171,255,379,38),19:(311,255,98,38),20:(92,1032,66,38),21:(28,1036,72,38),
 22:(92,262,535,76),23:(92,262,535,76),24:(92,262,535,76),25:(58,227,605,76),
 26:(58,227,605,38),27:(58,227,605,38),28:(301,255,118,38)}
SCENE6 = [(58,634,178,662),(58,660,204,708)]     # its box runs off-frame past the monitor

# NOTE: scene11/14/15 are re-exported from Figma with their "ping" text nodes
# hidden, so the SFX lettering can be drawn live and animated on its own sound
# (comic-animation.md). Nothing to strip here.

def fill_flat(a, box):
    x0,y0,x1,y1 = box
    strip = np.concatenate([a[max(0,y0-10):y0-2, x0:x1].reshape(-1,3),
                            a[y1+2:y1+10, x0:x1].reshape(-1,3)])
    a[y0:y1, x0:x1] = np.median(strip, axis=0).astype(np.uint8)

for i in range(1, 29):
    a = np.asarray(RGB("scene%d"%i)).copy()
    if i == 6:
        for b in SCENE6: fill_flat(a, b)
    else:
        x,y,w,h = TXT[i]
        fill_flat(a, (max(0,int(x*1.5)-14), int(y*1.5)-12,
                      min(1080,int((x+w)*1.5)+14), int((y+h)*1.5)+14))
    Image.fromarray(a).save(P+"clean%d.png"%i)

# ---- 2c. scene24.5 / 24.6 -- the catch. Same shot twice: 24.5 is her staring
#        with her mouth shut (the beat), 24.6 is her talking. Both have their
#        caption node hidden in Figma, so they copy straight through and then
#        become an open/shut PAIR for the question. 24.7 is his nervous-laugh
#        beat -- as drawn it renders identical to 24.5, so it reads as her
#        holding the same flat stare while he laughs.
for n in ("245", "246", "247"):
    Image.open(P+"scene%s.png"%n).convert("RGB").save(P+"clean%s.png"%n)

# ---- 3. mouth variants. Which frame is OPEN is decided by ink: an open mouth
#        is a filled oval, a closed one a thin line.
def ink(n, box):
    y0,y1,x0,x1 = box
    return int((L(n)[y0:y1, x0:x1] < 120).sum())
def pair(a, b, box):
    return (a,b) if ink(a,box) > ink(b,box) else (b,a)
def crop(n, box):
    y0,y1,x0,x1 = box
    return RGB(n).crop((x0,y0,x1,y1))
HER2=(867,903,249,309); HER3=(878,905,255,306)
HIM_2S=(848,880,767,823); HIM_CU=(1348,1425,398,572); HIM_89=(1103,1157,382,499)
def build(scenes, box, a, b):
    o,s = pair(a,b,box); y0,y1,x0,x1 = box
    co,cs = crop(o,box), crop(s,box)
    for i in scenes:
        for tag,src in (("open",co),("shut",cs)):
            im = RGB("clean%s"%i); im.paste(src,(x0,y0)); im.save(P+"clean%s_%s.png"%(i,tag))
    return o,s
build(["1","3","7","10","14","15","16","17"], HER2,  "scene1","scene2")
build(["22","23","24"],                        HER3,  "scene22","scene23")
build(["8","9"],                               HIM_89,"scene8","scene9")
build(["20","21"],                             HIM_CU,"scene20","scene21")
HER245=(873,905,254,306)
build(["246"],                                 HER245,"scene246","scene245")
# 24.7 is the same two-shot with PETER's mouth open -- his nervous laugh. Same
# box as the scene11 two-shot, and pair() measures which is which.
build(["247"],                                 HIM_2S,"scene247","scene245")
ho,hs = pair("scene11","scene10",HIM_2S); mo,ms = pair("scene1","scene2",HER2)
hy0,hy1,hx0,hx1 = HIM_2S; my0,my1,mx0,mx1 = HER2
cho,chs = crop(ho,HIM_2S), crop(hs,HIM_2S)
cmo,cms = crop(mo,HER2),   crop(ms,HER2)
for her in (True,False):
    for him in (True,False):
        im = RGB("clean11")
        im.paste(cmo if her else cms,(mx0,my0)); im.paste(cho if him else chs,(hx0,hy0))
        im.save(P+"clean11_%s%s.png"%("o" if her else "s","o" if him else "s"))
# ---- 2b. scene4.5 -- the bridge frame. The drawn "..." meant "he says
#        nothing"; he now thinks "wait. i can just remote control it." over it,
#        so it is masked like any other baked caption. It also sat directly
#        above the live one.
a = np.asarray(RGB("scene45")).copy()
x,y,w,h = (349,255,23,38)
fill_flat(a, (max(0,int(x*1.5)-14), int(y*1.5)-12,
              min(1080,int((x+w)*1.5)+14), int((y+h)*1.5)+14))
Image.fromarray(a).save(P+"clean45.png")

print("plates rebuilt:", len([f for f in os.listdir(P) if f.startswith("clean")]))
print("  her two-shot open <- %s   him two-shot open <- %s" % (mo, ho))
