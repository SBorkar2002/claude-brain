import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import cut from "./cut.json";

/**
 * E001 `loop` -- 9:16.
 *
 * Everything here is driven by src/cut.json, which is emitted from the same
 * spec.py / timeline.py the ffmpeg build reads. Change a timing there and both
 * paths move together; nothing about the cut is hard-coded in this file.
 *
 * Plates are 720x1280 with every dialogue layer hidden. Captions are drawn
 * live, one word at a time, all at the same point -- so retiming a line is a
 * number, not 232 re-rendered PNGs.
 */

const S = cut.scale; // plates are 720x1280, the master is 1080x1920
const PRELOAD_FRAMES = 12; // ~0.4s of lead-in for the browser to decode a plate

/** A panel, mounted early and invisible so it is decoded before its cut.
 *
 * A panel carrying `bg` PUSHES IN partway through: it plays as an ordinary
 * plate until `pushFrom`, then the plate is gone and the screen becomes the
 * frame with everything on it drawn live. Frame 15 is the only one so far.
 * The swap is a hard cut -- a dissolve here would read as a mistake. */
const Plate: React.FC<{
  src: string; visibleFrom: number; bg?: string; pushFrom?: number;
}> = ({ src, visibleFrom, bg, pushFrom }) => {
  const frame = useCurrentFrame();
  const shown = frame >= visibleFrom;
  if (bg !== undefined && (pushFrom === undefined || frame >= pushFrom)) {
    return <div style={{ width: "100%", height: "100%", background: bg,
                         opacity: shown ? 1 : 0 }} />;
  }
  return (
    <Img
      src={staticFile(`v10/plates/${src}`)}
      style={{
        width: "100%",
        height: "100%",
        objectFit: "cover",
        opacity: shown ? 1 : 0,
      }}
    />
  );
};

/**
 * Lato is the COMIC's face -- it draws the captions, and the caption wrap is
 * measured against it in Python (captions.py), so it cannot change without
 * re-measuring every line break.
 *
 * The other three are the BRAND faces, and they are confined to the explainer
 * panels and the card. That split is the point: the comic is the story and the
 * explainer is the product's own voice, so the moment the film starts teaching,
 * it starts speaking in the brand's type.
 *
 * Latin subsets from Google Fonts. They are only ever rendered in Chrome, so
 * woff2 is fine -- PIL only needs a real file for Lato.
 */
const FONT = `
@font-face { font-family:'LatoLocal';
  src:url('${staticFile("v10/fonts/Lato-Regular.ttf")}') format('truetype');
  font-weight:400; font-style:normal; }
@font-face { font-family:'MonaSans';
  src:url('${staticFile("v10/fonts/MonaSans-Bold.woff2")}') format('woff2');
  font-weight:700; font-style:normal; }
@font-face { font-family:'MonaSans';
  src:url('${staticFile("v10/fonts/MonaSans-ExtraBold.woff2")}') format('woff2');
  font-weight:800; font-style:normal; }
@font-face { font-family:'JakartaSans';
  src:url('${staticFile("v10/fonts/PlusJakartaSans-Medium.woff2")}') format('woff2');
  font-weight:500; font-style:normal; }
@font-face { font-family:'JakartaSans';
  src:url('${staticFile("v10/fonts/PlusJakartaSans-Bold.woff2")}') format('woff2');
  font-weight:700; font-style:normal; }
@font-face { font-family:'GeistMono';
  src:url('${staticFile("v10/fonts/GeistMono-Regular.woff2")}') format('woff2');
  font-weight:400; font-style:normal; }
@font-face { font-family:'GeistMono';
  src:url('${staticFile("v10/fonts/GeistMono-Bold.woff2")}') format('woff2');
  font-weight:700; font-style:normal; }`;

/** The brand type system. Display, UI chrome, and code-like values. */
const DISPLAY = "'MonaSans', 'Helvetica Neue', Arial, sans-serif";
const LABEL = "'JakartaSans', 'Helvetica Neue', Arial, sans-serif";
const MONO_B = "'GeistMono', 'SF Mono', Menlo, Consolas, monospace";

