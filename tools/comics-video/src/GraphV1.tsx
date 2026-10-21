import React from "react";
import {
  AbsoluteFill, Audio, Img, Sequence, staticFile,
  interpolate, useCurrentFrame,
} from "remotion";
import mouth from "./graph_mouth.json";
import { DoorReveal, GraphTeach, DOORS_LEAD, DOORS_SLAM } from "./GraphExplainers";

/**
 * EP002 — "graph engineering"  (channel: AI FOMO)
 *
 * Assembly rules carried over from EP001 (loop) and the intro:
 *  - Panels HARD-CUT. No crossfades, ever.
 *  - Captions: loop style — Lato 800, 32px/720 (48px here), white fill,
 *    5px/720 (7.5px) black stroke, paintOrder stroke, whole line at once.
 *  - AI mark pulses like the loop: 1 + sin(t*2.1)*0.035.
 *  - Lip flap: open/closed plates switched on the VO's RMS envelope
 *    (graph_mouth.json), same as the intro.
 *  - Night = silence: office bed fades out when the lights go off and only
 *    returns with daylight. A snore loop carries the night instead.
 *  - "click" lettering pops with the keyboard hits (loop's Click behaviour).
 *  - Ends on "…but. what time is it?" and loops straight into frame 1.
 *
 * Voices: KEN = Thomas · AJ = Kai (kai_re = shouts + "you're done") · AI = David.
 * NOTE: snore.mp3 is SYNTHESIZED (no snore in the Drive SFX folder) — swap the
 * file when Sejal finds a real one; timing stays.
 */

export const FPS = 30;
const S = 1.5; // 720-space -> 1080 comp
const F = (n: string) => staticFile(`v10/graph/${n}.png`);
const A = (n: string) => staticFile(`v10/audio/graph/${n}`);
const SFX = (n: string) => staticFile(`v10/sfx/${n}`);

const FONT = `
@font-face { font-family:'LatoLocal';
  src:url('${staticFile("v10/fonts/Lato-Regular.ttf")}') format('truetype'); font-weight:400; }
@font-face { font-family:'MonaSans';
  src:url('${staticFile("v10/fonts/MonaSans-ExtraBold.woff2")}') format('woff2'); font-weight:800; }
@font-face { font-family:'GeistMono';
  src:url('${staticFile("v10/fonts/GeistMono-Bold.woff2")}') format('woff2'); font-weight:700; }
@font-face { font-family:'JakartaLocal';
  src:url('${staticFile("v10/fonts/PlusJakartaSans-Medium.woff2")}') format('woff2'); font-weight:500; }`;
const CAP = "'LatoLocal','Helvetica Neue',Arial,sans-serif";
const DISPLAY = "'MonaSans','Helvetica Neue',Arial,sans-serif";
const MONO = "'GeistMono','SFMono-Regular',monospace";
const CHROME = "'JakartaLocal','Helvetica Neue',Arial,sans-serif";
const TEAL = "#03A6CF";

// ---- AI mark, loop pulse ----------------------------------------------------
const AIMark: React.FC<{ size: number }> = ({ size }) => {
  const f = useCurrentFrame();
  const pulse = 1 + Math.sin((f / FPS) * 2.1) * 0.035;
  return (
    <div style={{ transform: `scale(${pulse})` }}>
      <svg width={size} height={size} viewBox="-6 -6 112 112">
        {[0, 60, 120, 180, 240, 300].map((r) => (
          <ellipse key={r} cx="50" cy="25" rx="14.5" ry="25" fill={TEAL} transform={`rotate(${r} 50 50)`} />
        ))}
        <circle cx="59" cy="50" r="17" fill="#ffffff" />
        <circle cx="59" cy="50" r="11" fill={TEAL} />
      </svg>
    </div>
  );
};

// ---- caption: loop style (sub block from cut.json) --------------------------
type Cap = { t: string; x: number; y: number; w: number; size?: number; italic?: boolean };
const Caption: React.FC<{ c: Cap }> = ({ c }) => {
  const size = (c.size ?? 32) * S;
  return (
    <div style={{
      position: "absolute", left: c.x * S, top: c.y * S, width: c.w * S,
      textAlign: "center", fontFamily: CAP, fontSize: size, fontWeight: 800,
      fontStyle: c.italic ? "italic" : "normal", lineHeight: 42 / 32,
      color: "#FFFFFF", WebkitTextStroke: `${5 * S}px #000000`,
      paintOrder: "stroke",
    }}>{c.t}</div>
  );
};

