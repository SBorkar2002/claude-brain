import React from "react";
import { AbsoluteFill, useCurrentFrame, staticFile } from "remotion";

/**
 * EP002 explainer visuals — the three doors, animated.
 *
 * Built from the Figma storyboard DOOR D1..D5 (page "graph", node 585:2).
 * The metaphor in one line: an ID badge is a door pass. Two of the four jobs
 * were wearing a pass for a door of their own, and queued at the shared one
 * all night anyway.
 *
 * Beats are timed to David's actual word timings, not to the panel start.
 * Everything is drawn in 720-space and scaled up, matching GraphV1.
 */

const FPS = 30;
const S = 1.5;
const TEAL = "#03A6CF";
const CORAL = "#FF6B6B";
const INK = "#121212";
const DIM = "#A8A8A8";
const PALE = "#E4E4E4";
const CAP = "'LatoLocal','Helvetica Neue',Arial,sans-serif";

const ease = (x: number) => 1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 3);
const at = (t: number, a: number, dur = 0.35) => ease((t - a) / dur);
const mix = (a: number, b: number, k: number) => a + (b - a) * k;
/** blend two hex colours — lets a figure grey out gradually instead of snapping */
const mixHex = (a: string, b: string, k: number) => {
  const p = (h: string) => [1,3,5].map(i => parseInt(h.slice(i,i+2),16));
  const [r1,g1,b1] = p(a), [r2,g2,b2] = p(b);
  const c = (x: number, y: number) => Math.round(mix(x,y,Math.max(0,Math.min(1,k)))).toString(16).padStart(2,"0");
  return `#${c(r1,r2)}${c(g1,g2)}${c(b1,b2)}`;
};

// ---------------------------------------------------------------- primitives
/** A doorway. Every door is titled — the colour doors say why they are empty. */
const DOOR_W = 150, DOOR_TOP = 280, FLOOR = 590;
const Door: React.FC<{ x: number; color: string; title: string; pass?: boolean; open?: number; stamp?: string; stampK?: number }> =
({ x, color, title, pass, open = 0, stamp, stampK = 1 }) => {
  const H = FLOOR - DOOR_TOP;
  return (
    <>
      {pass && (
        <div style={{
          position: "absolute", left: (x + DOOR_W / 2 - 34) * S, top: 196 * S, width: 68 * S, height: 24 * S,
          background: color, borderRadius: 5 * S,
        }} />
      )}
      <div style={{
        position: "absolute", left: (x - 45) * S, top: 232 * S, width: (DOOR_W + 90) * S, textAlign: "center",
        fontFamily: CAP, fontWeight: 800, fontSize: 19 * S, letterSpacing: 1.3 * S, color,
      }}>{title}</div>
      {/* the dark doorway behind the panel — this is what "open" looks like */}
      <div style={{
        position: "absolute", left: (x + 5) * S, top: (DOOR_TOP + 5) * S,
        width: (DOOR_W - 10) * S, height: (H - 5) * S, background: "#2B2B31",
      }} />
      {/* the panel sweeps across the opening as the door shuts */}
      <div style={{
        position: "absolute", left: (x + 5) * S, top: (DOOR_TOP + 5) * S,
        width: (DOOR_W - 10) * (1 - open) * S, height: (H - 5) * S, overflow: "hidden",
      }}>
        <div style={{
          position: "absolute", left: 0, top: 0,
          width: (DOOR_W - 10) * S, height: (H - 5) * S, background: "#F0F0F0",
        }} />
        <div style={{
          position: "absolute", left: 27 * S, top: 31 * S, width: 86 * S, height: 112 * S,
          border: `${2 * S}px solid rgba(0,0,0,0.16)`, borderRadius: 3 * S, boxSizing: "border-box",
        }} />
        <div style={{
          position: "absolute", left: 27 * S, top: 161 * S, width: 86 * S, height: 112 * S,
          border: `${2 * S}px solid rgba(0,0,0,0.16)`, borderRadius: 3 * S, boxSizing: "border-box",
        }} />
        <div style={{
          position: "absolute", left: (DOOR_W - 35) * S, top: 143 * S,
          width: 13 * S, height: 13 * S, borderRadius: "50%", background: color,
        }} />
        {stamp && stampK > 0 && (
          <div style={{
            position: "absolute", left: 16 * S, top: 56 * S, width: 118 * S, height: 40 * S,
            border: `${3.5 * S}px solid ${color}`, borderRadius: 4 * S,
            background: "rgba(255,255,255,0.35)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontFamily: CAP, fontWeight: 800, fontSize: 20 * S, letterSpacing: 2 * S, color,
            // comes down like a stamp: oversized, then presses to size
            transform: `rotate(-8deg) scale(${1 + 0.75 * (1 - stampK)})`,
            opacity: 0.92 * Math.min(1, stampK * 2.2),
          }}>{stamp}</div>
        )}
      </div>
      {/* the jamb runs to the floor — a door that floats reads as a picture frame */}
      <div style={{
        position: "absolute", left: x * S, top: DOOR_TOP * S, width: DOOR_W * S, height: H * S,
        border: `${5 * S}px solid ${color}`, borderBottom: "none",
        borderTopLeftRadius: 5 * S, borderTopRightRadius: 5 * S, boxSizing: "border-box",
      }} />
    </>
  );
};