/** One word, centred on the point where the caption block used to sit. */
const Caption: React.FC<{ c: (typeof cut.captions)[number] }> = ({ c }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = c.at + frame / fps;

  // Some captions clear while their panel keeps holding -- the "...Oh" beat
  // needs the face to stay after the word has gone.
  if (c.clearAt != null && t >= c.clearAt) return null;

  let idx = -1;
  for (let i = 0; i < c.words.length; i++) {
    if (t + 1e-6 >= c.words[i].t) idx = i;
  }
  if (idx < 0) return null; // before the first word the panel is bare -- this is
  //                           what lets the dark-room beat sit in silence

  const type = {
    fontFamily: "LatoLocal, Lato, sans-serif",
    fontSize: 32 * S,
    lineHeight: 1.2,
    color: c.color,
    whiteSpace: "nowrap" as const,
  };

  /**
   * "build" keeps every word that has been spoken, each in the position Figma
   * laid it out in, so the sentence accumulates and stays readable. "flash"
   * is the original: one word alone at the centre of the box.
   *
   * The Figma boxes are sized for the whole caption -- frame 41's is four
   * lines tall, frame 14's is five -- so "flash" was showing one word in the
   * middle of a box built for twelve, which is what made the longer lines
   * hard to follow. Positions come from Python (captions.word_positions) so
   * the wrap is Figma's wrap; re-wrapping here would drift by a word.
   */
  const mode = (c as { mode?: string }).mode ?? "flash";

  /**
   * "lines" -- Natural Habitat Shorts style. A whole line at a time, white on a
   * heavy black outline, in one fixed place near the bottom.
   *
   * The outline is the load-bearing part. Black caption text needed clean paper
   * under it, which is exactly why every caption had its own hand-placed Figma
   * box; an outlined caption is legible over anything, so one fixed position
   * works for the whole film and the placement system stops being needed.
   *
   * paint-order: stroke draws the outline BEHIND the fill. Without it a 7px
   * -webkit-text-stroke is centred on the glyph edge and eats half the
   * letterform, which at this weight closes up the counters in a and e.
   */
  if (mode === "lines") {
    const sub = cut.sub;
    const ls = (c as { lines?: { t: number; text: string }[] }).lines ?? [];
    let li = -1;
    for (let i = 0; i < ls.length; i++) if (t + 1e-6 >= ls[i].t) li = i;
    if (li < 0) return null;
    const from = Math.max(0, li - (sub.stack - 1));
    const shown = ls.slice(from, li + 1);
    // Its own Figma placement, not one band for the whole film: sx is the box's
    // centre nudged only as far as the safe area demands, sy is the box's
    // vertical centre. The block is centred on that point, so a caption that
    // used to wrap to three lines and now fits on one still sits where it sat.
    const cx = (c as { sx?: number }).sx ?? 360;
    const cy = (c as { sy?: number }).sy ?? 930;
    return (
      <AbsoluteFill>
        <div style={{
          position: "absolute", left: cx * S, top: cy * S,
          transform: "translate(-50%, -50%)",
          whiteSpace: "nowrap", textAlign: "center",
          fontFamily: "LatoLocal, Lato, sans-serif",
          fontSize: sub.size * S, fontWeight: sub.weight,
          lineHeight: `${sub.line * S}px`,
          color: sub.fill,
          WebkitTextStrokeWidth: `${sub.stroke_w * S}px`,
          WebkitTextStrokeColor: sub.stroke,
          paintOrder: "stroke",
        }}>
          {shown.map((L, i) => <div key={from + i}>{L.text}</div>)}
        </div>
      </AbsoluteFill>
    );
  }

  if (mode === "build") {
    const ws = c.words as { t: number; w: string; x?: number; cy?: number }[];
    return (
      <AbsoluteFill>
        {ws.slice(0, idx + 1).map((w, i) =>
          w.x === undefined ? null : (
            <div key={i} style={{
              ...type, position: "absolute",
              left: w.x * S, top: (w.cy as number) * S,
              transform: `translateY(-50%)${c.italic ? " skewX(-12deg)" : ""}`,
            }}>{w.w}</div>
          )
        )}
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill>
      <div
        style={{
          ...type,
          position: "absolute",
          left: c.cx * S,
          top: c.cy * S,
          transform: `translate(-50%, -50%)${c.italic ? " skewX(-12deg)" : ""}`,
        }}
      >
        {c.words[idx].w}
      </div>
    </AbsoluteFill>
  );
};

/** blend two #rrggbb colours; used where a shape changes meaning mid-move */
const mix = (a: string, b: string, k: number) => {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [r1, g1, b1] = p(a), [r2, g2, b2] = p(b);
  const c = (x: number, y: number) => Math.round(x + (y - x) * Math.max(0, Math.min(1, k)));
  return `rgb(${c(r1, r2)},${c(g1, g2)},${c(b1, b2)})`;
};

const ease3 = (k: number) => k * k * (3 - 2 * k);

const clamp01 = (v: number) => Math.min(1, Math.max(0, v));
const lerpCol = (a: string, b: string, k: number) => {
  const h = (c: string) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
  const [r1, g1, b1] = h(a);
  const [r2, g2, b2] = h(b);
  const m = (x: number, y: number) => Math.round(x + (y - x) * k);
  return `rgb(${m(r1, r2)},${m(g1, g2)},${m(b1, b2)})`;
};

const TEAL = "#03A6CF";   // working
const DONE = "#1B8E4F";   // passed
const IDLE = "#B9B9BE";   // not yet
const FAIL = "#D24B3E";   // failed, exactly once per panel

/** A "click" over the keyboard: two quick flickers, then it holds, then it goes.
 *  Baked lettering can't do this -- both used to appear at once, which read as
 *  one event rather than a hand typing. */
const Sfx: React.FC<{ s: (typeof cut.sfx)[number] }> = ({ s }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const first = s.hits[0];
  const last = s.hits[s.hits.length - 1];
  if (t < first - 0.1 || t > last + 0.7) return null;

  // sits quietly on the keyboard, then snaps to full on each keystroke it was
  // assigned -- so the lettering ticks with what you can actually hear
  let spike = 0;
  for (const h of s.hits) {
    if (t >= h && t < h + 0.26) spike = Math.max(spike, 1 - (t - h) / 0.26);
  }
  const fadeIn = clamp01((t - (first - 0.1)) / 0.15);
  const fadeOut = 1 - clamp01((t - (last + 0.25)) / 0.45);
  const opacity = (0.3 + 0.7 * spike * spike) * fadeIn * fadeOut;
  const scale = 1 + 0.1 * spike;

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: s.cx * S,
          top: s.cy * S,
          transform: `translate(-50%, -50%) rotate(${s.rot}deg) scale(${scale})`,
          fontFamily: "Arial, Helvetica, sans-serif",
          fontSize: s.size * S,
          color: s.color,
          opacity,
          whiteSpace: "nowrap",
        }}
      >
        {s.text}
      </div>
    </AbsoluteFill>
  );
};



/**
 * The card: LOOP - cleared - and, under it, what it cost.
 *
 * The stamp says the job finished. The number says what finishing took. Putting
 * them on the same card is the joke the whole episode has been building: it did
 * exactly what he asked, all night, and nobody was watching the meter.
 */
const CreditsOut: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cr = cut.credits;
  const t = frame / fps;
  if (t < cr.appear) return null;

  const k = clamp01((t - cr.appear) / cr.run);
  const eased = 1 - Math.pow(1 - k, 2.6);          // fast, then grinds to a halt
  const left = Math.round(cr.start * (1 - eased));
  const done = left === 0;
  const pop = done ? 1 + 0.10 * Math.max(0, 1 - (t - cr.appear - cr.run) / 0.3) : 1;
  const inK = clamp01((t - cr.appear) / 0.22);

  return (
    <AbsoluteFill style={{ opacity: inK }}>
      <div
        style={{
          position: "absolute",
          left: cr.cx * S,
          top: cr.label_cy * S,
          transform: "translate(-50%, -50%)",
          fontFamily: "'SF Mono', Menlo, Consolas, monospace",
          fontSize: 19 * S,
          letterSpacing: 3 * S,
          color: "#8C8C93",
          whiteSpace: "nowrap",
        }}
      >
        CREDITS REMAINING
      </div>
      <div
        style={{
          position: "absolute",
          left: cr.cx * S,
          top: cr.num_cy * S,
          transform: `translate(-50%, -50%) scale(${pop})`,
          fontFamily: "'SF Mono', Menlo, Consolas, monospace",
          fontSize: 68 * S,
          fontWeight: 700,
          color: done ? "#D24B3E" : "#2b2b2b",
          fontVariantNumeric: "tabular-nums",
          whiteSpace: "nowrap",
        }}
      >
        {left.toLocaleString("en-US")}
      </div>
    </AbsoluteFill>
  );
};

