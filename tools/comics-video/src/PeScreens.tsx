import React from "react";
import {Img, staticFile} from "remotion";
import {AIMark} from "./AIMark";

/**
 * prompt engineering: the screens and the one white explainer.
 *
 * Visual source: the review artifact's Script A ("Wait, What?"). The Figma board
 * draws these monitors blank with a placeholder line of text; everything inside
 * them is built here, in 720 x 1280 space, and the caller scales the stage.
 *
 * Motion language (the series bar): mask rises, wipes, draw-ons, count-ups,
 * expo-out. No bounce, no lone fades, no tilt. Every event is keyed to a word
 * time measured off the take (`ev`, seconds from the panel start).
 * Colour: teal = working / passed, coral = failed, used once (Peter's cost).
 */

export const C = {
  ink: "#17171A", muted: "#808087", soft: "#C7C7C9", hair: "#E7E7E3",
  wash: "#F4F4F2", teal: "#03A6CF", tealbg: "#E0F5FB", coral: "#FF6B6B", coralbg: "#FFEEEE", white: "#FFFFFF",
};
const LBL = "'LatoSemi','LatoLocal','Helvetica Neue',Arial,sans-serif";
const BODY = "'LatoLocal','Helvetica Neue',Arial,sans-serif";
const MONO = "'GeistMono',ui-monospace,Menlo,monospace";
const DISPLAY = "'MonaSans','LatoSemi',sans-serif";
const SHADOW = "0 1px 2px rgba(18,18,26,.06), 0 14px 36px -6px rgba(18,18,26,.10)";
export const SCR = {x: 41, y: 528, w: 638, h: 371};

type Ev = Record<string, number>;

/* ------------------------------------------------------------------ easing */
const clamp = (x: number) => Math.max(0, Math.min(1, x));
const expoOut = (x: number) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x));
const quartInOut = (x: number) => (x < 0.5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2);
export const k = (t: number, at: number | null | undefined, dur = 0.45, ease = expoOut) =>
  at == null ? 0 : ease(clamp((t - at) / dur));
const lerp = (a: number, b: number, x: number) => a + (b - a) * x;

const Rise: React.FC<{k: number; style?: React.CSSProperties; children: React.ReactNode}> = ({k: v, style, children}) => (
  <div style={{position: "absolute", overflow: "hidden", ...style}}>
    <div style={{transform: `translateY(${(1 - v) * 105}%)`}}>{children}</div>
  </div>
);
const wipeX = (v: number): React.CSSProperties => (v >= 0.999 ? {} : {clipPath: `inset(-40px ${(1 - v) * 100}% -40px -40px)`});

const Label: React.FC<{children: React.ReactNode; color?: string; size?: number; style?: React.CSSProperties}> =
({children, color = C.muted, size = 12, style}) => (
  <div style={{fontFamily: LBL, fontWeight: 800, fontSize: size, letterSpacing: size * 0.14,
    textTransform: "uppercase", color, whiteSpace: "nowrap", lineHeight: 1.25, ...style}}>{children}</div>
);

const Screen: React.FC<{children: React.ReactNode; rect?: typeof SCR}> = ({children, rect = SCR}) => (
  <div style={{position: "absolute", left: rect.x, top: rect.y, width: rect.w, height: rect.h, overflow: "hidden"}}>{children}</div>
);

/** the AI, small, in the screen's top-right corner while it speaks */
export const CornerMark: React.FC<{t: number}> = ({t}) => (
  <div style={{position: "absolute", left: SCR.x + SCR.w - 46, top: SCR.y + 40, width: 0, height: 0,
    display: "flex", alignItems: "center", justifyContent: "center"}}>
    <AIMark size={46} t={t} />
  </div>
);

const Caret: React.FC<{t: number; h?: number}> = ({t, h = 20}) =>
  Math.floor(t * 2.2) % 2 === 0
    ? <span style={{display: "inline-block", width: 9, height: h, background: C.ink, marginLeft: 2, transform: "translateY(3px)"}} />
    : <span style={{display: "inline-block", width: 9, marginLeft: 2}} />;

const Tab: React.FC<{label: string}> = ({label}) => (
  <div style={{position: "absolute", left: 22, top: 18, display: "flex", alignItems: "center", gap: 8,
    padding: "5px 13px 5px 11px", borderRadius: 8, background: C.wash}}>
    <div style={{width: 9, height: 11, borderRadius: 2, border: `1.5px solid ${C.muted}`}} />
    <span style={{fontFamily: MONO, fontWeight: 500, fontSize: 14, color: C.muted}}>{label}</span>
  </div>
);