/** blank silhouette wearing a lanyard ID; colour = has a pass of their own */
const Person: React.FC<{
  cx: number; y: number; label: string; color?: string | null;
  op?: number; grey?: number; catK?: number; catSince?: number; k?: number;
}> = ({ cx, y, label, color = null, op = 1, grey = 0, catK = 0, catSince = 0, k = 1 }) => {
  const stroke = mixHex(INK, DIM, grey);
  const tone = color ? color : stroke;
  const border = `${4 * S}px solid ${tone}`;
  const f = useCurrentFrame();
  const ci = Math.max(0, Math.floor((f / FPS - catSince) * CAT_FPS)) % CAT_FRAMES;
  return (
    <div style={{
      position: "absolute", left: 0, top: 0, opacity: op,
      transform: `scale(${k})`, transformOrigin: `${cx * S}px ${y * S}px`,
    }}>
      {/* the cat takes their place once the door is shut — same footprint */}
      {catK > 0 && (
        <img src={staticFile(`v10/graph/cat/c_${String(ci).padStart(3, "0")}.png`)}
          style={{
            position: "absolute", left: (cx - 56) * S, top: (y - 6) * S,
            width: 112 * S, height: 140 * S, opacity: catK,
            transform: `scale(${0.88 + 0.12 * catK})`, transformOrigin: "50% 100%",
          }} />
      )}
      <div style={{
        position: "absolute", left: (cx - 26) * S, top: y * S, width: 52 * S, height: 52 * S,
        border, borderRadius: "50%", background: "#fff", boxSizing: "border-box",
        opacity: 1 - catK,
      }} />
      <div style={{
        position: "absolute", left: (cx - 50) * S, top: (y + 50) * S, width: 100 * S, height: 84 * S,
        border, borderRadius: `${50 * S}px ${50 * S}px ${10 * S}px ${10 * S}px`,
        background: "#fff", boxSizing: "border-box", opacity: 1 - catK,
      }} />
      <div style={{ position: "absolute", left: (cx - 16) * S, top: (y + 52) * S, width: 6 * S, height: 26 * S, background: tone, opacity: 1 - catK }} />
      <div style={{ position: "absolute", left: (cx + 12) * S, top: (y + 52) * S, width: 6 * S, height: 26 * S, background: tone, opacity: 1 - catK }} />
      <div style={{
        position: "absolute", left: (cx - 56) * S, top: (y + 76 + 66 * catK) * S, width: 112 * S, height: 34 * S,
        background: color ? color : "#fff", border: `${3 * S}px solid ${tone}`,
        borderRadius: 6 * S, boxSizing: "border-box",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: CAP, fontWeight: 800, fontSize: (label.length > 6 ? 13 : 16) * S,
        color: color ? "#fff" : tone,
      }}>{label}</div>
    </div>
  );
};

/** the square bracket that says "this one really is stuck behind that one".
    `draw` grows it once; `op` fades it. Never scale height to fade — that is
    what made it look like it was snapping in half. */
