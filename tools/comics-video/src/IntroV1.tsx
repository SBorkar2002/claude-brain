import React from "react";
import {
  AbsoluteFill, Audio, Img, Sequence, staticFile,
  interpolate, useCurrentFrame, useVideoConfig, spring,
} from "remotion";
import mouth from "./intro_mouth.json";

/**
 * Channel bumper — "AI FOMO".
 *
 * Dev 2 spews jargon the whole time (intro_dev2.mp3), ducked to barely-there
 * under Peter's to-camera promise (intro_peter.mp3). Mouths are driven off the
 * actual voice: each pose has an OPEN and a CLOSED plate, and we show OPEN only
 * while that speaker is making sound (intro_mouth.json, computed from the RMS
 * envelope). So the mouth opens on every word, not just the last one.
 *
 * End card matches the loop card: dark bookend, white text, a single teal rule
 * -- teal is the one accent (it also lives on the profile mark), nowhere else.
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
  font-weight:800; font-style:normal; }`;

const CAP = "'LatoLocal', 'Helvetica Neue', Arial, sans-serif";
const DISPLAY = "'MonaSans', 'Helvetica Neue', Arial, sans-serif";
const TEAL = "#03A6CF";
const PLATE = (n: string) => staticFile(`v10/intro/${n}.png`);

// ---- pose windows: [openPlate, closedPlate, at, until, speaker] -------------
// speaker: "peter" | "dev2" | "static" (open plate held)
type Win = [string, string, number, number, "peter" | "dev2" | "static"];
const WINDOWS: Win[] = [
  // First scene — hand up/down gesture while Dev 2 talks (same treatment as the last scene)
  ["twoshot_3",      "twoshot_3",    0.0,  0.9, "static"],  // hand down
  ["twoshot_open",   "twoshot_open", 0.9,  1.7, "static"],  // hand up
  ["twoshot_3",      "twoshot_3",    1.7,  2.6, "static"],  // hand down
  ["twoshot_open",   "twoshot_open", 2.6,  3.4, "static"],  // hand up
  ["twoshot_3",      "twoshot_3",    3.4,  3.9, "static"],  // hand down
  ["peter_listen",   "peter_listen", 3.9,  4.8, "static"],  // cut to Peter listening (Dev 2 still in bg)
  ["peter_huge",     "peter_blank",  4.8,  8.9, "peter"],   // "oh, yeah. huge." (blank = the … closed)
  ["peter_thought",  "peter_thought",8.9, 10.9, "static"],  // "I have no idea what that means"
  ["peter_plain_c2", "peter_plain_c2",10.9,12.5,"static"],  // … BLANK PAUSE before "you too" (Frame 9)
  ["peter_youtoo",   "peter_youtoo",12.5, 13.6, "static"],  // "you too?"
  ["peter_cheek",    "peter_cheek_c",13.6, 15.3, "peter"],  // "don't worry…" (cheek pair)
  ["peter_cheek_c2", "peter_cheek_c",15.3, 16.9, "peter"],  // "…channel for this" (2nd cheek open)
  ["peter_allstuff", "peter_allstuff",16.9,20.4, "static"], // "all the stuff… nod at" (thumb held)
  ["peter_explained","peter_plain_c3_al",20.4,21.9,"peter"],// "actually explained" (plain pair)
  ["peter_plain_c3_al","peter_plain_c3_al",21.9,23.3,"static"], // … BLANK PAUSE (held ~1.4s incl the +0.5s silence)
  ["peter_smile",    "peter_smile", 23.3, 25.4, "static"],  // "so next time you can nod for real" — smile held
  // Last scene — hand up/down gesture (Sejal's call; twoshot_open is a separate
  // drawing so a small shift is expected). Mouth stays open, no mouth-close frame.
  ["twoshot_3",      "twoshot_3",   25.4, 26.1, "static"],  // hand down
  ["twoshot_open",   "twoshot_open",26.1, 26.9, "static"],  // hand up
  ["twoshot_3",      "twoshot_3",   26.9, 27.8, "static"],  // hand down
];

// ---- captions: one line at a time, on the voice, TOP band ------------------
const CAPS: { t: string; at: number; until: number; italic?: boolean }[] = [
  { t: "…yeah, made it agentic.",           at: 0.20, until: 2.05 },
  { t: "RAG, couple of agents,",            at: 2.10, until: 3.85 },
  { t: "whole thing's a graph now.",        at: 3.90, until: 4.80 },
  { t: "oh, yeah.",                         at: 4.95, until: 7.40 },
  { t: "huge.",                             at: 7.50, until: 8.90 },
  { t: "I have no idea what that means.",   at: 9.10, until: 11.40, italic: true },
  { t: "…you too?",                         at: 12.55, until: 13.60 },
  { t: "don't worry.",                      at: 14.15, until: 15.30 },
  { t: "we made a whole channel for this.", at: 15.35, until: 17.00 },
  { t: "all the stuff people say",          at: 17.65, until: 19.05 },
  { t: "at your desk that you nod at.",     at: 19.10, until: 20.40 },
  { t: "actually explained.",               at: 20.85, until: 22.40 },
  { t: "so next time you can nod for real.",at: 22.95, until: 24.85 },
  { t: "…and then I vibe-coded the pipeline", at: 25.55, until: 27.60 },
];

const PETER_AT = 4.8;
const BUTTON_AT = 25.4;
const CARD_AT = 27.8;
const END = 31.5;

const Panels: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const w = WINDOWS.find(([, , at, until]) => frame >= f(at) && frame < f(until)) ?? WINDOWS[WINDOWS.length - 1];
  const [openP, closedP, , , spk] = w;
  const voiced =
    spk === "static" ? true :
    spk === "peter"  ? !!(mouth.peter as number[])[frame] :
                       !!(mouth.dev2 as number[])[frame];
  // mount both, toggle opacity -> no src-swap decode flicker within a pose
  return (
    <AbsoluteFill>
      <Img src={PLATE(closedP)} style={{ width: "100%", height: "100%", objectFit: "cover", position: "absolute" }} />
      <Img src={PLATE(openP)}  style={{ width: "100%", height: "100%", objectFit: "cover", position: "absolute", opacity: voiced ? 1 : 0 }} />
    </AbsoluteFill>
  );
};

const Caption: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const c = CAPS.find((c) => t >= c.at && t < c.until);
  if (!c) return null;
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute", left: 60, right: 60, top: 160, textAlign: "center",
          fontFamily: CAP, fontSize: 52, lineHeight: "62px", fontWeight: 800,
          fontStyle: c.italic ? "italic" : "normal",
          color: "#FFFFFF", WebkitTextStrokeWidth: "7px", WebkitTextStrokeColor: "#000000",
          paintOrder: "stroke",
        }}
      >
        {c.t}
      </div>
    </AbsoluteFill>
  );
};

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 18 });
  const scale = interpolate(pop, [0, 1], [0.92, 1]);
  const ruleW = interpolate(pop, [0, 1], [0, 240]);
  const tagIn = interpolate(frame, [16, 28], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const asideIn = interpolate(frame, [48, 62], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }); // lands ~1s after the tagline
  return (
    <AbsoluteFill style={{ background: "#141416", justifyContent: "center", alignItems: "center" }}>
      <div style={{ transform: `scale(${scale})`, opacity: pop, textAlign: "center" }}>
        <div style={{ fontFamily: DISPLAY, fontWeight: 800, fontSize: 82, letterSpacing: "-2px", lineHeight: 1.12, color: "#FFFFFF" }}>
          I HAVE NO IDEA<br />WHAT THAT MEANS
        </div>
      </div>
      {/* the one teal element — a horizontal rule, like the loop card */}
      <div style={{ width: ruleW, height: 6, background: TEAL, marginTop: 44, borderRadius: 3 }} />
      <div style={{ marginTop: 40, fontFamily: DISPLAY, fontWeight: 700, fontSize: 40, color: "#FFFFFF", opacity: tagIn, letterSpacing: "0.5px", textAlign: "center" }}>
        new one every week
        <div style={{ fontSize: 27, fontWeight: 500, color: "#96969E", marginTop: 12, letterSpacing: "0.3px", opacity: asideIn }}>
          (or maybe more, or maybe less)
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const IntroV1: React.FC = () => {
  const { fps } = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const duckStart = f(PETER_AT), duckEnd = f(PETER_AT + 0.5);
  const bedVol = (fr: number) =>
    fr <= duckStart ? 1 : fr >= duckEnd ? 0.08 : interpolate(fr, [duckStart, duckEnd], [1, 0.08]);

  return (
    <AbsoluteFill style={{ background: "#f5f5f2" }}>
      <style>{FONT}</style>

      <Sequence from={0} durationInFrames={f(CARD_AT)}>
        <Panels />
        <Caption />
      </Sequence>

      <Sequence from={f(CARD_AT)}>
        <EndCard />
      </Sequence>

      {/* audio */}
      <Sequence from={0}>
        <Audio src={staticFile("v10/audio/intro_dev2.mp3")} startFrom={0} endAt={f(BUTTON_AT)} volume={bedVol} />
      </Sequence>
      <Sequence from={f(PETER_AT)}>
        <Audio src={staticFile("v10/audio/intro_peter.mp3")} startFrom={0} endAt={f(20.7)} />
      </Sequence>
      <Sequence from={f(BUTTON_AT)}>
        <Audio src={staticFile("v10/audio/intro_dev2.mp3")} startFrom={f(35.94)} endAt={f(38.3)} />
      </Sequence>
    </AbsoluteFill>
  );
};

export const INTRO_DURATION = Math.round(END * 30);