/* ================================================================== f8  AJ's four lines */
const AJ_ROWS = [
  {k: "g", v: "gv", label: "GOAL", text: "any office message, back in plain English"},
  {k: "c", v: "cv", label: "CONSTRAINTS", text: "no login. two lines max"},
  {k: "o", v: "ov", label: "OUTPUT", text: "one link"},
  {k: "f", v: "fv", label: "FAILURE", text: "not sure? ask me"},
];
export const AjPromptScreen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => {
  const ends = [ev.c, ev.o, ev.f, ev.end];
  return (
    <Screen>
      <Tab label="prompt.txt" />
      {AJ_ROWS.map((r, i) => {
        const chip = k(t, ev[r.k], 0.35);
        const span = Math.max(0.5, Math.min(ends[i] - ev[r.v] - 0.15, r.text.length * 0.075));
        const n = Math.floor(r.text.length * clamp((t - ev[r.v]) / span));
        const typing = t >= ev[r.v] && n < r.text.length;
        const last = i === AJ_ROWS.length - 1 && n >= r.text.length;
        return (
          <div key={r.k} style={{position: "absolute", left: 22, top: 62 + i * 76, width: 596, height: 70}}>
            <div style={{position: "absolute", left: 0, top: 6, width: 170, ...wipeX(chip)}}>
              <div style={{display: "inline-block", padding: "7px 12px", borderRadius: 8, background: C.tealbg}}>
                <Label color={C.teal} size={15}>{r.label}</Label>
              </div>
            </div>
            <div style={{position: "absolute", left: 182, top: 4, width: 414, fontFamily: MONO, fontWeight: 500,
              fontSize: 22, lineHeight: "30px", color: C.ink}}>
              {r.text.slice(0, n)}{typing || last ? <Caret t={t} /> : null}
            </div>
          </div>
        );
      })}
    </Screen>
  );
};

/* ================================================================== f10  the AI asks before it builds */
export const QuestionScreen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => {
  const card = k(t, ev.q - 0.05, 0.5);
  const a = k(t, ev.new, 0.4), b = k(t, ev.five, 0.4);
  return (
    <Screen>
      <div style={{position: "absolute", left: 74, top: 62, width: 490, height: 250, borderRadius: 16,
        background: C.white, boxShadow: SHADOW, border: `1.5px solid ${C.hair}`,
        transform: `translateY(${(1 - card) * 40}px)`, ...(card < 0.999 ? {clipPath: `inset(${(1 - card) * 100}% -40px -40px -40px)`} : {})}}>
        <Label color={C.teal} size={14} style={{position: "absolute", left: 28, top: 26}}>ONE QUESTION</Label>
        <div style={{position: "absolute", left: 28, top: 60, width: 420, fontFamily: BODY, fontWeight: 600,
          fontSize: 28, lineHeight: "34px", color: C.ink}}>Explain it like they're...</div>
        {[["new here", a, 28], ["five", b, 228]].map(([lab, v, x]) => (
          <div key={lab as string} style={{position: "absolute", left: x as number, top: 150, ...wipeX(v as number)}}>
            <div style={{padding: "12px 24px", borderRadius: 999, border: `2px solid ${C.ink}`,
              fontFamily: MONO, fontWeight: 600, fontSize: 22, color: C.ink}}>{lab as string}</div>
          </div>
        ))}
      </div>
    </Screen>
  );
};

/* ================================================================== the Wait, What? app (f12, f13, f25, f26) */
const UsersPill: React.FC<{n: string; roll?: number}> = ({n, roll = 1}) => (
  <div style={{position: "absolute", right: 82, top: 18, display: "flex", alignItems: "center", gap: 8,
    padding: "6px 14px", borderRadius: 999, background: C.tealbg}}>
    <svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="5" r="3.2" fill={C.teal} /><path d="M2 15c0-3.6 2.7-5.6 6-5.6s6 2 6 5.6" fill={C.teal} /></svg>
    <div style={{height: 22, overflow: "hidden", fontFamily: MONO, fontWeight: 700, fontSize: 17, color: C.teal}}>
      <div style={{transform: `translateY(${(roll - 1) * 22}px)`}}>{n}</div>
    </div>
  </div>
);

