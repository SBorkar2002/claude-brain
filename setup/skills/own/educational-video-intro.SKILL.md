# Skill: Educational Product Intro Video

Rules and guardrails for 15-second educational intro animations that introduce a framework, metric system, or product concept using real product UI as the opening scene.

---

## When to use this skill

Use this skill when creating a short (10–20 second) animated intro that:
- Introduces a named framework or methodology (e.g. DORA, OKRs, SLAs)
- Opens on a real product screen to establish context before revealing the framework
- Ends on a summary of 3–6 key metrics or concepts in a data card grid

Do NOT use this skill for:
- Product launch / feature announcements → use `project-launch` skill instead
- Long-form explainers (>30s)
- Animations without a real product UI anchor scene

---

## Format & Stage

| Property | Value |
|---|---|
| Resolution | 1280 × 720 (16:9) |
| Stage background | `#ffffff` |
| Page background | `#0e0e13` |
| Shadow | `0 30px 90px rgba(0,0,0,0.55)` |
| Overflow | hidden |

The stage must be letterboxed on a dark background — never full-bleed white to the viewport edge.

---

## Typography

| Role | Font | Weight | Size | Color |
|---|---|---|---|---|
| Framework/title | Geist | 800 | 118px | accent color |
| Metric label | Geist | 500 | 16px | `#34332e` |
| Metric value | Geist | 700 | 52px | `#1b1b18` |
| Metric unit | Geist | 500 | 20px | `#9b9a90` |
| Tier/badge | Geist Mono | 500 | 12.5px | `#2f8a4e` (elite/good) |
| Letter spacing (title) | — | — | 0.12em | — |

Always load Geist and Geist Mono from Google Fonts. Never substitute system sans-serif for the title reveal.

---

## Color

- **Accent**: `#03A6CF` (default) — used for title text, scrubber fill, progress bar. Exposed as a configurable prop.
- **Card background**: `#f6f6f3`
- **Elite / passing tier**: `#2f8a4e`
- **Warning tier**: `#b45309` (amber)
- **Failing tier**: `#b91c1c` (red)

Tier color must only appear on the badge line, never on the metric value itself.

---

## Animation Structure (15s canonical sequence)

```
0s      ─── Scene opens on real product UI (static hold)
~1.4s   ─── Event card pops open on the product screen
~2.6s   ─── First notification slides in from right edge
~3.8s   ─── Second notification arrives; stack shifts down
~4.9s   ─── Camera zooms in toward the notification cluster
~5.9s   ─── Third notification arrives
~6.9s   ─── Fourth notification arrives; full stack visible
~8.2s   ─── Camera pulls back to reveal full screen
~9.4s   ─── Wash/overlay fades in (covers product UI)
~10.0s  ─── Framework title appears (large, centred, faded in)
~11.0s  ─── Title glides up to final position
~11.3s  ─── Metric card 1 pops in
~11.65s ─── Metric card 2 pops in
~12.0s  ─── Metric card 3 pops in
~12.35s ─── Metric card 4 pops in
~13.0s  ─── Hold on final frame (minimum 2 seconds)
~15.0s  ─── End
```

**Rules:**
- Always open on a static product screen for ≥1 second before any animation begins.
- Notifications must arrive sequentially — never simultaneously.
- Camera zoom must precede the final notification; pull-back before the wash.
- The wash overlay must reach full opacity before the title appears.
- Metric cards must stagger in sequentially (never all at once), left-to-right, top-to-bottom.
- Hold the final frame for at least 2 seconds before the video ends.

---

## Easing Vocabulary

| Motion type | Ease |
|---|---|
| Element pop-in (card, notification, metric) | `back.out(1.4)` – `back.out(1.5)` |
| Camera translate / scale | `power2.inOut` |
| Stack shift (pushing items down) | `power3.out` |
| Wash fade-in | `power2.out` |
| Title fade-in | `power2.out` |
| Title glide to position | `power2.inOut` |

