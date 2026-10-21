import React from "react";
import {AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame} from "remotion";
import cut from "./ins_cut.json";
import caps from "./ins_caps.json";
import keystrokes from "./ins_keystrokes.json";
import {AIMark} from "./AIMark";
import {HookScreen, SkillScreen, WrongScreen, HinderScreen, AgentsScreen, HorizonScreen, ScreenTitle} from "./InsExplainer";

export const INS_FPS = cut.fps;
export const INS_DURATION = cut.durationF;

/**
 * `/insights`.
 *
 * Plates are the 46 frames off the Figma `/insights` page, exported at 720x1280
 * and used IN ORDER. Captions are baked into those plates.
 *
 * Two things are composited live:
 *  - the LIP FLAP, which swaps between two REAL drawn frames (1/2 for Sameer,
 *    19/20 and 22/23 for AJ) on the take's own envelope. No mouth is painted.
 *    Which of each pair is open was MEASURED by ink, not assumed.
 *  - the AI MARK, centred on the blank monitor. The plates ship blank on
 *    purpose; the mark is the AI's one body and goes on every screen it speaks
 *    from. Its position is locked from frame6, never re-detected per plate.
 *
 * Every number comes from src/ins_cut.json, emitted by v10/ins_emit.py.
 * Hard cuts throughout — nothing crossfades, per the series rule.
 */

const plate = (name: string) => staticFile(`ins/plates/${name}.png`);

/* where each hand-lettered sound sits, and the moments it fires on.
   frame5's two labels alternate across the REAL keystrokes in typing.wav. */
const KS = keystrokes as number[];
const SFX_WORDS: Record<string, {t: string; x: number; y: number; size: number; hits: number[]}[]> = {
  frame3:  [{t: "*slurps*", x: 92,  y: 208,  size: 32, hits: [0.55]}],
  frame5:  [{t: "click",    x: 504, y: 732,  size: 32, hits: KS.filter((_, i) => i % 2 === 0).map((h) => h + 0.15)},
            {t: "click",    x: 504, y: 988,  size: 32, hits: KS.filter((_, i) => i % 2 === 1).map((h) => h + 0.15)}],
  frame28: [{t: "click",    x: 515, y: 1044, size: 32, hits: [0.12]}],
  frame30: [{t: "click",    x: 515, y: 1044, size: 32, hits: [0.02]}],
  frame32: [{t: "click",    x: 515, y: 1044, size: 32, hits: [0.12]}],
};

/* Captions are NOT baked into the plates: the dialogue layers were hidden for
   the export and the words are drawn here instead, in the series caption
   style — Lato 800, 32px in 720-space, white with a 5px black stroke,
   paintOrder stroke, whole line at once. Same as `loop` and `graph`.
   Geometry is the Figma text block's own x/y/w, so nothing moves. */
const FONT = `
@font-face { font-family:'LatoLocal';
  src:url('${staticFile("v10/fonts/Lato-Regular.ttf")}') format('truetype'); font-weight:400; }
@font-face { font-family:'GeistMono';
  src:url('${staticFile("v10/fonts/GeistMono-Bold.woff2")}') format('woff2'); font-weight:700; }`;
const CAP = "'LatoLocal','Helvetica Neue',Arial,sans-serif";
const SCREEN_FONT = "'GeistMono',ui-monospace,Menlo,monospace";

/* META RULE: text that lives ON A SCREEN is never caption style. A caption is
   somebody talking; screen text is the machine's own interface. They must not
   look the same. Anything whose box falls inside the monitor is drawn in the
   screen face — mono, dark ink, no stroke. */
const onScreen = (c: {y: number}) => c.y >= cut.screen.y && c.y <= cut.screen.y + cut.screen.h;

/* SFX lettering is drawn live and SPIKES on its own sound -- never baked flat.
   Same behaviour as loop and graph: opacity and scale ride the hit, then ease
   back down rather than switching off. */