/**
 * The AI's mark.
 *
 * Not a face -- the AIs never have faces -- and not a four-point sparkle, which
 * every AI product on the market already uses. A rounded body with a forward
 * chevron: abstract, and unmistakably facing somewhere.
 *
 * Facing is the point. The check in the plain explanation is a look BACK at
 * where it came from, and a symmetric mark cannot turn its head.
 */
const AIMark: React.FC<{
  cx: number; cy: number; size: number; rot?: number; pulse?: number;
  color?: string; gaze?: number; squint?: number; wide?: number;
}> = ({ cx, cy, size, rot = 0, pulse = 1, color = TEAL, gaze = 1, squint = 0, wide = 0 }) => (
  <div
    style={{
      position: "absolute",
      left: cx,
      top: cy,
      width: size,
      height: size,
      marginLeft: -size / 2,
      marginTop: -size / 2,
      transform: `rotate(${rot}deg) scale(${pulse})`,
    }}
  >
    <svg viewBox="-6 -6 112 112" width="100%" height="100%">
      {/* Six rounded petals radiating from the centre -- the shape everyone
          recognises as "an AI thing", drawn generically rather than copying any
          company's mark. The eye in the middle is what gives it a face's worth
          of expression without being a face. */}
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <ellipse key={i} cx="50" cy="25" rx="14.5" ry="25" fill={color}
                 transform={`rotate(${i * 60} 50 50)`} />
      ))}
      {/* the eye: shifts to look, narrows under effort, widens when it lands */}
      <circle cx={50 + gaze * 9} cy="50" r="17" fill="#ffffff" />
      <ellipse cx={50 + gaze * 9} cy="50"
               rx={11 * (1 + wide * 0.25)}
               ry={11 * (1 + wide * 0.25) * (1 - squint * 0.62)}
               fill={color} />
    </svg>
  </div>
);

/** The mark sitting on a blank monitor: present, awake, breathing. */
const MarkOnScreen: React.FC<{ f: (typeof cut.aiMark.frames)[number] }> = ({ f }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const m = cut.aiMark;
  const o = f as { cx?: number; cy?: number; size?: number };
  const t = frame / fps;
  const inK = clamp01(t / 0.3);
  const breathe = 1 + Math.sin((f.at + t) * 2.1) * 0.035;
  return (
    <AbsoluteFill style={{ opacity: inK }}>
      <AIMark
        cx={(o.cx ?? m.screen_cx) * S}
        cy={(o.cy ?? m.screen_cy) * S}
        size={(o.size ?? m.screen_size) * S}
        pulse={breathe}
      />
    </AbsoluteFill>
  );
};

/**
 * A caption that arrives as a WHOLE SENTENCE and holds.
 *
 * The rest of the film reveals a word at a time on each word's own voice onset.
 * That is wrong for a line that is meant to arrive as a wall of jargon: across
 * this film the median caption word is on screen for 299ms and 30% are under
 * 200ms, which is under the time it takes to read one. A wall is easier to take
 * in one piece than in twenty-three flickers.
 */
const HoldCaption: React.FC<{ h: (typeof cut.holdCaptions)[number] }> = ({ h }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = h.at + frame / fps;
  const inK = clamp01((t - h.at) / h.fade);
  const outK = 1 - clamp01((t - (h.until - h.fade)) / h.fade);
  const sub = cut.sub;
  // Same white-on-black-outline treatment as every other caption. This one is
  // held as a WHOLE sentence rather than revealed a line at a time -- it sits
  // above the monitor while the ring draws itself, and reading it in one go is
  // the point -- but it should not look like it belongs to a different film,
  // which is exactly what a plain black fill did next to the outlined ones.
  return (
    <div style={{
      position: "absolute",
      left: h.x * S, top: h.y * S, width: h.w * S,
      textAlign: h.align === "C" ? "center" : "left",
      fontFamily: "'LatoLocal', Lato, sans-serif",
      fontSize: h.size * S,
      lineHeight: `${h.line * S}px`,
      fontWeight: sub.weight,
      color: sub.fill,
      WebkitTextStrokeWidth: `${sub.stroke_w * S}px`,
      WebkitTextStrokeColor: sub.stroke,
      paintOrder: "stroke",
      opacity: Math.min(inK, outK),
    }}>
      {h.text}
    </div>
  );
};

/**
 * The technical explanation, built from Sejal's Figma frame (429:1420).
 *
 * The version this replaces said one thing with four elements -- a dot, a
 * separate 0/2, a pip row and a label -- and Anandhi read the counter as a
 * number of weeks. Here the count sits INSIDE the ring and the ring is its
 * gauge, so the fraction and the arc are the same fact stated twice.
 *
 * Two gates collapse into one place. RUN A STEP is the heading, CHECK is a
 * status chip at the top, and a lap IS a step: the dot leaves the top, comes
 * back, and the chip reports what the check found. They stay conceptually
 * distinct -- they have to, because the check is the termination condition and
 * that is the term being defined -- without two labelled positions on the ring.
 *
 * The ARC TRACKS THE COUNT, NOT THE DOT. That is the important one: a failed
 * lap is a whole revolution where the arc does not move, which is the most
 * legible way to show an iteration that cost something and bought nothing.
 */