const AppFrame: React.FC<{
  t: number; inText: string; inShown: number; outText: string; outShown: number; outWipe: number;
  users?: React.ReactNode; thinking?: boolean; inFlash?: number; link?: number; caret?: boolean;
}> = ({t, inText, inShown, outText, outShown, outWipe, users, thinking, inFlash = 0, link = 0, caret}) => (
  <Screen>
    <div style={{position: "absolute", left: 24, top: 16, fontFamily: DISPLAY, fontWeight: 800, fontSize: 26, color: C.ink, letterSpacing: -0.3}}>Wait, What?</div>
    <div style={{position: "absolute", left: 26, top: 50, fontFamily: MONO, fontSize: 12, color: C.muted}}>office speak → plain English</div>
    {users}
    {/* IN */}
    <div style={{position: "absolute", left: 24, top: 84, width: 590, height: 92, borderRadius: 12,
      background: inFlash > 0 ? `rgba(3,166,207,${0.12 * inFlash})` : C.wash}}>
      <Label size={11} style={{position: "absolute", left: 16, top: 12}}>IN</Label>
      <div style={{position: "absolute", left: 16, top: 32, width: 560, fontFamily: MONO, fontWeight: 500, fontSize: 21, lineHeight: "27px", color: C.ink}}>
        {inText.slice(0, inShown)}{caret ? <Caret t={t} h={18} /> : null}
      </div>
    </div>
    {/* OUT */}
    <div style={{position: "absolute", left: 24, top: 190, width: 590, height: 120, borderRadius: 12,
      background: C.white, border: `2px solid ${outWipe > 0 ? C.teal : C.hair}`}}>
      <Label size={11} color={outWipe > 0 ? C.teal : C.muted} style={{position: "absolute", left: 16, top: 12}}>OUT</Label>
      <div style={{position: "absolute", left: 16, top: 32, width: 560, fontFamily: MONO, fontWeight: 600, fontSize: 21, lineHeight: "27px", color: C.ink, ...wipeX(outWipe)}}>
        {outText.split(" ").slice(0, outShown).join(" ")}
      </div>
      {thinking ? (
        <div style={{position: "absolute", left: 16, top: 42, display: "flex", gap: 8}}>
          {[0, 1, 2].map((i) => (
            <div key={i} style={{width: 9, height: 9, borderRadius: 5, background: C.soft,
              transform: `translateY(${-4 * Math.max(0, Math.sin(t * 7 - i * 0.9))}px)`}} />
          ))}
        </div>
      ) : null}
    </div>
    {link > 0 ? (
      <div style={{position: "absolute", left: 24, top: 322, ...wipeX(link)}}>
        <div style={{display: "flex", alignItems: "center", gap: 8, padding: "6px 14px 6px 10px", borderRadius: 999, background: C.teal}}>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke={C.white} strokeWidth="2" strokeLinecap="round">
            <path d="M7.5 10.5l3-3M6 8.5L4.5 10a2.5 2.5 0 003.5 3.5L9.5 12M12 9.5L13.5 8A2.5 2.5 0 0010 4.5L8.5 6" />
          </svg>
          <span style={{fontFamily: MONO, fontWeight: 600, fontSize: 15, color: C.white}}>waitwhat.app</span>
        </div>
      </div>
    ) : null}
  </Screen>
);

const EOD_IN = "let's take this offline and circle back EOD";
const EOD_OUT = "Let's talk later. Reply by end of day.";
export const AppScreen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => {
  const n = Math.floor(EOD_IN.length * clamp((t - ev.in) / 1.2));
  const out = k(t, ev.out, 0.6);
  return <AppFrame t={t} inText={EOD_IN} inShown={n} caret={n < EOD_IN.length && t > ev.in}
    outText={EOD_OUT} outShown={99} outWipe={out} thinking={n >= EOD_IN.length && out === 0} />;
};
export const AppLinkScreen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => (
  <AppFrame t={t} inText={EOD_IN} inShown={99} outText={EOD_OUT} outShown={99} outWipe={1} link={k(t, ev.link - 0.05, 0.45)} />
);

const LOL = "just prompt engineered it lol";
/** Peter pastes AJ's line in. The counter ticking 40 -> 41 is the joke: he is the 41st user. */
export const App41Screen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => {
  const pasted = t >= ev.paste;
  const flash = pasted ? Math.max(0, 1 - (t - ev.paste) / 0.5) : 0;
  const roll = k(t, ev.tick, 0.4);
  const users = (
    <div style={{position: "absolute", right: 82, top: 18, display: "flex", alignItems: "center", gap: 8,
      padding: "6px 14px", borderRadius: 999, background: C.tealbg, transform: `scale(${1 + 0.12 * Math.max(0, 1 - Math.abs(t - ev.tick - 0.15) / 0.3)})`}}>
      <svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="5" r="3.2" fill={C.teal} /><path d="M2 15c0-3.6 2.7-5.6 6-5.6s6 2 6 5.6" fill={C.teal} /></svg>
      <div style={{height: 22, overflow: "hidden", fontFamily: MONO, fontWeight: 700, fontSize: 17, color: C.teal, display: "flex"}}>
        <div style={{height: 22, overflow: "hidden"}}>
          <div style={{transform: `translateY(${-roll * 22}px)`, lineHeight: "22px"}}><div>40</div><div>41</div></div>
        </div>
        <span style={{lineHeight: "22px"}}>&nbsp;users</span>
      </div>
    </div>
  );
  return <AppFrame t={t} inText={LOL} inShown={pasted ? 99 : 0} inFlash={flash} caret={!pasted}
    outText="" outShown={0} outWipe={0} thinking={pasted} users={users} />;
};