const Sfx: React.FC<{t: string; x: number; y: number; size: number; hits: number[]; local: number}> =
({t, x, y, size, hits, local}) => {
  let spike = 0;
  for (const h of hits) {
    if (local >= h && local < h + 0.30) spike = Math.max(spike, 1 - (local - h) / 0.30);
  }
  if (local < (hits[0] ?? 0) - 0.05) return null;
  const opacity = 0.22 + 0.78 * spike * spike;
  return (
    <div style={{
      position: "absolute", left: x, top: y,
      transform: `scale(${1 + 0.12 * spike})`, transformOrigin: "left top",
      /* SFX lettering is NOT caption style. It is hand-lettering that belongs
         to the artwork: plain sans, dark grey, no stroke -- same as graph. */
      fontFamily: CAP, fontWeight: 400, fontSize: size, color: "#3a3a3a",
      opacity, whiteSpace: "nowrap",
    }}>{t}</div>
  );
};

type Cap = {t: string; x: number; y: number; w: number; size?: number; italic?: boolean; at?: string; after?: string};

const Caption: React.FC<{c: Cap}> = ({c}) => {
  const size = c.size ?? 32;
  if (onScreen(c)) {
    return (
      <div style={{
        position: "absolute", left: c.x, top: c.y, width: c.w,
        textAlign: "center", fontFamily: SCREEN_FONT, fontSize: size * 0.82,
        fontWeight: 700, letterSpacing: 0.2, lineHeight: 1.45,
        color: "#17171A", whiteSpace: "pre-wrap",
      }}>{c.t}</div>
    );
  }
  return (
    <div style={{
      position: "absolute", left: c.x, top: c.y, width: c.w,
      textAlign: "center", fontFamily: CAP, fontSize: size, fontWeight: 800,
      fontStyle: c.italic ? "italic" : "normal", lineHeight: 42 / 32,
      color: "#FFFFFF", WebkitTextStroke: `${(5 * size) / 32}px #000000`, paintOrder: "stroke",
      whiteSpace: "pre-wrap",
    }}>{c.t}</div>
  );
};
type Panel = (typeof cut.panels)[number];

