import React from "react";
import {AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame} from "remotion";
import cut from "./s1m_cut.json";
import caps from "./s1m_caps.json";
import {AIMark} from "./AIMark";
import {
  CodeScreen, NightScreen, DenseScreen, TestScreen, DiffScreen, PilesScreen, PayoffScreen,
  DoctorExplainer, NurseExplainer, DoorsExplainer, SetupExplainer, StepFiveExplainer, AIMorph, EndCard,
} from "./S1mExplainers";

export const S1M_FPS = cut.fps;
export const S1M_DURATION = cut.durationF;

/**
 * EP005 `system one model`.
 *
 * Plates are Sejal's 61 frames off the Figma page `system one model`, exported
 * at 720x1280 with EVERY text layer hidden. All words are drawn here:
 *  - captions in the series style (Lato 800, 32/720, white, 5px black stroke,
 *    paintOrder stroke, whole line at once) at the Figma text block's x/y/w;
 *  - SFX lettering in plain sans #3a3a3a, no stroke, spiking on real keystrokes;
 *  - screen text in Geist Mono, drawn inside the measured monitor rect.
 * No caption ever sits on an explainer or a screen visual.
 *
 * Lip flap swaps two REAL drawn plates (Sejal's open-mouth layer on/off, or two
 * board frames that differ only at the mouth) on the take's own envelope.
 * The AI mark sits only on the blank monitors the AI speaks from.
 *
 * Everything is authored in 720 x 1280 and the stage is scaled 1.5x to 1080 x 1920.
 * Every number comes from src/s1m_cut.json (v10/s1m_emit.py). Hard cuts only.
 */

const S = cut.S;
const FONT = `
@font-face { font-family:'LatoLocal'; src:url('${staticFile("s1m/fonts/Lato-Regular.ttf")}') format('truetype'); font-weight:400; }
@font-face { font-family:'LatoSemi'; src:url('${staticFile("s1m/fonts/Lato-Semibold.ttf")}') format('truetype'); font-weight:600; }
@font-face { font-family:'GeistMono'; src:url('${staticFile("s1m/fonts/geist-mono-latin-400-normal.woff2")}') format('woff2'); font-weight:400; }
@font-face { font-family:'GeistMono'; src:url('${staticFile("s1m/fonts/geist-mono-latin-500-normal.woff2")}') format('woff2'); font-weight:500; }
@font-face { font-family:'GeistMono'; src:url('${staticFile("s1m/fonts/geist-mono-latin-600-normal.woff2")}') format('woff2'); font-weight:600; }
@font-face { font-family:'GeistMono'; src:url('${staticFile("s1m/fonts/geist-mono-latin-700-normal.woff2")}') format('woff2'); font-weight:700; }
@font-face { font-family:'MonaSans'; src:url('${staticFile("s1m/fonts/MonaSans-ExtraBold.woff2")}') format('woff2'); font-weight:800; }
@font-face { font-family:'JakartaLocal'; src:url('${staticFile("s1m/fonts/PlusJakartaSans-Medium.woff2")}') format('woff2'); font-weight:500; }`;
const CAP = "'LatoLocal','Helvetica Neue',Arial,sans-serif";
const MONO = "'GeistMono',ui-monospace,Menlo,monospace";

const plate = (name: string) => staticFile(`s1m/plates/${name}.png`);

type Cap = {t: string; x: number; y: number; w: number; italic?: boolean};
type Panel = (typeof cut.panels)[number] & {
  flap: {open: string; shut: string; track: boolean[]} | null;
  ev: Record<string, number>;
};
const PANELS = cut.panels as unknown as Panel[];

/* ---------------------------------------------------------------- captions */
const Caption: React.FC<{c: Cap}> = ({c}) => (
  <div style={{
    position: "absolute", left: c.x, top: c.y, width: c.w,
    textAlign: "center", fontFamily: CAP, fontSize: 32, fontWeight: 800,
    fontStyle: c.italic ? "italic" : "normal", lineHeight: 42 / 32,
    color: "#FFFFFF", WebkitTextStroke: "5px #000000", paintOrder: "stroke",
    whiteSpace: c.t.includes(" ") ? "pre-wrap" : "nowrap",
  }}>{c.t}</div>
);

