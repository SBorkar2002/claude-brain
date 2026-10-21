# Portfolio · Pixel · Component research

17 Oct 2026. Covers 5 libraries: Componentry, Space UI, Skecher UI, Planes, Arc UI. Each was checked through its site, registry JSON, terms or license page, and GitHub. This builds on `portfolio-v2/research.md` section 4 (16 Oct). Standing rule: no paid components. Stack from PLAN.md: Next.js, Tailwind v4, native scroll, View Transitions.

## 0. Verdict in one screen

| Need | Use | Library | License |
|---|---|---|---|
| Cmd+K palette | Command (Base UI) + Kbd | Space UI | MIT |
| `?` shortcut sheet, keycap hints | Shortcut recorder (ShortcutKbd, ShortcutList, usePlatform) | Arc | MIT |
| Case study section nav | Section Scrollspy | Space UI | MIT |
| Theme toggle | Theme Toggle (View Transition, polygon variant) | Space UI | MIT |
| Art gallery with video | Showcase Gallery block | Space UI | MIT |
| Pixel hover field (hero, footer, cat perch) | Pixel Canvas | Componentry | MIT |
| Project tile hover preview | Pixel Image Trail + Hover Transition ("strips", "wipe") | Componentry | MIT |
| Dithered pastel backgrounds | Dither Gradient, ASCII Effect | Componentry | MIT |
| Status line / counters | Split Flap Display | Componentry | MIT |
| Before/after in case studies | Image Compare | Arc | MIT |
| Experience | Timeline (or Activity Heatmap as a "shipping log") | Arc | MIT |
| Cat speech bubble | Popover + Tooltip + Toast | Space UI | MIT |
| Marquee | Logo Marquee block (has pause control) | Arc | MIT |

Pick ONE primitive layer: Space UI (Base UI + Tailwind v4 + `motion`). Lift Arc and Componentry pieces one at a time. Arc uses CSS modules plus some Radix, and Componentry imports `framer-motion`. Mixing them unchecked means shipping Radix + Base UI and both `framer-motion` + `motion`. Fix: rewrite Componentry imports to `motion/react` (same API), and port Arc pieces to Tailwind.

## 1. What changed since 16 Oct

- **Componentry**: still MIT. GitHub LICENSE is MIT, 610 stars, last push 12 Oct. The terms page adds a hedge: "generally ... MIT unless otherwise specified". 54 components; "Blocks" is still "200+ coming soon" (only 3 in the registry). No paid tier, only sponsorship.
- **Space UI**: the license is now **clear**: the Terms (Section 2) put free source under MIT, and every component page repeats it. Pro is $99/yr (struck from $169, "41% off") or $129 lifetime. 27 catalogue items are PRO, including **all three pixel items** (Pixel Fill Button, Pixel Reveal Text, Pixel Reveal Image) and Morphing Command Bar. All 61 primitives are free. Caveat from the site: some components are "inspired by or recreated from" ideas elsewhere.
- **Skecher UI**: still **no LICENSE file** (GitHub reports license null). The README now says "open source. See the repository license", which contradicts the missing file. Stays reference only. 27 components. Some use Nucleo icon packages, so check their icon license too.
- **Planes**: same split: 142 total, 10 free, 132 Pro. $99 launch price, "$199 after Oct 18" (tomorrow); irrelevant under no-paid. New finding: the 10 free items are "public", but the terms only grant a licence for Pro. Free items carry **no OSS license text**. Treat them as reference or use with caution. The gated registry returns 404 without a key (verified).
- **Arc UI**: grew to 167 components + 91 blocks. Free = **112 components + 22 blocks under MIT** (Copyright 2026 Elia Kuratli; LICENSE in the public repo; license page updated 26 Sep). Pro is $129/yr or $199 lifetime, and teams $599 once or $349/yr. Free now includes a command palette block, shortcut recorder, 4 theme switches and image compare. Dock, Lightbox gallery, Keycap keyboard and Typewriter terminal are Pro.

## 2. Componentry (componentry.dev)

