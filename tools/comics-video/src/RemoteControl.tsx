import React from "react";
import {AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import cut from "./rc_cut.json";
import {AIMark} from "./AIMark";

export const RC_FPS = cut.fps;
export const RC_DURATION = cut.durationInFrames;

/**
 * EP003 `remote control`.
 *
 * Plates are the 28 frames off the Figma `remote control` page, exported at
 * 1080x1920. Captions are baked into those plates, so nothing is drawn over
 * them here except the AI mark.
 *
 * Two things are composited live:
 *  - the LIP FLAP, which swaps between two REAL drawn frames (scene1/scene2 for
 *    her, scene8/scene9 for him) on the VO's own envelope. No mouth is ever
 *    painted on.
 *  - the AI MARK, on the monitor and on the phone in the split screens. The
 *    phone is drawn crooked, so the mark leans with it by the angle measured
 *    off the plate.
 *
 * Everything reads src/rc_cut.json. No timing is typed into this file.
 */

// caption-free plates -- the baked text is masked out and captions are drawn
// here instead, so they can carry the words the VO actually says
const plate = (name: string) => staticFile(`rc/plates/${name}.png`);

const Plate: React.FC<{p: (typeof cut.panels)[number]; frame: number; t: number}> = ({p, frame, t}) => {
  // a slow push in, where the board calls for one. It eases out rather than
  // stopping dead, and the next panel comes back to full size.
  const z = p.zoom as null | number[];
  const k = z ? (frame - p.from_) / Math.max(1, p.to - p.from_) : 0;
  const scale = z ? z[0] + (z[1] - z[0]) * (1 - Math.pow(1 - Math.min(1, k), 2)) : 1;
  // lip flap -- pick the already-drawn open or shut frame for this scene
  // `plate` lets two panels share one drawing but keep separate identities --
  // his last line cuts CU / two-shot / CU and the two CUs are the same frame.
  const art = (p as {plate?: string}).plate ?? p.scene;
  let src = `clean${art}`;
  // A scene only flaps where a REAL open/shut pair was cut for that framing.
  // "both" is the two-shot, where each mouth follows its own voice.
  if (p.flap === "both") {
    const h = cut.flapHer[frame] ? "o" : "s";
    const m = cut.flapHim[frame] ? "o" : "s";
    src = `clean${art}_${h}${m}`;
  } else if (p.flap === "her" || p.flap === "him") {
    const on = p.flap === "her" ? cut.flapHer[frame] : cut.flapHim[frame];
    src = `clean${art}_${on ? "open" : "shut"}`;
  }
  const s = p.screens as null | {mon: number[]; ph: number[]};
  // asleep until he actually asks it for something
  const wakeT = cut.aiWake as number;
  const asleep = t < wakeT;
  const since = t - wakeT;
  const mark = (x: number, y: number, size: number, rot: number) => (
    <div style={{
      position: "absolute", left: x, top: y, width: 0, height: 0,
      display: "flex", alignItems: "center", justifyContent: "center",
    }}>
      <div style={{position: "absolute", left: -size / 2, top: -size / 2, width: size, height: size}}>
        <AIMark size={size} t={t} asleep={asleep} since={since} rotate={rot}/>
      </div>
    </div>
  );
  return (
    <AbsoluteFill style={{backgroundColor: "#F2F2F2", overflow: "hidden"}}>
      <AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: "50% 42%"}}>
        <Img src={plate(src)} style={{width: "100%", height: "100%", objectFit: "cover"}}/>
      </AbsoluteFill>
      {/* the monitor is somewhere he is not -- say so, once, above it */}
      {s && (
        <div style={{
          position: "absolute", left: 0, right: 0, top: s.mon[1] - 262,
          textAlign: "center", fontFamily: MONO, fontWeight: 700,
          fontSize: 17 * S, letterSpacing: 4 * S, color: "#6E6E78",
        }}>AT THE OFFICE</div>
      )}
      {s && mark(s.mon[0], s.mon[1], s.mon[2], 0)}
      {s && mark(s.ph[0], s.ph[1], s.ph[2], s.ph[3])}
    </AbsoluteFill>
  );
};

const S = 1.5;                       // 720-space -> 1080 comp
const FONT = `
@font-face { font-family:'LatoLocal';
  src:url('${staticFile("v10/fonts/Lato-Regular.ttf")}') format('truetype'); font-weight:400; }
@font-face { font-family:'GeistMono';
  src:url('${staticFile("v10/fonts/GeistMono-Bold.woff2")}') format('woff2'); font-weight:700; }`;
const CAP = "'LatoLocal','Helvetica Neue',Arial,sans-serif";
const MONO = "'GeistMono','SFMono-Regular',monospace";

/**
 * The series caption style, unchanged from `loop` and `graph`
 * (comic-animation.md -> The assembly contract):
 *   Lato 800, size 32 in 720-space, line-height 42/32,
 *   white fill with a 5px (720-space) black stroke, paint-order: stroke,
 *   whole line at once, at the storyboard's caption positions.
 */
const Caption: React.FC<{c: (typeof cut.captions)[number]}> = ({c}) => (
  <div style={{
    position: "absolute",
    left: c.align === "left" ? c.x - 150 : 60,
    right: c.align === "left" ? undefined : 60,
    width: c.align === "left" ? 900 : undefined,
    top: c.y - 34 * S,
    textAlign: c.align === "left" ? "left" : "center",
    fontFamily: CAP, fontSize: 32 * S, fontWeight: 800, lineHeight: 42 / 32,
    color: "#FFFFFF", WebkitTextStroke: `${5 * S}px #000000`,
    paintOrder: "stroke",
  }}>{c.text}</div>
);