const ANSWER = "Prompt engineering: telling the AI exactly what you want, so it doesn't have to guess.";
export const AppAnswerScreen: React.FC<{t: number; ev: Ev & {words?: number[]}}> = ({t, ev}) => {
  const W = ANSWER.split(" ");
  const times = (ev.words as unknown as number[]) ?? [];
  const shown = times.length === W.length
    ? times.filter((x) => t >= x - 0.04).length
    : Math.floor(W.length * clamp((t - ev.start) / Math.max(0.5, ev.end - ev.start)));
  return <AppFrame t={t} inText={LOL} inShown={99} outText={ANSWER} outShown={shown} outWipe={shown > 0 ? 1 : 0}
    thinking={shown === 0} users={<UsersPill n="41 users" />} />;
};

/* ================================================================== f15  OfficeOS: 212 features */
const TABS = ["chat", "calendar", "crypto", "horoscope", "dating", "karaoke", "recipes", "weather", "polls", "memes",
  "timesheet", "gym", "astrology", "stocks", "music", "games", "notes", "wiki", "lunch", "pets", "fantasy league",
  "tarot", "nft", "podcasts", "birthdays", "carpool", "sudoku", "vlogs", "plants", "trivia", "ringtones", "jokes"];
export const FeaturesScreen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => {
  const fill = lerp(0.97, 1, k(t, 0, Math.max(0.3, ev.done), quartInOut));
  const span = Math.max(0.6, ev.feat - ev.two);
  const shownTabs = Math.floor(TABS.length * clamp((t - ev.two) / span));
  const count = Math.round(212 * expoOut(clamp((t - ev.two) / (span + 0.2))));
  return (
    <Screen>
      <div style={{position: "absolute", left: 24, top: 16, fontFamily: DISPLAY, fontWeight: 800, fontSize: 26, color: C.ink}}>OfficeOS</div>
      <div style={{position: "absolute", left: 24, top: 58, width: 520, height: 10, borderRadius: 5, background: C.hair}}>
        <div style={{width: 520, height: 10, borderRadius: 5, background: C.ink, transform: `scaleX(${fill})`, transformOrigin: "left"}} />
      </div>
      <div style={{position: "absolute", left: 24, top: 74, fontFamily: MONO, fontSize: 12, color: C.muted}}>
        {fill >= 0.999 ? "build complete · 2:01 PM → 4:58 PM" : `building... ${Math.floor(fill * 100)}%`}
      </div>
      <div style={{position: "absolute", left: 24, top: 104, width: 590, display: "flex", flexWrap: "wrap", gap: 7}}>
        {TABS.slice(0, shownTabs).map((x, i) => (
          <div key={i} style={{padding: "4px 10px", borderRadius: 7, background: C.wash, border: `1px solid ${C.hair}`,
            fontFamily: MONO, fontSize: 13, color: C.ink}}>{x}</div>
        ))}
        {shownTabs >= TABS.length ? (
          <div style={{padding: "4px 10px", borderRadius: 7, background: C.ink, fontFamily: MONO, fontSize: 13, color: C.white}}>+180 more</div>
        ) : null}
      </div>
      <div style={{position: "absolute", right: 24, bottom: 18, display: "flex", alignItems: "baseline", gap: 8, opacity: t >= ev.two ? 1 : 0}}>
        <span style={{fontFamily: MONO, fontWeight: 700, fontSize: 34, color: C.ink}}>{count}</span>
        <span style={{fontFamily: MONO, fontWeight: 500, fontSize: 16, color: C.muted}}>features</span>
      </div>
    </Screen>
  );
};

