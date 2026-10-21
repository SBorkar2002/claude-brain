import React from "react";
import {interpolate, spring} from "remotion";

/**
 * The two educational screens: the hook, and the skill.
 *
 * Design is the `exp-hook-*` / `exp-skill-*` frames on the Figma /insights page;
 * it is drawn here rather than exported so it can MOVE — nothing switches on,
 * everything eases to a resting position.
 *
 * Every event is timed to the word it illustrates (times measured off the AI's
 * own envelope, not whisper's):
 *   hook   1.00 "Tests run"   2.35/2.95 the passes   3.70 "shows up" -> the cross
 *   skill  2.27 "five steps"  3.13 "one command"     4.93 "read the error"
 *
 * Colour is narrow and does real work: teal = passed, coral = failed and it
 * appears exactly ONCE in the whole film, grey = waiting.
 */

const INK = "#17171A";
const GREY = "#9E9EA2";
const TEAL = "#03A6CF";
const CORAL = "#FF6B6B";
const GREEN = "#2E9E4F";
const FONT = "'GeistMono',ui-monospace,Menlo,monospace";

// eased 0->1 over `dur` starting at `at`, decelerating to rest
const ramp = (t: number, at: number, dur = 0.34) =>
  interpolate(t, [at, at + dur], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp",
    easing: (x) => 1 - Math.pow(1 - x, 3)});

const Tick: React.FC<{k: number; color: string}> = ({k, color}) => (
  <svg width={30} height={24} viewBox="0 0 30 24" style={{overflow: "visible"}}>
    <path d="M 1 12 L 9 20 L 27 2" fill="none" stroke={color} strokeWidth={5}
      strokeLinecap="round" strokeLinejoin="round"
      strokeDasharray={44} strokeDashoffset={44 * (1 - k)} />
  </svg>
);

const Cross: React.FC<{k: number}> = ({k}) => (
  <svg width={26} height={26} viewBox="0 0 26 26" style={{overflow: "visible"}}>
    <path d="M 3 3 L 23 23" fill="none" stroke={CORAL} strokeWidth={5} strokeLinecap="round"
      strokeDasharray={29} strokeDashoffset={29 * (1 - Math.min(1, k * 2))} />
    <path d="M 23 3 L 3 23" fill="none" stroke={CORAL} strokeWidth={5} strokeLinecap="round"
      strokeDasharray={29} strokeDashoffset={29 * (1 - Math.max(0, k * 2 - 1))} />
  </svg>
);

const Dots: React.FC<{t: number}> = ({t}) => (
  <div style={{display: "flex", gap: 6}}>
    {[0, 1, 2].map((i) => (
      <div key={i} style={{
        width: 8, height: 8, borderRadius: 4, background: GREY,
        opacity: 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * 6 - i * 0.8)),
      }} />
    ))}
  </div>
);

const Row: React.FC<{y: number; label: string; children: React.ReactNode; k: number}> =
({y, label, children, k}) => (
  <div style={{
    position: "absolute", left: 118, top: y, width: 460,
    display: "flex", alignItems: "center", justifyContent: "space-between",
    opacity: k, transform: `translateY(${(1 - k) * 10}px)`,
  }}>
    <span style={{fontFamily: FONT, fontSize: 26, color: INK}}>{label}</span>
    <span style={{display: "flex", alignItems: "center"}}>{children}</span>
  </div>
);