Free, MIT, shadcn registry `npx shadcn@latest add @componentry/<name>` or `https://componentry.dev/r/<name>.json`, plus MCP. Deps per item: none (canvas), `framer-motion`, `gsap`, `lenis`, or three/r3f.

**All 54 free components.**
Text: Velocity Scroll (scroll-speed marquee that skews), Letter Cascade, Text Repel (letters flee cursor), Text Morph (fluid label swap), Flipping Word Swap (GSAP char flip), Kinetic Text Reveal (blur + stagger), Particle Typography, Annotated Text (hand-drawn marks), Signature (handwriting draw-on, opentype.js).
UI: Lens Clock, Music Player, Mac Keyboard (keys light on real keydown, optional sound), Magnetic Dock (macOS dock, 4 positions), Eye Tracking, Flight Status Card, Github Calendar, Split Flap Display, Newsletter Bookshelf, Case Study Flip Stack (cards fold up on scroll), Sticky Scroll Cards (lenis), Scroll Choreography, Scroll Split Card, Layered Stack (GSAP), Orbit Card Stack, Collection Surfer, Wheel Carousel, Spiral 3D Slider, Liquid Glass Carousel, Hover Transition (8 hover swaps: wipe, ripple, parallax, curtain, diagonal, morph, strips, slide), Ripple Transition.
Backgrounds: Animated Gradient, Grain Gradient, Hero Geometric, WebGL Liquid, Silk Aurora, Aurora Flow, Closing Plasma, Liquid Chrome, Prism Gradient, Spectral Ribbon, Dither Prism Hero (three.js), Circuit Board.
Effects: Image Trail (GSAP), Pixel Image Trail (cursor-painted squares reveal an image), Infinite Image Field, Image Ripple Effect, Fisheye Infinite Grid, Scroll Tilted Grid, Dither Gradient (Bayer canvas), Dithered Logo (image to dithered particle field, cursor ripples), Magnet Lines, Pixel Canvas (grid lights up under cursor, decays, color ramp), Matrix Rain, ASCII Effect (image/flow/glitch, Bayer or Floyd-Steinberg dither).

**Shortlist** (all MIT, no paid).
- Pixel Canvas `/docs/components/pixel-canvas`: no deps, canvas. Props `gap`, `speed`, `colors[]`, `variant` (default, trail, glow). Restyle: set `gap` to the pixel unit (4 or 8), feed pastel tokens, drop "glow". Best native fit in all five libraries.
- Pixel Image Trail `/docs/components/pixel-image-trail`: no deps, reduced-motion aware. Use as the project tile hover: the cover image appears in pixel squares under the cursor. Mobile needs a tap fallback.
- Hover Transition `/docs/components/hover-transition`: no motion dep (clsx, tailwind-merge), keyboard focusable. Use "strips" or "wipe" with `steps()` easing. Skip "ripple", "morph" and "parallax".
- Dither Gradient + ASCII Effect: no deps. Pastel two-stop dither as section backgrounds; ASCII "image" variant for the art section intro only. Never dither the work itself (PLAN thesis).
- Dithered Logo: no deps. Could render the monogram or cat silhouette as a dithered field in the footer.
- Split Flap Display: no deps. Status line ("OPEN TO ROLES"), project counters. Swap fonts for the pixel face.
- Mac Keyboard: lucide-react, listens to real keydown. Base for the `?` overlay where pressed keys light up. Redraw keys as pixel keycaps; remove the Mac-specific look.
- Magnetic Dock: framer-motion, tabIndex + reduced motion. Only if a dock is wanted; the magnification is the macOS cliche. Restyle as fixed-size keycaps that step up 1 unit on hover.
- Eye Tracking: only if the cat keeps pupils (PLAN.md "look" state). The brief says faceless, so likely skip.

**Generic or rule-breaking, skip**: every aurora/plasma/chrome/silk/liquid/prism background, Matrix Rain, Liquid Glass Carousel. Scroll Tilted Grid, Orbit Card Stack, Spiral 3D Slider and Wheel Carousel break the no-tilt rule. Velocity Scroll skews text (close to tilt).