/* ================================================================== f17  the leaderboard (full-frame monitor) */
const LB = {x: 0, y: 300, w: 720, h: 648};
const DOG_FRAMES = 120;
/** a profile picture: one grey circle, the face cropped into it */
const Avatar: React.FC<{src: string; v: number}> = ({src, v}) => (
  <div style={{position: "absolute", left: 0, top: 0, width: 136, height: 136, borderRadius: 68, overflow: "hidden",
    background: "#EBEBEB", border: `4px solid ${C.ink}`, boxSizing: "border-box",
    ...(v < 0.999 ? {clipPath: `inset(${(1 - v) * 100}% 0 0 0 round 68px)`} : {})}}>
    <Img src={src} style={{width: "100%", height: "100%", display: "block"}} />
  </div>
);
export const LeaderboardScreen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => {
  const rows = [
    {at: ev.aj, rank: "1", who: "AJ", app: "Wait, What?", n: 40, label: "40 users", bar: 1, color: C.teal, face: "pe/avatars/aj.png"},
    {at: ev.pe, rank: "2", who: "PETER", app: "OfficeOS", n: 1, label: "1 user (you)", bar: 0.04, color: C.soft, face: "pe/avatars/peter.png"},
  ];
  // Peter's picture becomes the crying dog: a hard swap inside the same circle, no sound
  const dogF = t >= ev.dog ? Math.min(DOG_FRAMES - 1, Math.floor((t - ev.dog) * 30)) : -1;
  return (
    <Screen rect={LB}>
      <Label size={18} color={C.ink} style={{position: "absolute", left: 48, top: 60}}>LEADERBOARD</Label>
      <div style={{position: "absolute", left: 48, top: 90, fontFamily: MONO, fontSize: 16, color: C.muted}}>most users by 5pm wins</div>
      {rows.map((r, i) => {
        const v = k(t, r.at, 0.5);
        const bar = k(t, r.at + 0.1, 0.9);
        const n = Math.round(r.n * bar);
        const face = i === 1 && dogF >= 0 ? `pe/dog/${String(dogF).padStart(3, "0")}.png` : r.face;
        return (
          <div key={i} style={{position: "absolute", left: 48, top: 168 + i * 220, width: 624, height: 160}}>
            <div style={{position: "absolute", left: 0, top: 6}}><Avatar src={staticFile(face)} v={v} /></div>
            <div style={{position: "absolute", left: 160, top: 10, width: 464, height: 160}}>
              <Rise k={v} style={{left: 0, top: 0, width: 464, height: 52}}>
                <div style={{display: "flex", alignItems: "baseline", gap: 14}}>
                  <span style={{fontFamily: MONO, fontWeight: 700, fontSize: 24, color: C.muted}}>#{r.rank}</span>
                  <span style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 36, color: C.ink}}>{r.who}</span>
                  <span style={{fontFamily: MONO, fontSize: 19, color: C.muted}}>{r.app}</span>
                </div>
              </Rise>
              <div style={{position: "absolute", left: 0, top: 62, width: 464, height: 24, borderRadius: 12, background: C.wash}}>
                <div style={{width: 464, height: 24, borderRadius: 12, background: r.color, transform: `scaleX(${r.bar * bar})`, transformOrigin: "left"}} />
              </div>
              <div style={{position: "absolute", left: 0, top: 100, fontFamily: MONO, fontWeight: 700, fontSize: 24, color: i === 0 ? C.teal : C.ink, opacity: v}}>
                {r.label.replace(String(r.n), String(n))}
              </div>
            </div>
          </div>
        );
      })}
    </Screen>
  );
};

/* ================================================================== f28  the wish words go */
type Tok = {s: string; kind: "core" | "fill" | "wish"; key?: string};
const PROMPT: Tok[][] = [
  [{s: "Build an app", kind: "core"}, {s: " the whole", kind: "fill"}],
  [{s: "office will ", kind: "fill"}, {s: "love", kind: "wish", key: "check"}, {s: ".", kind: "fill"}],
  [{s: "Make it ", kind: "fill"}, {s: "amazing", kind: "wish", key: "amazing"}, {s: ".", kind: "fill"}],
  [{s: "Make no mistakes", kind: "wish", key: "mistakes"}, {s: ".", kind: "fill"}],
];
const CH = 16.8;   // Geist Mono 28px advance
export const TeachScreen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => {
  const strike = k(t, ev.check, 0.5);
  const move = k(t, ev.build - 0.15, 0.7, quartInOut);
  const coreW = "Build an app".length * CH;
  const dx = (SCR.w - coreW) / 2 - 40, dy = 164 - 66;
  return (
    <Screen>
      <Label size={13} style={{position: "absolute", left: 40, top: 26}}>PETER'S PROMPT</Label>
      {PROMPT.map((ln, li) => {
        let x = 0;
        return ln.map((tok, ti) => {
          const left = 40 + x * CH; x += tok.s.length;
          const top = 66 + li * 62;
          const lit = tok.kind === "wish" ? k(t, tok.key === "check" ? ev.check - 0.2 : ev[tok.key!], 0.3) : 0;
          // everything but the core drops away on "take them out", staggered by line
          const drop = tok.kind === "core" ? 0 : k(t, ev.take + 0.08 * li + 0.03 * ti, 0.6, quartInOut);
          const isCore = tok.kind === "core";
          return (
            <div key={`${li}-${ti}`} style={{position: "absolute", left, top, height: 40, whiteSpace: "pre",
              fontFamily: MONO, fontWeight: 600, fontSize: 28, lineHeight: "44px", color: C.ink,
              transform: isCore ? `translate(${dx * move}px, ${dy * move}px)` : `translateY(${drop * 380}px)`}}>
              {tok.kind === "wish" ? (
                <span style={{position: "relative", display: "inline-block"}}>
                  <span style={{position: "absolute", left: -4, right: -4, top: 4, bottom: 4, borderRadius: 6, background: C.tealbg, ...wipeX(lit)}} />
                  <span style={{position: "relative", color: lit > 0.5 ? C.teal : C.ink}}>{tok.s}</span>
                  <span style={{position: "absolute", left: -2, top: 21, height: 3, width: "calc(100% + 4px)", background: C.ink,
                    transform: `scaleX(${strike})`, transformOrigin: "left"}} />
                </span>
              ) : isCore ? (
                <span style={{position: "relative", display: "inline-block"}}>
                  {tok.s}
                  <span style={{position: "absolute", left: 0, top: 41, height: 3, width: "100%", background: C.teal,
                    transform: `scaleX(${k(t, ev.build + 0.35, 0.5)})`, transformOrigin: "left"}} />
                </span>
              ) : tok.s}
            </div>
          );
        });
      })}
    </Screen>
  );
};

