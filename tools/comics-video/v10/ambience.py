#!/usr/bin/env python3
"""
Rebuild public/v10/sfx/amb_track.mp3 — the office bed, pre-rendered whole.

THE PRINTER.  v10/amb_spikes.json lists 19 *instantaneous* transients, and
earlier versions trusted it.  It is the wrong map: the printer is not a click,
it is a ~10 second run (0:35 to 0:45 in the raw, peaking +23 dB over the room
in 2.5-8 kHz), plus shorter runs at 1:04, 1:10, 1:19 and 2:18.  Patching a
quarter-second around each listed click left almost all of it in the film.
This version derives the printer map FROM THE AUDIO — sustained high-frequency
energy relative to the room's own rumble — and cuts the whole run out.

That leaves ~90s of clean room for a ~98s film, so the bed has to repeat.  It
repeats where Sejal said to put it: the material restarts from the beginning at
the night, where the office is silent anyway, so the seam is under a fade to
zero and there is nothing to hear.

Also here:
 - LENGTH: the bed is baked, not looped (a looped <Audio>'s volume callback
   gets loop-relative frames and re-fires the night dip mid-film), so it must
   be regenerated whenever the cut changes length.
 - NIGHT: the office empties with the lights and returns with the daylight.
 - THE LOOP: rendered long, with the overrun crossfaded back over the opening,
   so t=0 continues the last second instead of butting against it.

usage:  python3 v10/ambience.py <total_sec> <night_at> <light_at> [out.mp3]
"""
import numpy as np, subprocess, sys, json

SR   = 44100
RAW  = "public/v10/sfx/ambience_raw.mp3"
SPIK = "v10/amb_spikes.json"
OUT  = "public/v10/sfx/amb_track.mp3"
MARGIN, MINWIN, XF, LOOP_XF = 0.5, 3.0, 0.9, 1.8
DETECT_OVER, VERIFY_OVER = 3.5, 6.0   # cut aggressively, verify at what is audible
TARGET_DB = -30.0

def read(path):
    raw = subprocess.run(["ffmpeg","-v","error","-i",path,"-ac","1","-ar",str(SR),
                          "-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).astype(np.float64)

def hf_runs(x, over=6.0, minlen=0.3, hop=0.1):
    """Stretches where 2.5-8 kHz sits well above the room's 80-500 Hz body.
       That ratio is what separates a printer from a voice or a chair."""
    h=int(hop*SR); m=len(x)//h
    X=np.abs(np.fft.rfft(x[:m*h].reshape(m,h)*np.hanning(h),axis=1))
    f=np.fft.rfftfreq(h,1/SR)
    b=lambda lo,hi: 10*np.log10((X[:,(f>=lo)&(f<hi)]**2).sum(1)+1e-12)
    r=b(2500,8000)-b(80,500); med=np.median(r)
    mask=r>med+over; out=[]; i=0
    while i<len(mask):
        if mask[i]:
            j=i
            while j<len(mask) and mask[j]: j+=1
            if (j-i)*hop>=minlen: out.append((i*hop,(j)*hop,float((r[i:j]-med).max())))
            i=j
        else: i+=1
    return out

def clean_windows(x):
    dur=len(x)/SR
    bad=[[a,b] for a,b,_ in hf_runs(x, over=DETECT_OVER)] + [[a,b] for a,b,_ in json.load(open(SPIK))]
    bad=sorted([max(0,a-MARGIN), min(dur,b+MARGIN)] for a,b in bad)
    merged=[]
    for a,b in bad:
        if merged and a<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],b)
        else: merged.append([a,b])
    out=[]; prev=0.0
    for a,b in merged:
        if a-prev>=MINWIN: out.append((prev,a))
        prev=b
    if dur-prev>=MINWIN: out.append((prev,dur))
    return out, merged

def splice(chunks, n, start=0):
    """Windows laid end to end with equal-power crossfades, wrapping if needed."""
    x=int(XF*SR); out=np.zeros(n+SR*60); pos=0; i=start
    while pos<n:
        seg=chunks[i%len(chunks)]; i+=1
        if pos>0:
            f=np.linspace(0,1,x)
            out[pos:pos+x]=out[pos:pos+x]*np.cos(f*np.pi/2)+seg[:x]*np.sin(f*np.pi/2)
            out[pos+x:pos+len(seg)]=seg[x:]
        else: out[:len(seg)]=seg
        pos+=len(seg)-x
    return out[:n]