**Site patterns to borrow**: a split doc page with scrolling text on the left and a **sticky live preview on the right**. Variant chips sit under the preview, with Reload, Expand and View Source in its corner. This is the case-study template: narrative left, Figma prototype or video stage right, with chips for Before / After / Prototype. The homepage groups items by category (Featured, Text, Components, Heroes, Effects). "Collections" pages group items by effect. ⌘K search.

## 3. Space UI (spaceui.one)

Free core MIT (Terms Section 2). Pro $99/yr or $129 lifetime. Base UI + Tailwind v4 + `motion`, Tabler/Lucide icons. Install `pnpm dlx shadcn@latest add @spaceui/<item>`. Also MCP, llms.txt and per-component markdown.

**Free primitives (61, all free)**: Accordion, Alert, Alert Dialog, Aspect Ratio, Autocomplete, Avatar, Badge, Breadcrumb, Button, Calendar, Card, Checkbox, Checkbox Group, Collapsible, Combobox, Command, Context Menu, Date Picker, Dialog, Drawer, Empty, Field, Fieldset, Form, Frame, Group, Input, Input Group, Kbd, Label, Link, Menu, Menubar, Meter, Navigation Menu, Number Field, OTP Field, Pagination, Popover, Preview Card, Preview Link Card, Progress, Radio Group, Segmented Control, Scroll Area, Select, Separator, Sheet, Sidebar, Skeleton, Slider, Spinner, Switch, Table, Tabs, Textarea, Toast, Toggle, Toggle Group, Toolbar, Tooltip. Also 61+ hooks (useKeyPress, useIsMac, useScrollTo, usePrefersTheme, useLocalStorage).

**Free components** (not marked PRO): Avatar Extended, Avatar Group, Frost Blurred (edge frost), Bouncy Accordion, Detachable Accordion, Tick Slider, Liquid Switch, Theme Toggle, Liquid Sortable List, Interactive Checklist, Team Roster Selector, Member Selector, Slide To Confirm, Squircle, Interest Picker, Voice Chat Widget, Badge Squircle, Morphing Area, User Presence Avatar, Event Calendar, Tournament Bracket, Status Badge, GitHub Activity, Section Scrollspy, Liquid Metal Border, Morph Icon, Adaptive Density Grid, Dirt Carousel, Doodle Callout (hand-drawn arrow + label), Gooey Experiments, Pin List, Phone Input, Gradient File Upload, Date Selector, Rating, Filters, Resizable, Scrollspy, Data Grid, Sortable (dnd-kit), Kanban, Timeline, Notification List, Icon Stack, Image Dark (light/dark image swap, no layout shift). Buttons: Button Squircle, Glass Button, Like Button. Text: Handle Reel, Fluid Countdown, Words Preloader, Blur Reveal Text, Morphing Text, Flip Text, Gooey Text Reveal (GSAP), Scroll Text Reveal, Textmoji, Textmoji Animated. Orbs: Thinking, Loading (matrix pixel grid loader), Smooth, Bloop. Backgrounds: Bubble, Gradient. Shaders: Cloud, Paper Shader, Mesh Gradient. Blocks: Interactive Grid Hero, Sign In Page, Card Info, Interactive Fun Facts, Eleven Labs Landing, Showcase Gallery. Carousels: Dither, Liquid Gooey, Prism, Lens. Templates: AI Chat Workspace, Immersive Lens Portfolio.
**PRO (avoid)**: Smooth Slider, Slosh Slider, Morphing Command Bar, Morphing Search Pill, Rainbow Glow Border, Silk Border, Chroma Palette, Autoscale Input, Pixel Fill Button, Aurora/Rainbow Glow Buttons, Scroll Manifesto, Scatter Text, Pixel Reveal Text, Pixel Reveal Image, Heat Shade, Silk Gradient, Silk Flare, the Fluid/Liquid shader set, Community Wall, Stats, Velocity Hover Preview, Stats Dashboard.

