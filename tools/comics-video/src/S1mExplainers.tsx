import React from "react";
import {Img, spring, staticFile} from "remotion";
import CATS from "./s1m_cats.json";
import {AIMark, TEAL} from "./AIMark";

/**
 * system one model — the explainers and the screens.
 *
 * Design source: Figma page `system one model`, section "explainers & screens"
 * (exp-08 … exp-55). Everything here is authored in 720 x 1280 space, the same
 * numbers as the Figma frames, and the caller scales the whole stage.
 *
 * Motion language (Sejal's bar): mask rises, wipes, stroke draw-ons, count-ups,
 * expo-out easing. No bounce, no lone fades, no scale pops — except the grid of
 * dots, which uses the series' one staggered spring pop-in, left to right.
 * Every event is keyed to a measured word time passed in `ev`.
 */

export const C = {
  ink: "#17171A", door: "#2A2A2E", muted: "#808087", soft: "#C7C7C9", hair: "#E7E7E3",
  wash: "#F4F4F2", teal: "#03A6CF", tealbg: "#E0F5FB", coral: "#FF6B6B", coralbg: "#FFEEEE",
  white: "#FFFFFF",
};
const LBL = "'LatoSemi','LatoLocal','Helvetica Neue',Arial,sans-serif";
const BODY = "'LatoLocal','Helvetica Neue',Arial,sans-serif";
const MONO = "'GeistMono',ui-monospace,Menlo,monospace";
const SHADOW = "0 1px 2px rgba(18,18,26,.06), 0 14px 36px -6px rgba(18,18,26,.10)";
export const SCR = {x: 41, y: 528, w: 638, h: 371};

/* ------------------------------------------------------------------ easing */
const clamp = (x: number) => Math.max(0, Math.min(1, x));
const expoOut = (x: number) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x));
const quartInOut = (x: number) => (x < 0.5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2);
const smoother = (x: number) => x * x * x * (x * (x * 6 - 15) + 10);
/** 0 -> 1 from `at` over `dur`, decelerating to rest */
export const k = (t: number, at: number | null | undefined, dur = 0.45, ease = expoOut) =>
  at == null ? 0 : ease(clamp((t - at) / dur));
const lerp = (a: number, b: number, x: number) => a + (b - a) * x;
const fmt = (n: number) => Math.round(n).toLocaleString("en-US");
/** an oscillation enveloped in AND out, so it never stops dead */
const pulse = (t: number, at: number, len: number, hz = 3.4) => {
  const e = t - at;
  if (e < 0 || e > len) return 0;
  return Math.abs(Math.sin(e * hz)) * Math.min(1, e / 0.28) * Math.min(1, (len - e) / 0.45);
};

/* ------------------------------------------------------------------ motion primitives */
/** content rises from behind a mask (the type-from-a-clip move) */
const Rise: React.FC<{k: number; style?: React.CSSProperties; children: React.ReactNode; dy?: number}> =
({k: v, style, children, dy = 1}) => (
  <div style={{position: "absolute", overflow: "hidden", ...style}}>
    <div style={{transform: `translateY(${(1 - v) * 105 * dy}%)`}}>{children}</div>
  </div>
);
/** a left-to-right mask wipe */
// fully revealed = no clip at all, so a card's shadow is never cut off at the mask edge
const wipeX = (v: number): React.CSSProperties => (v >= 0.999 ? {} : {clipPath: `inset(-60px ${(1 - v) * 100}% -60px -60px)`});
const wipeY = (v: number): React.CSSProperties => (v >= 0.999 ? {} : {clipPath: `inset(-60px -60px ${(1 - v) * 100}% -60px)`});

const Label: React.FC<{children: React.ReactNode; color?: string; size?: number; style?: React.CSSProperties}> =
({children, color = C.muted, size = 12, style}) => (
  <div style={{fontFamily: LBL, fontWeight: 800, fontSize: size, letterSpacing: size * 0.14,
    textTransform: "uppercase", color, whiteSpace: "nowrap", lineHeight: 1.25, ...style}}>{children}</div>
);

/* ================================================================== SCREENS (inside the monitor) */
const Tab: React.FC<{label: string; dot?: string; t?: number}> = ({label, dot, t = 0}) => (
  <div style={{position: "absolute", left: 24, top: 20, display: "flex", alignItems: "center", gap: 8,
    padding: "6px 14px 6px 12px", borderRadius: 8, background: C.wash}}>
    {dot ? (
      <div style={{width: 8, height: 8, borderRadius: 4, background: dot,
        opacity: 0.55 + 0.45 * (0.5 + 0.5 * Math.sin(t * 3.4))}} />
    ) : (
      <div style={{width: 9, height: 11, borderRadius: 2, border: `1.5px solid ${C.muted}`}} />
    )}
    <span style={{fontFamily: MONO, fontWeight: 500, fontSize: 14, color: C.muted}}>{label}</span>
  </div>
);

const Screen: React.FC<{children: React.ReactNode; bg?: string}> = ({children, bg}) => (
  <div style={{position: "absolute", left: SCR.x, top: SCR.y, width: SCR.w, height: SCR.h,
    overflow: "hidden", background: bg}}>{children}</div>
);

/* exp-08  the ask_ai script, typed, then the ten-for-ten test */
// customer-PDF version (v7): the same script, asking what kind of document each PDF is
const CODE = ["def sort_doc(file):", "    return ask_ai(", "        \"What kind of document",
  "         is this?\",", "        file)"];
export const CodeScreen: React.FC<{t: number}> = ({t}) => {
  const total = CODE.join("").length;
  // slower, so it can be read (Sejal, 9 Oct): 2.6s of typing, then the test lands at 3.1s
  const typed = Math.floor(total * clamp((t - 0.2) / 2.6));
  let left = typed;
  const caretOn = Math.floor(t * 2.2) % 2 === 0 || typed < total;
  const badge = k(t, 3.1, 0.5);
  const n = Math.round(10 * k(t, 3.15, 0.65));
  return (
    <Screen>
      <Tab label="sort.py" />
      {CODE.map((ln, i) => {
        const shown = ln.slice(0, Math.max(0, left)); left -= ln.length;
        const last = left < 0 && left + ln.length >= 0;
        return (
          <div key={i} style={{position: "absolute", left: 32, top: 78 + i * 30, display: "flex", alignItems: "baseline"}}>
            <span style={{width: 46, fontFamily: MONO, fontSize: 14, color: C.soft}}>{i + 1}</span>
            <span style={{fontFamily: MONO, fontWeight: 500, fontSize: 19, color: C.ink, whiteSpace: "pre"}}>{shown}</span>
            {last && caretOn ? <span style={{display: "inline-block", width: 10, height: 21, background: C.ink, marginLeft: 1, transform: "translateY(3px)"}} /> : null}
          </div>
        );
      })}
      <div style={{position: "absolute", right: 24, bottom: 22, display: "flex", alignItems: "center", gap: 10,
        padding: "8px 16px 8px 14px", borderRadius: 10, background: C.tealbg, ...wipeX(badge)}}>
        <Label color={C.teal} size={13}>TEST</Label>
        <span style={{fontFamily: MONO, fontWeight: 600, fontSize: 18, color: C.teal}}>{n} / 10 {n === 10 ? "✓" : ""}</span>
      </div>
    </Screen>
  );
};

/* exp-19 / 20 / 21  the night run, and the limit */
const REASONING = ["Let me think this through carefully…", "Page 6 of 9. Mostly transactions.",
  "But page 1 shows a home address.", "So: address proof, or a statement?",
  "Consider the letterhead. And the…", "On page 2, the account holder…"];
export const NightScreen: React.FC<{t: number; variant: "night" | "limit_night" | "limit_day"}> = ({t, variant}) => {
  const limit = variant !== "night";
  const animate = variant !== "limit_day";
  // night: the reasoning streams in, line by line, under a blinking cursor
  const shown = limit ? REASONING.length : Math.min(REASONING.length, Math.floor((t - 0.1) / 0.36) + 1);
  // limit: the last few tickets tick over, the bar fills, then it stops dead
  const tick = limit && animate ? k(t, 0.05, 0.75, quartInOut) : 1;
  const count = limit ? Math.round(lerp(10409, 10416, tick)) : 8548;
  const spend = limit ? lerp(249.83, 250, tick) : 205.15;
  const frac = limit ? lerp(0.9993, 1, tick) : 0.82;
  const dim = limit ? (animate ? lerp(1, 0.32, k(t, 0.85, 0.4)) : 0.32) : 1;
  const banner = limit ? (animate ? k(t, 1.0, 0.5) : 1) : 0;
  return (
    <Screen>
      <Tab label={limit ? "sort.py · stopped" : "sort.py · running"} dot={limit ? C.coral : C.teal} t={t} />
      <div style={{position: "absolute", left: 28, top: 70, fontFamily: MONO, fontWeight: 600, fontSize: 20, color: C.ink, opacity: dim}}>
        Document #{fmt(count)} <span style={{fontWeight: 400, fontSize: 14, color: C.muted}}>· bank statement · p. 6 / 9</span>
      </div>
      {REASONING.slice(0, Math.max(0, shown)).map((l, i) => {
        const v = limit ? 1 : k(t, 0.1 + i * 0.36, 0.3);
        const op = (limit ? 0.32 : Math.max(0.35, 1 - i * 0.12));
        return (
          <Rise key={i} k={v} style={{left: 28, top: 106 + i * 26, height: 24, width: 560}}>
            <span style={{fontFamily: MONO, fontSize: 16, color: C.muted, opacity: op, whiteSpace: "nowrap"}}>
              {l}{!limit && i === shown - 1 && Math.floor(t * 2.4) % 2 === 0 ? " ▍" : ""}
            </span>
          </Rise>
        );
      })}
      <div style={{position: "absolute", left: 0, top: SCR.h - 66, width: SCR.w, height: 66, background: C.white, borderTop: `1px solid ${C.hair}`}} />
      <div style={{position: "absolute", left: 28, top: SCR.h - 50, fontFamily: MONO, fontWeight: 600, fontSize: 22, color: C.ink}}>
        {fmt(count)} / 80,000
      </div>
      <div style={{position: "absolute", left: 330, top: SCR.h - 38, width: 170, height: 10, borderRadius: 5, background: C.wash, overflow: "hidden"}}>
        <div style={{width: 170, height: 10, borderRadius: 5, background: C.coral, transform: `translateX(${-(1 - frac) * 170}px)`}} />
      </div>
      <div style={{position: "absolute", left: 512, top: SCR.h - 45, fontFamily: MONO, fontWeight: 600, fontSize: 16, color: C.coral}}>
        ${limit ? Math.round(spend) : Math.round(spend)} / $250
      </div>
      {limit ? (
        <div style={{position: "absolute", left: "50%", top: 118, transform: "translateX(-50%)",
          borderRadius: 16, background: C.coral, padding: "18px 28px", textAlign: "center",
          boxShadow: "0 10px 28px -6px rgba(255,107,107,.30)", ...wipeY(banner)}}>
          <Label color={C.white} size={15}>USAGE LIMIT REACHED</Label>
          <div style={{fontFamily: MONO, fontWeight: 600, fontSize: 30, color: C.white, marginTop: 6}}>$250 / $250</div>
        </div>
      ) : null}
    </Screen>
  );
};