export const HookScreen: React.FC<{t: number; fps: number}> = ({t, fps}) => {
  const head = ramp(t, 0.15);
  // rows arrive on "Tests run", the passes while he says "after every",
  // and the failure lands on "edit" -- the whole line is only 3.4s now
  const rows = [0, 1, 2].map((i) => ramp(t, 1.78 + i * 0.10));
  const p1 = ramp(t, 2.30, 0.26);
  const p2 = ramp(t, 2.62, 0.26);
  const failK = spring({frame: Math.max(0, Math.round((t - 3.00) * fps)), fps,
    config: {damping: 14, mass: 0.6}, durationInFrames: Math.round(0.45 * fps)});
  return (
    <>
      <div style={{position: "absolute", left: 90, top: 570, width: 26, height: 32,
        border: `3px solid ${INK}`, borderRadius: 3, opacity: head}} />
      <div style={{position: "absolute", left: 134, top: 566, fontFamily: FONT,
        fontSize: 30, color: INK, opacity: head}}>auth.ts</div>
      <Row y={700} label="login" k={rows[0]}>
        {p1 > 0 ? <Tick k={p1} color={TEAL} /> : <Dots t={t} />}
      </Row>
      <Row y={750} label="logout" k={rows[1]}>
        {p2 > 0 ? <Tick k={p2} color={TEAL} /> : <Dots t={t} />}
      </Row>
      <Row y={800} label="session" k={rows[2]}>
        {failK > 0.001 ? <Cross k={failK} /> : <Dots t={t} />}
      </Row>
    </>
  );
};

export const SkillScreen: React.FC<{t: number; fps: number}> = ({t, fps}) => {
  const head = ramp(t, 0.15);
  // one staggered pop-in landing on "five steps", not five separate arrivals
  // the five pop in ON "Five steps", the command lands ON "One command"
  const pop = (i: number) => spring({frame: Math.max(0, Math.round((t - (1.92 + i * 0.06)) * fps)),
    fps, config: {damping: 15, mass: 0.5}, durationInFrames: Math.round(0.4 * fps)});
  const cmd = ramp(t, 2.72, 0.28);
  // the "four of them are read the error" line is gone, so the gang-up goes
  // with it -- the four identical icons still make the point on their own
  const gang = 1;
  return (
    <>
      <div style={{position: "absolute", left: 90, top: 556, fontFamily: FONT,
        fontSize: 28, color: GREY, opacity: head}}>debug.md</div>
      <div style={{position: "absolute", left: 90, top: 596, display: "flex",
        alignItems: "center", gap: 10, opacity: cmd, transform: `translateY(${(1 - cmd) * 8}px)`}}>
        <svg width={14} height={20}><path d="M 1 1 L 11 10 L 1 19" fill="none"
          stroke={TEAL} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" /></svg>
        <span style={{fontFamily: FONT, fontSize: 34, color: TEAL}}>/debug</span>
      </div>
      {[0, 1, 2, 3, 4].map((i) => {
        const k = pop(i);
        const four = i < 4;
        return (
          <div key={i} style={{
            position: "absolute", left: 120, top: 672 + i * 44,
            display: "flex", alignItems: "center", gap: 14,
            opacity: k, transform: `translateY(${(1 - k) * 12}px)`,
          }}>
            {four ? (
              <svg width={20} height={20}>
                <circle cx={8} cy={8} r={7} fill="none"
                  stroke={interpolateColor(gang)} strokeWidth={3} />
                <path d="M 13 13 L 19 19" stroke={interpolateColor(gang)} strokeWidth={3}
                  strokeLinecap="round" />
              </svg>
            ) : (
              <svg width={20} height={20}><path d="M 1 9 L 7 15 L 19 2" fill="none"
                stroke={INK} strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round" /></svg>
            )}
            <span style={{fontFamily: FONT, fontSize: 25,
              color: four ? interpolateColor(gang) : INK}}>
              {four ? "read the error" : "fix it"}
            </span>
          </div>
        );
      })}
    </>
  );
};


/* ---- WHERE THINGS GO WRONG -------------------------------------------------
   Two columns. The machine indicts ITSELF first and only then turns to him,
   which is what the real report does and what stops this reading as a roast.
   phase "mine": only the left fills.  phase "yours": the right fills too. */
const COLW = 300;
const LX = 52, RX = 372, HEAD = 566, BODY = 610;