// ---- "click" lettering that pops with the keyboard (loop behaviour) ---------
const Click: React.FC<{ cx: number; cy: number; size: number; hits: number[] }> = ({ cx, cy, size, hits }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  let spike = 0;
  for (const h of hits) if (t >= h && t < h + 0.26) spike = Math.max(spike, 1 - (t - h) / 0.26);
  const opacity = 0.3 + 0.7 * spike * spike;
  const scale = 1 + 0.1 * spike;
  return (
    <div style={{
      position: "absolute", left: cx * S, top: cy * S,
      transform: `translate(-50%,-50%) scale(${scale})`,
      fontFamily: "Arial, Helvetica, sans-serif", fontSize: size * S,
      color: "#3a3a3a", opacity, whiteSpace: "nowrap",
    }}>click</div>
  );
};

// ---- time header ---------------------------------------------------------
// Sits over the intern and changes when the LIGHT does, not when a sound does:
// 10 PM on the dark plate, 8:50 AM the moment daylight is back — which is the
// frame before the ding, not after it. A card here interrupted the
// laugh-to-sleep cut, so the time rides the panel instead of stopping it.
const TimeHeader: React.FC<{ t: string }> = ({ t }) => {
  const f = useCurrentFrame();
  const k = Math.min(1, f / 5);
  return (
    <div style={{
      position: "absolute", left: 0, top: 78 * S, width: "100%", textAlign: "center",
      fontFamily: MONO, fontWeight: 700, fontSize: 46 * S, letterSpacing: 1 * S,
      color: "#FFFFFF", WebkitTextStroke: `${4.5 * S}px #000000`, paintOrder: "stroke",
      opacity: k,
    }}>{t}</div>
  );
};

// ---- SFX lettering: every sound word pops, same language as the click -------
// RULE: no SFX word is ever baked flat into a plate. It snaps in ON its sound,
// overshoots, settles, and clears. (click / swipe / *ding* / -AH / AHHHHHH-)
type Sfx = { t: string; x: number; y: number; w: number; size: number; at: number; rot?: number; hold?: number; color?: string };
const SfxText: React.FC<{ s: Sfx }> = ({ s }) => {
  const f = useCurrentFrame();
  const e = f / FPS - s.at;
  if (e < 0) return null;
  const hold = s.hold ?? 0.75;
  const inK = Math.min(1, e / 0.05);
  const outK = 1 - Math.max(0, Math.min(1, (e - hold) / 0.22));
  const spike = Math.max(0, 1 - e / 0.26); // the click's 0.26s decay
  return (
    <div style={{
      position: "absolute", left: s.x * S, top: s.y * S, width: s.w * S,
      transform: `rotate(${-(s.rot ?? 0)}deg) scale(${1 + 0.18 * spike})`,
      transformOrigin: "0 0", textAlign: "center",
      fontFamily: CAP, fontSize: s.size * S, color: s.color ?? "#1e1e1e",
      opacity: inK * outK, whiteSpace: "nowrap",
    }}>{s.t}</div>
  );
};

