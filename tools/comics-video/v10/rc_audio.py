import subprocess, numpy as np, os, json
OUT="public/rc"; T="/tmp/rcparts"; M=T+"/mono_fast.wav"; TL=T+"/tail_fast.wav"
NEW="/Users/sejal/Downloads/ElevenLabs_2026-09-22T07_51_51_Vanessa - Beach Girl_pvc_sp100_s50_sb75_v3.mp3"
TEMPO=1.15; K=1.4/TEMPO          # all cut points are held in 1.4x time and scaled
def run(a): subprocess.run(a,check=True,capture_output=True)
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
def sil(d,p): run(["ffmpeg","-v","error","-y","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t","%.3f"%d,p])
def seg(src,a,b,dst):
    run(["ffmpeg","-v","error","-y","-ss","%.3f"%a,"-t","%.3f"%(b-a),"-i",src,"-ac","1","-ar","44100",
         "-af","afade=t=in:st=0:d=0.010,afade=t=out:st=%.3f:d=0.010"%max(0,(b-a)-0.010),dst])
def cat(ps,d):
    open("/tmp/_n.txt","w").write("".join("file '%s'\n"%p for p in ps))
    run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","/tmp/_n.txt","-c","copy",d])
D=json.load(open("/tmp/rc_durs.json"))
N1="/Users/sejal/Downloads/ElevenLabs_2026-09-22T14_31_17_Vanessa - Beach Girl_pvc_sp100_s50_sb75_v3.mp3"
N2="/Users/sejal/Downloads/ElevenLabs_2026-09-22T14_33_49_Vanessa - Beach Girl_pvc_sp100_s50_sb75_v3.mp3"
def tseg(src,a,b,dst,gain=0.0,tempo=None):
    """`tempo` overrides the episode tempo for ONE take. A single multiplier
    does not equalise delivery: ElevenLabs picks its own pace per generation,
    so a take can sit at the right tempo and still sound slower than the take
    beside it. Measure syllables/sec across the track before using this."""
    tp = tempo or TEMPO
    run(["ffmpeg","-v","error","-y","-ss","%.3f"%a,"-t","%.3f"%(b-a),"-i",src,"-ac","1","-ar","44100",
         "-af","atempo=%.4f,volume=%.2fdB,afade=t=in:st=0:d=0.010,afade=t=out:st=%.3f:d=0.012"%(
             tp,gain,((b-a)/tp)-0.012),dst])
# THE LOOP TAKE. One recording, cut THREE ways: the last thing in the film and
# the first thing in the film are halves of one sentence over the same plate, so
# they have to come from the same generation or her pitch steps across the join.
# The third piece follows 0.26s later with nothing to hide a mismatch behind.
#   0.00-1.81  "oh yeah, as i was saying.."   -> the LAST panel
#   1.81-3.81  "my sister just books the whole thing."  -> the FIRST panel
#   3.81-5.24  "doesn't ask anyone."          -> panel 3
# Both cuts land mid-gap (0.40s and 0.30s of silence). +4.9dB to match the take
# it replaces.
N8="/Users/sejal/Downloads/ElevenLabs_2026-09-23T17_37_51_Vanessa - Beach Girl_pvc_sp100_s50_sb75_v3.mp3"
tseg(N8, 0.00, 1.81, T+"/NEWCLOSE.wav", 4.9)
tseg(N8, 1.81, 3.81, T+"/NEWOPEN.wav",  4.9)
# From "doesn't ask anyone" the OLD take carries on, because she is not supposed
# to go silent while Peter works. Her 1am beat is the old take's longer version
# of it, so nothing is said twice.
tseg(N8, 3.81, 5.24, T+"/M2a.wav",      4.9)
tseg(N2, 0.00, 3.16, T+"/M3a.wav", -2.7)        # OH MY GOD you guessed it right
# ONE unbroken run all the way through the 1am confirmation -- she does not
# pause mid-anecdote. The only silence comes AFTER "like it's completely
# normal.", so "and you know what she did next??" arrives on its own.
seg(M,  7.95, 14.30, T+"/M2c1.wav")   # doesn't say a word .. completely normal.
sil(3.10, T+"/gb.wav")   # +0.75 buys room for his remote-control beat; the
                         # silence still falls ONLY while he is talking
