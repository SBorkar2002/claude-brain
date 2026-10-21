import React from "react";
import {AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame} from "remotion";
import cut from "./pe_cut.json";
import {
  AjPromptScreen, QuestionScreen, AppScreen, AppLinkScreen, App41Screen, AppAnswerScreen, FeaturesScreen,
  LeaderboardScreen, TeachScreen, ContractExplainer, CostScreen, CardScreen, CornerMark,
} from "./PeScreens";

export const PE_FPS = cut.fps;
export const PE_DURATION = cut.durationF;

/**
 * `prompt engineering` (Script A, "Wait, What?").
 *
 * Plates: Sejal's 36 frames off the Figma page `Prompt engieering`, exported at
 * 720x1280 with the dialogue, SFX and placeholder-screen text hidden. All words
 * are drawn here:
 *  - captions in the series style (Lato 800, 32/720, white, 5px black stroke,
 *    paintOrder stroke, whole line at once) at the Figma text block's x/y/w;
 *  - SFX lettering in plain sans #3a3a3a, no stroke, popping on its sound;
 *  - screen text in Geist Mono, inside the measured monitor rect.
 * Lip flap swaps two REAL drawn plates on the take's own envelope (calm flap).
 * Authored in 720 x 1280, stage scaled 1.5x to 1080 x 1920. Hard cuts only.
 * Every number comes from src/pe_cut.json (v10/pe_emit.py).
 */

const S = cut.S;
const FONT = `
@font-face { font-family:'LatoLocal'; src:url('${staticFile("pe/fonts/Lato-Regular.ttf")}') format('truetype'); font-weight:400; }
@font-face { font-family:'LatoSemi'; src:url('${staticFile("pe/fonts/Lato-Semibold.ttf")}') format('truetype'); font-weight:600; }
@font-face { font-family:'GeistMono'; src:url('${staticFile("pe/fonts/geist-mono-latin-400-normal.woff2")}') format('woff2'); font-weight:400; }
@font-face { font-family:'GeistMono'; src:url('${staticFile("pe/fonts/geist-mono-latin-500-normal.woff2")}') format('woff2'); font-weight:500; }
@font-face { font-family:'GeistMono'; src:url('${staticFile("pe/fonts/geist-mono-latin-600-normal.woff2")}') format('woff2'); font-weight:600; }
@font-face { font-family:'GeistMono'; src:url('${staticFile("pe/fonts/geist-mono-latin-700-normal.woff2")}') format('woff2'); font-weight:700; }
@font-face { font-family:'MonaSans'; src:url('${staticFile("pe/fonts/MonaSans-ExtraBold.woff2")}') format('woff2'); font-weight:800; }`;
const CAP = "'LatoLocal','Helvetica Neue',Arial,sans-serif";
const MONO = "'GeistMono',ui-monospace,Menlo,monospace";

const plate = (name: string) => staticFile(`pe/plates/${name}.png`);

type Cap = {t: string; x: number; y: number; w: number; align: string; italic: boolean; from: number; until: number | null};
type SfxWord = {w: string; x: number; y: number; rot: number; at?: number; hits?: number[]; type?: boolean};
type Panel = {
  plate: string; start: number; startF: number; durF: number; exp: string | null; header: string | null;
  mark: boolean; ev: Record<string, number>; sfxw: SfxWord[]; capList?: Cap[];
  flap: {open: string; shut: string; track: boolean[]} | null;
};
const PANELS = cut.panels as unknown as Panel[];

/* ---------------------------------------------------------------- captions */
const Caption: React.FC<{c: Cap}> = ({c}) => (
  <div style={{
    position: "absolute", left: c.x, top: c.y, width: c.w,
    textAlign: c.align as "left" | "center", fontFamily: CAP, fontSize: 32, fontWeight: 800,
    fontStyle: c.italic ? "italic" : "normal", lineHeight: 42 / 32,
    color: "#FFFFFF", WebkitTextStroke: "5px #000000", paintOrder: "stroke",
    whiteSpace: c.t.includes(" ") ? "pre-wrap" : "nowrap",
  }}>{c.t}</div>
);

/* ---------------------------------------------------------------- time header */
const TimeHeader: React.FC<{t: string}> = ({t}) => (
  <div style={{
    position: "absolute", left: 0, top: 177, width: 720, textAlign: "center",
    fontFamily: MONO, fontWeight: 700, fontSize: 40, letterSpacing: 1,
    color: "#FFFFFF", WebkitTextStroke: "4px #000000", paintOrder: "stroke",
  }}>{t}</div>
);

/* ---------------------------------------------------------------- SFX lettering */
// Figma rotation is CCW-positive, CSS is CW. Snap in, overshoot, decay over 0.26s, hold.
const SfxWordView: React.FC<{s: SfxWord; hits: number[]; local: number}> = ({s, hits, local}) => {
  if (!hits.length || local < hits[0] - 0.02) return null;
  let spike = 0;
  for (const h of hits) if (local >= h && local < h + 0.26) spike = Math.max(spike, 1 - (local - h) / 0.26);
  const keys = !!s.type;   // keyboard clicks breathe 0.3 -> 1 on every stroke; a ping lands and holds
  const snap = Math.min(1, (local - hits[0]) / 0.05);
  return (
    <div style={{
      position: "absolute", left: s.x, top: s.y, transformOrigin: "left top",
      transform: `rotate(${-s.rot}deg) scale(${(keys ? 1 : 0.6 + 0.4 * snap) + (keys ? 0.1 : 0.18) * spike})`,
      fontFamily: "Arial, Helvetica, sans-serif", fontWeight: 400, fontSize: 32, color: "#3a3a3a",
      opacity: keys ? 0.3 + 0.7 * spike : 1, whiteSpace: "nowrap",
    }}>{s.w}</div>
  );
};