/* exp-34  the dense rung: real request / response, slightly too fast to read */
/**
 * exp-34 v2 (Sejal, 9 Oct: the API log was too hard to follow; Figma "exp-34 v2 · 1-4").
 * The VO stays deliberately dense -- it sets up "again, but for a noob" -- so the picture does
 * the work: one big idea per clause, each landing on its word.
 *   outputs   -> the four folder cards rise in (the same doors the nurse uses later)
 *   calibrated-> each card counts up to its probability, bars fill
 *   parallel  -> one PDF fans out to all four cards at once; all four light together
 *   nothing   -> the PDF clears, a word-by-word token stream types in and is struck out,
 *                and the bank card is picked
 */
const D_LABELS = ["BANK\nSTATEMENT", "ID\nPROOF", "ADDRESS\nPROOF", "OTHER"];
const D_P = [97, 1, 1, 1];
const D_TOKENS = ["This", "doc", "ument", "looks", "like", "a", "bank", "state", "ment", "…"];
const mixHex = (a: string, b: string, x: number) => {
  const p = (h: string, i: number) => parseInt(h.slice(1 + i * 2, 3 + i * 2), 16);
  return "#" + [0, 1, 2].map((i) => Math.round(p(a, i) + (p(b, i) - p(a, i)) * clamp(x)).toString(16).padStart(2, "0")).join("");
};
export const DenseScreen: React.FC<{t: number; ev: Record<string, number>}> = ({t, ev}) => {
  const O = ev.outputs ?? 1.5, CAL = ev.calibrated ?? 3.5, PAR = ev.parallel ?? 6.3, NO = ev.nothing ?? 7.4, TOK = ev.token ?? 8.1;
  const CX = [95.5, 244.5, 393.5, 542.5];
  // status, top right: what this beat proves, swapped by a mask rise
  const STATUS: [number, string, string][] = [[O, "4 outputs", C.muted], [PAR - 0.45, "1 pass · 140 ms", C.teal], [NO, "0 tokens generated", C.teal]];
  const cur = STATUS.filter(([at]) => t >= at).pop();
  // beat 3: the PDF and its fan, drawn on together, then undrawn when the tokens arrive
  const chipIn = k(t, PAR - 0.45, 0.4);
  const out = k(t, NO - 0.12, 0.35, quartInOut);
  const fan = k(t, PAR - 0.05, 0.45, quartInOut) * (1 - out);
  const lit = k(t, PAR + 0.36, 0.25);
  const pick = k(t, TOK + 0.45, 0.3);
  const check = k(t, TOK + 0.5, 0.45, quartInOut);
  const tick = k(t, TOK + 0.8, 0.3, quartInOut);
  const strike = k(t, TOK + 0.05, 0.4, quartInOut);
  return (
    <Screen>
      <Tab label="system one model" />
      {cur ? (
        <Rise key={cur[1]} k={k(t, cur[0], 0.3)} style={{left: 300, top: 24, width: 314, height: 22}}>
          <div style={{textAlign: "right", fontFamily: MONO, fontWeight: 600, fontSize: 14, color: cur[2], whiteSpace: "nowrap"}}>{cur[1]}</div>
        </Rise>
      ) : null}

      {/* beat 3: one PDF, one pass, all four at once */}
      <svg width={638} height={371} style={{position: "absolute", left: 0, top: 0}}>
        {CX.map((x) => (
          <path key={x} d={`M 319 88 C 319 118 ${x} 108 ${x} 138`} fill="none" stroke={C.teal} strokeWidth={2}
            strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - fan} opacity={fan > 0.001 ? 1 : 0} />
        ))}
      </svg>
      {chipIn > 0 && out < 0.999 ? (
        <div style={{position: "absolute", left: 0, top: 54, width: 638, display: "flex", justifyContent: "center",
          clipPath: `inset(-30px -30px ${out * 100}% -30px)`}}>
          <div style={{display: "flex", alignItems: "center", gap: 9, padding: "7px 14px 7px 12px", borderRadius: 9,
            background: C.white, border: `1.5px solid ${C.ink}`, boxShadow: SHADOW,
            transform: `translateY(${(1 - chipIn) * 18}px)`, ...wipeY(chipIn)}}>
            <PdfIcon size={16} color={C.ink} />
            <span style={{fontFamily: MONO, fontWeight: 500, fontSize: 14, color: C.ink}}>statement_0417.pdf</span>
          </div>
        </div>
      ) : null}

      {/* beat 4: what a generating model would have done, word by word -- struck out */}
      <div style={{position: "absolute", left: 0, top: 74, width: 638, display: "flex", justifyContent: "center"}}>
        <div style={{position: "relative", display: "flex", gap: 5}}>
          {D_TOKENS.map((tk, j) => {
            const v = k(t, NO + 0.12 + j * 0.055, 0.22);
            return (
              <div key={j} style={{padding: "5px 7px", borderRadius: 6, background: "#EDEDEA", fontFamily: MONO, fontSize: 14,
                color: C.muted, whiteSpace: "pre", transform: `translateY(${(1 - v) * 10}px)`, ...wipeY(v),
                visibility: v > 0 ? "visible" : "hidden"}}>{tk}</div>
            );
          })}
          <div style={{position: "absolute", left: -4, right: -4, top: 13, height: 2.5, borderRadius: 2, background: C.coral,
            ...wipeX(strike), visibility: strike > 0 ? "visible" : "hidden"}} />
        </div>
      </div>

      {/* the four outputs */}
      {D_LABELS.map((lab, i) => {
        const v = k(t, O - 0.05 + i * 0.12, 0.55);
        const n = Math.round(D_P[i] * k(t, CAL + i * 0.1, 0.7));
        const num = k(t, CAL - 0.05 + i * 0.1, 0.35);
        const bar = k(t, CAL + 0.15 + i * 0.1, 0.8, quartInOut);
        const hot = i === 0;
        const on = hot ? lit : lit * (1 - pick);
        const bw = hot ? 1 + 0.5 * lit + 0.5 * pick : 1 + 0.5 * on;
        return (
          <div key={lab} style={{position: "absolute", left: 28 + i * 149, top: 140, width: 135, height: 168, borderRadius: 14,
            background: C.white, boxShadow: `inset 0 0 0 ${bw}px ${mixHex(C.hair, C.teal, on)}, ${SHADOW}`,
            transform: `translateY(${(1 - v) * 26}px)`, ...(v >= 0.999 ? {} : {clipPath: `inset(-40px -40px ${(1 - v) * 100}% -40px)`}),
            visibility: v > 0 ? "visible" : "hidden"}}>
            <div style={{position: "absolute", left: 14, top: 14, width: 40, height: 52, borderRadius: "10px 10px 3px 3px", background: C.door, overflow: "hidden"}}>
              <div style={{position: "absolute", left: 0, top: 0, width: 34, height: 44, transform: "scale(1.1765)", transformOrigin: "0 0"}}><TileGlyph i={i} /></div>
            </div>
            <div style={{position: "absolute", left: 14, top: 78, width: 112, fontFamily: LBL, fontWeight: 800, fontSize: 11,
              letterSpacing: 1.4, lineHeight: "14px", color: C.ink, whiteSpace: "pre"}}>{lab}</div>
            <Rise k={num} style={{left: 14, top: 110, width: 110, height: 34}}>
              <span style={{fontFamily: MONO, fontWeight: 600, fontSize: 26, color: hot ? C.teal : C.muted}}>{n}%</span>
            </Rise>
            <div style={{position: "absolute", left: 14, top: 148, width: 107, height: 6, borderRadius: 3, background: C.wash, ...wipeX(num),
              visibility: num > 0 ? "visible" : "hidden"}}>
              <div style={{width: Math.max(bar > 0 ? 4 : 0, 107 * D_P[i] / 100 * bar), height: 6, borderRadius: 3, background: hot ? C.teal : C.soft}} />
            </div>
            {hot && check > 0 ? (
              <svg width={26} height={26} viewBox="0 0 26 26" style={{position: "absolute", left: 97, top: 14}}>
                <circle cx={13} cy={13} r={6.5} fill="none" stroke={C.teal} strokeWidth={13} pathLength={1} strokeDasharray={1}
                  strokeDashoffset={1 - check} transform="rotate(-90 13 13)" />
                <path d="M 7.5 13.5 L 11.5 17.5 L 18.5 9.5" fill="none" stroke={C.white} strokeWidth={2.6} strokeLinecap="round"
                  strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - tick} />
              </svg>
            ) : null}
          </div>
        );
      })}
    </Screen>
  );
};

/* exp-48  the test batch: 200 dots, three wrong */
const WRONG = new Set([37, 118, 171]);
export const TestScreen: React.FC<{t: number; fps: number}> = ({t, fps}) => {
  const done = k(t, 1.35, 0.55, quartInOut);
  return (
    <Screen>
      <Tab label="test batch" />
      {Array.from({length: 200}).map((_, i) => {
        const at = 0.15 + i * 0.006;
        const s = spring({frame: Math.max(0, Math.round((t - at) * fps)), fps, config: {damping: 18, mass: 0.5}, durationInFrames: 12});
        const cx = 28 + (i % 25) * 22.5, cy = 76 + Math.floor(i / 25) * 22;
        return <div key={i} style={{position: "absolute", left: cx, top: cy, width: 13, height: 13, borderRadius: 7,
          background: WRONG.has(i) ? C.coral : C.teal, opacity: t < at ? 0 : clamp(s * 1.4),
          transform: `scale(${0.7 + 0.3 * s})`}} />;
      })}
      <div style={{position: "absolute", left: 28, top: 270, fontFamily: MONO, fontWeight: 600, fontSize: 40, color: C.teal}}>
        {Math.round(197 * done)} / 200
      </div>
      <Rise k={k(t, 1.85, 0.4)} style={{left: 250, top: 288, height: 30, width: 360}}>
        <span style={{fontFamily: MONO, fontWeight: 500, fontSize: 18, color: C.ink}}>match last night{"’"}s sorting {"✓"}</span>
      </Rise>
    </Screen>
  );
};