const ColHead: React.FC<{x: number; label: string; k: number}> = ({x, label, k}) => (
  <div style={{position: "absolute", left: x, top: HEAD, width: COLW, textAlign: "center",
    fontFamily: FONT, fontSize: 21, letterSpacing: 2, color: INK, opacity: k}}>
    {label}
    <div style={{height: 2, background: GREY, marginTop: 8, opacity: 0.6}} />
  </div>
);

export const WrongScreen: React.FC<{t: number; fps: number; phase: string}> = ({t, fps, phase}) => {
  const mine = phase === "mine";
  const heads = ramp(t, mine ? 0.15 : 0, 0.3);
  // LEFT -- a counter running up to 38. One moving part, and it is countable.
  const cK = mine ? ramp(t, 1.15, 1.5) : 1;
  const count = Math.round(38 * cK);
  // RIGHT -- nine failing tests; seven delete themselves; he asks for ones that pass
  const born = (i: number) => mine ? 0 : spring({
    frame: Math.max(0, Math.round((t - (1.30 + i * 0.045)) * fps)), fps,
    config: {damping: 15, mass: 0.5}, durationInFrames: Math.round(0.4 * fps)});
  const gone = (i: number) => (!mine && i < 7) ? ramp(t, 3.55 + i * 0.08, 0.2) : 0;
  const wrote = (i: number) => (!mine && i < 7) ? ramp(t, 5.55 + i * 0.06, 0.26) : 0;
  const cell = (i: number) => ({x: RX + 44 + (i % 3) * 72, y: BODY + 30 + Math.floor(i / 3) * 66});
  return (
    <>
      <ColHead x={LX} label="ON MY SIDE" k={heads} />
      <ColHead x={RX} label="ON YOURS" k={mine ? ramp(t, 0.45, 0.3) * 0.35 : 1} />

      <div style={{position: "absolute", left: LX, top: BODY + 46, width: COLW,
        textAlign: "center", fontFamily: FONT, fontSize: 64, color: CORAL, opacity: heads}}>
        {count}
      </div>
      <div style={{position: "absolute", left: LX, top: BODY + 126, width: COLW,
        textAlign: "center", fontFamily: FONT, fontSize: 20, color: GREY, opacity: heads}}>
        wrong approach
      </div>

      {Array.from({length: 9}).map((_, i) => {
        const {x, y} = cell(i);
        const b = born(i), g = gone(i), w = wrote(i);
        if (b <= 0 && w <= 0) return null;
        return (
          <React.Fragment key={i}>
            <div style={{position: "absolute", left: x, top: y, width: 48, height: 48,
              border: `3px solid ${CORAL}`, borderRadius: 7,
              opacity: b * (1 - g), transform: `scale(${(0.6 + 0.4 * b) * (1 - 0.35 * g)})`,
              display: "flex", alignItems: "center", justifyContent: "center"}}>
              <svg width={20} height={20}><path d="M 3 3 L 17 17 M 17 3 L 3 17" fill="none"
                stroke={CORAL} strokeWidth={4} strokeLinecap="round" /></svg>
            </div>
            {w > 0 ? (
              <div style={{position: "absolute", left: x, top: y, width: 48, height: 48,
                border: `3px solid ${TEAL}`, borderRadius: 7, opacity: w,
                transform: `scale(${0.7 + 0.3 * w})`,
                display: "flex", alignItems: "center", justifyContent: "center"}}>
                <svg width={22} height={18}><path d="M 2 9 L 7 14 L 20 2" fill="none"
                  stroke={TEAL} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" /></svg>
              </div>
            ) : null}
          </React.Fragment>
        );
      })}
    </>
  );
};

/* ---- THE SUGGESTION --------------------------------------------------------
   Mohit's note: a viewer has to be able to DO this. So the card names the file,
   shows the exact line, and offers the button. Nothing is described. */
