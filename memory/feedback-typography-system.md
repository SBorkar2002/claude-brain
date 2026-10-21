---
name: feedback-typography-system
description: "Font families, type scale, color tokens, spacing, and component specs for the DORA video — sourced directly from Figma file oCrvQrJRk2n7uyecM6imK8"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d34891d5-bf3d-45da-a44f-bd55ac4ba270
---

## Font families — five families, fixed roles

| Family | Role | Notes |
|---|---|---|
| `'Mona Sans'` | Section/scene titles, large KPI numbers | ExtraBold weight primarily. The main display font. |
| `'Plus Jakarta Sans'` | Category labels, ELITE badge, stat units, STATUS labels, stat descriptions | Bold or Medium. UI chrome layer. |
| `'Geist'` | Table body text, row content | Medium weight. Readable data layer. |
| `'Geist Mono'` | PR numbers, durations, badge text, notification timestamps, terminal | Medium weight. All code-like values. |
| `'JetBrains Mono'` | Chart axis labels only | Regular, small size. |

**Why:** Extracted from Figma nodes directly. These aren't guidelines — they're the actual fonts in the file.

---

## Type scale (from Figma)

| Element | Family | Size | Weight | Color | Other |
|---|---|---|---|---|---|
| Category label (e.g. "SPEED") | Geist SemiBold | 12px | 600 | `#666` | uppercase, tracking 0.55px |
| Scene title (e.g. "Lead time for changes") | Mona Sans | 36px | ExtraBold | `#0d0d0d` | line-height 44px, tracking -0.88px |
| Scene subtitle / description | Plus Jakarta Sans | 22px | Medium | `#888` | |
| KPI big number | Mona Sans | 76px | ExtraBold | `#0d0d0d` | line-height 72px, tracking -1.44px |
| KPI unit label (e.g. "min median") | Plus Jakarta Sans | 20px | Medium | `#6b7280` | tracking -0.88px |
| ELITE badge text | Plus Jakarta Sans | 11px | Medium | `#fff` | |
| Table header labels | Geist Bold | 10px | Bold | `#666` | uppercase, tracking 0.45px |
| Table row — PR number | Geist Mono | 14px | Medium | `#ff6b6b` | CORAL — signals slow/blocked |
| Table row — title text | Geist | 16px | Medium | `#0d0d0d` | |
| Table row — duration | Geist Mono | 14px | Medium | `#0d0d0d` | text-right |
| Badge text | Geist Mono | 12px | Medium | `#fff` | |
| Chart annotation text | Plus Jakarta Sans | 14px | Medium | `#666` | |
| Chart axis labels | JetBrains Mono | 11px | Regular | `#666` | |
| Stat card — big number | Mona Sans / Geist Bold | 64–76px | ExtraBold/Bold | `#111` | |
| Stat card — label | Plus Jakarta Sans | 14px | Medium | `#666` | |
| STATUS label | Plus Jakarta Sans | 12px | Bold | `#03a6cf` | TEAL, uppercase |
| Stat card — description | Plus Jakarta Sans | 14px | Medium | `#111` | text-center |
| Notification title | Geist Bold | 14px | Bold | `#fff` | line-height 21px |
| Notification body | Geist Regular | 12.5px | Regular | `#fff` | line-height 18.75px |
| Notification timestamp | Geist Mono | 11px | Medium | `#c1c3c3` | |

---

## Color tokens (from Figma)