/* exp-52  same script, one call changed */
export const DiffScreen: React.FC<{t: number; ev: Record<string, number>}> = ({t, ev}) => {
  const del = k(t, ev.only ?? 1.3, 0.4);
  const strike = k(t, (ev.only ?? 1.3) + 0.15, 0.45);
  const adds = [["    a = ask_system_one(question,", (ev.changes ?? 2.07)], ["            text, doors=FOLDERS)", (ev.changes ?? 2.07) + 0.22],
    ["    if a.confidence < 0.85:", (ev.me ?? 2.98)], ["        return \"AJ\"", (ev.me ?? 2.98) + 0.25],
    ["    return a.choice", (ev.me ?? 2.98) + 0.5]] as const;
  const line = (y: number, n: number, txt: string, extra?: React.ReactNode, color = C.ink) => (
    <div style={{position: "absolute", left: 32, top: y, display: "flex", alignItems: "baseline"}}>
      <span style={{width: 46, fontFamily: MONO, fontSize: 13, color: C.soft}}>{n}</span>
      <span style={{fontFamily: MONO, fontWeight: 500, fontSize: 18, color, whiteSpace: "pre", position: "relative"}}>{txt}{extra}</span>
    </div>
  );
  return (
    <Screen>
      <Tab label="sort.py" />
      {line(70, 1, "def sort_doc(file):")}
      {/* the new first line: pull the text out of each PDF */}
      <div style={{position: "absolute", left: 0, top: 103, width: SCR.w, height: 36, background: C.tealbg, ...wipeX(k(t, 0.55, 0.4))}} />
      <div style={{position: "absolute", left: 56, top: 106, fontFamily: MONO, fontWeight: 600, fontSize: 18, color: C.teal, opacity: k(t, 0.55, 0.4)}}>+</div>
      <div style={{position: "absolute", left: 0, top: 0, width: SCR.w, height: SCR.h, ...wipeX(k(t, 0.55, 0.4))}}>{line(106, 2, "    text = pdf_to_text(file)")}</div>
      <div style={{position: "absolute", left: 0, top: 137, width: SCR.w, height: 34, background: C.coralbg, ...wipeX(del)}} />
      <div style={{position: "absolute", left: 56, top: 140, fontFamily: MONO, fontWeight: 600, fontSize: 18, color: C.coral, opacity: del}}>-</div>
      {line(140, 3, "    return ask_ai(question, file)",
        <span style={{position: "absolute", left: 40, right: 0, top: "52%", height: 2, background: C.coral, transformOrigin: "left", transform: `scaleX(${strike})`}} />,
        del > 0.5 ? C.muted : C.ink)}
      {adds.map(([txt, at], i) => {
        const v = k(t, at as number, 0.4);
        const y = 174 + i * 33;
        return (
          <React.Fragment key={i}>
            <div style={{position: "absolute", left: 0, top: y - 3, width: SCR.w, height: 33, background: C.tealbg, ...wipeX(v)}} />
            <div style={{position: "absolute", left: 56, top: y, fontFamily: MONO, fontWeight: 600, fontSize: 18, color: C.teal, opacity: v}}>+</div>
            <div style={{position: "absolute", left: 0, top: 0, width: SCR.w, height: SCR.h, ...wipeX(v)}}>{line(y, i + 4, txt as string)}</div>
          </React.Fragment>
        );
      })}
    </Screen>
  );
};

/* exp-53  the nurse sorts: four piles and the small one for AJ */
const PILES = [["BANK", 21406], ["ID", 17893], ["ADDRESS", 18121], ["OTHER", 11952]] as const;
export const PilesScreen: React.FC<{t: number; ev: Record<string, number>}> = ({t, ev}) => {
  const fill = k(t, 0.05, 1.25, quartInOut);
  const aj = k(t, ev.comes ?? 1.45, 0.45);
  const total = Math.round(69372 * fill + 212 * k(t, ev.you ?? 1.9, 0.35));
  const base = 290, maxH = 190, colW = 104, gap = 18, x0 = 28;
  return (
    <Screen>
      <div style={{position: "absolute", left: 28, top: 24}}><Label>SORTED</Label></div>
      <div style={{position: "absolute", right: 28, top: 20, fontFamily: MONO, fontWeight: 600, fontSize: 18, color: C.teal}}>
        {fmt(total)} / 69,584 {total >= 69584 ? "✓" : ""}
      </div>
      {PILES.map(([lab, v], i) => {
        const x = x0 + i * (colW + gap);
        const h = Math.round(maxH * v / 21406);
        const n = Math.max(3, Math.round(h / 14));
        const shown = Math.round(n * fill);
        const cnt = Math.round(v * fill);
        return (
          <React.Fragment key={lab}>
            {Array.from({length: n}).map((_, j) => {
              const on = j < shown;
              const y = base - 14 - j * (h / n);
              return <div key={j} style={{position: "absolute", left: x + (j % 2 ? 3 : 0), top: y, width: colW - 3, height: 14,
                borderRadius: 4, background: C.white, border: `1.5px solid ${C.soft}`, boxSizing: "border-box",
                opacity: on ? 1 : 0, transform: on ? "none" : "translateY(-14px)"}} />;
            })}
            <div style={{position: "absolute", left: x, top: base - h - 6, width: colW, height: 4, borderRadius: 2, background: C.teal, opacity: fill > 0.98 ? 1 : 0}} />
            <div style={{position: "absolute", left: x, top: base + 12, width: colW, textAlign: "center"}}><Label color={C.ink} size={11}>{lab}</Label></div>
            <div style={{position: "absolute", left: x, top: base + 30, width: colW, textAlign: "center", fontFamily: MONO, fontWeight: 600, fontSize: 15, color: C.muted}}>{fmt(cnt)}</div>
          </React.Fragment>
        );
      })}
      {(() => {
        const x = x0 + 4 * (colW + gap);
        return (
          <div style={{position: "absolute", left: 0, top: 0, width: SCR.w, height: SCR.h, ...wipeY(aj)}}>
            {[0, 1].map((j) => <div key={j} style={{position: "absolute", left: x + (j ? 3 : 0), top: base - 14 - j * 12, width: 82, height: 12,
              borderRadius: 4, border: `1.5px dashed ${C.ink}`, background: C.white, boxSizing: "border-box"}} />)}
            <div style={{position: "absolute", left: x - 6, top: base + 12, width: 96, textAlign: "center"}}><Label color={C.ink} size={11}>FOR AJ</Label></div>
            <div style={{position: "absolute", left: x - 6, top: base + 30, width: 96, textAlign: "center", fontFamily: MONO, fontWeight: 600, fontSize: 15, color: C.ink}}>
              {Math.round(212 * k(t, ev.you ?? 1.9, 0.35))}
            </div>
          </div>
        );
      })()}
    </Screen>
  );
};

/* exp-55  last night vs this morning */
export const PayoffScreen: React.FC<{t: number}> = ({t}) => {
  const cards = [
    {when: "LAST NIGHT", who: "big model", col: C.coral, bg: C.coralbg, at: 0.1,
      stats: [["PDFs", (v: number) => fmt(10416 * v)], ["time", (v: number) => `${Math.max(1, Math.round(9 * v))} hours`], ["cost", (v: number) => `$${Math.round(250 * v)}`]]},
    {when: "THIS MORNING", who: "system one model", col: C.teal, bg: C.tealbg, at: 1.0,
      stats: [["PDFs", (v: number) => fmt(69584 * v)], ["time", (v: number) => `${Math.max(1, Math.round(9 * v))} minutes`], ["cost", (v: number) => `$${(11.69 * v).toFixed(2)}`]]},
  ] as const;
  return (
    <Screen>
      {cards.map((c, i) => {
        const x = 22 + i * 306;
        const open = k(t, c.at, 0.55);
        return (
          <div key={i} style={{position: "absolute", left: x, top: 22, width: 290, height: 327, borderRadius: 18, background: c.bg, ...wipeY(open)}}>
            <div style={{position: "absolute", left: 22, top: 20}}><Label color={c.col}>{c.when}</Label></div>
            <div style={{position: "absolute", left: 22, top: 42, fontFamily: MONO, fontWeight: 600, fontSize: 17, color: C.ink}}>{c.who}</div>
            {c.stats.map(([lab, f], j) => {
              const v = k(t, c.at + 0.25 + j * 0.18, i === 1 && j === 2 ? 1.0 : 0.7);
              const y = 96 + j * 72;
              return (
                <React.Fragment key={j}>
                  <div style={{position: "absolute", left: 22, top: y - 10, width: 246, height: 1, background: c.col, opacity: 0.25}} />
                  <div style={{position: "absolute", left: 22, top: y}}><Label size={11} style={lab === "PDFs" ? {textTransform: "none"} : undefined}>{lab}</Label></div>
                  <div style={{position: "absolute", left: 22, top: y + 18, fontFamily: MONO, fontWeight: 600,
                    fontSize: j === 2 ? 34 : 28, color: j === 2 ? c.col : C.ink}}>{(f as (v: number) => string)(v)}</div>
                </React.Fragment>
              );
            })}
          </div>
        );
      })}
    </Screen>
  );
};

/* ================================================================== FULL-FRAME EXPLAINERS */
const Title: React.FC<{t: number; text: string; y: number; inAt: number; outAt: number}> = ({t, text, y, inAt, outAt}) => {
  const vin = k(t, inAt, 0.45);
  const vout = k(t, outAt, 0.35, quartInOut);
  if (vout >= 1) return null;
  return (
    <div style={{position: "absolute", left: 0, top: y, width: 720, height: 30, overflow: "hidden"}}>
      <div style={{transform: `translateY(${(1 - vin) * 105 - vout * 105}%)`, textAlign: "center",
        fontFamily: LBL, fontWeight: 900, fontSize: 20, letterSpacing: 2.8, color: C.ink}}>{text}</div>
    </div>
  );
};

/** a stroke that draws itself on */
const Draw: React.FC<{d: string; v: number; w?: number; color?: string; len?: number; fill?: string}> =
({d, v, w = 5, color = C.ink, len = 1200, fill = "none"}) => (
  <path d={d} fill={fill} stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round"
    strokeDasharray={len} strokeDashoffset={len * (1 - v)} />
);

/** the patient / nurse bust from the Figma frames, 200 x 250 box, scaled by s */
const Bust: React.FC<{x: number; y: number; s: number; v?: number; children?: React.ReactNode; sw?: number}> =
({x, y, s, v = 1, children, sw = 5}) => (
  <svg style={{position: "absolute", left: x - 8, top: y - 8, overflow: "visible"}} width={200 * s + 16} height={250 * s + 16}
    viewBox={`${-8 / s} ${-8 / s} ${200 + 16 / s} ${250 + 16 / s}`}>
    <g>
      <path d="M 0 250 L 0 196 C 0 140 40 112 100 112 C 160 112 200 140 200 196 L 200 250 Z" fill="#fff" stroke="none" opacity={v > 0 ? 1 : 0} />
      <Draw d="M 0 250 L 0 196 C 0 140 40 112 100 112 C 160 112 200 140 200 196 L 200 250" v={v} w={sw / s} len={560} />
      <circle cx={100} cy={44} r={40} fill="#fff" opacity={v > 0 ? 1 : 0} />
      <Draw d="M 100 4 A 40 40 0 1 1 99.9 4" v={v} w={sw / s} len={260} />
      {children}
    </g>
  </svg>
);