export const AgentsScreen: React.FC<{t: number; fps: number}> = ({t, fps}) => {
  // nothing is on the screen while it says "I can't pick for you" -- the card
  // arrives with the sentence that actually names the file
  const head = ramp(t, 3.35, 0.3);
  const line = spring({frame: Math.max(0, Math.round((t - 3.55) * fps)), fps,
    config: {damping: 16, mass: 0.6}, durationInFrames: Math.round(0.45 * fps)});
  const why = ramp(t, 5.9, 0.3);
  return (
    <>
      <div style={{position: "absolute", left: 41, top: 552, width: 637, textAlign: "center",
        fontFamily: FONT, fontSize: 21, letterSpacing: 2, color: INK, opacity: head}}>
        SUGGESTED agents.md ADDITION
      </div>
      <div style={{position: "absolute", left: 82, top: 626, width: 470,
        border: `3px solid ${INK}`, borderRadius: 8, padding: "16px 18px",
        fontFamily: FONT, fontSize: 22, lineHeight: 1.45, color: INK,
        opacity: line, transform: `translateY(${(1 - line) * 12}px)`, boxSizing: "border-box"}}>
        When he says whatever, ask which approach before starting.
      </div>
      <div style={{position: "absolute", left: 566, top: 640, padding: "10px 16px",
        border: `3px solid ${TEAL}`, borderRadius: 8, fontFamily: FONT, fontSize: 20,
        color: TEAL, opacity: line}}>Copy</div>
      <div style={{position: "absolute", left: 82, top: 764, width: 470,
        fontFamily: FONT, fontSize: 19, color: GREY, opacity: why}}>why: 41 sessions</div>
    </>
  );
};

/* ---- WHAT'S HINDERING YOU --------------------------------------------------
   He asks for a summary, never opens it, and the machine reads the original
   twice. The countable thing is the read counter going 1 -> 2. */
export const HinderScreen: React.FC<{t: number; fps: number}> = ({t, fps}) => {
  /* centred in the screen: doc 108 + gap 66 + summary 100 = 274 wide,
     so it starts at 41 + (637-274)/2 */
  const DOC = 222, SUM = 396;
  const doc = ramp(t, 0.15);
  const sum = spring({frame: Math.max(0, Math.round((t - 0.65) * fps)), fps,
    config: {damping: 15, mass: 0.5}, durationInFrames: Math.round(0.4 * fps)});
  const unread = ramp(t, 3.40, 0.3);
  // the arc back was over before you could see it. The counter POPS instead --
  // one thing moving, and it is the thing that carries the point.
  const again = spring({frame: Math.max(0, Math.round((t - 3.95) * fps)), fps,
    config: {damping: 11, mass: 0.7}, durationInFrames: Math.round(0.55 * fps)});
  const lines = (n: number, w: number) => Array.from({length: n}).map((_, i) => (
    <div key={i} style={{width: w - i * 6, height: 4, borderRadius: 2,
      background: GREY, marginBottom: 7}} />
  ));
  return (
    <>
      <div style={{position: "absolute", left: DOC, top: 618, width: 108, height: 140,
        border: `3px solid ${INK}`, borderRadius: 6, padding: "14px 12px",
        opacity: doc, boxSizing: "border-box"}}>{lines(6, 80)}</div>
      <div style={{position: "absolute", left: DOC - 30, top: 772, width: 168,
        textAlign: "center", fontFamily: FONT,
        fontSize: 20 + 16 * Math.min(1, again), fontWeight: 700,
        color: again > 0.15 ? CORAL : GREY, opacity: doc,
        transform: `scale(${1 + 0.18 * Math.sin(Math.min(1, again) * Math.PI)})`}}>
        read {again > 0.15 ? "\u00d72" : "\u00d71"}
      </div>

      <div style={{position: "absolute", left: DOC + 118, top: 660, width: 46, height: 3,
        background: GREY, opacity: sum}} />
      <div style={{position: "absolute", left: SUM, top: 640, width: 100, height: 76,
        border: `3px solid ${unread > 0.5 ? GREY : INK}`, borderRadius: 6, padding: "12px 12px",
        opacity: sum * (1 - 0.45 * unread), boxSizing: "border-box"}}>{lines(3, 70)}</div>
      <div style={{position: "absolute", left: SUM, top: 640, width: 100, height: 76,
        opacity: unread, display: "flex", alignItems: "center", justifyContent: "center"}}>
        <svg width={100} height={76}><path d="M 12 12 L 88 64" stroke={GREY} strokeWidth={4}
          strokeLinecap="round" fill="none" /></svg>
      </div>
      <div style={{position: "absolute", left: SUM - 10, top: 726, width: 120, textAlign: "center",
        fontFamily: FONT, fontSize: 19, color: GREY, opacity: unread}}>unopened</div>
    </>
  );
};