const Ring: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sc = cut.screen;
  const R = sc.ring;
  const t = sc.at + frame / fps;

  const ease = (k: number) => k * k * (3 - 2 * k);
  const rad = (d: number) => (d * Math.PI) / 180;
  const pt = (deg: number, r = R.r) =>
    [R.cx + r * Math.cos(rad(deg)), R.cy + r * Math.sin(rad(deg))] as const;

  const drawK = clamp01((t - R.draw.at) / R.draw.dur);
  if (drawK <= 0) return null;
  const splitK = ease(clamp01((t - R.split.at) / R.split.dur));
  const fillK = ease(clamp01((t - R.fill.at) / R.fill.dur));
  const exitK = ease(clamp01((t - R.exit_at.at) / R.exit_at.dur));
  const doneK = ease(clamp01((t - R.done_at.at) / 0.35));

  const C = R.count;
  let done = 0;
  for (const [at, n] of R.count_steps as [number, number][]) if (t + 1e-6 >= at) done = n;
  let lit: boolean | null = null;
  let litAt = 0;
  for (const [at, ok] of R.checks as [number, boolean][]) {
    if (t + 1e-6 >= at && t < at + R.flash) { lit = ok; litAt = at; }
  }
  const failing = lit === false;
  const finished = done >= C.total;

  // the dot: one continuous traveller, the current iteration
  const arc = R.arc as [number, number][];
  const dotAt = arc[0][0];
  let angle = arc[0][1];
  if (t >= dotAt) {
    let seg = 0;
    for (let k = 0; k < arc.length - 1; k++) if (t >= arc[k][0]) seg = k;
    const [t0, a0] = arc[seg];
    const [t1, a1] = arc[Math.min(seg + 1, arc.length - 1)];
    const k = t1 > t0 ? clamp01((t - t0) / (t1 - t0)) : 1;
    angle = a0 + (a1 - a0) * ease(k);
  }
  const [dx, dy] = pt(angle);
  const dotIn = ease(clamp01((t - dotAt) / 0.22));


  const CIRC = 2 * Math.PI * R.r;
  const shake = failing ? Math.sin(((t - litAt) / R.flash) * Math.PI * 6) * 4 : 0;
  const arcCol = fillK > 0 ? DONE : TEAL;
  const numCol = failing ? FAIL : finished && fillK > 0 ? DONE : TEAL;
  const MONO = MONO_B;      // values and badges
  const HEAD = DISPLAY;     // headings and the terminal statement

  const txt = (st: React.CSSProperties, body: React.ReactNode, key: string) => (
    <div key={key} style={{ position: "absolute", ...st }}>{body}</div>
  );

  return (
    <AbsoluteFill style={{ backgroundColor: R.bg }}>
      {txt({ left: 0, top: R.header.cy * S, width: "100%", textAlign: "center",
             transform: "translateY(-50%)", fontFamily: HEAD,
             fontSize: R.header.size * S, fontWeight: 800, color: R.header.color,
             opacity: drawK },
           R.header.text, "hdr")}

      <svg viewBox="0 0 720 1280" width="100%" height="100%"
           style={{ position: "absolute", inset: 0 }}>
        {/* The ring is `total` arcs, not one circle. Their gap is zero until the
            split, so it reads as one continuous ring and then visibly BECOMES
            two -- which is the decomposition, and a 4px nick was not saying it.
            After that each arc fills as its own step passes, so the gauge and
            the fraction are the same fact and cannot disagree. */}
        {Array.from({ length: C.total }, (_, i) => {
          const span = 360 / C.total;
          // overshoot: the gap springs past its resting width, then settles
          const g = R.split_gap * (splitK + 0.35 * Math.sin(splitK * Math.PI));
          const a0 = -90 + i * span + g / 2;
          const a1 = -90 + (i + 1) * span - g / 2;
          const len = ((a1 - a0) / 360) * CIRC;

          // counted out in turn as they separate
          // swell and settle, one arc then the next -- never both at once
          const pulseAt = R.split.at + R.split_stagger * (i + 1);
          const pulse = t >= pulseAt && t < pulseAt + R.split_pulse
            ? Math.sin(((t - pulseAt) / R.split_pulse) * Math.PI) : 0;

          // this segment's own step
          const stepAt = (R.count_steps as [number, number][]).find(([, n]) => n === i + 1);
          const fill = stepAt && t >= stepAt[0]
            ? ease(clamp01((t - stepAt[0]) / 0.45)) : 0;

          // The count-out is GEOMETRIC, not coloured: each segment thickens and
          // steps outward for a moment. Flashing them teal made the whole ring
          // look full and then empty again, which reads as progress being made
          // and lost -- the opposite of what a decomposition means.
          // Thicken, do not grow outward. The ring sits 13px under the CHECK
          // chip at rest, so a radius swell of even +8 touches it; thickening
          // grows both ways, so the same visual weight costs half the clearance.
          const pr = R.r;
          const pw = R.w + 14 * pulse;
          return (
            <g key={i} transform={`rotate(${a0} ${R.cx} ${R.cy})`}>
              <circle cx={R.cx} cy={R.cy + shake} r={pr} fill="none"
                      strokeWidth={pw} strokeLinecap="butt"
                      stroke={fillK > 0 ? DONE : R.track}
                      opacity={(fillK > 0 ? 0.3 + 0.7 * fillK : 1) *
                               (0.55 + 0.45 * drawK)}
                      strokeDasharray={`${((a1 - a0) / 360) * 2 * Math.PI * pr * drawK} ${CIRC}`} />
              {fill > 0 && (
                <circle cx={R.cx} cy={R.cy + shake} r={R.r} fill="none"
                        stroke={arcCol} strokeWidth={R.w} strokeLinecap="round"
                        strokeDasharray={`${len * fill} ${CIRC}`} />
              )}
            </g>
          );
        })}

        {/* the current iteration */}
        {t >= dotAt && (
          <>
            <circle cx={dx} cy={dy + shake} r={(R.dot_r + R.dot_collar) * dotIn}
                    fill="#ffffff" />
            <circle cx={dx} cy={dy + shake} r={R.dot_r * dotIn}
                    fill={failing ? FAIL : finished && fillK > 0 ? DONE : TEAL} />
          </>
        )}

        {/* the way out, shut until the count fills */}
        <rect x={R.exit.x} y={R.exit.y} width={R.exit.w} height={R.exit.h}
              rx={R.exit.w / 2} fill={exitK > 0 ? DONE : R.exit.color}
              opacity={(exitK > 0 ? 1 : R.exit.op) * drawK} />
      </svg>

      {/* CHECK -- a status chip, not a second gate */}
      <div style={{
        position: "absolute", left: (R.chip.cx - R.chip.w / 2) * S,
        top: (R.chip.cy - R.chip.h / 2) * S,
        width: R.chip.w * S, height: R.chip.h * S,
        borderRadius: 100 * S, background: R.chip.face,
        border: `${1 * S}px solid ${lit === null ? R.chip.edge : lit ? DONE : FAIL}`,
        boxSizing: "border-box", display: "flex", alignItems: "center",
        justifyContent: "center", gap: 8 * S, opacity: drawK,
        transform: `scale(${1 + (lit !== null ? 0.08 * Math.sin(clamp01((t - litAt) / R.flash) * Math.PI) : 0)})`,
      }}>
        <div style={{ width: R.chip.dot * S, height: R.chip.dot * S, borderRadius: "50%",
                      background: lit === null ? R.chip.edge : lit ? DONE : FAIL }} />
        <div style={{ fontFamily: MONO, fontSize: R.chip.size * S, fontWeight: 700,
                      color: lit === null ? R.chip.color : lit ? DONE : FAIL,
                      whiteSpace: "nowrap" }}>{R.chip.text}</div>
      </div>

      {/* the count, inside its own gauge */}
      {splitK > 0 && (
        <>
          {txt({ left: 0, top: (C.num_cy + shake) * S, width: "100%", textAlign: "center",
                 transform: "translateY(-50%)", fontFamily: MONO,
                 fontSize: C.num_size * S, fontWeight: 700, color: numCol,
                 fontVariantNumeric: "tabular-nums", opacity: splitK },
               `${done}/${C.total}`, "num")}
          {txt({ left: 0, top: C.label_cy * S, width: "100%", textAlign: "center",
                 transform: "translateY(-50%)", fontFamily: LABEL,
                 fontSize: C.label_size * S, fontWeight: 500, letterSpacing: 0.6 * S,
                 color: C.label_color, opacity: splitK },
               C.label, "lab")}
        </>
      )}

      {/* the other two termination conditions, kept quiet */}
      {([["left", R.caps.left_x, R.caps.left], ["right", R.caps.right_x, R.caps.right]] as
        [string, number, [string, string]][]).map(([side, x, [label, value]]) => (
        <React.Fragment key={side}>
          {txt({ left: side === "left" ? x * S : undefined,
                 right: side === "right" ? (720 - x) * S : undefined,
                 top: R.caps.label_cy * S, transform: "translateY(-50%)",
                 fontFamily: LABEL, fontSize: R.caps.label_size * S, fontWeight: 500,
                 color: R.caps.label_color, whiteSpace: "nowrap", opacity: drawK },
               label, `${side}l`)}
          {txt({ left: side === "left" ? x * S : undefined,
                 right: side === "right" ? (720 - x) * S : undefined,
                 top: R.caps.value_cy * S, transform: "translateY(-50%)",
                 fontFamily: MONO, fontSize: R.caps.value_size * S, fontWeight: 700,
                 color: R.caps.value_color, whiteSpace: "nowrap", opacity: drawK },
               value, `${side}v`)}
        </React.Fragment>
      ))}

      {/* the gate at the bottom */}
      <div style={{
        position: "absolute", left: R.done.x * S, top: R.done.y * S,
        width: R.done.w * S, height: R.done.h * S, boxSizing: "border-box",
        borderRadius: R.done.r * S,
        background: doneK > 0 ? DONE : "transparent",
        border: doneK > 0 ? "none" : `${R.done.edge_w * S}px solid ${R.done.color}`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: HEAD, fontSize: R.done.size * S, fontWeight: 800,
        color: doneK > 0 ? "#ffffff" : R.done.color,
        opacity: drawK, transform: `scale(${0.96 + 0.04 * doneK})`,
      }}>{R.done.label}</div>
    </AbsoluteFill>
  );
};

