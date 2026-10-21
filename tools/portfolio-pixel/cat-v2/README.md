# Cat v2

The mascot cat. **Approved and live since 17 Oct**: the v2 art is in the Cat component set 8:159, which every instance uses. v1's source (`../cat/`) is kept for the record. Since her 17 Oct note, v2 has a fuller, squishier body (round rump, plump tail, 5 px legs, soft pear sit); research.md section 9 explains the changes.

## Files

- `audit.md`: every distortion in v1, frame by frame, and the fix for each one.
- `research.md`: the pixel-art rules applied, with sources, plus the self-critique log. `research-raw.md` has the full notes, and `refs/` has the study images (including her reference cat).
- `sprites.py`: the source. 48x48, hand-drawn ASCII stamps, with a legend in the docstring. `TIMINGS` drives the Figma After-delays.
- `render.py`: writes `preview/`: sheet-4x.png (both colourways), strip-1x.png and strip-2x.png (true size), one GIF per state per colourway, and frames.json.
- `runs.py`: merged rectangles per colour layer (`preview/runs.json`), used to build the Figma vectors.
- `preview/compare-v1-v2.png`: v1 and v2 side by side, the same layout as the Figma comparison.

```bash
cd ~/Documents/career/portfolio-pixel/cat-v2 && python3 render.py && python3 runs.py preview/runs.json
```

## Figma (file hfj2locm0N5bssdEU6NaoH, page "Pixel portfolio · v1")

| Node | Id | Where |
|---|---|---|
| Comparison "Cat · v1 vs v2" (flow start "Cat v1 vs v2") | 35:564 | x 5200 |
| v2 playground (flow start "Cat v2 playground") | 34:731 | x 6960 |
| Component set "Cat v2" (63 variants, 144x144, 3 px per pixel) | 31:706 | x 6960, y 2100 |
| "Cat v2 · Walk lane" | 34:709 | x 8560, y 2100 |
| Motion review page (private artifact) | https://claude.ai/artifact/V49VCbcdBkAtMHav3f29yx | `motion.html`, built from `motion.template.html` |

Frame counts: Sit 4, Idle 5, Walk 4, Look 6, Inspect 8, Yawn 5, Sleep 4, Peek 7, React 5, Fall 8 (page-load spin loop), Land 7 (lands, beat, stands, sits). Layers per variant are body, eyes, pupils, shine, mouth, mouth-inner, zzz and heart, each a vector bound to cat/*.

## The swap (done 17 Oct)

Done as planned below. The live set 8:159 now sits at x 6960, y 2100 with all 63 variants. Instances were re-seated (up 24, peek up 16, left 8). The v1 sprite sheets (12:246, 12:558) and the v1 cells of the comparison were detached first, so they keep the old art. 31:706, 34:731 and 34:709 are staging copies marked superseded. Future cat edits go into 8:159.

### Original plan

Replace the vectors inside the 8:159 variants so every existing instance updates. Two things differ from v1 and have to be handled:

1. **Size:** v2 variants are 144x144 (48 px at 3 px), v1 are 128x128. Resize each 8:159 variant to 144. Then move every existing Cat instance up 16 px and left 8 px, so feet stay on their floor and the cat stays centred (instances keep their top-left corner).
2. **Frame counts:** v2 adds Sit 4, Idle 5, Inspect 5 to 8, Yawn 5, Sleep 3 and 4, React 4 and 5, and the new Fall and Land states. Add those variants to 8:159 with the same naming, then rewire the After-delay chain from `TIMINGS` (the v2 set 31:706 already has the right chain to copy).

Then rebuild the sprite sheets 12:246 and 12:558 from v2, or retire them in favour of the comparison frame.