const Tether: React.FC<{ x: number; yTop: number; yBot: number; draw: number; op?: number }> =
({ x, yTop, yBot, draw, op = 1 }) => (
  <div style={{ opacity: op }}>
    <div style={{ position: "absolute", left: x * S, top: yTop * S, width: 5 * S, height: (yBot - yTop) * draw * S, background: INK }} />
    <div style={{ position: "absolute", left: x * S, top: yTop * S, width: 20 * S, height: 5 * S, background: INK }} />
    <div style={{ position: "absolute", left: x * S, top: (yBot - 5) * S, width: 20 * S, height: 5 * S, background: INK, opacity: draw > 0.9 ? 1 : 0 }} />
  </div>
);

const Stamp: React.FC<{ t: string; x: number; y: number; w: number; k: number; size?: number; color?: string }> =
({ t, x, y, w, k, size = 26, color = INK }) => (
  <div style={{
    position: "absolute", left: x * S, top: y * S, width: w * S, textAlign: "center",
    fontFamily: CAP, fontWeight: 800, fontSize: size * S, letterSpacing: 1.6 * S, color,
    opacity: k, transform: `scale(${0.9 + 0.1 * k})`, transformOrigin: "50% 50%",
  }}>{t}</div>
);

/** the waiting-room cat: green screen keyed out, watermark cropped, 120 frames */
const CAT_FRAMES = 120, CAT_FPS = 50 / 3;

/** The reason the shared queue crawls: everyone through ALL ENTRY gets checked,
    one at a time. A pass door just opens. The arch sits behind the figure; the
    beam passes OVER it, because that is what a scanner does. */
const CHK_TOP = 646, CHK_H = 150;
const CheckArch: React.FC<{ cx: number; k: number }> = ({ cx, k }) => (
  <div style={{
    position: "absolute", left: (cx - 62) * S, top: CHK_TOP * S, width: 124 * S, height: CHK_H * S,
    border: `${4 * S}px solid ${INK}`, borderBottom: "none",
    borderTopLeftRadius: 10 * S, borderTopRightRadius: 10 * S, boxSizing: "border-box",
    opacity: k * 0.55,
  }} />
);
const ScanBeam: React.FC<{ cx: number; k: number }> = ({ cx, k }) => {
  const t = useCurrentFrame() / FPS;
  const y = CHK_TOP + 12 + (CHK_H - 26) * (0.5 - 0.5 * Math.cos(t * 2.4));
  return (
    <>
      <div style={{
        position: "absolute", left: (cx - 56) * S, top: y * S, width: 112 * S, height: 4 * S,
        background: INK, opacity: k * 0.75,
      }} />
      <div style={{
        position: "absolute", left: (cx - 56) * S, top: (y - 7) * S, width: 112 * S, height: 18 * S,
        background: INK, opacity: k * 0.10,
      }} />
    </>
  );
};

/** SFX lettering. Every sound that plays gets its word on screen, popping on
    the sound — click, swipe, *ding*, and now *thud*. */
const SfxWord: React.FC<{ t: string; cx: number; cy: number; w: number; size: number; at: number; k?: number }> =
({ t, cx, cy, w, size, at: a, k = 1 }) => {
  const now = useCurrentFrame() / FPS;
  const e = now - a;
  if (e < 0) return null;
  const inK = Math.min(1, e / 0.05);
  const outK = 1 - Math.max(0, Math.min(1, (e - 0.7) / 0.25));
  const spike = Math.max(0, 1 - e / 0.26);
  return (
    <div style={{
      position: "absolute", left: (cx - w / 2) * S, top: cy * S, width: w * S,
      textAlign: "center", fontFamily: CAP, fontSize: size * S, color: "#1e1e1e",
      opacity: inK * outK * k, transform: `scale(${1 + 0.18 * spike})`,
      transformOrigin: "50% 50%", whiteSpace: "nowrap",
    }}>{t}</div>
  );
};