**Shortlist** (all MIT).
- Command `/primitives/command` (`@spaceui/primitives-command`): Base UI, lucide, `@usespaceui/squircle`; pulls Autocomplete + Kbd. Keyboard-first, live search announcements, `CommandShortcut` slots. Restyle: drop squircle, 2px hard border + offset shadow, pixel font for group labels only, `steps(4)` open.
- Kbd `/primitives/kbd`: no deps, 724 B. Becomes the pixel keycap used in nav hints, the palette and the cat's tips.
- Section Scrollspy `/components/section-scrollspy`: motion. Mark sections `data-page-section` + `h2`, with an optional `portal`. Restyle the floating bar into a stepped pixel ruler; the cat can perch on the active tick.
- Theme Toggle `/components/theme-toggle`: motion, next-themes, Tabler. Uses View Transition with circle, circle-blur, rectangle and polygon reveals. Use "polygon" or "rectangle" with a stepped clip (or a dithered mask on `::view-transition-new`) so the swap reads as a pixel wipe. Skip blur.
- Showcase Gallery `/blocks/showcase-gallery`: motion + squircle. Justified rows of stills and looping videos. The focused tile springs forward and only it plays video; mouse, touch, Tab and Escape all work; video metadata loads lazily. Best free fit for /art. It has no fullscreen lightbox: add one with Dialog + a View Transition. Remove squircle and set spring bounce to 0.
- Tabs / Segmented Control: Base UI. For /art categories (Illustration, Comics, Graphic, Motion) and the case-study media chips.
- Tooltip / Popover / Toast: Base UI. Build the cat speech bubble on Popover (anchored, dismissible) with a 9-slice pixel border; use Toast for "Email copied".
- Doodle Callout: motion. A one-time "press ? for shortcuts" pointer near the nav; swap the hand-drawn path for a stepped pixel arrow.
- Loading Orb (matrix pixel grid): motion. Possible loading state while a Figma embed boots.
- Interactive Grid Hero block: motion. Square cell field; keep `shape="square"`, since rounding cells is anti-pixel. Overlaps Pixel Canvas; pick one.
- Image Dark: swaps light/dark artwork sources with no hydration flash. Useful for pastel light/dark variants of thumbnails.

**Generic, skip**: orbs, squircles, gooey, liquid/silk/mesh shaders, Dither/Lens/Prism carousels (3D, template-y), Eleven Labs Landing.

**Site patterns to borrow**: a dense left sidebar of category headers with **item counts** and inline PRO badges. Prev/Next and "Copy Page" on every item. A meta line under the title (size, updated date): for her, role, year, type. A right "On this page" TOC. A theme toggle **inside each preview**, plus Favorites. ⌘K search in the top bar.

## 4. Skecher UI (skecher-ui.com)

No license file, so **reference only, do not copy code**. Shadcn registry `npx shadcn@latest add CoDesign-Spa27/skecher-ui/<name>`. All motion-based.
Components (27): Cookie Consent, 3D Wheel Carousel, Apple Mail Tabs, Add To Cart, AI Chat Box, Animated Book (3D book opens on hover/focus), AI Orb, Dither Credit Card, Dock, Expandable Mobile Nav, Gooey Toolbar, Image Density Grid, Image Glide (viewer with thumbnail rail), Interactive Grid Hero, Liquid Glass Social, Liquid Morphology Slideshow, Magazine Scroller (velocity poster scroller), Morphing Action Dock, Morph Menu, Morph Stack, Scroll Reveal Text, Sliding Panel (direction-aware), Snap Text, Spring Slider, Streaming Text, Text Morphing, Velocity Tabs.
**Ideas worth rebuilding from scratch**: Animated Book (the comics section as a book that opens on focus), Image Glide (thumbnail rail for comic pages), Sliding Panel (direction-aware prev/next between case studies), Expandable Mobile Nav (bottom-anchored nav for phones).
**Site patterns to borrow, the strongest of the five for "each project gets its own space"**: every component gets a **full-bleed stage** with a breadcrumb top-left and a collapsible sidebar. A floating "super island" at the bottom holds the install command plus a details drawer that Escape closes. There is also an isolated `/preview/<slug>` route and a Replay button. Map it to: a full-bleed project stage, with a bottom island for role, year, prev/next and "read the case study".

## 5. Planes (useplanes.com)