export const DoctorExplainer: React.FC<{t: number; ev: Record<string, number>}> = ({t, ev}) => {
  const titleOut = (ev.doctor ?? 0.55) + 0.55;
  const fig = k(t, (ev.read ?? 1.5) - 0.35, 0.8, quartInOut);
  const pages = k(t, ev.read ?? 1.5, 0.55);
  const pageNo = Math.max(1, Math.min(6, 1 + Math.floor(5 * clamp((t - (ev.page ?? 2.2)) / Math.max(0.3, (ev.reason ?? 2.85) - (ev.page ?? 2.2) + 0.6)))));
  const readRow = Math.min(8, Math.floor(clamp((t - (ev.read ?? 1.5)) / 2.2) * 9));
  const bubble = k(t, ev.reason ?? 2.85, 0.4);
  const dots = pulse(t, ev.reason ?? 2.85, 2.0, 4.2);
  const card = k(t, (ev.pay ?? 4.36) - 0.3, 0.55);
  const r1 = k(t, ev.reading ?? 4.9, 0.7);
  const r2 = k(t, ev.reasoning ?? 5.8, 0.7);
  const price = 0.024 * k(t, ev.reading ?? 4.9, 1.6, quartInOut);
  const W = [150, 170, 120, 160, 140, 168, 96, 150, 130];
  return (
    <div style={{position: "absolute", inset: 0, background: C.white}}>
      <Title t={t} text="THE DOCTOR" y={150} inAt={0.02} outAt={titleOut} />
      {/* the doctor, the bubble and the chart move as ONE group, centred on the frame (v3) */}
      <div style={{position: "absolute", left: 0, top: 0, width: 720, height: 1280, transform: "translate(39px, 19px)"}}>
      {/* the doctor, drawn on. Everything on the coat is clipped to the coat, so nothing pokes out of it */}
      <svg style={{position: "absolute", left: 64, top: 360, overflow: "visible"}} width={200} height={250} viewBox="0 0 200 250">
        <defs><clipPath id="docBody"><path d="M 0 250 L 0 196 C 0 140 40 112 100 112 C 160 112 200 140 200 196 L 200 250 Z" /></clipPath></defs>
        <path d="M 0 250 L 0 196 C 0 140 40 112 100 112 C 160 112 200 140 200 196 L 200 250 Z" fill="#fff" opacity={fig > 0 ? 1 : 0} />
        <g clipPath="url(#docBody)">
          <Draw d="M 64 108 L 100 182 L 136 108" v={k(t, (ev.read ?? 1.5) - 0.05, 0.5)} w={4} len={170} />
          <Draw d="M 100 182 L 100 250" v={k(t, (ev.read ?? 1.5) + 0.05, 0.4)} w={4} len={70} />
          <Draw d="M 26 196 L 62 196 L 62 226 L 26 226 Z" v={k(t, (ev.read ?? 1.5) + 0.1, 0.4)} w={3.5} len={140} />
          <Draw d="M 36 184 L 36 210" v={k(t, (ev.read ?? 1.5) + 0.2, 0.3)} w={4} color={C.ink} len={30} />
          {/* the stethoscope: coral, round the collar, the tube hanging to the chestpiece */}
          <Draw d="M 70 108 C 70 160 82 176 100 176 C 118 176 130 160 130 108" v={k(t, (ev.read ?? 1.5) + 0.1, 0.55)} w={5.5} color={C.coral} len={220} />
          <Draw d="M 116 172 C 132 184 142 194 147 204" v={k(t, (ev.read ?? 1.5) + 0.4, 0.3)} w={5.5} color={C.coral} len={50} />
        </g>
        <g opacity={k(t, (ev.read ?? 1.5) + 0.55, 0.3)}>
          <circle cx={149} cy={214} r={13} fill="#fff" stroke={C.coral} strokeWidth={5} />
          <circle cx={149} cy={214} r={4.5} fill={C.coral} />
        </g>
        <path d="M 0 250 L 0 196 C 0 140 40 112 100 112 C 160 112 200 140 200 196 L 200 250" fill="none" stroke="none" />
        <Draw d="M 0 250 L 0 196 C 0 140 40 112 100 112 C 160 112 200 140 200 196 L 200 250" v={fig} len={560} />
        <circle cx={100} cy={44} r={40} fill="#fff" opacity={fig > 0 ? 1 : 0} />
        <Draw d="M 100 4 A 40 40 0 1 1 99.9 4" v={fig} len={260} />
      </svg>
      {/* reasoning bubble */}
      <div style={{position: "absolute", left: 214, top: 300, width: 92, height: 46, borderRadius: 23, background: C.white,
        border: `3px solid ${C.ink}`, boxSizing: "border-box", boxShadow: SHADOW, ...wipeX(bubble),
        display: "flex", alignItems: "center", justifyContent: "center", gap: 6}}>
        {[0, 1, 2].map((i) => <div key={i} style={{width: 12, height: 12, borderRadius: 6, background: C.ink,
          transform: `translateY(${-4 * Math.max(0, Math.sin((t - (ev.reason ?? 2.85)) * 6 - i * 0.9)) * (dots > 0 ? 1 : 0)}px)`}} />)}
      </div>
      <div style={{position: "absolute", left: 206, top: 346, width: 14, height: 14, borderRadius: 7, border: `3px solid ${C.ink}`, boxSizing: "border-box", background: C.white, opacity: bubble}} />
      <div style={{position: "absolute", left: 196, top: 364, width: 8, height: 8, borderRadius: 4, border: `2.5px solid ${C.ink}`, boxSizing: "border-box", background: C.white, opacity: bubble}} />
      {/* the thick chart: nine pages fan out from one */}
      <div style={{position: "absolute", left: 340, top: 300}}>
        {Array.from({length: 9}).map((_, j) => {
          const i = 8 - j;
          return <div key={j} style={{position: "absolute", left: i * 4 * pages, top: lerp(32, (8 - i) * 4, pages),
            width: 206, height: 272, borderRadius: 12, background: C.white, border: `1.5px solid ${C.soft}`, boxSizing: "border-box",
            boxShadow: i === 0 ? SHADOW : undefined, opacity: pages > 0 ? 1 : 0}} />;
        })}
        <div style={{position: "absolute", left: 0, top: 32, width: 206, height: 272, ...wipeY(pages)}}>
          <div style={{position: "absolute", left: 18, top: 20, fontFamily: MONO, fontWeight: 500, fontSize: 13, letterSpacing: 0.5, color: C.muted}}>STATEMENT</div>
          <div style={{position: "absolute", left: 128, top: 16, width: 64, height: 22, borderRadius: 11, background: C.ink,
            fontFamily: MONO, fontWeight: 600, fontSize: 12, color: C.white, display: "flex", alignItems: "center", justifyContent: "center"}}>{pageNo} / 9</div>
          {W.map((w, i) => (
            <div key={i} style={{position: "absolute", left: 18, top: 56 + i * 20, width: w, height: 8, borderRadius: 4,
              background: i === readRow && t > (ev.read ?? 1.5) ? C.coral : C.hair}} />
          ))}
        </div>
      </div>
      </div>
      {/* the bill */}
      <div style={{position: "absolute", left: 90, top: 749, width: 540, height: 212, borderRadius: 20, background: C.white,
        border: `1px solid ${C.hair}`, boxSizing: "border-box", boxShadow: SHADOW,
        transform: `translateY(${(1 - card) * 26}px)`, ...wipeY(card)}}>
        {[["READING", r1, 0.62], ["REASONING", r2, 0.94]].map(([lab, v, max], i) => (
          <React.Fragment key={i}>
            <div style={{position: "absolute", left: 32, top: 40 + i * 74}}><Label size={14}>{lab as string}</Label></div>
            <div style={{position: "absolute", left: 32, top: 68 + i * 74, width: 300, height: 14, borderRadius: 7, background: C.wash, overflow: "hidden"}}>
              <div style={{width: 300 * (max as number), height: 14, borderRadius: 7, background: C.coral,
                transform: `translateX(${-(1 - (v as number)) * 300 * (max as number)}px)`}} />
            </div>
          </React.Fragment>
        ))}
        <div style={{position: "absolute", left: 372, top: 58, fontFamily: MONO, fontWeight: 600, fontSize: 40, color: C.coral}}>${price.toFixed(3)}</div>
        <div style={{position: "absolute", left: 374, top: 118}}><Label size={13}>PER PDF</Label></div>
      </div>
    </div>
  );
};

/* the shared ER scene: doors, nurse, the queue, the bench */
const DOORX = (i: number) => 97 + i * 138;
/** distance walked after tau seconds over a walk of length D: 0.25s up to pace, cruise at 505 px/s, 0.35s to settle */
const walk = (tau: number, D: number) => {
  const V = 505, TA = 0.25, TD = 0.35;
  const tc = Math.max(0, (D - V * (TA + TD) / 2) / V), T = TA + tc + TD;
  if (tau <= 0) return 0;
  if (tau < TA) return V * tau * tau / (2 * TA);
  if (tau < TA + tc) return V * TA / 2 + V * (tau - TA);
  if (tau < T) return D - V * (T - tau) ** 2 / (2 * TD);
  return D;
};
const SLOTS = [[52, 826], [160, 838], [268, 846], [376, 850], [484, 854]];
const DOOR_SPOT = [111, 333];            // feet on the doorway floor (v5): the cat stands low, under the door's icon
const BENCH_SPOT = [505, 635];           // v5: the bench sits apart, right of the nurse, at eye level -- not by the queue