/* ================================================================== f29 / f30  the prompt contract (white explainer) */
const Icon: React.FC<{name: string; color: string}> = ({name, color}) => {
  const p = {fill: "none", stroke: color, strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const};
  return (
    <svg width="34" height="34" viewBox="0 0 34 34">
      {name === "goal" && <><circle cx="17" cy="17" r="13" {...p} /><circle cx="17" cy="17" r="7.5" {...p} /><circle cx="17" cy="17" r="2.4" fill={color} /></>}
      {name === "con" && <><circle cx="17" cy="17" r="13" {...p} /><path d="M8 26L26 8" {...p} /></>}
      {name === "out" && <><rect x="5" y="9" width="17" height="17" rx="3" {...p} /><path d="M17 17h12M24 12l5 5-5 5" {...p} /></>}
      {name === "fail" && <><circle cx="17" cy="17" r="13" {...p} /><path d="M13 13.5a4 4 0 117 2.6c-1.6 1.2-3 2-3 4" {...p} /><circle cx="17" cy="24.6" r="1.6" fill={color} /></>}
    </svg>
  );
};
const ROWS = [
  {key: "goal", label: "GOAL", hint: "what done looks like", aj: "any message → plain English"},
  {key: "con", label: "CONSTRAINTS", hint: "what to avoid", aj: "no login · 2 lines max"},
  {key: "out", label: "OUTPUT", hint: "what you want back", aj: "one link"},
  {key: "fail", label: "FAILURE", hint: "if unsure, what then?", aj: "not sure? ask me"},
];
const COL = {lab: 32, aj: 262, pe: 486, ajW: 210, peW: 202};
const ROW_Y = (i: number) => 420 + i * 172;
const ROW_H = 146;
const FLY = [{s: "crypto"}, {s: "dating"}, {s: "karaoke"}];