seg(M, 14.30, 16.20, T+"/M2c2.wav")   # and you know what she did next??
run(["ffmpeg","-v","error","-y","-ss","17.80","-t","%.3f"%(22.71-17.80),"-i",M,"-ac","1","-ar","44100",
     "-af","afade=t=in:st=0:d=0.010,afade=t=out:st=%.3f:d=0.020"%((22.71-17.80)-0.020),T+"/M3b.wav"])
sil(0.26,T+"/g1.wav"); sil(0.18,T+"/g2.wav")
seg(M,  5.060*K, 13.305*K, T+"/M2_old.wav")
# ONE continuous line -- she does not pause for him. His "right." goes on top
# and she is ducked under it, so he never actually gets a turn.

seg(TL, 0.00,     1.71*K,  T+"/T1.wav")
seg(TL, 1.71*K,   2.39*K,  T+"/T2.wav")
N3="/Users/sejal/Downloads/ElevenLabs_2026-09-23T08_45_55_Vanessa - Beach Girl_pvc_sp100_s50_sb75_v3.mp3"
# NEW take of "oh, hold on. my AI just finished raising my PR. been remote
# controlling it since the appetisers." -- whole file, her words run to 6.55
# and the decay to 6.58. -1.5dB puts it where the take it replaces sat.
N5="/Users/sejal/Downloads/ElevenLabs_2026-09-23T09_03_10_Vanessa - Beach Girl_pvc_sp100_s50_sb75_v3.mp3"
tseg(N5, 0.00,   6.58,     T+"/T3a.wav", -1.5)
# "well.. it's on auto mode and only pings me when it's done." -- the setup the
# punchline needs. Take the WHOLE file: her words end at 3.84 and the decay
# runs to 3.99, and a segment split never lands inside a tail (comic-audio.md).
# +0.6dB, which is what this take needs to sit where the old one sat.
# 1.28x, not 1.15x: this take was DELIVERED 30% slower than T3a and T3b either
# side of it (4.15 syl/s against 5.42 and 5.62), which reads as the voice
# changing mid-block. 1.28 closes most of that without making her sound rushed.
tseg(N3, 0.00,   4.05,     T+"/T3p.wav", 0.6, tempo=1.28)
sil(0.22, T+"/gq.wav"); sil(0.90, T+"/gp.wav")                        # a beat before "i mean, only a noob"
# "i mean, only a noob sits there approving every single step." -- ONLY a noob,
# not WHICH noob: a verdict, not a question. Captioned "noob", plain. This take
# leads in after 0.14s so it plays whole; the pause before it is `gp`.
# +4.4dB puts it at the level the previous take sat at (-21.3 dBFS).
N7="/Users/sejal/Downloads/ElevenLabs_2026-09-23T15_05_58_Vanessa - Beach Girl_pvc_sp100_s50_sb75_v3.mp3"
tseg(N7, 0.00,    3.68,     T+"/T3b.wav", 4.4)
# THE CATCH. A ping gives him away and she starts to join it up. Her line is
# +3.9dB puts it level with the rest of her.
N6="/Users/sejal/Downloads/ElevenLabs_2026-09-23T13_42_59_Vanessa - Beach Girl_pvc_sp100_s50_sb75_v3.mp3"
# The beat: she looks up, his ping lands, and she stares at him before she
# says anything. The pause is the joke, so it is long -- 0.75s, then the ping,
# then a second and a half of her just looking at him.
sil(2.65, T+"/gc.wav")
# She is CUT OFF at "every" -- Peter interrupts. 1.92s: "every" lands whole and
# "step" never starts. (1.82 sounded right on the envelope but severs the "-y";
# transcribing each candidate cut is what settled it.) The fade is 4ms -- just
# enough to stop a click and nothing more. The loop episode got this by having
# the AI take RECORDED already severed; here the take is whole, so the cut has
# to do it, and anything longer than a few ms reads as a fade rather than an
# interruption.
run(["ffmpeg","-v","error","-y","-ss","0.00","-t","1.92","-i",N6,"-ac","1","-ar","44100",
     "-af","atempo=%.4f,volume=3.9dB,afade=t=in:st=0:d=0.010,afade=t=out:st=%.3f:d=0.004"
     % (TEMPO, (1.92/TEMPO)-0.004), T+"/T4.wav"])
