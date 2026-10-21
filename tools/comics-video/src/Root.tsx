import React from "react";
import { Composition } from "remotion";
import { LoopV10 } from "./LoopV10";
import { IntroV1, INTRO_DURATION } from "./IntroV1";
import { GraphV1, GRAPH_DURATION, FPS as GRAPH_FPS } from "./GraphV1";
import { RemoteControl, RC_DURATION, RC_FPS } from "./RemoteControl";
import { Insights, INS_DURATION, INS_FPS } from "./Insights";
import {SystemOne, S1M_DURATION, S1M_FPS} from "./SystemOne";
import {PromptEng, PE_DURATION, PE_FPS} from "./PromptEng";
import cut from "./cut.json";

/**
 * One composition. Every timing, caption and audio cue comes from cut.json,
 * which v10/emit.py writes from spec.py + timeline.py -- so nothing here is a
 * number anyone edits by hand.
 */
export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="LoopV10"
      component={LoopV10}
      durationInFrames={cut.durationInFrames}
      fps={cut.fps}
      width={cut.width}
      height={cut.height}
    />
    <Composition
      id="IntroV1"
      component={IntroV1}
      durationInFrames={INTRO_DURATION}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="GraphV1"
      component={GraphV1}
      durationInFrames={GRAPH_DURATION}
      fps={GRAPH_FPS}
      width={1080}
      height={1920}
    />
    {/* EP003 -- audio cut. Placeholder plates until the panels are generated. */}
    <Composition
      id="RemoteControl"
      component={RemoteControl}
      durationInFrames={RC_DURATION}
      fps={RC_FPS}
      width={1080}
      height={1920}
    />
    {/* /insights -- timing build. Placeholder cards until the 46 plates are exported. */}
    <Composition
      id="Insights"
      component={Insights}
      durationInFrames={INS_DURATION}
      fps={INS_FPS}
      width={720}
      height={1280}
    />
    {/* EP005 system one model */}
    <Composition
      id="SystemOne"
      component={SystemOne}
      durationInFrames={S1M_DURATION}
      fps={S1M_FPS}
      width={1080}
      height={1920}
    />
    {/* prompt engineering (Script A, "Wait, What?") */}
    <Composition
      id="PromptEng"
      component={PromptEng}
      durationInFrames={PE_DURATION}
      fps={PE_FPS}
      width={1080}
      height={1920}
    />
    {/* same film, no overlaid text — for the "Frames - no captions" storyboard set */}
    <Composition
      id="GraphV1Plain"
      component={GraphV1}
      defaultProps={{ caps: false }}
      durationInFrames={GRAPH_DURATION}
      fps={GRAPH_FPS}
      width={1080}
      height={1920}
    />
  </>
);