export const ContractExplainer: React.FC<{t: number; ev: Ev; phase: 1 | 2; prev?: Ev; prevEnd?: number}> =
({t, ev, phase, prev, prevEnd = 0}) => {
  // phase 2 continues phase 1's last frame exactly (matched positions, no re-entry)
  const T1 = phase === 1 ? t : prevEnd + t;
  const e1 = phase === 1 ? ev : prev!;
  const e2 = phase === 2 ? ev : ({} as Ev);
  const T2 = phase === 2 ? t : -99;
  const enter = k(T1, 0, 0.6);
  const ajFill = (i: number) => k(T1, e1.boxes + i * 0.12, 0.45);
  const peDraw = (i: number) => k(T1, e1.none + i * 0.1, 0.45);
  const lit = [k(T1, e1.goal, 0.4), k(T2, e2.skip, 0.4), k(T2, e2.back, 0.4), 0];
  // the current row is emphasised; a row already explained steps back
  const cur = phase === 1 ? 0 : (T2 >= e2.back ? 2 : 1);
  const spin = k(T1, e1.never, 1.6);
  const goalDone = k(T1, e1.done, 0.4);
  return (
    <div style={{position: "absolute", inset: 0, background: C.white}}>
      <div style={{position: "absolute", left: 0, top: 0, width: 720, height: 1280, transform: `translateY(${(1 - enter) * 60}px)`,
        ...(enter < 0.999 ? {clipPath: `inset(${(1 - enter) * 100}% 0 0 0)`} : {})}}>
        <Label size={16} color={C.ink} style={{position: "absolute", left: 0, width: 720, textAlign: "center", top: 250}}>THE PROMPT CONTRACT</Label>
        <div style={{position: "absolute", left: COL.aj, top: 330, width: COL.ajW, textAlign: "center", fontFamily: DISPLAY, fontWeight: 800, fontSize: 30, color: C.ink}}>AJ</div>
        <div style={{position: "absolute", left: COL.pe, top: 330, width: COL.peW, textAlign: "center", fontFamily: DISPLAY, fontWeight: 800, fontSize: 30, color: C.ink}}>PETER</div>
        {ROWS.map((r, i) => {
          const on = lit[i];
          const dim = on > 0 && i !== cur ? 0.45 : 1;
          return (
            <div key={r.key}>
              {/* the lit band behind the whole row */}
              <div style={{position: "absolute", left: 18, top: ROW_Y(i) - 10, width: 684, height: ROW_H + 20, borderRadius: 18,
                background: C.tealbg, opacity: dim, ...wipeX(on)}} />
              <div style={{position: "absolute", left: COL.lab, top: ROW_Y(i) + 24}}>
                <Icon name={r.key} color={on > 0.5 ? C.teal : C.ink} />
              </div>
              <Label size={15} color={on > 0.5 ? C.teal : C.ink} style={{position: "absolute", left: COL.lab, top: ROW_Y(i) + 70}}>{r.label}</Label>
              <div style={{position: "absolute", left: COL.lab, top: ROW_Y(i) + 94, width: 210, fontFamily: BODY, fontSize: 16, lineHeight: "20px", color: C.muted}}>{r.hint}</div>
              {/* AJ: filled */}
              <div style={{position: "absolute", left: COL.aj, top: ROW_Y(i) + 14, width: COL.ajW, height: ROW_H - 28, borderRadius: 14,
                background: C.white, boxShadow: SHADOW, border: `2px solid ${i === 0 && goalDone > 0 ? C.teal : C.hair}`,
                ...(ajFill(i) < 0.999 ? {clipPath: `inset(${(1 - ajFill(i)) * 100}% -40px -40px -40px)`} : {})}}>
                <div style={{position: "absolute", left: 16, top: 0, width: COL.ajW - 32, height: ROW_H - 28, display: "flex", alignItems: "center",
                  fontFamily: MONO, fontWeight: 600, fontSize: 20, lineHeight: "26px", color: C.ink}}>{r.aj}</div>
                {i === 0 ? (
                  <div style={{position: "absolute", right: -12, top: -12, width: 30, height: 30, borderRadius: 15, background: C.teal,
                    transform: `scale(${goalDone})`, display: "flex", alignItems: "center", justifyContent: "center"}}>
                    <svg width="16" height="16" viewBox="0 0 16 16"><path d="M3 8.5l3.2 3L13 4.5" stroke={C.white} strokeWidth="2.4" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
                  </div>
                ) : null}
              </div>
              {/* Peter: empty, drawn on as a dashed outline */}
              <svg style={{position: "absolute", left: COL.pe, top: ROW_Y(i) + 14, overflow: "visible"}} width={COL.peW} height={ROW_H - 28}>
                <rect x="1" y="1" width={COL.peW - 2} height={ROW_H - 30} rx="14" fill="none" stroke={C.soft} strokeWidth="2.5"
                  strokeDasharray="9 8" pathLength={1000} strokeDashoffset={0}
                  style={{clipPath: `inset(0 ${(1 - peDraw(i)) * 100}% 0 0)`}} />
              </svg>
              {i === 0 && spin > 0 ? (
                <div style={{position: "absolute", left: COL.pe, top: ROW_Y(i) + 14, width: COL.peW, height: ROW_H - 28,
                  display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column"}}>
                  <span style={{fontFamily: MONO, fontWeight: 700, fontSize: 40, color: C.muted}}>{Math.round(212 * spin)}</span>
                  <span style={{fontFamily: MONO, fontSize: 14, color: C.muted}}>features, still going</span>
                </div>
              ) : null}
            </div>
          );
        })}
        {/* output: AJ got a link; Peter's empty box fills with karaoke (inside the box, never over a neighbour) */}
        {phase === 2 ? FLY.map((f, i) => {
          const v = k(T2, e2.karaoke - 0.3 + i * 0.1, 0.55);
          const cx = COL.pe + COL.peW / 2, cy = ROW_Y(2) + ROW_H / 2;
          const land = [{x: COL.pe + 16, y: ROW_Y(2) + 30}, {x: COL.pe + 108, y: ROW_Y(2) + 30}, {x: COL.pe + 52, y: ROW_Y(2) + 76}][i];
          return v > 0 ? (
            <div key={f.s} style={{position: "absolute", left: 0, top: 0,
              transform: `translate(${lerp(cx - 40, land.x, v)}px, ${lerp(cy - 16, land.y, v)}px)`,
              padding: "6px 12px", borderRadius: 8, background: C.ink, fontFamily: MONO, fontWeight: 600, fontSize: 16, color: C.white,
              ...(v < 0.999 ? {clipPath: `inset(0 ${(1 - Math.min(1, v * 2.5)) * 100}% 0 0)`} : {})}}>{f.s}</div>
          ) : null;
        }) : null}
      </div>
    </div>
  );
};

/* ================================================================== f31  ask vs guess, what it cost */
export const CostScreen: React.FC<{t: number; ev: Ev}> = ({t, ev}) => {
  const head = k(t, ev.fail, 0.4);
  const cols = [
    {at: ev.aj, who: "AJ", line: "asked 1 question", cost: "4 seconds", color: C.teal, bg: C.tealbg},
    {at: ev.pe, who: "PETER", line: "212 guesses", cost: "3 hours", color: C.coral, bg: C.coralbg},
  ];
  return (
    <Screen>
      <div style={{position: "absolute", left: 24, top: 22, display: "flex", alignItems: "center", gap: 12, ...wipeX(head)}}>
        <Icon name="fail" color={C.teal} />
        <Label size={15} color={C.teal}>FAILURE</Label>
        <span style={{fontFamily: MONO, fontSize: 15, color: C.muted}}>if unsure, ask</span>
      </div>
      {cols.map((c, i) => {
        const v = k(t, c.at, 0.5);
        return (
          <div key={c.who} style={{position: "absolute", left: 24 + i * 302, top: 92, width: 286, height: 250, borderRadius: 16,
            background: c.bg, ...(v < 0.999 ? {clipPath: `inset(${(1 - v) * 100}% 0 0 0)`} : {})}}>
            <div style={{position: "absolute", left: 22, top: 20, fontFamily: DISPLAY, fontWeight: 800, fontSize: 26, color: C.ink}}>{c.who}</div>
            <div style={{position: "absolute", left: 22, top: 74, fontFamily: MONO, fontWeight: 500, fontSize: 19, color: C.ink}}>{c.line}</div>
            <div style={{position: "absolute", left: 22, top: 150, fontFamily: MONO, fontWeight: 700, fontSize: 40, color: c.color}}>{c.cost}</div>
          </div>
        );
      })}
    </Screen>
  );
};

/* ================================================================== f32 / f33  the card (the screenshot frame) */
const CARD = [
  {k: "g", key: "goal", label: "GOAL", hint: "what done looks like"},
  {k: "c", key: "con", label: "CONSTRAINTS", hint: "what to avoid"},
  {k: "o", key: "out", label: "OUTPUT", hint: "what you want back"},
  {k: "f", key: "fail", label: "FAILURE", hint: "if unsure, ask"},
];
export const CardScreen: React.FC<{t: number; ev: Ev; full?: boolean}> = ({t, ev, full}) => (
  <Screen>
    {CARD.map((r, i) => {
      const on = full ? 1 : k(t, ev[r.k] - 0.05, 0.4);
      return (
        <div key={r.k} style={{position: "absolute", left: 24, top: 26 + i * 84, width: 520, height: 70}}>
          <div style={{position: "absolute", left: 0, top: 0, width: 520, height: 70, borderRadius: 12, background: C.tealbg, ...wipeX(on)}} />
          <div style={{position: "absolute", left: 14, top: 18}}><Icon name={r.key} color={on > 0.5 ? C.teal : C.soft} /></div>
          <Label size={15} color={on > 0.5 ? C.teal : C.muted} style={{position: "absolute", left: 60, top: 12}}>{r.label}</Label>
          <div style={{position: "absolute", left: 60, top: 36, fontFamily: MONO, fontWeight: 500, fontSize: 18, color: on > 0.5 ? C.ink : C.soft}}>{r.hint}</div>
          <div style={{position: "absolute", left: 330, top: 50, width: 172, height: 2, background: on > 0.5 ? C.teal : C.hair}} />
          {full && i === 0 ? <div style={{position: "absolute", left: 332, top: 22}}><Caret t={t} h={24} /></div> : null}
        </div>
      );
    })}
  </Screen>
);