/** the wait, as a clock: hands sweep four hours while they stand there */
const WaitClock: React.FC<{ cx: number; cy: number; r: number; k: number; p: number }> =
({ cx, cy, r, k, p }) => {
  const hand = (deg: number, len: number) => {
    const a = (deg - 90) * Math.PI / 180;
    return { x2: (r + Math.cos(a) * len) * S, y2: (r + Math.sin(a) * len) * S };
  };
  const h = hand(p * 120, r * 0.46);        // four hours of hour hand
  const m = hand(p * 4 * 360, r * 0.72);    // four full sweeps of minute hand
  return (
    <svg width={r * 2 * S} height={r * 2 * S}
      style={{ position: "absolute", left: (cx - r) * S, top: (cy - r) * S, opacity: k }}>
      <circle cx={r * S} cy={r * S} r={(r - 3) * S} fill="#fff" stroke={DIM} strokeWidth={4 * S} />
      {[0, 90, 180, 270].map((d) => {
        const o = hand(d, r * 0.82), i = hand(d, r * 0.66);
        return <line key={d} x1={i.x2} y1={i.y2} x2={o.x2} y2={o.y2} stroke={DIM} strokeWidth={3 * S} strokeLinecap="round" />;
      })}
      <line x1={r * S} y1={r * S} x2={h.x2} y2={h.y2} stroke={INK} strokeWidth={4.5 * S} strokeLinecap="round" />
      <line x1={r * S} y1={r * S} x2={m.x2} y2={m.y2} stroke={INK} strokeWidth={3 * S} strokeLinecap="round" />
      <circle cx={r * S} cy={r * S} r={3.5 * S} fill={INK} />
    </svg>
  );
};

const DX = [75, 285, 495];   // centres stay at 150 / 360 / 570
const QCX = 150, GCX = [360, 570];
const QY = [668, 818, 968, 1118];   // 150 pitch; dropped to leave a sign slot above the queue
const QK = 0.85;                    // figure size, so four of them + the bar fit the frame
/** the head circle's centre — this is the point a figure turns into a dot at */
const HEAD_CY = (y: number) => Math.round(y + 26 * QK);
/** they file in one at a time before David starts, then the line stands */
export const DOORS_LEAD = 0.95;
/** The doors slam HERE, in the clear gap before David's last line. It used to
 *  land on 6.25 — the exact frame he starts "they sat in line four hours for
 *  nothing" — so a wooden knock was competing with a male voice in the same
 *  register and lost. A cue that plays under speech in its own band is a cue
 *  nobody hears, however loud you make it. */
export const DOORS_SLAM = 5.90;

const Stage: React.FC<{ colourOpen?: number; stampTeal?: number; stampCoral?: number }> =
({ colourOpen = 0, stampTeal = 0, stampCoral = 0 }) => (
  <>
    <Door x={DX[0]} color={INK} title="ALL ENTRY" open={1} />
    <Door x={DX[1]} color={TEAL} title="PASS ONLY" pass open={colourOpen} stamp="CLOSED" stampK={stampTeal} />
    <Door x={DX[2]} color={CORAL} title="PASS ONLY" pass open={colourOpen} stamp="CLOSED" stampK={stampCoral} />
    <div style={{ position: "absolute", left: 30 * S, top: FLOOR * S, width: 660 * S, height: 4 * S, background: PALE }} />
  </>
);