/* ---------------------------------------------------------------- time header (graph's) */
const TimeHeader: React.FC<{t: string}> = ({t}) => (
  <div style={{
    position: "absolute", left: 0, top: 177, width: 720, textAlign: "center",
    fontFamily: MONO, fontWeight: 700, fontSize: 40, letterSpacing: 1,
    color: "#FFFFFF", WebkitTextStroke: "4px #000000", paintOrder: "stroke",
  }}>{t}</div>
);

/* ---------------------------------------------------------------- SFX lettering */
// the two "click"s as Sejal lettered them; Figma rotation is CCW-positive, CSS CW
const CLICKS = [{x: 504, y: 732, rot: 9}, {x: 504, y: 988, rot: 25}];
const Click: React.FC<{x: number; y: number; rot: number; hits: number[]; local: number}> = ({x, y, rot, hits, local}) => {
  let spike = 0;
  for (const h of hits) if (local >= h && local < h + 0.26) spike = Math.max(spike, 1 - (local - h) / 0.26);
  if (!hits.length || local < hits[0] - 0.05) return null;
  return (
    <div style={{
      position: "absolute", left: x, top: y, transformOrigin: "left top",
      transform: `rotate(${-rot}deg) scale(${1 + 0.1 * spike})`,
      fontFamily: "Arial, Helvetica, sans-serif", fontWeight: 400, fontSize: 32, color: "#3a3a3a",
      opacity: 0.3 + 0.7 * spike, whiteSpace: "nowrap",
    }}>click</div>
  );
};

/* ---------------------------------------------------------------- explainer dispatch */
const nurseP = PANELS.find((p) => p.exp === "nurse")!;
const setupP = PANELS.filter((p) => p.exp === "setup");
const SETUP_EV = {
  a: setupP[0].ev, b: setupP[1].ev, c: setupP[2].ev,
  aDur: setupP[0].durF / cut.fps, bDur: setupP[1].durF / cut.fps,
};

const Visual: React.FC<{p: Panel; local: number}> = ({p, local}) => {
  switch (p.exp) {
    case "code": return <CodeScreen t={local} />;
    case "night": return <NightScreen t={local} variant="night" />;
    case "limit_night": return <NightScreen t={local} variant="limit_night" />;
    case "limit_day": return <NightScreen t={local} variant="limit_day" />;
    case "dense": return <DenseScreen t={local} ev={p.ev} />;
    case "test": return <TestScreen t={local} fps={cut.fps} />;
    case "diff": return <DiffScreen t={local} ev={p.ev} />;
    case "piles": return <PilesScreen t={local} ev={p.ev} />;
    case "payoff": return <PayoffScreen t={local} />;
    case "doctor": return <DoctorExplainer t={local} ev={p.ev} />;
    case "nurse": return <NurseExplainer t={local} ev={p.ev} />;
    case "doors": return <DoorsExplainer t={local} ev={p.ev} nurseEv={nurseP.ev} nurseEnd={nurseP.durF / cut.fps} />;
    case "setup": return <SetupExplainer t={local} phase={p.phase as "a" | "b" | "c"} ev={SETUP_EV} />;
    case "stepfive": return <StepFiveExplainer t={local} ev={p.ev} />;
    case "endcard": return <EndCard t={local} />;
    default: return null;
  }
};

