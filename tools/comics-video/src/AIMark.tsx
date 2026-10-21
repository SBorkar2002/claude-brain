import React from "react";

/**
 * The AI's one body. Geometry is the series spec in
 * product-brain/video/youtube/comics/characters/appearance.md:
 *   six petals  cx 50 cy 25 rx 14.5 ry 25, each rotated i*60 about (50,50)
 *   eye ring    white r 17
 *   pupil       mark-coloured r 11
 *   gaze rests at 1, so the eye centre sits at 50 + 9 = 59, NOT centred.
 * viewBox is padded to -6 -6 112 112 because the petals reach past 100 and a
 * tight box clips them, which reads as a render bug.
 */
export const TEAL = "#03A6CF";

export const AIMark: React.FC<{
  size: number;
  /** eye closed, breathing slowly -- nobody has asked it for anything yet */
  asleep?: boolean;
  /** seconds since it woke; negative while still asleep */
  since?: number;
  /** seconds, for the breathe */
  t: number;
  rotate?: number;
  opacity?: number;
}> = ({size, asleep = false, since = 99, t, rotate = 0, opacity = 1}) => {
  const eye = 50 + 9;                       // gaze = 1, resting
  // awake: 1 + sin(t*2.1)*0.035. Asleep it breathes slower and shallower.
  const pulse = asleep
    ? 1 + Math.sin(t * 0.95) * 0.022
    : 1 + Math.sin(t * 2.1) * 0.035;
  // The eye POPS open -- no easing. A lid that slides up reads as a UI
  // animation; a hard switch reads as something waking up.
  const lid = asleep ? 1 : 0;
  const lidR = asleep ? 0 : 11;
  const pop = 1 + (asleep ? 0 : Math.max(0, 1 - Math.max(0, since) / 0.16) * 0.13);

  return (
    <svg
      width={size} height={size} viewBox="-6 -6 112 112"
      style={{
        transform: `rotate(${rotate}deg) scale(${pulse * pop})`,
        transformOrigin: "50% 50%",
        opacity,
        overflow: "visible",
      }}
    >
      <g>
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <ellipse key={i} cx={50} cy={25} rx={14.5} ry={25} fill={TEAL}
            transform={`rotate(${i * 60} 50 50)`} />
        ))}
      </g>
      <circle cx={eye} cy={50} r={17} fill="#fff" />
      {lid < 0.98 && <circle cx={eye} cy={50} r={lidR} fill={TEAL} />}
      {lid > 0.02 && (
        // the closed lid: a real shut eye, not a shrunken pupil
        <path
          d={`M ${eye - 12.5} 50 q 12.5 ${9.5 * lid} 25 0`}
          stroke={TEAL} strokeWidth={3.4} fill="none" strokeLinecap="round"
        />
      )}
    </svg>
  );
};