Never use linear easing for any user-visible motion. Never use `elastic` or `bounce` eases — they read as playful, not professional.

---

## Notification Stack

- Notifications slide in from the **right edge** (start `x: 430`, off-screen)
- Each new notification lands at the **top** of the stack; older ones push down
- Vertical pitch between stacked notifications: **84px** (in scene coordinate space)
- Stack shift duration: `0.4s`
- Notification slide-in duration: `0.55s`

---

## Camera Motion

- Camera operates on a `transform-origin: 0px 0px` container with `scale`, `x`, `y`
- Zoom-in target: `scale(1.85)`, translated to frame the notification cluster
- Always return to `scale(1.0), x:0, y:0` before the wash transition begins
- Camera move duration: `0.85s – 0.95s`

---

## Metric Card Grid

- Layout: **2×2 grid**, `gap: 26px 28px`
- Position: centered, with generous horizontal margins (~150px each side on 1280px stage)
- Card background: `#f6f6f3`, `border-radius: 11px`
- Card shadow: `0 6px 22px rgba(45,45,55,0.16), 0 1px 4px rgba(0,0,0,0.09)`
- Each card entrance: `opacity 0→1`, `y 26→0`, `scale 0.9→1`, `duration: 0.45s`, ease `back.out(1.5)`
- Stagger: **0.35s** between cards

Card content order (top to bottom within each card):
1. Metric label (16px, medium weight)
2. Value + unit on same baseline row (52px value, 20px unit)
3. Tier badge (Geist Mono, 12.5px, all-caps label · benchmark description)

---

## Title Reveal

- Title starts: `opacity:0`, `y: 255px` below final position, `scale: 1.32`
- Title appears large and centred first (fade-in only, no movement yet)
- Then glides up and shrinks to final position simultaneously
- Final position: `top: 96px`, centered horizontally
- Font size: 118px, weight 800, letter-spacing 0.12em

---

## Wash / Scene Transition

- The wash element is a **full-stage image** (`position:absolute; inset:0; object-fit:cover`)
- It sits in z-order between the camera layer and the title/cards layer
- It fades from `opacity:0` to `opacity:1` over `0.6s`
- Its image should be a cleaned, simplified version of the product UI or a neutral branded background — never a blank color fill

---

## Player Controls

Every video must include a playback control bar:
- Play/pause button (bottom-left)
- Scrubber with filled progress (accent color) and white handle
- Timecode display (monospace, `mm:ss / mm:ss` format)
- Controls auto-hide after **2.6 seconds** of playback; reappear on pointer move
- Controls must fade in on hover over the stage at any time

---

## Props (configurable per instance)

| Prop | Type | Default | Description |
|---|---|---|---|
| `autoplay` | boolean | `true` | Start playing on load |
| `loop` | boolean | `false` | Loop the timeline |
| `accentColor` | color | `#03A6CF` | Title color and scrubber fill |

---

## Guardrails

- **No localStorage resume** — always start from `t=0` on page load. Never resume mid-animation from a saved position.
- **Always use GSAP** for all animated properties. Do not mix CSS transitions with GSAP on the same element.
- **Set initial states with `gsap.set()`** before building the timeline. Never rely on CSS `opacity:0` alone as the only initial state guard — CSS hides the flash, GSAP owns the animation state.
- **Stage must be invisible until `fitStage()` runs** — use `visibility:hidden` on the stage element and set `visibility:visible` in the resize handler after scaling.
- **Fonts must be loaded before animation begins** — always `<link rel="preconnect">` for Google Fonts at the top of `<head>`.
- **GSAP must be loaded before setup** — poll for `window.gsap` with a `waitForGsap()` retry loop; max 240 retries × 25ms.
- **The animation must be self-contained** — no external runtime dependencies beyond GSAP CDN and Google Fonts. No React, no framework, no `support.js`.
- **Scrubber seek must pause the timeline** and resume only if it was playing before drag started.
- **Space bar** must toggle play/pause globally.
- **`onComplete`** must show the replay icon and keep controls visible indefinitely.