132 Pro behind a gated registry ($99 now, $199 after 18 Oct). 10 free, installable by URL `npx shadcn add https://useplanes.com/r/<name>.json`. Free items have **no stated license**, so they are reference or use-with-caution. Deps: `motion`, sometimes lucide.
**Free (10)**: Thinking Loader (AI phase pill), Cover Flow (3D, drag/wheel/keys, optional audio), Segmented Control (stretching pill), Number Stepper, OTP Input, Ripple Grid (nodes lit by wavefronts), Pendulum Wave (physics ornament), Smooth Stagger Text, Cinematic Text (blur-down film title), Scroll Stage (pinned stage exposing 0 to 1 progress).
**Pro items that match the brief, so build our own instead**: Command Palette, Keyboard, Marquee, Photo Lightbox, Hover Reveal, Link Preview, Dither Field, Dither Renderer, ASCII WebGL, Split-Flap Board, Retro Music Player, Progressive Blur, Receipt Printer, Physical Knob.
**Maybe**: Ripple Grid as a reference for a pixel "ping" when the cat lands. Scroll Stage only if one scrubbed moment is ever wanted (PLAN says native scroll). Its Segmented Control is well built (keyboard arrows, reduced motion), but the unclear license makes Space UI or Arc the safer pick.
**Site patterns to borrow**: a full-bleed centred stage and a sidebar where each item has a **ruler tick**, which reads like a minimap. Pixel version: ticks become 1-unit squares, and the cat walks the ruler. A bottom floating toolbar (Usage, Props, Copy), ⌘K, and "Copy prompt / Open in AI". Every page returns **markdown for `Accept: text/markdown`** plus `llms.txt`. A plain-text case-study endpoint is a cheap win for recruiters who paste links into AI tools.

## 6. Arc UI (uiarc.dev)

Free core MIT (112 components, 22 blocks). Install `npx shadcn@latest add https://uiarc.dev/r/<name>.json` or register the `@uiarc` namespace. Needs `arc-foundation` tokens once. Styling is **CSS modules + CSS variables, not Tailwind**; dark mode via `data-theme="dark"` on `<html>`; 8 accents. Deps: `motion`, lucide, some Radix. Every item has markdown docs covering keyboard, a11y, motion, and when not to use it.

**Free components (112)**, grouped. Actions: button, action-button, split-button, button-group, floating-button-group, expanding-button-group (label grows on hover/focus), dropdown-menu, context-menu, copy-button, icon-morph, confirm-morph, hold-to-confirm, swipe-actions, reactions. Theme: theme-switch, theme-switch-eclipse, theme-switch-split, theme-switch-rise. Inputs: input, textarea, select, combobox, morph-select, multi-select, checkbox, switch, radio-group, radio-cards, segmented-control, chip-group, number-field, password-field, password-strength, search-field, expanding-search, tag-input, inline-edit, mention-input, phone-input, money-input, file-dropzone, shortcut-recorder, slider, elastic-slider, calendar, date-picker, date-range-picker, time-picker, color-picker, signature-pad, rich-text-editor, billing-toggle. Disclosure and overlays: accordion, dialog, drawer, bottom-sheet, popover, hover-card, tooltip, tabs, expandable-card, expandable-text, scroll-area, resizable-panels, breadcrumb, pagination, stepper, user-menu, tree-view. Feedback: alert, toast, toast-stack, progress, usage-meter, skeleton, empty-state, badge, cookie-consent, announcement-bar, countdown. Data: card, metric-card, sortable-data-table, filter-toolbar, json-viewer, code-block, sparkline, gauge, animated-counter, bar-chart, line-chart, donut-chart, streamgraph, brush-chart, ridgeline, treemap, waffle-chart, slope-chart, activity-heatmap, timeline. Media: image-compare, carousel, card-stack (throw + undo). Text: text-reveal, in-view-title, text-morph, text-shimmer, slot-text. Social: avatar, avatar-group, chat-thread, comment-thread.
**Free blocks (22)**: signup-form, logo-marquee, plan-comparison, command-palette, notification-center, file-upload, otp-input, changelog-feed, sign-in, page-header (folds to compact bar with tabs), empty-states, login-centered, site-header, site-footer, hero-section, faq-section, contact-section, blog-grid, comparison-table, stats-band, cta-section, newsletter-signup.
**Pro (avoid)**: Dock, Morph nav, Liquid/Glass tab bar, Lightbox gallery, Photo grid, Cover flow, Keycap keyboard, Typewriter terminal, Dot grid, Gravity well, Sticker peel, Page curl, Layout morph, Settings command, plus 55 components and 69 blocks in total.