G=lambda c,l,t: round(l+D[c]+t,2)
gaps={"Sb": G("peter_p06.wav",0.35,0.35),
      "S11":G("peter_p11.wav",0.40,0.40),
      "Sp": 1.80, "Sc": G("peter_p14.wav",0.40,0.45), "Sq": 2.70}
for k,v in gaps.items(): sil(v,T+"/%s.wav"%k)
# NOTE: no gap before "Permission to push?" any more -- it plays OVER M3b, which
# drops to background underneath it.
order=["M2a","g1","M2c1","gb","M2c2","Sb","M3a","g2","M3b","S11","Sp","T1","Sc","T2","Sq","T3a","gq","T3p","gp","T3b","gc","T4"]
cat([T+"/%s.wav"%n for n in order],T+"/dm8.wav")
run(["ffmpeg","-v","error","-y","-i",T+"/dm8.wav","-af","volume=-2dB","-ac","1","-ar","44100",OUT+"/date_main.wav"])
run(["ffmpeg","-v","error","-y","-i",T+"/NEWOPEN.wav","-af","volume=-2dB","-ac","1","-ar","44100",OUT+"/loop_open.wav"])
run(["ffmpeg","-v","error","-y","-i",T+"/NEWCLOSE.wav","-af","volume=-2dB","-ac","1","-ar","44100",OUT+"/loop_close.wav"])
D["loop_open.wav"]=dur(OUT+"/loop_open.wav"); D["loop_close.wav"]=dur(OUT+"/loop_close.wav")
# ------------------------------------------------- Peter's remote-control beat
# "Wait, [0.83s] I can just remote control it." -- the episode's term, on the
# man doing it, at the moment he decides to. Played WHOLE: the pause between
# the two halves is the take's own, and it is what the push-in moves under.
P03SRC="/Users/sejal/Downloads/ElevenLabs_2026-09-23T16_09_32_Eric - Uninterested and Fast_pvc_sp100_s50_sb75_v3.mp3"
run(["ffmpeg","-v","error","-y","-i",P03SRC,"-ac","1","-ar","44100",
     "-af","atempo=1.10,volume=1.6dB,afade=t=in:st=0:d=0.010,afade=t=out:st=%.3f:d=0.020"
     % ((dur(P03SRC)/1.10)-0.020), OUT+"/peter_p03.wav"])
D["peter_p03.wav"]=dur(OUT+"/peter_p03.wav")

# ------------------------------------------------- Peter's last line
# "Your sister! [nervous laugh] What did your sister do next?" -- ONE take,
# played whole. The three parts get three different frames, but the audio is
# never cut: the pause between the laugh and the question is the take's own
# and splicing it would only make the join audible.
P20SRC="/Users/sejal/Downloads/ElevenLabs_2026-09-23T14_29_48_Eric - Uninterested and Fast_pvc_sp100_s50_sb75_v3.mp3"
PT=1.10                       # Peter's tempo, measured 1.081x / 1.090x on the
                              # two Eric lines already in the film
run(["ffmpeg","-v","error","-y","-i",P20SRC,"-ac","1","-ar","44100",
     "-af","atempo=%.4f,volume=-1.6dB,afade=t=in:st=0:d=0.010,afade=t=out:st=%.3f:d=0.020"
     % (PT, (dur(P20SRC)/PT)-0.020), OUT+"/peter_p20.wav"])
D["peter_p20.wav"]=dur(OUT+"/peter_p20.wav")
json.dump(D, open("/tmp/rc_durs.json","w"), indent=1)
print("peter_p20 %.2fs at %.2fx" % (D["peter_p20.wav"], PT))

t=0.0; A={}
for n in order:
    d=dur(T+"/%s.wav"%n); A[n]=(round(t,3),round(t+d,3)); t+=d
json.dump(A,open("/tmp/anchors.json","w"))
print("date_main %.2fs  (her VO at %.2fx)"%(t,TEMPO))
for n in order: print("  %-4s %6.2f -> %6.2f  (%5.2f)"%(n,A[n][0],A[n][1],A[n][1]-A[n][0]))