// ---- scene table ------------------------------------------------------------
type Zoom = { from: number; to: number; ox?: string; oy?: string };
type Scene = {
  img: string; vo: string | null; sec: number;
  // reuse another panel's artwork under a different scene identity (the loop
  // frame is literally frame 1's plate, so the cut back to the top is invisible)
  plate?: string;
  cap?: Cap; mark?: "screen" | "card" | null; zoom?: Zoom; end?: boolean;
  ding?: boolean; scream?: boolean; swipeAt?: number; thudAt?: number;
  voAt?: number;   // hold the VO back while something walks into frame
  clicks?: { cx: number; cy: number; size: number }[]; hits?: number[];
  sfx?: Sfx[];
  // the AI's two long teaching lines play over an animated explainer instead of
  // a plate, and their caption is split into clauses that land with the beats
  header?: string;
  explainer?: "doors" | "teach";
  caps?: (Cap & { at: number; until: number })[];
};
const S_: Scene[] = [
  // s1.mp3 is now the SECOND half of Ken's panel-33 take — same voice, same
  // breath across the loop point, which is the whole reason it works
  { img: "s1",  vo: "s1.mp3",  sec: 3.05, cap: { t: "you took all night for this??", x: 175, y: 219, w: 379 } },
  { img: "s2",  vo: "s2.mp3",  sec: 2.85, swipeAt: 0.7, cap: { t: "…you're an intern, it's fine.", x: 175, y: 178, w: 429 },
    sfx: [{ t: "swipe", x: 326, y: 769.76, w: 62, size: 24, rot: 31.9, at: 0.7, color: "#ffffff" }] },
  { img: "s3",  vo: null,      sec: 0.70 },
  { img: "s4",  vo: null,      sec: 0.30 }, // Ken walks — a flash, he's gone
  { img: "s5",  vo: "s45.mp3", sec: 3.20, swipeAt: 1.2, cap: { t: "just graph it next time, saves you the all-nighter.", x: 175, y: 150, w: 440 },
    sfx: [{ t: "swipe", x: 326, y: 769.76, w: 62, size: 24, rot: 31.9, at: 1.2, color: "#ffffff" }] },
  { img: "s6",  vo: "s6.mp3",  sec: 3.05, cap: { t: "yeah, got it. out by ten tonight.", x: 96, y: 486, w: 200 } },
  { img: "s7",  vo: "s7.mp3",  sec: 2.80, cap: { t: "I have no idea what that means.", x: 372, y: 330, w: 236, size: 26, italic: true } },
  { img: "s8",  vo: "s8.mp3",  sec: 3.62, cap: { t: "okay, build the API, write the tests, docs,", x: 200, y: 96, w: 370 },
    clicks: [{ cx: 538, cy: 755, size: 30 }, { cx: 540, cy: 1018, size: 36 }],
    hits: [0.45, 0.7, 1.15, 1.6, 1.85, 2.2, 2.7, 2.95, 3.25] },
  { img: "s9",  vo: "s9.mp3",  sec: 2.30, cap: { t: "and the changelog. do all four.", x: 200, y: 96, w: 370 },
    clicks: [{ cx: 554, cy: 732, size: 36 }],
    hits: [0.38, 0.68, 0.93, 1.43, 1.83, 2.23] },
  { img: "s10", vo: "s10.mp3", sec: 3.37, cap: { t: "and uh, graph it or something.", x: 200, y: 96, w: 370 },
    clicks: [{ cx: 538, cy: 755, size: 30 }, { cx: 540, cy: 1018, size: 36 }],
    hits: [0.18, 0.43, 0.78, 1.13, 2.63, 2.88, 3.33] },
  { img: "s11", vo: "s11.mp3", sec: 2.98, mark: "screen", cap: { t: "On it. Do any of these depend on each other?", x: 100, y: 285, w: 520, size: 28 } },
  { img: "s12", vo: "s12.mp3", sec: 2.05, cap: { t: "whatever, go", x: 200, y: 214, w: 370 } },
  { img: "s13", vo: "s13_hell.mp3", sec: 1.40, cap: { t: "what the hell?", x: 200, y: 214, w: 370 } },
  { img: "s14", vo: "s14_laugh.mp3", sec: 0.50, cap: { t: "HAHAHA-", x: 200, y: 214, w: 370 } }, // cut MID-laugh, hard
  { img: "s15", vo: null,      sec: 1.70, header: "10:00 PM" }, // night — long past ten
  { img: "s16", vo: null,      sec: 1.20, header: "8:50 AM" },
  { img: "s17", vo: "s17_ah.mp3", sec: 0.70, ding: true, header: "8:50 AM", // ding → AH → instant cut
    sfx: [{ t: "*ding*", x: 376, y: 341, w: 370, size: 32, at: 0.0, hold: 0.4 },
          { t: "-AH", x: 56, y: 303, w: 370, size: 32, at: 0.167, hold: 0.4 }] },
  { img: "s18", vo: "s18.mp3", sec: 2.36, cap: { t: "you're done?? you didn't even need me.", x: 40, y: 140, w: 380 } },
  { img: "s19", vo: "s19.mp3", sec: 1.42, cap: { t: "sick!!!", x: 40, y: 140, w: 380, size: 36 } },
  { img: "s20", vo: "s20.mp3", sec: 3.05, mark: "screen", cap: { t: "Yes. Though you could've been home by eight.", x: 100, y: 285, w: 520, size: 28 } },
  { img: "s21", vo: "s21.mp3", sec: 1.50, cap: { t: "…what do you mean?", x: 40, y: 140, w: 380 } },
  // the explainer carries itself: no subtitle, no AI mark, no narration on screen
  // the queue walks in first (DOORS_LEAD), and David only starts once the line
  // is standing — so the panel, the VO and the thud all carry the same offset
  { img: "s22", vo: "s22.mp3", sec: 9.70 + DOORS_LEAD, explainer: "doors",
    voAt: DOORS_LEAD, thudAt: DOORS_SLAM + DOORS_LEAD },  // slam + cat, then out
  { img: "s23", vo: "s23.mp3", sec: 2.46, cap: { t: "wait, you can run them at the same time??", x: 40, y: 140, w: 380 } },
  { img: "s24", vo: "s24.mp3", sec: 12.30, explainer: "teach" },
  // The defence, in the vocabulary the viewer was just taught. The static
  // screen used to hold 6.8s on one long line — now it carries one sentence
  // and hands the rest to the push-in, which at least moves.
  { img: "s25", vo: "s25.mp3", sec: 2.75, mark: "screen",
    cap: { t: "You gave me four dots and no arrows.", x: 100, y: 150, w: 520, size: 28 } },
  { img: "s26", vo: "s26.mp3", sec: 5.80, zoom: { from: 1.0, to: 1.26, ox: "22%", oy: "42%" },
    caps: [{ t: "So I assumed everything might depend on everything", x: 240, y: 140, w: 390, size: 28, at: 0.00, until: 2.30 },
           { t: "and ran them one at a time.", x: 240, y: 140, w: 390, size: 28, at: 2.30, until: 4.10 },
           { t: "It was the only safe way.", x: 240, y: 140, w: 390, size: 28, at: 4.10, until: 5.80 }] },
  { img: "s27", vo: "s27.mp3", sec: 1.39, cap: { t: "…and you're telling me this…", x: 80, y: 130, w: 380 } },
  { img: "s28", vo: "s28.mp3", sec: 1.30, cap: { t: "NOW?", x: 80, y: 130, w: 380, size: 42 } },
  { img: "s29", vo: "s29_ai.mp3", sec: 1.95, mark: "screen", scream: true, cap: { t: "You said 'whatever.'", x: 100, y: 165, w: 520, size: 28 } },
  { img: "END", vo: null,      sec: 4.60, end: true },
  { img: "s31", vo: "s31.mp3", sec: 2.60, cap: { t: "…you know what? couldn't care less.", x: 80, y: 415, w: 240, size: 26 } },
  { img: "s32", vo: "s32.mp3", sec: 2.45, cap: { t: "…but. what time is it?", x: 372, y: 330, w: 236, size: 26, italic: true } }, // a THOUGHT — mouth stays closed, italic like s7
  // THE LOOP. Same plate as frame 1, so the picture never changes across the
  // cut — only Ken's sentence carries on. He answers the thought with the time,
  // walks straight into the setup, and stops on "but-"; the film restarts and
  // finishes his line for him. Both halves come off ONE Ken take so the join
  // has the same room tone and the same breath.
  // first half of the Ken take; its second half is s1.mp3, so the sentence
  // simply carries on across the cut
  // The caption is split on his own pause. Held as one block it puts "but-" on
  // screen five seconds before he says it, and the whole loop depends on that
  // word arriving late.
  { img: "s33", plate: "s1", vo: "s33.mp3", sec: 5.30,
    caps: [{ t: "it's 9 am.", x: 150, y: 180, w: 420, at: 0.00, until: 1.70 },
           { t: "you said you'd be done by 10 pm yesterday but-", x: 150, y: 180, w: 420, at: 1.70, until: 5.30 }] },
];