/**
 * SFX lettering. comic-animation.md: every sound that plays gets a word, and
 * the word animates ON its sound -- snap in ~0.05s, overshoot, decay over
 * 0.26s, hold, then clear. It is never baked flat into the plate.
 */
const SfxWord: React.FC<{s: (typeof cut.sfx)[number]; t: number}> = ({s, t}) => {
  const e = t - s.t;
  if (e < -0.02 || e > 1.15) return null;
  const snap = Math.min(1, Math.max(0, e / 0.05));           // in over ~0.05s
  const decay = e <= 0.05 ? 0 : Math.min(1, (e - 0.05) / 0.26);
  const scale = 1 + 0.26 * snap * (1 - decay);               // overshoot, settle
  const hold = e > 0.78 ? Math.max(0, 1 - (e - 0.78) / 0.28) : 1;   // hold, clear
  return (
    <div style={{
      position: "absolute", left: s.x, top: s.y,
      transform: `scale(${scale})`, transformOrigin: "left top",
      opacity: snap * hold,
      fontFamily: CAP, fontSize: 25 * S, fontWeight: 800, fontStyle: "italic",
      color: s.col, letterSpacing: "-0.01em",
    }}>ping</div>
  );
};

/**
 * The shivering dog. A keyed meme clip cut in over Peter -- the one photoreal
 * thing in a film of line art, which is the joke. No entrance animation: it
 * arrives on the same hard cut as the shot behind it, which is this film's
 * only transition. The clip runs at its NATIVE 30fps and ping-pongs if the
 * hold outlasts it, so the shiver never speeds up or jumps.
 */
const Dog: React.FC<{d: typeof cut.dog; frame: number; t: number}> = ({d, frame, t}) => {
  if (frame < d.from_ || frame >= d.to) return null;
  const period = 2 * (d.n - 1);
  const k = (frame - d.from_) % period;
  const i = k < d.n ? k : period - k;
  const pop = 1;
  return (
    <Img
      src={staticFile(`${d.dir}/${String(i).padStart(3, "0")}.png`)}
      style={{
        position: "absolute", left: d.cx - d.w / 2, top: d.bottom - d.h,
        width: d.w, height: d.h,
        transform: `scale(${pop})`, transformOrigin: "50% 100%",
      }}
    />
  );
};

export const RemoteControl: React.FC = () => {
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const t = frame / fps;

  const dateStart = (cut.cues.find((c) => c.id === "date_main")?.frame ?? 0) / fps;
  const dateVolume = (f: number) => {
    const tt = f / fps + dateStart;
    let g = 1;
    for (const [a, b, v] of cut.ducks as [number, number, number][]) {
      const R = 0.18;
      if (tt > a - R && tt < b + R) {
        const inR = Math.min(1, Math.max(0, (tt - (a - R)) / R));
        const outR = Math.min(1, Math.max(0, ((b + R) - tt) / R));
        g = Math.min(g, 1 - (1 - v) * Math.min(inR, outR));
      }
    }
    return g;
  };

  // the room tone sits UNDER every voice and comes back up in the gaps
  const ambVolume = (f: number) => {
    const tt = f / fps;
    let g = 1;
    for (const [a, b, v] of cut.ambDucks as [number, number, number][]) {
      const R = 0.22;
      if (tt > a - R && tt < b + R) {
        const inR = Math.min(1, Math.max(0, (tt - (a - R)) / R));
        const outR = Math.min(1, Math.max(0, ((b + R) - tt) / R));
        g = Math.min(g, 1 - (1 - v) * Math.min(inR, outR));
      }
    }
    return g;
  };

  const p = cut.panels.find((q) => frame >= q.from_ && frame < q.to) ?? cut.panels[cut.panels.length - 1];

  return (
    <AbsoluteFill style={{backgroundColor: "#000"}}>
      <style>{FONT}</style>
      <Plate p={p} frame={frame} t={t}/>
      <Dog d={cut.dog} frame={frame} t={t}/>
      {(cut.dog as {aud?: string}).aud && (
        <Sequence from={cut.dog.from_}>
          <Audio src={staticFile((cut.dog as {aud: string}).aud)}
                 volume={(f) => ambVolume(f + cut.dog.from_)}/>
        </Sequence>
      )}
      {cut.captions.map((c, i) =>
        frame >= c.from_ && frame < c.to ? <Caption key={i} c={c}/> : null
      )}
      {cut.sfx.map((s) => <SfxWord key={s.id} s={s} t={t}/>)}
      {cut.cues.map((c) =>
        c.id === "date_main" ? (
          <Sequence key={c.id} from={c.frame}>
            <Audio src={staticFile(c.src)} volume={dateVolume}/>
          </Sequence>
        ) : c.id === "amb" ? (
          <Sequence key={c.id} from={c.frame}>
            <Audio src={staticFile(c.src)} volume={ambVolume}/>
          </Sequence>
        ) : (
          <Sequence key={c.id} from={c.frame}>
            <Audio src={staticFile(c.src)}/>
          </Sequence>
        )
      )}
    </AbsoluteFill>
  );
};