/**
 * The plain explanation: he sets a race running and goes to sleep.
 *
 * The track is a real circuit with a FORK, traced from generated art (9 Sep):
 * thinned to a centreline it came back as exactly two junctions and no
 * endpoints, so there are three distinct routes between the same two points.
 *
 * That fork is what makes the failure legible. The old version ran the same leg
 * twice, so "failing" was a lap on which a number did not move. Here the runner
 * takes the SHORT chord, and checkpoint 2 -- which only exists on the LONG leg
 * -- is left sitting on the road it did not take. You can see the reason, not
 * just the result. Then it reverses out of the shortcut and does it properly.
 *
 * The itinerary is a list of legs in spec.PLAIN, each naming a route and a
 * direction, so reversing is just u0 > u1 and needs no special case.
 */
const Plain: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pl = cut.plain;
  const t = pl.at + frame / fps;
  const ease = (k: number) => k * k * (3 - 2 * k);

  /** every route measured once, so a u is a real distance along that route */
  const geo = React.useMemo(() => {
    const build = (raw: number[][]) => {
      const P = raw.map(([x, y]) => [x * S, y * S] as [number, number]);
      let d = `M ${P[0][0]} ${P[0][1]}`;
      const pts: [number, number][] = [P[0]];
      for (let i = 0; i < P.length - 1; i++) {
        const a = P[i], b = P[i + 1];
        const m: [number, number] = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
        d += ` Q ${a[0]} ${a[1]} ${m[0]} ${m[1]}`;
        for (let k = 1; k <= 6; k++) {
          const u = k / 6, v = 1 - u;
          pts.push([v * v * a[0] + 2 * v * u * a[0] + u * u * m[0],
                    v * v * a[1] + 2 * v * u * a[1] + u * u * m[1]]);
        }
      }
      d += ` L ${P[P.length - 1][0]} ${P[P.length - 1][1]}`;
      pts.push(P[P.length - 1]);
      const cum = [0];
      for (let i = 1; i < pts.length; i++)
        cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
      return { d, pts, cum, len: cum[cum.length - 1] };
    };
    const out: Record<string, ReturnType<typeof build>> = {};
    for (const k of pl.order as string[]) out[k] = build((pl.routes as never)[k]);
    return out;
  }, []);

  /** [x, y, heading] at a fraction along a named route */
  const at = (route: string, u: number): [number, number, number] => {
    const g = geo[route];
    const target = clamp01(u) * g.len;
    let i = 1;
    while (i < g.cum.length - 1 && g.cum[i] < target) i++;
    const a = g.cum[i - 1], b = g.cum[i];
    const f = b > a ? (target - a) / (b - a) : 0;
    const [x0, y0] = g.pts[i - 1], [x1, y1] = g.pts[i];
    return [x0 + (x1 - x0) * f, y0 + (y1 - y0) * f,
            (Math.atan2(y1 - y0, x1 - x0) * 180) / Math.PI];
  };

  /** put a label beside the track, on whichever side is clearer */
  const beside = (route: string, u: number, dist: number): [number, number] => {
    const [gx, gy, ga] = at(route, u);
    let best: [number, number] = [gx, gy], clear = -1;
    for (const sgn of [1, -1]) {
      const a = ((ga + 90 * sgn) * Math.PI) / 180;
      const lx = gx + dist * S * Math.cos(a), ly = gy + dist * S * Math.sin(a);
      let c = Infinity;
      for (const k of pl.order as string[])
        for (const [px, py] of geo[k].pts) c = Math.min(c, Math.hypot(px - lx, py - ly));
      if (c > clear) { clear = c; best = [lx, ly]; }
    }
    return best;
  };

  // ---- state ----
  const trackK = ease(clamp01((t - pl.track_at) / pl.track_dur));
  const flagK = ease(clamp01((t - pl.flag_at) / pl.flag_dur));
  const gateK = (i: number) =>
    ease(clamp01((t - (pl.gates_at + i * pl.gates_stagger)) / pl.gates_dur));
  const crossed = t >= pl.cross_at;

  const CK = pl.checks as [number, number, boolean][];
  const state: Record<number, boolean | null> = {};
  for (const c of pl.cps as { n: number }[]) state[c.n] = null;
  let flashing: number | null = null, flashAt = 0;
  for (const [ct, n, ok] of CK) {
    if (t + 1e-6 >= ct) {
      state[n] = ok;
      if (t < ct + pl.flash) { flashing = n; flashAt = ct; }
    }
  }

  // ---- the runner walks its itinerary; reversing is just u0 > u1 ----
  const legs = pl.legs as { at: number; until: number; route: string; u0: number; u1: number }[];
  const running = t >= legs[0].at;
  let leg = legs[0], u = legs[0].u0;
  if (running) {
    leg = legs[0];
    for (const l of legs) if (t >= l.at) leg = l;
    const k = ease(clamp01((t - leg.at) / (leg.until - leg.at)));
    u = leg.u0 + (leg.u1 - leg.u0) * k;
  }
  const [rx, ry] = at(leg.route, u);
  const missing = flashing !== null && state[flashing] === false;

  const H = pl.head as unknown as {
    cx: number; cy: number; h: number;
    awake: string; awake_ar: number; awake_dx: number; awake_dy: number;
    asleep: string | null; asleep_ar: number; asleep_scale: number;
    asleep_dx: number; asleep_dy: number;
    sleep_at: number; wake_at: number;
    step: number[]; run: number[]; run_u: number; run_h: number;
    x_at: number; x_dur: number; x_size: number; x_w: number;
  };
  const gone = t >= pl.gone_at;
  const stepK = ease(clamp01((t - H.step[0]) / (H.step[1] - H.step[0])));
  const runK = ease(clamp01((t - H.run[0]) / (H.run[1] - H.run[0])));
  const [htx, hty] = at("main", pl.start_u - H.run_u * runK);
  const hx = H.cx * S + (htx - H.cx * S) * stepK;
  const hy = H.cy * S + (hty - H.cy * S) * stepK;
  const SWAP = 0.12;
  const sleepMix = ease(clamp01((t - H.sleep_at) / SWAP)) * (1 - ease(clamp01((t - H.wake_at) / SWAP)));
  const bump = 1 + 0.05 * Math.sin(
    clamp01((t - (t >= H.wake_at ? H.wake_at : H.sleep_at)) / 0.22) * Math.PI);
  const pose = (isAsleep: boolean) => {
    const fh = (H.h + (H.run_h - H.h) * stepK) * S * bump * (isAsleep ? H.asleep_scale : 1);
    const fw = fh * (isAsleep ? H.asleep_ar : H.awake_ar);
    return { src: (isAsleep ? H.asleep : H.awake) as string, width: fw, height: fh,
             dx: (isAsleep ? H.asleep_dx : H.awake_dx) * fw,
             dy: (isAsleep ? H.asleep_dy : H.awake_dy) * fh };
  };
  const fadeIn = ease(clamp01((t - pl.at - 0.1) / 0.35));
  const xK = ease(clamp01((t - H.x_at) / H.x_dur));
  const XS = H.x_size * S, EM = pl.emoji_size * S;
  const ei = Math.floor((t - pl.gone_at) * pl.emoji_fps);

  const [fx, fy, fang] = at("main", pl.start_u);
  const cols = Math.round(pl.flag_w / pl.flag_sq), rows = Math.round(pl.flag_h / pl.flag_sq);

  return (
    <AbsoluteFill>
      <svg width="100%" height="100%" style={{ position: "absolute", inset: 0 }}>
        {(pl.order as string[]).map((k) => (
          <path key={k} d={geo[k].d} fill="none" stroke="#dcdcd6"
                strokeWidth={pl.w * S} strokeLinecap="round" strokeLinejoin="round"
                strokeDasharray={geo[k].len}
                strokeDashoffset={geo[k].len * (1 - trackK)} />
        ))}

        {(pl.cps as { n: number; route: string; u: number }[]).map((c, i) => {
          const [gx, gy, ga] = at(c.route, c.u);
          const st = state[c.n];
          const col = st === null ? "#9a9a95" : st ? DONE : FAIL;
          const gk = gateK(i);
          const pop = c.n === flashing
            ? 1 + 0.24 * Math.sin(clamp01((t - flashAt) / pl.flash) * Math.PI)
            : 1 + 0.18 * Math.sin(gk * Math.PI);
          return (
            <g key={c.n} transform={`translate(${gx} ${gy}) rotate(${ga}) scale(${gk * pop})`}>
              <rect x={(-pl.gate_w / 2) * S} y={(-pl.gate_h / 2) * S}
                    width={pl.gate_w * S} height={pl.gate_h * S}
                    rx={(pl.gate_w / 2) * S} fill={col} />
            </g>
          );
        })}

        {flagK > 0 && (
          <g transform={`translate(${fx} ${fy}) rotate(${fang})`} opacity={flagK}>
            {Array.from({ length: rows }, (_, r) =>
              Array.from({ length: cols }, (_, c) => {
                const w = pl.flag_sq * S, dark = (r + c) % 2 === 0;
                return (
                  <rect key={`${r}-${c}`} x={(-pl.flag_h / 2) * S + r * w}
                        y={(-pl.flag_w / 2) * S + c * w} width={w + 0.6} height={w + 0.6}
                        fill={dark ? (crossed ? DONE : "#2b2b2b") : "#ffffff"}
                        stroke={dark ? "none" : "#2b2b2b"} strokeWidth={dark ? 0 : 1.4 * S} />
                );
              })
            )}
          </g>
        )}
      </svg>

      {!gone && [false, true].map((isAsleep) => {
        if (isAsleep && H.asleep === null) return null;
        const p = pose(isAsleep);
        const mix = isAsleep ? sleepMix : 1 - sleepMix;
        if (mix <= 0) return null;
        return (
          <Img key={p.src} src={staticFile(`v10/plates/${p.src}`)}
               style={{ position: "absolute", left: hx + p.dx, top: hy + p.dy,
                        width: p.width, height: p.height,
                        marginLeft: -p.width / 2, marginTop: -p.height / 2,
                        opacity: fadeIn * mix }} />
        );
      })}

      {running && !gone && (
        <AIMark cx={rx} cy={ry} size={pl.size * S}
                color={crossed ? DONE : missing ? FAIL : TEAL} />
      )}

      {(pl.cps as { n: number; route: string; u: number }[]).map((c, i) => {
        const [lx, ly] = beside(c.route, c.u, pl.num_d);
        const st = state[c.n];
        return (
          <div key={c.n} style={{
            position: "absolute", left: lx, top: ly, transform: "translate(-50%,-50%)",
            fontFamily: MONO_B, fontSize: 19 * S, fontWeight: 700, opacity: gateK(i),
            color: st === null ? "#9a9a95" : st ? DONE : FAIL,
          }}>{c.n}</div>
        );
      })}
      {/* the running tally -- confirms the count without competing with the road */}
      {(() => {
        const c = pl.counter;
        const hit = (pl.cps as { n: number }[]).filter((p) => state[p.n] === true).length;
        const all = (pl.cps as unknown[]).length;
        const k = ease(clamp01((t - pl.gates_at) / 0.4));
        if (k <= 0) return null;
        const col = hit >= all ? DONE : missing ? FAIL : TEAL;
        return (
          <div style={{
            position: "absolute", left: (c.cx - c.w / 2) * S, top: (c.cy - c.h / 2) * S,
            width: c.w * S, height: c.h * S, borderRadius: c.r * S,
            background: c.face, border: `${1.5 * S}px solid ${hit >= all ? DONE : c.edge}`,
            boxSizing: "border-box", display: "flex", alignItems: "center",
            justifyContent: "center", opacity: k,
            fontFamily: MONO_B, fontSize: c.size * S, fontWeight: 700, color: col,
            fontVariantNumeric: "tabular-nums",
            transform: `scale(${1 + 0.09 * Math.sin(clamp01((t - flashAt) / pl.flash) * Math.PI)})`,
          }}>{hit}/{all}</div>
        );
      })()}

      {flagK > 0 && (() => {
        const [lx, ly] = beside("main", pl.start_u, pl.label_d);
        return (
          <div style={{ position: "absolute", left: lx, top: ly,
                        transform: "translate(-50%,-50%)", fontFamily: MONO_B,
                        fontSize: 18 * S, letterSpacing: 1 * S, opacity: flagK,
                        color: crossed ? DONE : "#6f6f6f" }}>FINISH</div>
        );
      })()}

      {!gone && xK > 0 && (
        <svg width={XS} height={XS}
             style={{ position: "absolute", left: hx - XS / 2, top: hy - XS / 2 }}>
          {([[0, 0, XS, XS], [XS, 0, 0, XS]] as number[][]).map(([x1, y1, x2, y2], i) => (
            <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={FAIL}
                  strokeWidth={H.x_w * S} strokeLinecap="round"
                  strokeDasharray={XS * 1.42}
                  strokeDashoffset={XS * 1.42 * (1 - clamp01(xK * 2 - i))} />
          ))}
        </svg>
      )}

      {gone && ei < pl.emoji_n && (
        <Img src={staticFile(`v10/emoji/e${String(Math.max(0, ei)).padStart(2, "0")}.png`)}
             style={{ position: "absolute", left: hx, top: hy, width: EM, height: EM,
                      marginLeft: -EM / 2, marginTop: -EM / 2 }} />
      )}
    </AbsoluteFill>
  );
};