const NurseScene: React.FC<{t: number; ev: Record<string, number>; labels?: Record<string, number>; chipText: string; chip2?: {text: string; v: number}; calmAt?: number}> =
({t, ev, labels, chipText, chip2, calmAt = 1e9}) => {
  const titleOut = (ev.built ?? 2.69) - 0.35;
  const doorsIn = (i: number) => k(t, titleOut + 0.3 + i * 0.08, 0.6);
  const floor = k(t, titleOut + 0.2, 0.6, quartInOut);
  const nurse = k(t, ev.built ?? 2.69, 0.75, quartInOut);
  const outline = (i: number) => k(t, (ev.define ?? 4.2) + i * 0.1, 0.5, quartInOut);
  const arm = k(t, (ev.picks ?? 5.3) - 0.25, 0.35, quartInOut);
  const chipV = k(t, (ev.sure ?? 6.75) - 0.1, 0.45);
  const notV = k(t, (ev.not ?? 7.76) + 0.2, 0.45);
  // the bench and its WAITING sign belong to the room: they rise with the doors, before anyone needs them (v3)
  const benchV = k(t, titleOut + 0.45, 0.6, quartInOut);
  const waitLbl = k(t, titleOut + 0.7, 0.45);
  // the queue forms single file from the right edge, front first, smootherstep, tight stagger
  const enterAt = titleOut + 0.9;
  const pos = (j: number): [number, number] => {
    // patient j enters to SLOTS[j]; patient 0 goes to the door on "picks"; j>0 shift one slot left;
    // the last one sits down on "not sure"
    // one walking pace for everyone (accelerate, cruise, settle), 0.32s apart: the gap between
    // centres never drops under ~95px for 84px-wide figures, so nobody fuses mid-walk
    const D = 760 - SLOTS[j][0];
    const walked = walk(t - (enterAt + j * 0.32), D);
    const e = walked / D;
    let [x, y] = [760 - walked, lerp(SLOTS[j][1] + 8, SLOTS[j][1], e)];
    const pk = smoother(clamp((t - (ev.picks ?? 5.3)) / 0.85));
    if (j === 0) { x = lerp(x, DOOR_SPOT[0], pk); y = lerp(y, DOOR_SPOT[1], pk); }
    else if (j < 4) { const sh = smoother(clamp((t - (ev.picks ?? 5.3) - 0.15 - j * 0.07) / 0.7)); x = lerp(x, SLOTS[j - 1][0], sh); y = lerp(y, SLOTS[j - 1][1], sh); }
    if (j === 4) { const sit = smoother(clamp((t - (ev.not ?? 7.76)) / 0.6)); x = lerp(x, BENCH_SPOT[0], sit); y = lerp(y, BENCH_SPOT[1], sit); }
    return [x, y];
  };
  // ---- the patients are cats (v4, Sejal): banana cat walks in and freezes while it waits;
  // the one the nurse picks is the happy-happy cat, dancing all the way through its door;
  // the one she is not sure about turns into crying banana cat on the bench.
  const picks = ev.picks ?? 5.3, notSure = ev.not ?? 7.76;
  const startJ = (j: number) => enterAt + j * 0.32;
  const walkDur = (D: number) => { const V = 505, TA = 0.25, TD = 0.35; return TA + Math.max(0, (D - V * (TA + TD) / 2) / V) + TD; };
  const arriveJ = (j: number) => startJ(j) + walkDur(760 - SLOTS[j][0]);
  const catFrame = (j: number): {kind: "walk" | "cry" | "happy"; idx: number} => {
    if (j === 0) {
      // v5 (Sejal): the first cat is a banana cat like the rest -- walking in, waiting, walking to the
      // door -- and only becomes the happy-happy cat once it is IN the doorway
      const atDoor = picks + 0.85;
      if (t >= atDoor) return {kind: "happy", idx: Math.floor((t - atDoor) * CATS.happy.fps) % CATS.happy.frames};
      const moving = (Math.min(t, arriveJ(0)) - startJ(0)) + clamp((t - picks) / 0.85) * 0.85;
      return {kind: "walk", idx: Math.floor(Math.max(0, moving) * CATS.walk.fps) % CATS.walk.frames};
    }
    // the unsure cat cries on the bench -- until the AI starts naming the doors (v6), then it just stands and waits
    if (j === 4 && t >= notSure && t < calmAt) return {kind: "cry", idx: Math.floor((t - notSure) * CATS.cry.fps) % CATS.cry.frames};
    if (j === 4 && t >= calmAt) return {kind: "walk", idx: Math.floor((arriveJ(4) - startJ(4)) * CATS.walk.fps) % CATS.walk.frames};
    // banana walk: the clock only runs while the cat is actually moving
    const shift0 = picks + 0.15 + j * 0.07;
    const moving = (Math.min(t, arriveJ(j)) - startJ(j)) + (j < 4 ? clamp((t - shift0) / 0.7) * 0.7 : 0);
    return {kind: "walk", idx: Math.floor(Math.max(0, moving) * CATS.walk.fps) % CATS.walk.frames};
  };
  const K = 0.282;   // source px -> 720 space, the same for all three clips so the cats share a scale
  return (
    <div style={{position: "absolute", inset: 0, background: C.white}}>
      <Title t={t} text="THE TRIAGE NURSE" y={112} inAt={0.02} outAt={titleOut} />
      {/* door labels, landing one by one */}
      {labels ? ["BANK\nSTATEMENT", "ID\nPROOF", "ADDRESS\nPROOF", "OTHER"].map((s, i) => {
        const v = k(t, labels["d" + i] ?? 99, 0.45);
        const two = s.includes("\n");
        return (
          <div key={i} style={{position: "absolute", left: DOORX(i) + 56 - 65, top: 220 - (two ? 36 : 18), width: 130, height: two ? 36 : 18, overflow: "hidden"}}>
            <div style={{transform: `translateY(${(1 - v) * 105}%)`, textAlign: "center", whiteSpace: "pre", fontFamily: LBL, fontWeight: 900,
              fontSize: 15, lineHeight: "18px", letterSpacing: 1.5, color: C.ink}}>{s}</div>
          </div>
        );
      }) : null}
      {/* doors rise from behind the floor */}
      <div style={{position: "absolute", left: 97, top: 228, width: 540, height: 214, overflow: "hidden"}}>
        {[0, 1, 2, 3].map((i) => (
          <div key={i} style={{position: "absolute", left: i * 138, top: 0, width: 112, height: 214, borderRadius: "14px 14px 0 0",
            background: C.door, transform: `translateY(${(1 - doorsIn(i)) * 216}px)`,
            boxShadow: `inset 0 0 0 ${2 * outline(i)}px rgba(3,166,207,${0.9 * outline(i)})`}}>
            <div style={{position: "absolute", left: 12, top: 14, width: 88, height: 200, borderRadius: "8px 8px 0 0", border: "1.5px solid rgba(255,255,255,.14)", borderBottom: "none", boxSizing: "border-box"}} />
            <div style={{position: "absolute", left: 86, top: 112, width: 10, height: 10, borderRadius: 5, background: "rgba(255,255,255,.65)"}} />
            {labels ? <DoorGlyph i={i} v={k(t, labels["d" + i] ?? 99, 0.5, quartInOut)} /> : null}
          </div>
        ))}
      </div>
      <div style={{position: "absolute", left: 48, top: 442, width: 624 * floor, height: 2, background: C.hair}} />
      {/* the patients (drawn before the nurse so the door patient sits in front of its door) */}
      {[0, 1, 2, 3, 4].map((j) => {
        if (t < startJ(j)) return null;
        const [x, y] = pos(j);
        const {kind, idx} = catFrame(j);
        const m = CATS[kind];
        const doorK = j === 0 ? lerp(1, 0.85, smoother(clamp((t - picks) / 0.85))) : 1;
        const sc = (j === 4 && t >= notSure ? 1.15 : 1) * doorK;   // the bench cat reads a size up, crying or not
        const w = (m.box[2] - m.box[0]) * K * sc, h = (m.box[3] - m.box[1]) * K * sc;
        const cx = x + 42, base = y + 105;          // same footprint the bust had: centre and feet line
        // a frozen happy cat stands on its own feet; moving, the clip's lowest point is the floor and it hops above it
        // the happy cat always stands on its own feet (no hops), so in the doorway it never climbs over the icon
        const feet = kind === "happy" ? CATS.happy.feetPerFrame[idx] : m.feet;
        return <Img key={j} src={staticFile(`s1m/cats/${kind}/${String(idx).padStart(3, "0")}.png`)}
          style={{position: "absolute", left: cx - w / 2, top: base - feet * h, width: w, height: h}} />;
      })}
      {/* bench */}
      <svg style={{position: "absolute", left: 474, top: 726, overflow: "visible"}} width={150} height={70}>
        <Draw d="M 10 14 L 136 14" v={benchV} w={8} len={136} />
        <Draw d="M 28 18 L 28 52" v={benchV} w={8} len={40} />
        <Draw d="M 118 18 L 118 52" v={benchV} w={8} len={40} />
      </svg>
      <div style={{position: "absolute", left: 474, top: 782, width: 146, textAlign: "center", ...wipeY(waitLbl)}}><Label size={13}>WAITING</Label></div>
      {/* nurse, pointing */}
      <svg style={{position: "absolute", left: 160, top: 540, overflow: "visible"}} width={140} height={160}>
        <Draw d="M 116 154 C 96 122 66 78 26 26" v={arm} w={6} len={170} />
        <circle cx={26} cy={24} r={11} fill="#fff" stroke={C.ink} strokeWidth={5} opacity={arm > 0.85 ? 1 : 0} />
      </svg>
      <Bust x={262} y={500} s={0.98} v={nurse}>
        <Draw d="M 58 112 L 98 164 L 138 112" v={k(t, (ev.built ?? 2.69) + 0.3, 0.4)} w={4 / 0.98} len={140} />
        <rect x={58} y={170} width={84} height={30} rx={7} fill={C.teal} opacity={k(t, (ev.built ?? 2.69) + 0.45, 0.3)} />
        <text x={100} y={190} textAnchor="middle" fontFamily={LBL} fontWeight={900} fontSize={13} letterSpacing={1.8} fill="#fff"
          opacity={k(t, (ev.built ?? 2.69) + 0.5, 0.3)}>TRIAGE</text>
        {/* the nurse's cap (v3) */}
        <g opacity={k(t, (ev.built ?? 2.69) + 0.35, 0.35)}>
          <path d="M 62 22 C 66 2 80 -10 100 -10 C 120 -10 134 2 138 22 C 124 16 112 14 100 14 C 88 14 76 16 62 22 Z"
            fill="#fff" stroke={C.ink} strokeWidth={4 / 0.98} strokeLinejoin="round" />
          <path d="M 100 -3 L 100 9 M 94 3 L 106 3" stroke={C.teal} strokeWidth={3.6 / 0.98} strokeLinecap="round" />
        </g>
      </Bust>
      {/* sure: the chip under door one */}
      <Chip x={153} y={456} text={chipText} v={chipV} />
      {chip2 ? <Chip x={153} y={456} text={chip2.text} v={chip2.v} /> : null}
      {/* not sure: says so */}
      <div style={{position: "absolute", left: 547, top: 549, transform: "translateX(-50%)"}}>
        <div style={{padding: "0 16px", height: 34, borderRadius: 17, background: C.white, border: `1px solid ${C.soft}`, boxSizing: "border-box",
          display: "flex", alignItems: "center", fontFamily: MONO, fontWeight: 600, fontSize: 18, color: C.muted, boxShadow: SHADOW, whiteSpace: "nowrap", ...wipeX(notV)}}>? 51%</div>
      </div>
    </div>
  );
};

const Chip: React.FC<{x: number; y: number; text: string; v: number}> = ({x, y, text, v}) => (
  <div style={{position: "absolute", left: Math.max(48, x - (text.length * 11 + 32) / 2), top: y}}>
    <div style={{padding: "0 16px", height: 34, borderRadius: 17, background: C.teal, display: "flex", alignItems: "center",
      fontFamily: MONO, fontWeight: 600, fontSize: 18, color: C.white, whiteSpace: "nowrap", boxShadow: SHADOW, ...wipeX(v)}}>{text}</div>
  </div>
);

const DoorGlyph: React.FC<{i: number; v: number}> = ({i, v}) => {
  // bank statement · ID proof · address proof · other (v7)
  const W = "rgba(255,255,255,.9)";
  return (
    <svg style={{position: "absolute", left: 0, top: -12}} width={112} height={214}>
      {i === 0 ? <>
        <Draw d="M 30 64 L 56 46 L 82 64 Z" v={v} w={4.5} color={W} len={110} />
        {[38, 53, 68].map((x) => <rect key={x} x={x} y={68} width={6} height={20} rx={1.5} fill={W} opacity={v} />)}
        <Draw d="M 30 94 L 82 94" v={v} w={4.5} color={W} len={60} />
      </> : i === 1 ? <>
        <Draw d="M 32 52 L 80 52 L 80 92 L 32 92 Z" v={v} w={4.5} color={W} len={190} />
        <circle cx={46} cy={67} r={6.5} fill={W} opacity={v} />
        <Draw d="M 36 85 C 38 77 54 77 56 85" v={v} w={3.5} color={W} len={30} />
        <Draw d="M 62 64 L 74 64 M 62 74 L 72 74" v={v} w={3.5} color={W} len={30} />
      </> : i === 2 ? <>
        <Draw d="M 28 70 L 56 46 L 84 70" v={v} w={4.5} color={W} len={80} />
        <Draw d="M 35 65 L 35 96 L 77 96 L 77 65" v={v} w={4.5} color={W} len={110} />
        <Draw d="M 50 96 L 50 80 L 62 80 L 62 96" v={v} w={4} color={W} len={45} />
      </> : <>
        {[40, 56, 72].map((x) => <circle key={x} cx={x} cy={72} r={5} fill={W} opacity={v} />)}
      </>}
    </svg>
  );
};

