#!/usr/bin/env python3
"""Per-10ms RMS envelope of a region, in dBFS. Finds true word edges."""
import subprocess, sys, array, math
def env(path, a, b, hop=0.01):
    raw = subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-to",str(b),"-i",path,
        "-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    s = array.array("h"); s.frombytes(raw[:len(raw)//2*2])
    n = int(16000*hop); out=[]
    for i in range(0, len(s)-n, n):
        w = s[i:i+n]
        r = math.sqrt(sum(x*x for x in w)/n)
        out.append((a+i/16000.0, 20*math.log10(r/32768.0) if r>0 else -120))
    return out
def edges(path, a, b, thr=-45):
    """print contiguous runs above thr"""
    e = env(path,a,b); runs=[]; cur=None
    for t,d in e:
        if d>thr:
            if cur is None: cur=[t,t]
            else: cur[1]=t
        else:
            if cur and t-cur[1]>0.05: runs.append(tuple(cur)); cur=None
    if cur: runs.append(tuple(cur))
    return runs
if __name__=="__main__":
    p,a,b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    thr = float(sys.argv[4]) if len(sys.argv)>4 else -45
    for s,t in edges(p,a,b,thr): print(f"  sound {s:.3f} -> {t:.3f}   ({t-s:.3f}s)")