| Token | Hex | Usage |
|---|---|---|
| Near-black | `#0d0d0d` | Primary text — titles, row content, KPI numbers |
| Dark text | `#111` | Stat card numbers, some title variants |
| Mid-gray | `#666` / `#6b7280` | Secondary labels, subtitles, table header, annotations |
| Light gray | `#888` | Scene subtitle/description text |
| Muted | `#9ca3af` / `#c1c3c3` | Timestamps, notification timestamps |
| TEAL | `#03a6cf` | STATUS label, elite highlights, success indicators |
| CORAL / Red | `#ff6b6b` | PR numbers (slow), blocked badges, chart bars (below threshold) |
| Amber | `#f5a623` | "in review" / "waiting" badge bg |
| Success green | `#06d6a0` | success-badge background |
| Scene bg | `#ffffff` | All content scenes (white, not off-white) |
| Stat card bg | `#f9f9f9` | Stat card background |
| Border | `#e5e7eb` | All dividers — table rows, cards, scene border |
| Notification bg | `#797b7a` | Notification card background |
| Notification border | `#888c8c` | Notification card border |
| ELITE badge bg | `#0d0d0d` | Black pill badge |
| Terminal bg | `#1c1c1e` | Terminal window only |

---

## Component specs (from Figma)

### Scene layout
- **Canvas size:** 1280 × 720px
- **Scene background:** `#ffffff` with `1px solid #e5e7eb` border and `drop-shadow: 0px 8px 12px rgba(0,0,0,0.05)`
- **Content margins (table/header scenes):** 79px left and right → content width = 1122px
- **Content margins (chart scenes like 4B):** 64px left
- **Header block top:** 63px from top
- **Scene subtitle top:** 157px from top (in table scenes)
- **Table top:** 213px from top (in table scenes)

### Header component (1122px wide)
- Height: 118px
- Layout: space-between (title-block left, kpi-block right)
- **title-block:** flex-col, gap 10px
  - Category label: Geist SemiBold 12px `#666`, uppercase, tracking 0.55px
  - Title: Mona Sans ExtraBold 36px `#0d0d0d`, line-height 44px, tracking -0.88px
- **kpi-block:** width 329px, flex-col, gap 12px, items-end
  - ELITE badge row → KPI number row

### ELITE badge
- Background: `#0d0d0d`
- Border-radius: 100px (pill)
- Padding: 10px top/bottom, 16px left/right
- Font: Plus Jakarta Sans Medium, 11px, white

### KPI number
- Font: Mona Sans ExtraBold, 76px, `#0d0d0d`, line-height 72px, tracking -1.44px
- Unit: Plus Jakarta Sans Medium, 20px, `#6b7280`, tracking -0.88px
- Gap between number and unit: 12px (flex row)

### Table
- Table header: height 44px, border-bottom `1px solid #e5e7eb`, gap 16px between columns
- Table row: height 64px, border-bottom `1px solid #e5e7eb`, gap 16px between columns
- Column widths: PR=72px, Title=flex-1, Duration=140px, Status=120px

### Status badge (in table rows)
- Container: height 28px, width 120px, justify-end
- Pill: border-radius 100px, padding 6px top/bottom, 12px left/right
- Colors: "in review"/"waiting" → `#f5a623`; "blocked" → `#ff6b6b`
- Font: Geist Mono Medium, 12px, white

### Stat card
- Background: `#f9f9f9`
- Border-radius: 24px
- Shadow: `0px 11px 22.45px rgba(110,110,128,0.26)`
- Padding: 50px top/bottom, 20–30px left/right
- Gap between children: 25–45px
- Width in 4B scene: 292px, positioned at left 936px, top 133px

### Notification card
- Background: `#797b7a`
- Border: `1px solid #888c8c`
- Border-radius: 16px
- Shadow: `0px 8px 13px rgba(40,30,20,0.17)`
- App icon: white bg, border-radius 7px, size 39×39px, icon 31×31px
- Content: left 15px, top 14px, gap 16px between icon and text

### Success badge
- Background: `#06d6a0`
- Border-radius: 79px (circle for 106×106px size)
- Size: 106×106px
- Check icon: 78×78px

### Chart scenes (e.g. 4B)
- Chart group: left 64px, top 306px, width 824px
- Bar chart bars: width 39px each, gap 21px between bars (starts at 0, next at 60px)
- Axis labels: JetBrains Mono Regular 11px `#666`, bottom of chart
- Annotation text: Plus Jakarta Sans Medium 14px `#666`, below chart

[[feedback-caption-meta-rules]]
[[feedback-animation-prefs]]
