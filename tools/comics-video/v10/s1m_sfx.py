"""Synthesise the UI sounds for `system one model` (the shared SFX library has none).

All short, all soft, all built to sit UNDER the voice: these are interface sounds,
not stings. Peaks are set here; the emitter only trims per cue.
  ui_pop       a card or chip arriving        (sine 1150 -> 620 Hz, 70 ms)
  ui_pop_low   the unsure / warning version   (sine 760 -> 430 Hz)
  ui_tick      a row / label landing          (2.3 kHz tap, 22 ms)
  ui_chime     a check passing                (1320 + 1760 Hz, the series ding, shorter)
  ui_error     the usage limit                (two descending buzzy tones)
  ui_whoosh    a panel sliding in             (band-passed noise swell, 240 ms)
  ui_ripple    a grid filling                 (14 soft taps, accelerating)
  ui_morph     the AI's body changing shape   (airy shimmer, very quiet)
"""
import numpy as np, os, wave
SR = 44100
OUT = os.path.expanduser("~/Documents/Work/comics-video/public/s1m/sfx")

def write(name, x, peak_db):
    x = x / (np.abs(x).max() + 1e-12) * 10 ** (peak_db / 20)
    fade = int(0.004 * SR)
    x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
    w = wave.open(os.path.join(OUT, name + ".wav"), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def t_(d): return np.arange(int(d * SR)) / SR

def sweep(f0, f1, d, decay):
    t = t_(d); f = f0 * (f1 / f0) ** (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)

def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x): acc = (1 - a) * v + a * acc; y[i] = acc
    return y

def bandnoise(d, lo, hi, seed=1):
    rng = np.random.default_rng(seed); n = rng.standard_normal(int(d * SR))
    return lowpass(n, hi) - lowpass(lowpass(n, hi), lo)

os.makedirs(OUT, exist_ok=True)
# pop: pitch drop + a tiny transient so it reads on phone speakers
pop = sweep(1150, 620, 0.09, 0.028)
pop[:int(0.003 * SR)] += bandnoise(0.003, 2000, 6000)[:int(0.003 * SR)] * 0.6
write("ui_pop", pop, -14)
write("ui_pop_low", sweep(760, 430, 0.11, 0.034), -15)
tick = np.sin(2 * np.pi * 2300 * t_(0.03)) * np.exp(-t_(0.03) / 0.006)
write("ui_tick", tick, -20)
t = t_(0.55)
ch = np.sin(2 * np.pi * 1320 * t) * np.exp(-t / 0.08)
d2 = np.zeros_like(t); k = int(0.09 * SR)
d2[k:] = np.sin(2 * np.pi * 1760 * t[:-k]) * np.exp(-t[:-k] / 0.16)
write("ui_chime", ch * 0.8 + d2, -15)
# error: two descending tones with odd harmonics (a soft buzz), the second longer
def buzz(f, d):
    tt = t_(d); env = np.minimum(1, tt / 0.006) * np.exp(-tt / (d * 0.6))
    return (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 3 * f * tt) + 0.15 * np.sin(2 * np.pi * 5 * f * tt)) * env
err = np.concatenate([buzz(520, 0.11), np.zeros(int(0.03 * SR)), buzz(370, 0.2)])
write("ui_error", lowpass(err, 3200), -12)
wn = bandnoise(0.26, 500, 3500, seed=3); tw = t_(0.26)
write("ui_whoosh", wn * np.sin(np.pi * tw / 0.26) ** 1.6, -22)
rip = np.zeros(int(1.3 * SR))
times = np.cumsum(np.linspace(0.13, 0.05, 14)); times = times / times[-1] * 1.15
for i, tt in enumerate(times):
    s = int(tt * SR); tk = np.sin(2 * np.pi * (1900 + 40 * i) * t_(0.025)) * np.exp(-t_(0.025) / 0.005)
    rip[s:s + len(tk)] += tk[: len(rip) - s]
write("ui_ripple", rip, -22)
mt = t_(0.3)
morph = bandnoise(0.3, 2500, 9000, seed=7) * np.sin(np.pi * mt / 0.3) ** 2 + 0.25 * np.sin(2 * np.pi * 2640 * mt) * np.exp(-mt / 0.08)
write("ui_morph", morph, -26)
print("written", sorted(f for f in os.listdir(OUT) if f.startswith("ui_")))