const Plate: React.FC<{p: Panel; frame: number}> = ({p, frame}) => {
  const i = frame - p.startF;
  // flap: pick the already-drawn open or shut frame for this shot
  const track = p.track as boolean[] | null;
  const src = p.flap && track
    ? p.plates[track[Math.max(0, Math.min(track.length - 1, i))] ? 0 : 1]
    : p.plates[0];
  const t = frame / cut.fps;
  const local = (frame - p.startF) / cut.fps + ((p as {expT0?: number}).expT0 ?? 0);
  const title = (p as {title?: string | null}).title ?? null;
  const sfx = SFX_WORDS[p.frames[0]] ?? [];
  const exp = (p as {explainer?: string | null}).explainer ?? null;
  const cat = cut.cat;
  const catT = t - cat.at;
  const catOn = cat.on.indexOf(p.frames[0]) >= 0 && catT >= 0 && t < cat.until;
  const catIdx = catOn ? Math.floor(catT * cut.fps) % cat.frames : 0;
  const s = cut.screen;
  return (
    <AbsoluteFill>
      <Img src={plate(src)} style={{width: cut.w, height: cut.h}} />
      {(((caps as Record<string, Cap[]>)[(p as {capKey?: string | null}).capKey ?? src]) ?? []).map((c, i) => {
        // a caption keyed to a later cue waits for that cue's own start
        if (c.at) {
          const cue = cut.vo.find((v) => v.file === c.at);
          if (cue && frame < Math.round(cue.at * cut.fps)) return null;
        }
        // this label arrives ON the ding, not with the card
        if (c.after === "ding" && frame < Math.round(cut.ding_at * cut.fps)) return null;
        return <Caption key={i} c={c} />;
      })}
      {/* the educational screens. Drawn, not exported, so they can move. */}
      {exp ? (
        <div style={{position: "absolute", inset: 0}}>
          {exp === "hook" ? <HookScreen t={local} fps={cut.fps} />
            : exp === "skill" ? <SkillScreen t={local} fps={cut.fps} />
            : exp === "agents" ? <AgentsScreen t={local} fps={cut.fps} />
            : exp === "horizon" ? <HorizonScreen t={local} fps={cut.fps} />
            : exp === "wrong" ? <WrongScreen t={local} fps={cut.fps}
                phase={(p as {phase?: string}).phase ?? "mine"} />
            : <HinderScreen t={local} fps={cut.fps} />}
        </div>
      ) : null}

      {/* the cat is ON the monitor, and his raised arm is drawn back on top of
          it from the plate itself -- so it reads as something playing on the
          screen rather than a sticker on the video */}
      {catOn ? (
        <>
          <div style={{
            position: "absolute", left: cat.x, top: cat.y, width: cat.w, height: cat.h,
            overflow: "hidden", display: "flex", alignItems: "center", justifyContent: "center",
            background: "#FFFFFF",
          }}>
            <Img
              src={staticFile(`ins/cat/${String(catIdx).padStart(3, "0")}.png`)}
              style={{height: cat.h, width: "auto"}}
            />
          </div>
          <Img
            src={staticFile(`ins/handmask/${p.frames[0]}.png`)}
            style={{position: "absolute", left: cat.x, top: cat.y, width: cat.w, height: cat.h}}
          />
        </>
      ) : null}

      {sfx.map((w, i) => (
        <Sfx key={i} t={w.t} x={w.x} y={w.y} size={w.size} hits={w.hits} local={local} />
      ))}

      {title ? <ScreenTitle t={title} k={1} /> : null}

      {p.mark ? (
        <div style={{
          position: "absolute",
          /* while a screen is busy the mark goes SMALL, bottom right --
             it is still the AI's body, it just stops being the subject */
          left: exp ? s.x + s.w - 46 : s.x + s.w / 2,
          top:  exp ? s.y + s.h - 46 : s.y + s.h / 2,
          width: 0, height: 0,
          display: "flex", alignItems: "center", justifyContent: "center",
        }}>
          <AIMark size={exp ? 46 : Math.round(s.h * 0.42)} t={t} asleep={!p.speaking} />
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const Insights: React.FC = () => {
  const frame = useCurrentFrame();
  const bick = cut.bicker;
  const bickFrom = Math.round(bick.at * cut.fps);
  const bickLen = Math.round((bick.until - bick.at) * cut.fps);

  return (
    <AbsoluteFill style={{backgroundColor: "#f3f3f0"}}>
      <style>{FONT}</style>
      {cut.panels.map((p, i) => (
        <Sequence
          key={i}
          from={p.startF}
          durationInFrames={Math.max(1, p.durF)}
          name={p.frames.join("+")}
        >
          <Plate p={p} frame={frame} />
        </Sequence>
      ))}

      {/* decode the next plates early at zero opacity, or Studio shows one
          white frame at every cut and a cut you cannot review is a cut you
          cannot judge */}
      {cut.panels.map((p, i) => (
        <Sequence key={"pre" + i} from={Math.max(0, p.startF - 12)} durationInFrames={12}>
          <AbsoluteFill style={{opacity: 0}}>
            {p.plates.map((n) => <Img key={n} src={plate(n)} />)}
          </AbsoluteFill>
        </Sequence>
      ))}

      {/* VO — every slice is its own file, played from zero. Never seek an mp3. */}
      {cut.vo.map((v, i) => (
        <Sequence key={v.file + i} from={Math.round(v.at * cut.fps)} name={v.file}>
          <Audio src={staticFile(`ins/${v.file}`)} volume={(v as {gain?: number}).gain ?? 1} />
        </Sequence>
      ))}

      {/* office bed -- graph's printer-free ambience, ducked under every voice.
          Present is not audible: it has to move out of the way or it masks. */}
      <Audio
        src={staticFile(`ins/${cut.amb.file}`)}
        volume={(f) => cut.amb.gain * (cut.duck[Math.min(cut.duck.length - 1, f)] ?? 1)}
      />

      {cut.sfx.map((x, i) => (
        <Sequence key={"sfx" + i} from={Math.round(x.at * cut.fps)} name={x.file}>
          <Audio src={staticFile(`ins/${x.file}`)} volume={x.gain} />
        </Sequence>
      ))}

      {/* the cat's own audio, kept right down -- four things are already playing */}
      <Sequence from={Math.round(cut.cat.at * cut.fps)}
        durationInFrames={Math.max(1, Math.round((cut.cat.until - cut.cat.at) * cut.fps))}
        name="cat">
        <Audio src={staticFile("ins/cat.wav")} volume={cut.cat.gain}
          muted={cut.cat.muted} loop />
      </Sequence>

      {/* AJ, still going, under the wide. Cut dead on the join to frame46. */}
      <Sequence from={bickFrom} durationInFrames={Math.max(1, bickLen)} name="aj bickering">
        <Audio src={staticFile("ins/bicker.wav")} volume={bick.gain} />
      </Sequence>
    </AbsoluteFill>
  );
};