/* ---------------------------------------------------------------- one panel */
const PanelView: React.FC<{p: Panel}> = ({p}) => {
  const i = useCurrentFrame();                 // local to the Sequence
  const local = i / cut.fps;
  const tGlobal = (p.startF + i) / cut.fps;
  const fullFrame = p.plate.startsWith("exp");
  let src = p.plate;
  if (p.flap) src = p.flap.track[Math.max(0, Math.min(p.flap.track.length - 1, i))] ? p.flap.open : p.flap.shut;
  // long lines show in parts in the same box, each part from its own first word (capChunks, from the emitter)
  const chunks = (p as {capChunks?: (Cap & {from: number; until: number | null})[]}).capChunks;
  const capList = chunks
    ? chunks.filter((c) => local >= c.from && (c.until === null || local < c.until))
    : p.caps ? ((caps as Record<string, Cap[]>)[p.caps] ?? []) : [];
  // keystrokes that land inside this panel, every third, alternating the two labels
  const hits: number[] = p.clicks
    ? (cut.sfx as {hits: number[]}[]).flatMap((x) => x.hits)
        .filter((h) => h >= p.start - 0.02 && h < p.start + p.durF / cut.fps).map((h) => h - p.start)
    : [];
  const every = hits.filter((_, k) => k % 3 === 0);
  const s = cut.screen;
  return (
    <AbsoluteFill>
      {fullFrame ? null : <Img src={plate(src)} style={{position: "absolute", left: 0, top: 0, width: 720, height: 1280}} />}
      {p.exp ? <Visual p={p} local={local} /> : null}
      {capList.map((c, k) => <Caption key={k} c={c} />)}
      {CLICKS.map((c, k) => (
        <Click key={k} x={c.x} y={c.y} rot={c.rot} local={local} hits={every.filter((_, n) => n % 2 === k)} />
      ))}
      {p.header ? <TimeHeader t={p.header} /> : null}
      {p.mark ? (
        <div style={{position: "absolute", left: s.x + s.w / 2, top: s.y + s.h / 2, width: 0, height: 0,
          display: "flex", alignItems: "center", justifyContent: "center"}}>
          {(p as {morph?: boolean}).morph
            ? <AIMorph t={local} tGlobal={tGlobal} ev={p.ev} size={Math.round(s.h * 0.42)} />
            : <AIMark size={Math.round(s.h * 0.42)} t={tGlobal} />}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const SystemOne: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: "#ffffff"}}>
    <style>{FONT}</style>
    <div style={{position: "absolute", left: 0, top: 0, width: 720, height: 1280, transform: `scale(${S})`, transformOrigin: "0 0", overflow: "hidden"}}>
      {PANELS.map((p, n) => (
        <Sequence key={n} from={p.startF} durationInFrames={Math.max(1, p.durF)} name={p.plate}>
          <PanelView p={p} />
        </Sequence>
      ))}
      {/* decode the next plates early at zero opacity, or Studio flashes white at every cut */}
      {PANELS.map((p, n) => {
        const names = p.plate.startsWith("exp") ? [] : p.flap ? [p.flap.open, p.flap.shut] : [p.plate];
        return names.length ? (
          <Sequence key={"pre" + n} from={Math.max(0, p.startF - 12)} durationInFrames={12}>
            <AbsoluteFill style={{opacity: 0}}>{names.map((m) => <Img key={m} src={plate(m)} style={{width: 10, height: 10}} />)}</AbsoluteFill>
          </Sequence>
        ) : null;
      })}
    </div>

    {/* VO — every line is its own file, played from zero. Never seek an mp3. */}
    {cut.vo.map((v, n) => (
      <Sequence key={"vo" + n} from={Math.round(v.at * cut.fps)} name={v.name}>
        <Audio src={staticFile(`s1m/${v.file}`)} />
      </Sequence>
    ))}
    {/* keyboard, sliced from the shared library, spiking the lettering above */}
    {/* keyboard + UI sounds + the cats' own audio (cat cues obey one mute flag in the cut) */}
    {(cut.sfx as {file: string; at: number; gain: number; cat?: boolean}[]).map((x, n) => (
      <Sequence key={"sfx" + n} from={Math.round(x.at * cut.fps)} name={x.file}>
        <Audio src={staticFile(`s1m/${x.file}`)} volume={x.gain} muted={!!x.cat && !!(cut as {catAudioMuted?: boolean}).catAudioMuted} />
      </Sequence>
    ))}
    {/* the office bed: printer-free, ducked under every voice, silent at night — baked whole */}
    <Audio src={staticFile(`s1m/${cut.bed.file}`)} volume={cut.bed.gain} />
  </AbsoluteFill>
);