export const NurseExplainer: React.FC<{t: number; ev: Record<string, number>}> = ({t, ev}) =>
  <NurseScene t={t} ev={ev} chipText="97%" />;

/** exp-39: the same room, frozen at its end state, and the doors get names */
export const DoorsExplainer: React.FC<{t: number; ev: Record<string, number>; nurseEv: Record<string, number>; nurseEnd: number}> =
({t, ev, nurseEv, nurseEnd}) => {
  // v7: no voice here any more -- the four folders are named on screen, one by one
  const d0 = ev.d0 ?? 0.35;
  return <NurseScene t={nurseEnd + t} ev={nurseEv} chipText="97%" calmAt={nurseEnd} chip2={{text: "BANK STATEMENT · 97%", v: k(t, d0 - 0.05, 0.5)}}
    labels={Object.fromEntries([0, 1, 2, 3].map((i) => ["d" + i, (ev["d" + i] ?? 99) + nurseEnd]))} />;
};

/* exp-43 a/b/c: the playground card grows in place across three takes */
type SetupEv = {a: Record<string, number>; b: Record<string, number>; c: Record<string, number>; aDur: number; bDur: number};
const ROWS: [string, string, string[]][] = [
  ["BANK STATEMENT", "account transactions from a bank", ["jan.pdf", "feb.pdf", "mar.pdf"]],
  ["ID PROOF", "passport, driving licence, national ID", ["passport.pdf", "licence.pdf", "id_card.pdf"]],
  ["ADDRESS PROOF", "utility bill, rent agreement", ["electricity.pdf", "rent.pdf", "water.pdf"]],
  ["OTHER", "anything else", ["invoice.pdf", "resume.pdf", "memo.pdf"]]];

/** a tiny PDF page: folded corner, red-free (ink), so it reads as a file not an app icon */
const PdfIcon: React.FC<{size?: number; color?: string}> = ({size = 12, color = C.muted}) => (
  <svg width={size * 0.8} height={size} viewBox="0 0 10 12.5" style={{flexShrink: 0}}>
    <path d="M 1 0.75 L 6.5 0.75 L 9.25 3.5 L 9.25 11.75 L 1 11.75 Z" fill="#fff" stroke={color} strokeWidth={1.1} strokeLinejoin="round" />
    <path d="M 6.5 0.75 L 6.5 3.5 L 9.25 3.5" fill="none" stroke={color} strokeWidth={1.1} strokeLinejoin="round" />
    <path d="M 2.8 6.5 L 7.4 6.5 M 2.8 8.6 L 6.4 8.6" stroke={color} strokeWidth={1} strokeLinecap="round" />
  </svg>
);

const TileGlyph: React.FC<{i: number}> = ({i}) => {
  // bank · ID card · house · other -- the same four as the doors (v7)
  const W = "rgba(255,255,255,.92)";
  return (
    <svg width={34} height={44} style={{position: "absolute", left: 0, top: 0}}>
      {i === 0 ? <><path d="M 6 16 L 15 10 L 24 16 Z" fill="none" stroke={W} strokeWidth={2} strokeLinejoin="round" />
          {[8.5, 13.5, 18.5].map((x) => <rect key={x} x={x} y={17.5} width={3} height={8} rx={0.8} fill={W} />)}
          <path d="M 6 28 L 24 28" stroke={W} strokeWidth={2} strokeLinecap="round" /></>
        : i === 1 ? <><rect x={5} y={12} width={20} height={15} rx={2} fill="none" stroke={W} strokeWidth={2} />
          <circle cx={10.5} cy={18} r={2.4} fill={W} /><path d="M 7.5 24 C 8.5 21.5 12.5 21.5 13.5 24" stroke={W} strokeWidth={1.5} fill="none" />
          <path d="M 16 17 L 22 17 M 16 21 L 20.5 21" stroke={W} strokeWidth={1.6} strokeLinecap="round" /></>
        : i === 2 ? <><path d="M 5 20 L 15 11 L 25 20" fill="none" stroke={W} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
          <path d="M 8 18 L 8 29 L 22 29 L 22 18" fill="none" stroke={W} strokeWidth={2} strokeLinejoin="round" />
          <path d="M 13 29 L 13 23.5 L 17 23.5 L 17 29" fill="none" stroke={W} strokeWidth={1.6} /></>
        : <>{[9, 15, 21].map((x) => <circle key={x} cx={x} cy={20} r={1.9} fill={W} />)}</>}
      <circle cx={28} cy={26} r={2} fill="rgba(255,255,255,.7)" />
    </svg>
  );
};