/* ---- ON THE HORIZON -------------------------------------------------------
   The same ring loop does the whole sentence: run, fail, fix, run, green.
   Three laps, not five -- the beat that teaches is the CHECK, not the travel,
   and five reads as frantic with no room to see the check land. */
export const HorizonScreen: React.FC<{t: number; fps: number}> = ({t, fps}) => {
  const R = 74, CX = 359, CY = 742;
  const start = 0.75, lap = 0.85;
  const laps = Math.max(0, (t - start) / lap);
  const done = Math.floor(laps);
  const k = Math.min(3, laps);
  // eased so it lands on a whole lap instead of stopping mid-travel
  const ang = -Math.PI / 2 + 2 * Math.PI * (k >= 3 ? 3 : k);
  const green = t > start + lap * 3;
  const col = green ? GREEN : (done >= 1 ? CORAL : GREY);
  const dot = {x: CX + R * Math.cos(ang), y: CY + R * Math.sin(ang)};
  const appear = ramp(t, 0.2, 0.3);
  return (
    <>
      <svg width={637} height={300} style={{position: "absolute", left: 41, top: CY - 150 - 0}}>
        <circle cx={318} cy={150} r={R} fill="none" stroke={GREY} strokeWidth={5}
          opacity={0.35 * appear} />
        <circle cx={318} cy={150} r={R} fill="none" stroke={col} strokeWidth={5}
          strokeLinecap="round" opacity={appear}
          strokeDasharray={2 * Math.PI * R}
          strokeDashoffset={2 * Math.PI * R * (1 - Math.min(1, k >= 3 ? 1 : k % 1))}
          transform={`rotate(-90 318 150)`} />
        {green ? (
          <path d="M 300 150 L 313 163 L 340 134" fill="none" stroke={GREEN} strokeWidth={7}
            strokeLinecap="round" strokeLinejoin="round" />
        ) : (
          <circle cx={318 + R * Math.cos(ang)} cy={150 + R * Math.sin(ang)} r={9}
            fill={col} opacity={appear} />
        )}
      </svg>
      <div style={{position: "absolute", left: 41, top: CY + 108, width: 637, textAlign: "center",
        fontFamily: FONT, fontSize: 22, color: green ? GREEN : GREY, opacity: appear}}>
        {green ? "green" : done >= 1 ? "fix \u00b7 run again" : "run"}
      </div>
    </>
  );
};

/* every explainer screen carries its section title at the TOP, inside the
   screen, so the visual below it has the room to do the work */
export const ScreenTitle: React.FC<{t: string; k: number}> = ({t, k}) => (
  <div style={{position: "absolute", left: 41, top: 552, width: 637, textAlign: "center",
    fontFamily: FONT, fontSize: 23, letterSpacing: 2.5, color: INK, opacity: k}}>{t}</div>
);

// grey -> ink as the line owns up to it
function interpolateColor(k: number) {
  const a = [158, 158, 162], b = [23, 23, 26];
  const c = a.map((v, i) => Math.round(v + (b[i] - v) * k));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