/* ---------------------------------------------------------------- screens */
const contract1 = PANELS.find((p) => p.exp === "contract")!;
const Visual: React.FC<{p: Panel; local: number}> = ({p, local}) => {
  switch (p.exp) {
    case "ajprompt": return <AjPromptScreen t={local} ev={p.ev} />;
    case "question": return <QuestionScreen t={local} ev={p.ev} />;
    case "app": return <AppScreen t={local} ev={p.ev} />;
    case "app_link": return <AppLinkScreen t={local} ev={p.ev} />;
    case "app41": return <App41Screen t={local} ev={p.ev} />;
    case "app_answer": return <AppAnswerScreen t={local} ev={p.ev} />;
    case "features": return <FeaturesScreen t={local} ev={p.ev} />;
    case "leaderboard": return <LeaderboardScreen t={local} ev={p.ev} />;
    case "teach": return <TeachScreen t={local} ev={p.ev} />;
    case "contract": return <ContractExplainer t={local} ev={p.ev} phase={1} />;
    case "contract2": return <ContractExplainer t={local} ev={p.ev} phase={2} prev={contract1.ev} prevEnd={contract1.durF / cut.fps} />;
    case "cost": return <CostScreen t={local} ev={p.ev} />;
    case "card": return <CardScreen t={local} ev={p.ev} />;
    case "card_full": return <CardScreen t={local} ev={p.ev} full />;
    default: return null;
  }
};

/* ---------------------------------------------------------------- one panel */
const TYPE_HITS = (cut.sfx as {hits: number[]; tag: string}[]).filter((x) => x.tag === "type").flatMap((x) => x.hits);

const PanelView: React.FC<{p: Panel}> = ({p}) => {
  const i = useCurrentFrame();
  const local = i / cut.fps;
  const tGlobal = (p.startF + i) / cut.fps;
  let src = p.plate;
  if (p.flap) src = p.flap.track[Math.max(0, Math.min(p.flap.track.length - 1, i))] ? p.flap.open : p.flap.shut;
  const caps = (p.capList ?? []).filter((c) => local >= c.from && (c.until === null || local < c.until));
  // keystrokes inside this panel: every third, alternating the two drawn labels
  const end = p.start + p.durF / cut.fps;
  const strokes = TYPE_HITS.filter((h) => h >= p.start - 0.02 && h < end).map((h) => h - p.start).filter((_, k) => k % 3 === 0);
  const typeWords = p.sfxw.filter((s) => s.type);
  return (
    <AbsoluteFill>
      {p.exp === "contract" || p.exp === "contract2" ? null
        : <Img src={plate(src)} style={{position: "absolute", left: 0, top: 0, width: 720, height: 1280}} />}
      {p.exp ? <Visual p={p} local={local} /> : null}
      {p.mark ? <CornerMark t={tGlobal} /> : null}
      {p.sfxw.map((s, k) => (
        <SfxWordView key={k} s={s} local={local}
          hits={s.type ? strokes.filter((_, n) => n % typeWords.length === typeWords.indexOf(s)) : s.hits ?? [s.at ?? 0]} />
      ))}
      {caps.map((c, k) => <Caption key={k} c={c} />)}
      {p.header ? <TimeHeader t={p.header} /> : null}
    </AbsoluteFill>
  );
};

export const PromptEng: React.FC = () => (
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
        const names = p.flap ? [p.flap.open, p.flap.shut] : [p.plate];
        return (
          <Sequence key={"pre" + n} from={Math.max(0, p.startF - 12)} durationInFrames={12}>
            <AbsoluteFill style={{opacity: 0}}>{names.map((m) => <Img key={m} src={plate(m)} style={{width: 10, height: 10}} />)}</AbsoluteFill>
          </Sequence>
        );
      })}
    </div>

    {/* VO: every line is its own wav, played from zero. Never seek an mp3. */}
    {cut.vo.map((v, n) => (
      <Sequence key={"vo" + n} from={Math.round(v.at * cut.fps)} name={v.name}>
        <Audio src={staticFile(`pe/${v.file}`)} />
      </Sequence>
    ))}
    {(cut.sfx as {file: string; at: number; gain: number}[]).map((x, n) => (
      <Sequence key={"sfx" + n} from={Math.round(x.at * cut.fps)} name={x.file}>
        <Audio src={staticFile(`pe/${x.file}`)} volume={x.gain} />
      </Sequence>
    ))}
    {/* the office bed, ducked under every voice, baked whole */}
    <Audio src={staticFile(`pe/${cut.bed.file}`)} volume={cut.bed.gain} />
  </AbsoluteFill>
);