**Shortlist** (all MIT).
- Shortcut recorder `/components/shortcut-recorder`: motion, lucide. Use only the display parts (ShortcutKbd, ShortcutKeys, ShortcutList searchable cheatsheet) for the `?` overlay. `matchesShortcut` + `usePlatform` handle ⌘ vs Ctrl.
- Command palette block `/blocks/command-palette`: motion, lucide. The most complete free palette (search, groups, shortcuts). Use it as the behaviour reference if Space UI Command feels thin.
- Theme switch (+ rise, split, eclipse): motion, lucide. "Split" (opens from a centre seam) becomes a strong pixel wipe if the seam steps in 8px bands.
- Image compare: drag divider, before/after. Meets the review note that before/after must visually differ. Pixel handle, hard 2px line.
- Timeline + activity-heatmap: experience section. The heatmap ("one square per day") is already pixel-shaped, so pastel ramp it.
- Expanding button group / floating button group: a nav where the focused keycap grows to show its label ("W Work"). Teaches shortcuts without a legend.
- Logo marquee block: lucide only, includes a **pause control** (a11y). Use for clients/tools.
- Tabs, segmented-control, tooltip, popover, toast, toast-stack, hover-card: fine, but prefer Space UI equivalents to keep one primitive layer.
- Slot-text: numbers on reels (stats like "30,000+ views"), which reads more arcade than a blur reveal.

**Site patterns to borrow**: the sidebar opens with an **All / Free / Pro / More filter** above category groups with counts. For her: All / Product / Art / Assessments. Previews carry a **"Live · keyboard ready" badge**, a teaching device to copy. A **Fit / Mobile / Fullscreen** toolbar on every preview is the exact control set for Figma prototype embeds. "What's new · 8 new" pins to the sidebar foot. An **Appearance popover with accent choices** could become a pastel accent picker for visitors (on brand, playful, cheap). Arc's agent rules also ban em dashes and decorative glows, so its defaults already lean her way.

## 7. Restyle recipe for pixel art (applies to every pick)

1. One pixel unit (4px, art at 2x = 8px). Every radius 0, border 2px, shadow = hard offset (2px 2px 0) in a darker pastel, never blur.
2. Chrome motion uses `steps(n)` or 2 to 4 frame keyframes. Content motion (opening a project, gallery focus) stays smooth, eased out, no bounce (motion bar memory). Set every spring `bounce: 0`.
3. Remove squircle, glass, backdrop-filter, gradient borders, glows. Replace icons (Tabler/Lucide) with a pixel icon set at integer scale; `image-rendering: pixelated` on raster sprites only.
4. Canvas items (Pixel Canvas, Dither Gradient, ASCII, Dithered Logo): cell size = pixel unit, colors from theme tokens, re-read tokens on theme change, pause offscreen and on `visibilitychange`.
5. Pixel font only for headings, keycaps, labels and the cat's bubble. Body and case-study text stay in a legible sans (PLAN thesis).
6. Keep each library's reduced-motion branch. Test light and dark, since pastel on dark needs contrast checks.

## 8. Gaps nobody covers for free (build in-house)

- Fullscreen lightbox for art (all free options lack it; Planes and Arc lightboxes are Pro). Build from Dialog + View Transition + arrow keys.
- Figma prototype embed: a click-to-load facade (poster + "Play prototype" keycap), then an iframe, with Arc's Fit / Mobile / Fullscreen control idea. Keeps Lighthouse clean.
- Video: native `<video>` with poster, muted loop on hover in tiles, and controls in the case-study stage.
- Global hotkeys (1 to 6, W A E C, R, T, ?, arrows, Esc): a small hook on top of Space UI `useKeyPress` / `useIsMac`, ignoring keys while typing in inputs.
- The cat and its perches (custom canvas, per PLAN.md).