// ------------------------------------------------- s22 — THE REVEAL
// The four file in from off-frame first (DOORS_LEAD), and only once the line
// is standing does David start — so every beat below is measured from the
// moment the VO starts, not from the first frame of the panel.
// 0.24 "the tests needed the API first"
// 3.14 "the docs and the changelog never needed anything"  -> they WALK to their doors
// 6.18 "they sat in line four hours for nothing"
export const DoorReveal: React.FC = () => {
  const t = useCurrentFrame() / FPS - DOORS_LEAD;
  const b1 = at(t, 0.24, 0.5);            // the real dependency
  const b3 = at(t, 6.18, 0.5);            // "sat in line four hours for nothing"
  const wait = ease((t - 6.4) / 1.7);     // the clock sweeping four hours

  // --- the entrance: a queue FORMS, one at a time. The first walks all the way
  // to the front of the line and stops; the next comes in and stops behind it;
  // and so on. They all enter from the same point off the bottom of frame and
  // walk up the same column, so each one has less distance to cover than the
  // one before — which is exactly why a real queue fills up from the front.
  const ENTER_Y = 1340;                  // just off the bottom edge
  const START = [0, 0.13, 0.26, 0.39];   // they set off close behind each other
  // Smootherstep, not ease-out: zero velocity at BOTH ends, so nobody is
  // launched from a standstill or braked into place. An ease-out alone is what
  // made the line look like it was being dealt out card by card.
  const smooth = (x: number) => {
    const c = Math.max(0, Math.min(1, x));
    return c * c * c * (c * (c * 6 - 15) + 10);
  };
  // a long walk and a short walk take almost as long as each other, so the
  // whole line flows in as one movement instead of four separate arrivals
  const dur = (i: number) => 0.30 + (ENTER_Y - QY[i]) / 2600;
  const entryK = (i: number) => smooth((t + DOORS_LEAD - START[i]) / dur(i));
  const enterY = (i: number) => mix(ENTER_Y, QY[i], entryK(i));
  // a soft gait: a signed sine (no cusps) inside a window that opens and shuts
  // on its own, so the bob has no first or last step to snap on
  const bob = (i: number) => {
    const k = entryK(i);
    return Math.sin(Math.PI * k) * Math.sin(k * Math.PI * 5 + i) * 5;
  };

  // they finally head for the doors that were theirs all along...
  const walkDocs = ease((t - 3.14) / 1.15);
  const walkChg  = ease((t - 3.46) / 1.15);
  // ...and the doors shut in front of them. No slide — one frame open, the
  // next frame shut, which is the same hard-cut language as the panels.
  const shut = t >= DOORS_SLAM ? 1 : 0;
  const cat  = at(t, 7.25, 0.5);
  // the stamps come down one after the other, a beat behind the slam
  const stampTeal  = at(t, DOORS_SLAM + 0.40, 0.20);
  const stampCoral = at(t, DOORS_SLAM + 0.75, 0.20);
  // API is being checked for the whole scene, so this never leaves
  const checkK = at(t, 0.0, 0.4);

  return (
    <AbsoluteFill>
      <Stage colourOpen={1 - shut} stampTeal={stampTeal} stampCoral={stampCoral} />
      <CheckArch cx={QCX} k={checkK} />

      <Person cx={QCX} y={enterY(0) - bob(0)} label="API" grey={at(t, 3.6, 0.9)} k={QK} />
      <Person cx={QCX} y={enterY(1) - bob(1)} label="TESTS" grey={at(t, 3.6, 0.9)} k={QK} />

      {/* beat 1 — one of them genuinely is stuck behind another */}
      <Tether x={20} yTop={QY[0] + 58} yBot={QY[1] + 58} draw={b1} op={b1 * (1 - at(t, 2.2, 0.45))} />
      {/* the bracket has said its piece; the sign over the checkpoint then
          explains the queue, and stays up for the rest of the scene — the
          wait never stops being the point */}
      <div style={{
        position: "absolute", left: (QCX - 130) * S, top: 600 * S, width: 260 * S,
        textAlign: "center", fontFamily: CAP, fontWeight: 800,
        fontSize: 19 * S, letterSpacing: 2.4 * S, color: DIM,
        opacity: at(t, 2.7, 0.5), whiteSpace: "nowrap",
      }}>PLEASE WAIT</div>

      {/* beat 2 — the two with their own pass leave the queue for it */}
      <Person cx={mix(QCX, GCX[0], walkDocs)} y={mix(enterY(2) - bob(2), QY[0], walkDocs)}
        label="DOCS" color={TEAL} catK={cat} catSince={DOORS_LEAD + 7.25} k={QK} />
      <Person cx={mix(QCX, GCX[1], walkChg)} y={mix(enterY(3) - bob(3), QY[0], walkChg)}
        label="CHANGELOG" color={CORAL} catK={cat} catSince={DOORS_LEAD + 7.38} k={QK} />

      {/* beat 3 — four hours, and the door closing on them */}
      {/* the doors slam together, so both words land on the one thud */}
      <SfxWord t="*thud*" cx={465} cy={372} w={62} size={16} at={DOORS_LEAD + DOORS_SLAM} />
      <SfxWord t="*thud*" cx={683} cy={372} w={62} size={16} at={DOORS_LEAD + DOORS_SLAM} />
      <ScanBeam cx={QCX} k={checkK} />
      <WaitClock cx={360} cy={1078} r={42} k={b3} p={wait} />
      <Stamp t="4h" x={210} y={1136} w={300} k={b3} size={30} color={DIM} />
    </AbsoluteFill>
  );
};