/**
 * The brand slate, on the panel that used to be the white "LOOP -cleared-" stamp.
 *
 * The series title is the hero and everything else is the entry it belongs to.
 * It began as a 21px masthead at 3.64:1 contrast, which Anandhi read as a
 * placeholder -- correctly, it was the weakest-executed thing on a card where
 * everything else was deliberate. Title first, then what the title is about:
 * the term, how it is said, what it means, and what the night cost.
 *
 * It sits mid-film rather than at the end because the last line runs into the
 * opening line and the video loops seamlessly; a card after that stops it dead.
 *
 * Set in the brand faces -- Mona Sans display, Plus Jakarta chrome, Geist Mono
 * for values. The comic keeps Lato; the moment the film speaks as the product,
 * it speaks in the product's type.
 */
const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const o = cut.outro;
  const cr = cut.credits;
  const t = frame / fps;

  // the title lands centred and alone, holds, then rises into a header
  const titleIn = ease3(clamp01(t / 0.35));
  const rise = ease3(clamp01((t - o.title_hold) / o.title_rise));
  const titleCy = o.title_cy_start + (o.title_cy - o.title_cy_start) * rise;
  const titleScale = o.title_scale_start + (1 - o.title_scale_start) * rise;
  // everything else waits for it to arrive -- the slate is not a slate if the
  // entry is already sitting under it
  const contentAt = o.title_hold + o.title_rise;
  const step = (i: number) => ease3(clamp01((t - contentAt - i * o.step) / 0.30));
  const meterK = ease3(clamp01((t - o.meter_at) / o.meter_fade));

  const run = clamp01((t - cr.appear) / cr.run);
  const eased = 1 - Math.pow(1 - run, 2.6);
  const left = t < cr.appear ? cr.start : Math.round(cr.start * (1 - eased));
  const spent = 1 - left / cr.start;
  const done = left === 0;
  const m = o.meter;
  const pop = done ? 1 + 0.09 * Math.max(0, 1 - (t - cr.appear - cr.run) / 0.3) : 1;

  const mid = (st: React.CSSProperties, body: React.ReactNode, key: string) => (
    <div key={key} style={{
      position: "absolute", left: 0, width: "100%", textAlign: "center",
      transform: "translateY(-50%)", ...st,
    }}>{body}</div>
  );

  return (
    <AbsoluteFill style={{ backgroundColor: o.bg }}>
      {/* the title. Scaled rather than resized, so the move cannot reflow. */}
      <div style={{
        position: "absolute", left: 0, width: "100%",
        top: titleCy * S, transform: `scale(${titleScale})`,
        transformOrigin: "50% 0%", opacity: titleIn,
      }}>
        {(o.title as string[]).map((line, i) => (
          <div key={i} style={{
            position: "absolute", left: 0, width: "100%", textAlign: "center",
            top: i * o.title_line * S, transform: "translateY(-50%)",
            fontFamily: DISPLAY, fontSize: o.title_size * S, fontWeight: 800,
            letterSpacing: -1 * S, lineHeight: 1, color: o.title_color,
          }}>{line}</div>
        ))}
      </div>

      <div style={{
        position: "absolute", left: `${50 - (o.rule_w / 720) * 50}%`,
        top: o.rule_cy * S, width: `${(o.rule_w / 720) * 100}%`,
        height: 2 * S, background: TEAL, opacity: step(0),
      }} />

      {/* the entry it belongs to */}
      {mid({ top: o.term_cy * S, fontFamily: DISPLAY, fontSize: o.term_size * S,
             fontWeight: 800, letterSpacing: -1.6 * S, color: "#F2F2EF",
             opacity: step(1) }, o.term, "term")}
      {mid({ top: o.pron_cy * S, fontFamily: MONO_B, fontSize: o.pron_size * S,
             letterSpacing: 1.4 * S, color: "#7E7E86",
             opacity: step(2) }, o.pron, "pron")}
      {(o.defn as string[]).map((line, i) =>
        mid({ top: (o.defn_cy + i * o.defn_line) * S, fontFamily: LABEL,
              fontSize: o.defn_size * S, fontWeight: 500, color: "#E4E4DF",
              opacity: step(3 + i) }, line, `d${i}`)
      )}

      {/* and what the night cost */}
      <div style={{
        position: "absolute", left: (m.cx - m.w / 2) * S, top: (m.cy - m.h / 2) * S,
        width: m.w * S, height: m.h * S, borderRadius: m.r * S,
        background: m.face, border: `${1.5 * S}px solid ${m.edge}`,
        boxSizing: "border-box", opacity: meterK,
      }} />
      {mid({ top: (m.cy + m.label_dy) * S, fontFamily: LABEL,
             fontSize: m.label_size * S, fontWeight: 500, letterSpacing: 3 * S,
             color: "#7E7E86", opacity: meterK }, m.label, "ml")}
      <div style={{
        position: "absolute", left: (m.cx - m.bar_w / 2) * S,
        top: (m.cy + m.bar_dy) * S, transform: "translateY(-50%)",
        width: m.bar_w * S, height: m.bar_h * S,
        borderRadius: (m.bar_h / 2) * S, background: m.track,
        overflow: "hidden", opacity: meterK,
      }}>
        {/* fill anchored LEFT so it empties the way a gauge empties */}
        <div style={{
          position: "absolute", left: 0, top: 0, bottom: 0,
          width: `${Math.max(0, 1 - spent) * 100}%`,
          background: done ? FAIL : TEAL, borderRadius: (m.bar_h / 2) * S,
        }} />
      </div>
      {mid({ top: (m.cy + m.num_dy) * S, fontFamily: MONO_B,
             fontSize: m.num_size * S, fontWeight: 700,
             color: done ? FAIL : "#F2F2EF", fontVariantNumeric: "tabular-nums",
             transform: `translateY(-50%) scale(${pop})`, opacity: meterK },
           left.toLocaleString("en-US"), "mn")}
    </AbsoluteFill>
  );
};