export const SetupExplainer: React.FC<{t: number; phase: "a" | "b" | "c"; ev: SetupEv}> = ({t, phase, ev}) => {
  // one clock across the three takes, so nothing restarts at the cuts
  const T = phase === "a" ? t : phase === "b" ? ev.aDur + t : ev.aDur + ev.bDur + t;
  const A = ev.a, B = Object.fromEntries(Object.entries(ev.b).map(([kk, v]) => [kk, v + ev.aDur])),
    Cc = Object.fromEntries(Object.entries(ev.c).map(([kk, v]) => [kk, v + ev.aDur + ev.bDur]));
  const cOn = ev.aDur + ev.bDur;
  const card = k(T, 0.1, 0.55);
  const step = T >= (Cc.step4 ?? 1e9) ? 4 : T >= (B.step3 ?? 1e9) ? 3 : T >= (A.step2 ?? 1e9) ? 2 : T >= (A.step1 ?? 1e9) ? 1 : 0;
  const qLbl = k(T, (A.step1 ?? 2.3) - 0.1, 0.4);
  const qBox = k(T, (A.step1 ?? 2.3) + 0.1, 0.5);
  const Q = "What kind of document is this?";
  const qTyped = Math.floor(Q.length * clamp((T - ((A.question ?? 3.2) - 0.35)) / 0.9));
  const dLbl = k(T, (A.step2 ?? 4.2), 0.4);
  const rowIn = (i: number) => k(T, (A.doors ?? 5.2) - 0.1 + i * 0.12, 0.45);
  const whatIn = (i: number) => k(T, (A.what ?? 6.7) + i * 0.12, 0.45);
  // b: the NOT FOR line opens space, then writes itself
  const nfGrow = k(T, (B.isnt ?? 1e9) - 0.45, 0.5, quartInOut);
  const nfText = k(T, (B.isnt ?? 1e9) - 0.05, 0.45);
  const tkGrow = k(T, (B.dark ?? 1e9) - 0.35, 0.55, quartInOut);
  const tkOut = k(T, cOn, 0.35, quartInOut);
  const tkTyped = clamp((T - (B.dark ?? 1e9)) / 0.8);
  const before = k(T, (B.dark ?? 1e9) + 0.25, 0.45);   // the 50 / 50 shows first, right after the item lands
  const after = k(T, (B.request ?? 1e9) - 0.2, 0.7);
  const fifty = pulse(T, (B.fifty ?? 1e9) - 0.1, 0.9, 4.0);
  // c: one example per door, then where they came from
  const chipGrow = (i: number) => k(T, (Cc.show ?? 1e9) + 0.15 + i * 0.35, 0.45, quartInOut);
  const chipIn = (i: number) => k(T, (Cc.show ?? 1e9) + 0.3 + i * 0.35, 0.4);
  const foot = k(T, (Cc.last ?? 1e9) - 0.05, 0.5);
  const sorted = Math.round(10416 * k(T, (Cc.last ?? 1e9) + 0.25, 1.8, quartInOut));

  // layout (card space), measured from the Figma auto-layout
  const ROW_H = 72, GAP = 12, NF = 22, EX = 34;
  const extra = (i: number) => (i === 2 ? NF * nfGrow : 0) + EX * chipGrow(i);
  const rowY: number[] = []; let y = 205;
  for (let i = 0; i < 4; i++) { rowY.push(y); y += ROW_H + extra(i) + GAP; }
  const rowsEnd = y - GAP;
  const ticketTop = rowsEnd + 26;
  const cardH = 563 + NF * nfGrow + (791 - 585) * tkGrow;
  const W = 560;
  return (
    <div style={{position: "absolute", inset: 0, background: C.white}}>
      <div style={{position: "absolute", left: 80, top: 640 - cardH / 2, width: W, height: 900, filter: "drop-shadow(0 14px 22px rgba(18,18,26,.09)) drop-shadow(0 1px 1px rgba(18,18,26,.05))",
        ...wipeY(card)}}>
        <svg style={{position: "absolute", left: 0, top: 0}} width={W} height={900}>
          <rect x={0.5} y={0.5} width={W - 1} height={Math.max(30, cardH - 1)} rx={26} fill="#fff" stroke={C.hair} />
        </svg>
        {/* header */}
        <div style={{position: "absolute", left: 30, top: 30, display: "flex", alignItems: "center", gap: 10}}>
          <div style={{width: 10, height: 10, borderRadius: 5, background: C.teal}} />
          <Label size={13}>SYSTEM ONE PLAYGROUND</Label>
        </div>
        <div style={{position: "absolute", right: 30, top: 34, display: "flex", gap: 6}}>
          {[1, 2, 3, 4, 5].map((i) => <div key={i} style={{width: 8, height: 8, borderRadius: 4,
            background: i < step ? C.ink : i === step ? C.teal : C.hair}} />)}
        </div>
        {/* question */}
        <Rise k={qLbl} style={{left: 30, top: 72, height: 16, width: 200}}><Label>QUESTION</Label></Rise>
        <div style={{position: "absolute", left: 30, top: 97, width: W - 60, height: 55, borderRadius: 14, background: C.wash,
          border: `1px solid ${C.hair}`, boxSizing: "border-box", ...wipeX(qBox)}}>
          <div style={{position: "absolute", left: 18, top: 15, fontFamily: MONO, fontWeight: 500, fontSize: 18, color: C.ink, whiteSpace: "pre"}}>
            {Q.slice(0, Math.max(0, qTyped))}{qTyped > 0 && qTyped < Q.length ? "▍" : ""}
          </div>
        </div>
        {/* doors */}
        <Rise k={dLbl} style={{left: 30, top: 178, height: 16, width: 200}}><Label>DOORS</Label></Rise>
        {ROWS.map(([name, what, eg], i) => {
          const h = ROW_H + extra(i);
          const nf = i === 2 ? nfGrow : 0;
          return (
            <div key={i} style={{position: "absolute", left: 30, top: 0, width: W - 60, height: 200,
              transform: `translateY(${rowY[i]}px)`, ...wipeX(rowIn(i))}}>
              <svg style={{position: "absolute", left: 0, top: 0}} width={W - 60} height={200}>
                <rect x={0.5} y={0.5} width={W - 61} height={h - 1} rx={14} fill="#fff"
                  stroke={i === 2 && nf > 0 ? C.coral : C.hair} strokeWidth={i === 2 && nf > 0 ? 1.5 : 1} />
              </svg>
              <div style={{position: "absolute", left: 14, top: 14, width: 34, height: 44, borderRadius: "8px 8px 2px 2px", background: C.door}}><TileGlyph i={i} /></div>
              <div style={{position: "absolute", left: 64, top: 14, fontFamily: LBL, fontWeight: 900, fontSize: 15, letterSpacing: 1.2, color: C.ink}}>{name}</div>
              <div style={{position: "absolute", left: 64, top: 36, fontFamily: BODY, fontSize: 16, color: C.muted, ...wipeX(whatIn(i))}}>{what}</div>
              {i === 2 ? (
                <div style={{position: "absolute", left: 64, top: 58, display: "flex", alignItems: "center", gap: 8, ...wipeX(nfText)}}>
                  <Label color={C.coral} size={11}>NOT FOR</Label>
                  <span style={{fontFamily: LBL, fontWeight: 700, fontSize: 15, color: C.coral}}>bank statements, even if they show an address</span>
                </div>
              ) : null}
              <div style={{position: "absolute", left: 64, top: 58 + (i === 2 ? NF : 0) + 4, display: "flex", alignItems: "center", gap: 8,
                padding: "5px 10px", borderRadius: 8, background: C.wash, border: `1px solid ${C.hair}`, ...wipeX(chipIn(i))}}>
                {/* three PDFs per folder, as files */}
                {eg.map((f) => (
                  <span key={f} style={{display: "inline-flex", alignItems: "center", gap: 4}}>
                    <PdfIcon size={13} />
                    <span style={{fontFamily: MONO, fontWeight: 500, fontSize: 11.5, color: C.ink, whiteSpace: "nowrap"}}>{f}</span>
                  </span>
                ))}
              </div>
            </div>
          );
        })}
        {/* b: the dark-mode ticket, before and after the NOT FOR line */}
        {tkGrow > 0 && tkOut < 1 ? (
          <div style={{position: "absolute", left: 30, top: ticketTop, width: W - 60, height: 180, borderRadius: 16, background: C.wash,
            border: `1px solid ${C.hair}`, boxSizing: "border-box", ...wipeY(tkGrow * (1 - tkOut))}}>
            {/* v6: the same example told with icons. The ticket points at both doors at 50 / 50; the NOT FOR line
                crosses one out, and the other turns solid at 94%. */}
            <svg style={{position: "absolute", left: 0, top: 0, overflow: "visible"}} width={W - 60} height={180}>
              {/* the two routes, dashed while it cannot decide */}
              {[["M 212 82 C 286 82 300 46 366 46", 0], ["M 212 98 C 286 98 300 132 366 132", 1]].map(([d, i]) => {
                const loser = i === 0, wv = after;
                const col = loser ? C.coral : C.teal;
                return (
                  <g key={i as number}>
                    <path d={d as string} fill="none" stroke={C.muted} strokeWidth={2.5} strokeDasharray="6 5" strokeLinecap="round"
                      opacity={before * (1 - wv * (loser ? 0.75 : 1))} />
                    {!loser ? <path d={d as string} fill="none" stroke={col} strokeWidth={4} strokeLinecap="round"
                      strokeDasharray={190} strokeDashoffset={190 * (1 - wv)} /> : null}
                  </g>
                );
              })}
              {/* NOT FOR: the losing route is crossed out, and the cross nods on "fifty-fifty" */}
              <g transform={`translate(296 ${60 - 3 * fifty})`} opacity={after}>
                <circle r={13} fill="#fff" stroke={C.coral} strokeWidth={2.5} />
                <path d="M -5 -5 L 5 5 M 5 -5 L -5 5" stroke={C.coral} strokeWidth={3} strokeLinecap="round"
                  strokeDasharray={15} strokeDashoffset={15 * (1 - clamp((after - 0.2) / 0.6))} />
              </g>
            </svg>
            {/* the ticket */}
            <div style={{position: "absolute", left: 18, top: 50, width: 190, height: 80, borderRadius: 12, background: C.white,
              border: `1px solid ${C.hair}`, boxSizing: "border-box", boxShadow: "0 6px 16px -6px rgba(18,18,26,.12)"}}>
              <div style={{position: "absolute", left: 14, top: 22}}><PdfIcon size={34} color={C.ink} /></div>
              <div style={{position: "absolute", left: 50, top: 18, fontFamily: MONO, fontWeight: 500, fontSize: 14, lineHeight: "21px", color: C.ink, whiteSpace: "pre"}}>
                {"Statement with\nan address".slice(0, Math.round(25 * tkTyped))}
              </div>
            </div>
            {/* the 50 / 50 chips, then the winner's 94% */}
            {[["50%", 236, 40, 0], ["50%", 236, 112, 1]].map(([txt, x, y, i]) => (
              <div key={i as number} style={{position: "absolute", left: x as number, top: y as number, padding: "3px 9px", borderRadius: 11,
                background: C.white, border: `1px solid ${C.soft}`, fontFamily: MONO, fontWeight: 600, fontSize: 12, color: C.muted,
                opacity: before * (1 - after), transform: `translateY(${-2 * fifty * (i ? -1 : 1)}px)`}}>{txt as string}</div>
            ))}
            <div style={{position: "absolute", left: 236, top: 112, padding: "3px 9px", borderRadius: 11, background: C.teal,
              fontFamily: MONO, fontWeight: 600, fontSize: 12, color: C.white, ...wipeX(after)}}>94%</div>
            {/* the two doors, with their own icons */}
            {[[0, "ADDRESS", 14], [1, "BANK", 100]].map(([i, lab, y]) => {
              const win = i === 1;
              return (
                <React.Fragment key={i as number}>
                  <div style={{position: "absolute", left: 372, top: y as number, width: 46, height: 64, borderRadius: "8px 8px 2px 2px", background: C.door,
                    opacity: before > 0 ? (win ? 1 : 1 - 0.55 * after) : 0,
                    boxShadow: win ? `0 0 0 ${3 * after}px rgba(3,166,207,${after})` : undefined}}>
                    <svg width={46} height={64} viewBox="0 0 34 44" style={{position: "absolute", left: 0, top: 0}}><TileGlyph i={win ? 0 : 2} /></svg>
                  </div>
                  <div style={{position: "absolute", left: 428, top: (y as number) + 24, opacity: before > 0 ? (win ? 1 : 1 - 0.55 * after) : 0}}>
                    <Label size={10} color={win && after > 0.5 ? C.teal : C.muted}>{lab as string}</Label>
                  </div>
                  {win ? (
                    <div style={{position: "absolute", left: 404, top: (y as number) - 8, width: 22, height: 22, borderRadius: 11, background: C.teal,
                      display: "flex", alignItems: "center", justifyContent: "center", ...wipeY(clamp((after - 0.3) / 0.7))}}>
                      <svg width={12} height={10} viewBox="0 0 12 10"><path d="M 1 5 L 4.5 8.5 L 11 1.5" fill="none" stroke="#fff" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" /></svg>
                    </div>
                  ) : null}
                </React.Fragment>
              );
            })}
          </div>
        ) : null}
        {/* c: where the examples came from */}
        <div style={{position: "absolute", left: 30, top: 713, width: W - 60, height: 44, borderRadius: 12, background: C.white,
          border: `1px solid ${C.hair}`, boxSizing: "border-box", display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "0 16px", ...wipeX(foot)}}>
          <Label size={11}>EXAMPLES FROM LAST NIGHT</Label>
          <span style={{fontFamily: MONO, fontWeight: 600, fontSize: 15, color: C.coral}}>{fmt(sorted)} sorted</span>
        </div>
      </div>
    </div>
  );
};

/* exp-50: step five, test first */
export const StepFiveExplainer: React.FC<{t: number; ev: Record<string, number>}> = ({t, ev}) => {
  const card = k(t, 0.05, 0.55);
  const all = k(t, 0.35, 0.5);
  const test = k(t, (ev.test ?? 1.25) - 0.05, 0.5);
  const glow = pulse(t, ev.small ?? 1.66, 1.2, 3.4);
  const back = k(t, (ev.ten ?? 3.16) - 0.25, 0.45);
  const strike = k(t, (ev.ten ?? 3.16) + 0.35, 0.5, quartInOut);
  const W = 560;
  const row = (top: number, children: React.ReactNode, style: React.CSSProperties) => (
    <div style={{position: "absolute", left: 30, top, width: W - 60, boxSizing: "border-box", ...style}}>{children}</div>
  );
  return (
    <div style={{position: "absolute", inset: 0, background: C.white}}>
      <div style={{position: "absolute", left: 80, top: 640 - 452 / 2, width: W, height: 452, borderRadius: 26, background: C.white,
        border: `1px solid ${C.hair}`, boxSizing: "border-box", boxShadow: SHADOW, ...wipeY(card)}}>
        <div style={{position: "absolute", left: 30, top: 30, display: "flex", alignItems: "center", gap: 10}}>
          <div style={{width: 10, height: 10, borderRadius: 5, background: C.teal}} />
          <Label size={13}>SYSTEM ONE PLAYGROUND</Label>
        </div>
        <div style={{position: "absolute", right: 30, top: 34, display: "flex", gap: 6}}>
          {[1, 2, 3, 4, 5].map((i) => <div key={i} style={{width: 8, height: 8, borderRadius: 4, background: i < 5 ? C.ink : C.teal}} />)}
        </div>
        <div style={{position: "absolute", left: 30, top: 70}}><Label>RUN</Label></div>
        {row(102, (
          <>
            <div>
              <Label color={C.white}>TEST A SMALL BATCH</Label>
              <div style={{fontFamily: MONO, fontWeight: 600, fontSize: 30, color: C.white, marginTop: 4}}>200 PDFs</div>
            </div>
            <svg width={24} height={26} style={{position: "absolute", right: 24, top: 34}}><path d="M 2 2 L 22 13 L 2 24 Z" fill="#fff" stroke="#fff" strokeWidth={3} strokeLinejoin="round" /></svg>
          </>
        ), {height: 96, borderRadius: 18, background: C.teal, padding: "22px", ...wipeX(test),
          boxShadow: `0 0 0 ${6 * glow}px rgba(3,166,207,${0.22 * glow}), 0 12px 30px -8px rgba(3,166,207,.45)`})}
        {row(222, (
          <>
            <div>
              <Label>RUN EVERYTHING</Label>
              <div style={{fontFamily: MONO, fontWeight: 600, fontSize: 30, color: C.soft, marginTop: 4}}>69,584 PDFs</div>
            </div>
            <svg width={26} height={30} style={{position: "absolute", right: 24, top: 34}}>
              <path d="M 5 12 L 5 8 C 5 3 9 0 13 0 C 17 0 21 3 21 8 L 21 12" fill="none" stroke={C.soft} strokeWidth={3} strokeLinecap="round" />
              <rect x={0} y={12} width={26} height={18} rx={4} fill={C.soft} />
            </svg>
          </>
        ), {height: 96, borderRadius: 18, background: C.wash, border: `1px solid ${C.hair}`, padding: "22px", ...wipeX(all)})}
        {row(342, (
          <>
            <Label>LAST NIGHT{"’"}S TEST</Label>
            <span style={{position: "relative", fontFamily: MONO, fontWeight: 600, fontSize: 18, color: C.coral}}>
              10 / 10 {"✓"}
              <span style={{position: "absolute", left: -2, right: -2, top: "52%", height: 2, background: C.coral, transformOrigin: "left", transform: `scaleX(${strike})`}} />
            </span>
          </>
        ), {height: 54, borderRadius: 14, border: `1px solid ${C.hair}`, padding: "0 18px", display: "flex", alignItems: "center",
          justifyContent: "space-between", ...wipeX(back)})}
      </div>
    </div>
  );
};