// -------------------------------------------------- s24 — THE TEACH
// Beats measured against the paused clip (a longer gap sits after "it's a
// graph" so the word has room to land).
// 0.22 "when you tell me what waits on what"
// 2.31 "it's a graph"            -> each figure becomes a dot WHERE IT STANDS
// 3.25                           -> the TESTS dot walks down to its own row
// 4.26 "dots for tasks"          -> the dots throb
// 6.03 "arrows for what depends on what"  -> the arrow draws in
// 8.86 "anything with no arrow between it runs at the same time" -> the capsule
const FREE_CX = [150, 360, 570];        // the three nothing points at
const FREE_CY = HEAD_CY(QY[0]);         // the dots land on the heads, not near them
const TESTS_START_CY = HEAD_CY(QY[1]);  // where TESTS was standing in the line
const TESTS_CY = 980;                   // dropped, so the arrow has room below the capsule
const LABEL_DY = 46;                    // dot -> label, sitting where the ID card was
const LABEL_FS = 18;
const DOT_R = 21;

// the capsule wraps the three free nodes and their labels, evenly padded
const API_LABEL_BOTTOM = FREE_CY + LABEL_DY + Math.round(LABEL_FS * 1.2);
const CAP_PAD = 30;
const CAP_CX = (FREE_CX[0] + FREE_CX[2]) / 2;
const CAP_HALF = 300;
const CAP_TOP = FREE_CY - DOT_R - CAP_PAD;
const CAP_BOTTOM = API_LABEL_BOTTOM + CAP_PAD;
const CAP_H = CAP_BOTTOM - CAP_TOP;

// the arrow starts BELOW the capsule, never inside it, with equal air at both ends
const ARROW_GAP = 22;
const HEAD_H = 18;
const TESTS_DOT_TOP = TESTS_CY - DOT_R;
const ARROW_TOP = CAP_BOTTOM + ARROW_GAP;
const SHAFT_H = (TESTS_DOT_TOP - ARROW_GAP) - HEAD_H - ARROW_TOP;