def main():
    total, night_at, light_at = (float(a) for a in sys.argv[1:4])
    global OUT
    if len(sys.argv) > 4: OUT = sys.argv[4]   # optional output path (default: graph's track)
    n, xl = int(total*SR), int(LOOP_XF*SR)
    raw = read(RAW)
    runs = hf_runs(raw, over=DETECT_OVER)
    wins, cut = clean_windows(raw)

    chunks=[raw[int(a*SR):int(b*SR)].copy() for a,b in wins]
    rms=np.array([np.sqrt((c**2).mean()) for c in chunks]); med=np.median(rms)
    chunks=[c*(med/r) for c,r in zip(chunks,rms)]

    # Two passes over the same clean material, restarting at the night — the
    # only place in the film where a repeat cannot be heard, because there is
    # nothing playing there.
    join = int((light_at-0.6)*SR)
    head = splice(chunks, int(light_at*SR))
    # Which window the second pass opens on decides what sits at the loop point.
    # Pick the one whose level either side of the seam matches, or the film ends
    # louder (or quieter) than it begins and the loop steps even though the
    # waveform is continuous.
    best=None
    for st in range(len(chunks)):
        cand = splice(chunks, (n+xl)-join, st)
        s0 = np.zeros(n+xl); s0[:int(light_at*SR)] = head; s0[join:] = cand
        pre  = np.sqrt((s0[n-int(1.2*SR):n]**2).mean())
        post = np.sqrt((s0[n:n+int(1.2*SR)]**2).mean())
        step = abs(20*np.log10((pre+1e-12)/(post+1e-12)))
        if best is None or step < best[0]: best = (step, st, s0)
    seam_step, seam_start, stream = best

    w=int(6.0*SR); N=len(stream)
    c=np.concatenate([[0.0],np.cumsum(stream**2)])
    lo=np.clip(np.arange(N)-w//2,0,N); hi=np.clip(np.arange(N)+w//2,0,N)
    loud=np.sqrt((c[hi]-c[lo])/np.maximum(hi-lo,1)+1e-12)
    stream*=np.clip((np.median(loud)/loud)**0.9,10**(-12/20),10**(12/20))

    # loop: the overrun fades back over the opening (must come AFTER levelling,
    # or the two ends get different gains and the seam steps)
    track=stream[:n].copy()
    f=np.linspace(0,1,xl)
    track[:xl]=stream[n:n+xl]*np.cos(f*np.pi/2)+stream[:xl]*np.sin(f*np.pi/2)

    day=lambda tr:[np.sqrt((tr[i*SR:(i+1)*SR]**2).mean()) for i in range(n//SR)
                   if not (night_at-0.5<i<light_at+1.5)]
    track*=10**(TARGET_DB/20)/np.median(day(track))
    t=np.arange(n)/SR
    track*=np.clip(np.clip((night_at-t)/0.5,0,1)+np.clip((t-light_at)/1.2,0,1),0,1)
    p=np.abs(track).max()
    if p>0.97: track*=0.97/p

    track.astype(np.float32).tofile("/tmp/amb.f32")
    subprocess.run(["ffmpeg","-y","-v","error","-f","f32le","-ar",str(SR),"-ac","1",
                    "-i","/tmp/amb.f32","-c:a","libmp3lame","-b:a","192k",OUT],check=True)

    probe = track.copy()
    i0, i1 = int(night_at*SR), int((light_at+0.3)*SR)   # one length for both sides: separate int()s can differ by a sample
    probe[i0:i1] = probe[:i1 - i0]
    left = [r for r in hf_runs(probe, over=VERIFY_OVER)]
    db=lambda v:20*np.log10(v+1e-12)
    a=track[-int(0.4*SR):]; b=track[int(0.05*SR):int(0.45*SR)]; d=[db(v) for v in day(track)]
    print(f"  printer in raw   {len(runs)} sustained runs, worst +{max(r[2] for r in runs):.1f} dB,"
          f" longest {max(r[1]-r[0] for r in runs):.1f}s")
    print(f"  cut              {sum(b-a for a,b in cut):.1f}s removed, "
          f"{sum(b-a for a,b in wins):.1f}s of clean room kept in {len(wins)} windows")
    print(f"  printer in bed   {len(left)} sustained runs"
          + (f"  <-- STILL THERE: {left}" if left else "  (clean)"))
    print(f"  loop match       second pass opens on window {seam_start},"
          f" level either side of the seam within {seam_step:.1f} dB")
    print(f"  repeat           material restarts at the night ({night_at:.1f}s), inside the silence")
    print(f"  length           {len(track)/SR:.2f}s  (asked {total:.2f}s)")
    print(f"  loop seam        tail {db(np.sqrt((a**2).mean())):.1f} dB -> head "
          f"{db(np.sqrt((b**2).mean())):.1f} dB   sample jump {abs(track[-1]-track[0]):.5f}")
    print(f"  night            {db(np.sqrt((track[int((night_at+0.6)*SR):int(light_at*SR)]**2).mean())):.1f} dB")
    print(f"  flatness         {min(d):.1f} .. {max(d):.1f} dB across the day")

main()