/* ================================================================== f33: the AI's body changes shape with its words (v3)
   Locked to the mark's position and size. Each shape lands on the word it illustrates:
     read every line   -> a magnifier hovering over lines of code
     reasoned it       -> a chain of thoughts lighting one by one
     paid ... reading  -> a coin
     and the thinking  -> a second coin
     built to choose   -> three doors, one picked
   The change is a morph in place: the old shape shrinks and blurs out, the new one
   grows out of the same point. No slide, no bounce. */

const MorphIcon: React.FC<{stage: number; since: number}> = ({stage, since}) => {
  const T = TEAL, faint = "rgba(3,166,207,.32)";
  if (stage === 1) {
    // the glass drifts along the lines it is reading
    const gx = 34 + 30 * (0.5 - 0.5 * Math.cos(since * 2.2)), gy = 44 + 6 * Math.sin(since * 1.6);
    return (
      <g>
        {[[14, 26, 64], [14, 40, 50], [24, 54, 52], [24, 68, 40], [14, 82, 30]].map(([x, y, w], i) => (
          <rect key={i} x={x} y={y} width={w} height={6} rx={3} fill={Math.abs(y + 3 - gy) < 12 && x < gx + 12 && x + w > gx - 12 ? T : faint} />
        ))}
        <circle cx={gx} cy={gy} r={15} fill="rgba(255,255,255,.55)" stroke={T} strokeWidth={6} />
        <path d={`M ${gx + 11} ${gy + 11} L ${gx + 26} ${gy + 26}`} stroke={T} strokeWidth={8} strokeLinecap="round" />
      </g>
    );
  }
  if (stage === 2) {
    const N = [[20, 74], [50, 34], [80, 66]];
    const on = (i: number) => clamp((since - 0.1 - i * 0.28) / 0.25);
    return (
      <g>
        <path d="M 20 74 L 50 34 L 80 66" fill="none" stroke={faint} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" />
        <path d="M 20 74 L 50 34 L 80 66" fill="none" stroke={T} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round"
          strokeDasharray={110} strokeDashoffset={110 * (1 - clamp((since - 0.1) / 0.8))} />
        {N.map(([x, y], i) => <circle key={i} cx={x} cy={y} r={11} fill="#fff" stroke={T} strokeWidth={5}>
        </circle>)}
        {N.map(([x, y], i) => <circle key={"f" + i} cx={x} cy={y} r={6} fill={T} opacity={on(i)} />)}
      </g>
    );
  }
  const Coin: React.FC<{x: number; y: number; r: number}> = ({x, y, r}) => (
    <g>
      <circle cx={x} cy={y} r={r} fill="#fff" stroke={T} strokeWidth={6} />
      <text x={x} y={y + r * 0.42} textAnchor="middle" fontFamily={LBL} fontWeight={900} fontSize={r * 1.25} fill={T}>$</text>
    </g>
  );
  if (stage === 3) return <Coin x={50} y={50} r={32} />;
  if (stage === 4) {
    const k2 = expoOut(clamp(since / 0.4));
    return <g><Coin x={lerp(50, 38, k2)} y={50} r={28} /><g opacity={k2}><Coin x={lerp(50, 64, k2)} y={50} r={28} /></g></g>;
  }
  // stage 5: three doors, the nurse picks one
  const pick = expoOut(clamp((since - 0.35) / 0.35));
  return (
    <g>
      {[14, 40, 66].map((x, i) => (
        <g key={i}>
          <rect x={x} y={28} width={22} height={44} rx={4} fill={i === 0 ? `rgba(3,166,207,${pick})` : "#fff"} stroke={T} strokeWidth={4.5} />
          <circle cx={x + 17} cy={52} r={2.2} fill={i === 0 && pick > 0.5 ? "#fff" : T} />
        </g>
      ))}
      <path d="M 18 84 L 28 84" stroke={T} strokeWidth={0} />
      <path d="M 19 50 L 24 56 L 32 44" fill="none" stroke="#fff" strokeWidth={4} strokeLinecap="round" strokeLinejoin="round"
        strokeDasharray={24} strokeDashoffset={24 * (1 - pick)} />
    </g>
  );
};

export const AIMorph: React.FC<{t: number; tGlobal: number; ev: Record<string, number>; size: number}> = ({t, tGlobal, ev, size}) => {
  const cuts = [ev.read, ev.reasoned, ev.paid, ev.thinking, ev.sorting].map((x) => (x ?? 99) - 0.15);
  let stage = 0;
  cuts.forEach((c, i) => { if (t >= c) stage = i + 1; });
  const since = stage === 0 ? t : t - cuts[stage - 1];
  const breathe = 1 + Math.sin(tGlobal * 2.1) * 0.035;     // the mark's own breathing, kept through every shape
  const inK = expoOut(clamp(since / 0.32));
  const outK = clamp(since / 0.16);
  const box = size * 100 / 112;                              // AIMark draws its 100 units inside a padded 112 box
  const layer = (node: React.ReactNode, sc: number, op: number, blur: number, key: string) => (
    <div key={key} style={{position: "absolute", left: -size / 2, top: -size / 2, width: size, height: size,
      display: "flex", alignItems: "center", justifyContent: "center",
      transform: `scale(${sc * breathe})`, opacity: op, filter: blur > 0.05 ? `blur(${blur}px)` : undefined}}>{node}</div>
  );
  const icon = (st: number, sn: number) => st === 0
    ? <AIMark size={size} t={tGlobal} />
    : <svg width={box} height={box} viewBox="0 0 100 100" style={{overflow: "visible"}}><MorphIcon stage={st} since={sn} /></svg>;
  const layers: React.ReactNode[] = [];
  if (stage > 0 && since < 0.16) layers.push(layer(icon(stage - 1, since + (stage - 1 > 0 ? cuts[stage - 1] - cuts[stage - 2] : 0)), 1 - 0.3 * outK, 1 - outK, 4 * outK, "out"));
  layers.push(layer(icon(stage, since), stage === 0 ? 1 : 0.7 + 0.3 * inK, stage === 0 ? 1 : inK, stage === 0 ? 0 : 4 * (1 - inK), "in"));
  return <>{layers}</>;
};

/* ------------------------------------------------------------------ end card */
/**
 * The series slate, as graph engineering and loop have it: "I HAVE NO IDEA WHAT THAT MEANS",
 * the teal rule, then the entry (term, how it's said, what it means). Same faces, sizes and
 * motion as GE's EndCard, in 720-space (GE's 1080 numbers / 1.5).
 *
 * No meter this time (Sejal, 9 Oct): GE's TIME odometer and loop's credits counter are out.
 * In their place, under the definition, a tiny "save this for later" pill whose bookmark
 * draws on and fills. With the meter gone the stack is re-centred, so it doesn't sit top-heavy.
 */
const ED = {
  bg: "#141416", ink: "#F2F2EF", sub: "#B9B9C0", dim: "#8A8A93", card: "#23232B", edge: "#40404B",
  display: "'MonaSans','Helvetica Neue',Arial,sans-serif",
  chrome: "'JakartaLocal','Helvetica Neue',Arial,sans-serif",
};
const DY = 120;   // the whole stack, moved down to sit centred without the meter
export const EndCard: React.FC<{t: number}> = ({t}) => {
  const ease = (x: number) => 1 - Math.pow(1 - clamp(x), 3);
  const titleIn = ease(t / 0.45);
  const ruleK = ease((t - 0.5) / 0.4);
  const step = (d: number) => ease((t - 0.7 - d) / 0.35);
  const pill = ease((t - 1.9) / 0.35);
  const draw = expoOut(clamp((t - 2.0) / 0.45));
  const fill = ease((t - 2.55) / 0.25);
  const row = (top: number, o: number, style: React.CSSProperties, body: React.ReactNode) => (
    <div style={{position: "absolute", left: 0, width: 720, top: top + DY, textAlign: "center", opacity: o, ...style}}>{body}</div>
  );
  const BM = "M1 1.5 H12 V17 L6.5 12.6 L1 17 Z";   // a bookmark, the platforms' own "save" glyph
  return (
    <div style={{position: "absolute", left: 0, top: 0, width: 720, height: 1280, background: ED.bg}}>
      <div style={{position: "absolute", left: 0, width: 720, top: 273.3 + DY, textAlign: "center",
        opacity: titleIn, transform: `translateY(${(1 - titleIn) * 16}px)`}}>
        {["I HAVE NO IDEA", "WHAT THAT MEANS"].map((l, i) => (
          <div key={i} style={{fontFamily: ED.display, fontWeight: 800, fontSize: 53.33, lineHeight: 1.15,
            letterSpacing: -1, color: ED.ink}}>{l}</div>
        ))}
      </div>
      <div style={{position: "absolute", left: 360 - 90 * ruleK, top: 400 + DY, width: 180 * ruleK, height: 2, background: C.teal}} />
      {row(449.3, step(0), {fontFamily: ED.display, fontWeight: 800, fontSize: 50.67, letterSpacing: -1.33, color: ED.ink},
        "system one model")}
      {row(524, step(0.12), {fontFamily: MONO, fontWeight: 700, fontSize: 20, color: ED.dim, whiteSpace: "pre"},
        "/ˈsɪs.təm wʌn ˈmɒd.əl/  noun")}
      {row(566.7, step(0.24), {fontFamily: ED.chrome, fontWeight: 500, fontSize: 26.67, lineHeight: 1.35, color: ED.sub},
        <>Built to choose. You give it the options,<br />it picks one and says how sure it is.</>)}
      <div style={{position: "absolute", left: 0, width: 720, top: 676 + DY, display: "flex", justifyContent: "center",
        opacity: pill, transform: `translateY(${(1 - pill) * 10}px)`}}>
        <div style={{display: "flex", alignItems: "center", gap: 9, padding: "8px 16px 8px 13px", borderRadius: 999,
          background: ED.card, border: `1.5px solid ${ED.edge}`}}>
          <svg width={14} height={19} viewBox="0 0 13.5 18.5" style={{overflow: "visible"}}>
            <path d={BM} fill={C.teal} fillOpacity={fill} stroke={fill > 0.02 ? C.teal : ED.dim} strokeWidth={1.6}
              strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
          </svg>
          <span style={{fontFamily: ED.chrome, fontWeight: 500, fontSize: 17, color: ED.dim, letterSpacing: 0.2}}>
            Save this for later</span>
        </div>
      </div>
    </div>
  );
};