export const LoopV10: React.FC = () => {
  const { fps } = useVideoConfig();
  const f = (sec: number) => Math.round(sec * fps);
  const f2 = f;
  const a = cut.ambience;

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      <style>{FONT}</style>

      {/* Panels. Hard cuts throughout -- consecutive panels continuing the same
          layout must never cross-fade.

          Each panel mounts PRELOAD_FRAMES early at zero opacity so the browser
          has decoded the plate before the cut lands. Without it, Studio playback
          shows one white frame at each cut while the image decodes -- the render
          is unaffected, but it makes the cut unreviewable. */}
      {cut.panels.map((p, i) => {
        const start = f(p.at);
        const end = f(p.until);
        const pre = Math.min(PRELOAD_FRAMES, i === 0 ? 0 : start - f(cut.panels[i - 1].at));
        const push = (p as { push_at?: number }).push_at;
        return (
          <Sequence
            key={`p${i}`}
            from={start - pre}
            durationInFrames={Math.max(1, end - start + pre)}
          >
            <Plate
              src={p.plate}
              visibleFrom={pre}
              bg={(p as { bg?: string }).bg}
              pushFrom={push === undefined ? undefined : f(push) - (start - pre)}
            />
          </Sequence>
        );
      })}

      {cut.holdCaptions.map((h, i) => (
        <Sequence key={`h${i}`} from={f(h.at)} durationInFrames={f(h.until) - f(h.at)}>
          <HoldCaption h={h} />
        </Sequence>
      ))}

      <Sequence
        from={f(cut.screen.at)}
        durationInFrames={f(cut.screen.until) - f(cut.screen.at)}
      >
        <Ring />
      </Sequence>

      <Sequence
        from={f(cut.plain.at)}
        durationInFrames={f(cut.plain.until) - f(cut.plain.at)}
      >
        <Plain />
      </Sequence>

      <Sequence
        from={f(cut.outro.at)}
        durationInFrames={f(cut.outro.until) - f(cut.outro.at)}
      >
        <Outro />
      </Sequence>

      {cut.aiMark.frames.map((f, i) => (
        <Sequence key={`m${i}`} from={f2(f.at)} durationInFrames={f2(f.until) - f2(f.at)}>
          <MarkOnScreen f={f} />
        </Sequence>
      ))}

      {cut.sfx.map((x, i) => (
        <Sfx key={`s${i}`} s={x} />
      ))}

      {cut.captions.map((c, i) => (
        <Sequence
          key={`c${i}`}
          from={f(c.at)}
          durationInFrames={Math.max(1, f(c.until) - f(c.at))}
        >
          <Caption c={c} />
        </Sequence>
      ))}

      {/* Each VO / SFX slice sits at its own absolute time, sliced out of the
          original block -- no line was ever re-rendered. */}
      {cut.audio.map((clip, i) => (
        <Sequence key={`a${i}`} from={f(clip.at)}>
          <Audio
            src={staticFile(`v10/audio/${clip.src}`)}
            startFrom={f(clip.startFrom)}
            endAt={f(clip.endAt)}
            volume={(clip as { gain?: number }).gain ?? 1}
          />
        </Sequence>
      ))}

      {/* Ambience. Compression and the printer duck are baked into the file;
          only the envelope lives here, because that is what follows the edit.
          It drops to nothing for the dark-room beat -- silence is what sells
          "everyone has gone home". */}
      <Audio
        src={staticFile(`v10/audio/${a.src}`)}
        volume={(fr) => {
          const t = fr / fps;
          if (t < a.lead) return t / a.lead;
          if (t < a.out_at) return 1;
          if (t < a.out_at + a.out_dur) return (a.out_at + a.out_dur - t) / a.out_dur;
          if (t < a.in_at) return 0;
          if (t < a.in_at + a.in_dur) return (t - a.in_at) / a.in_dur;
          if (t < a.end - a.tail) return 1;
          return Math.max(0, (a.end - t) / a.tail);
        }}
      />
    </AbsoluteFill>
  );
};