const starts: number[] = [];
let cursor = 0;
S_.forEach((sc) => { starts.push(cursor); cursor += Math.round(sc.sec * FPS); });
export const GRAPH_DURATION = cursor;
const durF = (i: number) => Math.round(S_[i].sec * FPS);
const IDX = (img: string) => S_.findIndex((s) => s.img === img);
const KB_FROM = IDX("s8");
const NIGHT_AT = starts[IDX("s15")] / FPS;
const MORNING_AT = starts[IDX("s18")] / FPS;
const S29_AI_SEC = 1.66;

// ---- end card: loop slate + TIME odometer rolling through the night ---------
const HOURS = ["8:50 AM","8:51 AM","8:52 AM","8:53 AM","8:54 AM","8:55 AM","8:56 AM","8:57 AM","8:58 AM","8:59 AM","9:00 AM"];
const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const ease = (x: number) => 1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 3);
  const titleIn = ease(t / 0.45);
  const ruleK = ease((t - 0.5) / 0.4);
  const step = (d: number) => ease((t - 0.7 - d) / 0.35);
  const meterK = ease((t - 1.5) / 0.4);
  // odometer: the clock spins through the night and lands on 9:00 AM
  const rollP = Math.max(0, Math.min(1, (t - 1.9) / 1.3));
  const eased = 1 - Math.pow(1 - rollP, 2.2);
  const hi = Math.min(HOURS.length - 1, Math.floor(eased * (HOURS.length - 1) + 0.0001));
  const landed = hi === HOURS.length - 1;
  const pop = landed ? 1 + 0.09 * Math.max(0, 1 - (t - (1.9 + 1.3)) / 0.3) : 1;
  return (
    <AbsoluteFill style={{ backgroundColor: "#141416" }}>
      <div style={{ position: "absolute", left: 0, width: "100%", top: 410, textAlign: "center",
        opacity: titleIn, transform: `translateY(${(1 - titleIn) * 24}px)` }}>
        {["I HAVE NO IDEA", "WHAT THAT MEANS"].map((l, i) => (
          <div key={i} style={{ fontFamily: DISPLAY, fontWeight: 800, fontSize: 80, lineHeight: 1.15,
            letterSpacing: -1.5, color: "#F2F2EF" }}>{l}</div>
        ))}
      </div>
      <div style={{ position: "absolute", left: "50%", top: 600, width: 270 * ruleK, height: 3,
        marginLeft: -135 * ruleK, background: TEAL }} />
      <div style={{ position: "absolute", left: 0, width: "100%", top: 674, textAlign: "center",
        fontFamily: DISPLAY, fontWeight: 800, fontSize: 76, letterSpacing: -2, color: "#F2F2EF",
        opacity: step(0) }}>graph engineering</div>
      <div style={{ position: "absolute", left: 0, width: "100%", top: 786, textAlign: "center",
        fontFamily: MONO, fontSize: 30, color: "#8A8A93", opacity: step(0.12) }}>/ɡraf ˈen.dʒɪ.nɪə.rɪŋ/  noun</div>
      <div style={{ position: "absolute", left: 0, width: "100%", top: 850, textAlign: "center",
        fontFamily: CHROME, fontWeight: 500, fontSize: 40, lineHeight: 1.35, color: "#B9B9C0",
        opacity: step(0.24) }}>
        Name what waits on what, and<br />independent work runs at once.
      </div>
      <div style={{ position: "absolute", left: "50%", top: 1140, width: 588, height: 260, marginLeft: -294,
        background: "#23232B", border: "2px solid #40404B", borderRadius: 24, opacity: meterK,
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
        <div style={{ fontFamily: CHROME, fontWeight: 500, fontSize: 28, letterSpacing: 3, color: "#8A8A93" }}>TIME</div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 92, color: TEAL, marginTop: 10,
          transform: `scale(${pop})` }}>{HOURS[hi]}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---- panel ------------------------------------------------------------------
const Panel: React.FC<{ sc: Scene; len: number; sceneStart: number }> = ({ sc, len }) => {
  const f = useCurrentFrame();
  if (sc.end) return <EndCard />;
  let scale = 1;
  if (sc.zoom) scale = interpolate(f, [0, len], [sc.zoom.from, sc.zoom.to], { extrapolateRight: "clamp" });
  // lip flap: show OPEN plate while the VO is voiced, CLOSED otherwise
  const m = (mouth as Record<string, { open: string; closed: string; v: boolean[] }>)[sc.img];
  const voiced = m ? (m.v[f] ?? false) : false;
  const plate = m ? (voiced ? m.open : m.closed) : (sc.plate ?? sc.img);
  const t = f / FPS;
  const screamOn = sc.scream && t >= S29_AI_SEC + 0.06;
  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      <AbsoluteFill style={{ transform: `scale(${scale})`, transformOrigin: `${sc.zoom?.ox ?? "50%"} ${sc.zoom?.oy ?? "50%"}` }}>
        {sc.explainer === "doors" ? <DoorReveal />
          : sc.explainer === "teach" ? <GraphTeach />
          : <Img src={F(plate)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />}
      </AbsoluteFill>
      {sc.mark === "screen" && (
        <div style={{ position: "absolute", left: "50%", top: 1078, transform: "translate(-50%,-50%)" }}>
          <AIMark size={232} />
        </div>
      )}
      {sc.mark === "card" && (
        <div style={{ position: "absolute", left: "50%", top: 1590, transform: "translate(-50%,-50%)" }}>
          <AIMark size={92} />
        </div>
      )}
      {sc.clicks?.map((c, i) => <Click key={i} cx={c.cx} cy={c.cy} size={c.size} hits={sc.hits ?? []} />)}
      {sc.sfx?.map((s, i) => <SfxText key={`x${i}`} s={s} />)}
      {sc.header && <TimeHeader t={sc.header} />}
      {sc.cap && <Caption c={sc.cap} />}
      {sc.caps?.filter(c => t >= c.at && t < c.until).map((c, i) => <Caption key={`c${i}`} c={c} />)}
      {screamOn && (
        <div style={{
          position: "absolute", left: 340 * S, top: 330 * S, width: 340 * S, textAlign: "center",
          fontFamily: CAP, fontWeight: 800, fontSize: 46 * S, color: "#FFFFFF",
          WebkitTextStroke: `${5 * S}px #000000`, paintOrder: "stroke",
          transform: `scale(${1 + 0.15 * Math.max(0, 1 - (t - (S29_AI_SEC + 0.06)) / 0.2)})`,
        }}>AHHHHHH-</div>
      )}
    </AbsoluteFill>
  );
};

/** Storyboard exports need the same frames twice: once as shipped, once clean.
 *  `caps={false}` drops every piece of overlaid text (captions, SFX lettering,
 *  the time header) and keeps the artwork, the AI mark and the explainers. */
export const GraphV1: React.FC<{ caps?: boolean }> = ({ caps = true }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <style>{FONT}</style>
      {/* office bed — PRE-RENDERED full-length track (amb_track.mp3):
          printer removed, night silence baked in, and the video's END is the
          stretch of ambience that leads directly INTO its START, so the loop
          back to frame 1 is sonically seamless.
          (Do NOT use volume-fn + loop on one Audio: the callback gets
          loop-relative frames, which re-applied the night dip mid-film — the
          v5 drop during "You said 'graph it'".) */}
      <Audio src={SFX("amb_track.mp3")} volume={0.5} />
      {/* snore through the night, until the ding wakes him (synthetic placeholder) */}
      <Sequence from={starts[IDX("s15")]} durationInFrames={starts[IDX("s17")] - starts[IDX("s15")]}>
        <Audio src={SFX("snore.mp3")} volume={0.65} loop />
      </Sequence>
      {/* keyboard ONLY while the intern types (s8..s10) — the Sequence length is
          the hard stop; a looped Audio's endAt does NOT stop it (v4 bug: clicks
          leaked over the AI's lines and the rest of the film) */}
      <Sequence from={starts[KB_FROM]}
        durationInFrames={Math.round((S_[KB_FROM].sec + S_[KB_FROM + 1].sec + S_[KB_FROM + 2].sec) * FPS)}>
        <Audio src={SFX("keyboard.mp3")} volume={0.34} loop />
      </Sequence>

      {S_.map((sc, i) => (
        <Sequence key={i} from={starts[i]} durationInFrames={durF(i)}>
          <Panel sc={caps ? sc : { ...sc, cap: undefined, caps: undefined, sfx: undefined, header: undefined }}
            len={durF(i)} sceneStart={starts[i]} />
          {sc.vo && !sc.ding && (sc.voAt
            ? <Sequence from={Math.round(sc.voAt * FPS)}><Audio src={A(sc.vo)} /></Sequence>
            : <Audio src={A(sc.vo)} />)}
          {sc.ding && <Audio src={SFX("ding.mp3")} volume={0.65} />}
          {sc.ding && sc.vo && <Sequence from={5}><Audio src={A(sc.vo)} /></Sequence>}
          {sc.thudAt !== undefined && (
            <Sequence from={Math.round(sc.thudAt * FPS)}>
              <Audio src={SFX("door_thud.mp3")} volume={1.0} />
            </Sequence>
          )}
          {sc.swipeAt !== undefined && (
            <Sequence from={Math.round(sc.swipeAt * FPS)}>
              <Audio src={SFX("phone_tick.mp3")} volume={0.55} />
            </Sequence>
          )}
          {sc.scream && (
            <Sequence from={Math.round((S29_AI_SEC + 0.06) * FPS)}>
              <Audio src={A("s29_scream.mp3")} volume={0.95} />
            </Sequence>
          )}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