export const GraphTeach: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  const c1 = at(t, 0.22, 0.5);
  const morph = ease((t - 2.31) / 0.8);
  // The handover has to be legible: a figure becomes a dot standing exactly
  // where it stood, and only THEN does TESTS move down to its own row. Landing
  // the dots straight into the graph layout read as a cut to a different
  // picture, because nothing was in the same place twice.
  const drop = ease((t - 3.25) / 0.7);
  const testsCy = mix(TESTS_START_CY, TESTS_CY, drop);
  // the arrow is drawn when it is named, after the dot has arrived
  const arrowK = at(t, 5.95, 0.5);

  // Each noun is emphasised only while it is being said — but the oscillation is
  // enveloped in and OUT. Cutting a pulse mid-cycle snaps the element back to
  // size and reads as a glitch; a pulse must always die down, never stop dead.
  // 5.5 rad/s is a 0.57s cycle — nearly two throbs a second, which on four dots
  // at once reads as a strobe rather than emphasis. 3.4 is about one a second.
  const beat = (a: number, b: number, hz = 3.4) => {
    if (t < a || t >= b) return 0;
    const e = t - a, len = b - a;
    const env = Math.min(1, e / 0.28) * Math.min(1, (len - e) / 0.45);
    return Math.abs(Math.sin(e * hz)) * env;
  };
  const dotBeat = beat(4.20, 5.75);
  const arrowBeat = beat(5.95, 8.50);

  const capK = at(t, 8.86, 0.45);       // drawn once and held — it does not pulse
  // The arrow is drawn at ONE fixed size and moved with transforms only.
  // Animating its width / border-widths / top made the renderer re-snap those
  // hard edges to whole pixels every frame, so the shaft and the head jumped a
  // pixel back and forth — a 1px toggle on a 250px black bar, which is what
  // the flicker was. Transforms resample the layer instead of re-rasterising
  // the box, so the same motion lands smooth.
  const SHAFT_W = 7;
  const HEAD_W = 13;
  const shaftK = 1 + 0.55 * arrowBeat;
  const headK = 1 + 0.30 * arrowBeat;

  const NODES = [
    { cx: FREE_CX[0], cy: FREE_CY,  label: "API",       color: null as string | null },
    { cx: FREE_CX[1], cy: FREE_CY,  label: "DOCS",      color: TEAL },
    { cx: FREE_CX[2], cy: FREE_CY,  label: "CHANGELOG", color: CORAL },
    { cx: FREE_CX[0], cy: testsCy,  label: "TESTS",     color: null as string | null },
  ];

  return (
    <AbsoluteFill>
      <div style={{ opacity: 1 - morph }}><Stage /></div>

      {/* the four, dissolving into the picture they already understand */}
      <div style={{ opacity: 1 - morph }}>
        <Person cx={QCX} y={QY[0]} label="API" k={QK} />
        <Person cx={QCX} y={QY[1]} label="TESTS" grey={1} k={QK} />
        <Person cx={GCX[0]} y={QY[0]} label="DOCS" color={TEAL} k={QK} />
        <Person cx={GCX[1]} y={QY[0]} label="CHANGELOG" color={CORAL} k={QK} />
      </div>
      <Tether x={20} yTop={QY[0] + 58} yBot={QY[1] + 58} draw={c1} op={c1 * (1 - morph)} />

      {/* the capsule sits under the dots; static once drawn */}
      <div style={{
        position: "absolute", left: (CAP_CX - CAP_HALF) * S, top: CAP_TOP * S,
        width: CAP_HALF * 2 * S, height: CAP_H * S,
        border: `${4 * S}px dashed ${INK}`, borderRadius: (CAP_H / 2) * S, boxSizing: "border-box",
        opacity: capK * 0.9, transform: `scale(${0.95 + 0.05 * capK})`, transformOrigin: "50% 50%",
      }} />

      {/* the same four, now as a graph — each dot inherits a head's position */}
      {NODES.map((n, i) => {
        const tone = n.color ?? INK;
        return (
          <div key={i} style={{ opacity: morph }}>
            <div style={{
              position: "absolute", left: (n.cx - DOT_R) * S, top: (n.cy - DOT_R) * S,
              width: DOT_R * 2 * S, height: DOT_R * 2 * S, borderRadius: "50%", background: tone,
              transform: `scale(${(0.9 + 0.1 * morph) * (1 + 0.30 * dotBeat)})`,
              transformOrigin: "50% 50%", willChange: "transform",
            }} />
            <div style={{
              position: "absolute", left: (n.cx - DOT_R) * S, top: (n.cy - DOT_R) * S,
              width: DOT_R * 2 * S, height: DOT_R * 2 * S, borderRadius: "50%",
              border: `${3 * S}px solid ${tone}`, boxSizing: "border-box",
              opacity: dotBeat * 0.50,
              transform: `scale(${1.25 + 0.50 * dotBeat})`, transformOrigin: "50% 50%",
              willChange: "transform, opacity",
            }} />
            <div style={{
              position: "absolute", left: (n.cx - 90) * S, top: (n.cy + LABEL_DY) * S, width: 180 * S,
              textAlign: "center", fontFamily: CAP, fontWeight: 800, fontSize: LABEL_FS * S, color: tone,
            }}>{n.label}</div>
          </div>
        );
      })}

      {/* the one dependency, now an arrow — drawn on the word, then thickened.
          Fixed boxes; every change below is a transform. */}
      <div style={{ opacity: morph * arrowK }}>
        <div style={{
          position: "absolute", left: (FREE_CX[0] - SHAFT_W / 2) * S, top: ARROW_TOP * S,
          width: SHAFT_W * S, height: SHAFT_H * S, background: INK,
          transform: `scaleY(${arrowK}) scaleX(${shaftK})`,
          transformOrigin: "50% 0", willChange: "transform",
        }} />
        <div style={{
          position: "absolute", left: (FREE_CX[0] - HEAD_W) * S,
          top: (ARROW_TOP + SHAFT_H) * S, width: 0, height: 0,
          borderLeft: `${HEAD_W * S}px solid transparent`,
          borderRight: `${HEAD_W * S}px solid transparent`,
          borderTop: `${HEAD_H * S}px solid ${INK}`,
          transform: `translateY(${-SHAFT_H * (1 - arrowK) * S}px) scale(${headK})`,
          transformOrigin: "50% 0", willChange: "transform",
        }} />
      </div>

      {/* the term, once, exactly where the VO defines it — nothing else */}
      <Stamp t="GRAPH" x={40} y={400} w={640} k={ease((t - 2.5) / 0.5)} size={58} />
    </AbsoluteFill>
  );
};
