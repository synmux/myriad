---
version: "alpha"
name: "System Interface - Skeuomorphic Clean"
description: "System Interface Card Component is designed for building reusable UI components in modern web projects. Key features include reusable structure, responsive behavior, and production-ready presentation. It is suitable for component libraries and responsive product interfaces."
colors:
  primary: "#5EBD3E"
  secondary: "#FFB900"
  tertiary: "#F78200"
  neutral: "#000000"
  background: "#000000"
  surface: "#FFFFFF"
  text-primary: "#FFFFFF"
  text-secondary: "#A3A3A3"
  border: "#C3C5C8"
  accent: "#5EBD3E"
typography:
  display-lg:
    fontFamily: "Instrument Serif"
    fontSize: "63px"
    fontWeight: 400
    lineHeight: "63px"
    letterSpacing: "-0.025em"
  body-md:
    fontFamily: "DM Mono"
    fontSize: "10.5px"
    fontWeight: 300
    lineHeight: "14px"
spacing:
  base: "5.25px"
  sm: "1px"
  md: "2px"
  lg: "3.5px"
  xl: "5.25px"
  gap: "1px"
  card-padding: "28px"
  section-padding: "28px"
components:
  card:
    rounded: "14px"
    padding: "28px"
---

## Overview

- **Composition cues:**
  - Layout: Grid
  - Content Width: Bounded
  - Framing: Glassy
  - Grid: Strong

## Colors

The color system uses dark mode with #5EBD3E as the main accent and #000000 as the neutral foundation.

- **Primary (#5EBD3E):** Main accent and emphasis color.
- **Secondary (#FFB900):** Supporting accent for secondary emphasis.
- **Tertiary (#F78200):** Reserved accent for supporting contrast moments.
- **Neutral (#000000):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Background: #000000; Surface: #FFFFFF; Text Primary: #FFFFFF; Text Secondary: #A3A3A3; Border: #C3C5C8; Accent: #5EBD3E

## Typography

Typography pairs Instrument Serif for display hierarchy with DM Mono for supporting content and interface copy.

- **Display (`display-lg`):** Instrument Serif, 63px, weight 400, line-height 63px, letter-spacing -0.025em.
- **Body (`body-md`):** DM Mono, 10.5px, weight 300, line-height 14px.

## Layout

Layout follows a grid composition with reusable spacing tokens. Preserve the grid, bounded structural frame before changing ornament or component styling. Use 5.25px as the base rhythm and let larger gaps step up from that cadence instead of introducing unrelated spacing values.

Treat the page as a grid / bounded composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Grid
- **Content width:** Bounded
- **Base unit:** 5.25px
- **Scale:** 1px, 2px, 3.5px, 5.25px, 7px, 10.5px, 11.72px, 14px
- **Section padding:** 28px
- **Card padding:** 28px
- **Gaps:** 1px, 5.25px, 10.5px, 21px

## Elevation & Depth

Depth is communicated through glass, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as glass first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Glass
- **Borders:** 1px #FFFFFF; 0.5px #C3C5C8
- **Shadows:** rgba(0, 0, 0, 0.6) 0px 1px 3px 0px, rgba(0, 0, 0, 0.5) 0px -1px 2px 0px inset; rgba(255, 255, 255, 0.4) 0px 1px 1px 0px inset, rgba(0, 0, 0, 0.3) 0px -1px 2px 0px inset, rgba(0, 0, 0, 0.4) 0px 2px 4px 0px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.4) 0px 12px 24px 0px
- **Blur:** 4px

### Techniques

- **Gradient border shell:** Use a thin gradient border shell around the main card. Wrap the surface in an outer shell with 2px padding and a 31.5px radius. Drive the shell with linear-gradient(rgb(255, 255, 255) 0%, rgb(163, 163, 163) 100%) so the edge reads like premium depth instead of a flat stroke. Keep the actual stroke understated so the gradient shell remains the hero edge treatment. Inset the real content surface inside the wrapper with a slightly smaller radius so the gradient only appears as a hairline frame.

## Shapes

Shapes rely on a tight radius system anchored by 3.3485px and scaled across cards, buttons, and supporting surfaces. Icon geometry should stay compatible with that soft-to-controlled silhouette.

Use the radius family intentionally: larger surfaces can open up, but controls and badges should stay within the same rounded DNA instead of inventing sharper or pill-only exceptions.

- **Corner radii:** 3.3485px, 5.25px, 14px, 29.5px, 31.5px, 9999px

## Components

Reuse the existing card surface recipe for content blocks.

### Cards and Surfaces

- **Card surface:** border 0px solid rgb(229, 231, 235), radius 14px, padding 28px, shadow rgba(255, 255, 255, 0.04) 0px 1px 2px 0px inset, rgba(0, 0, 0, 0.6) 0px -2px 6px 0px inset.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do

- Do use the primary palette as the main accent for emphasis and action states.
- Do keep spacing aligned to the detected 5.25px rhythm.
- Do reuse the Glass surface treatment consistently across cards and controls.
- Do keep corner radii within the detected 3.3485px, 5.25px, 14px, 29.5px, 31.5px, 9999px family.

### Don't

- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't mix unrelated shadow or blur recipes that break the current depth system.
- Don't exceed the detected moderate motion intensity without a deliberate reason.

## Motion

Motion feels controlled and interface-led across text, layout, and section transitions. Timing clusters around 2000ms and 150ms. Easing favors ease and 1). Hover behavior focuses on px changes.

**Motion Level:** moderate

**Durations:** 2000ms, 150ms, 500ms

**Easings:** ease, 1), cubic-bezier(0.4, 0, 0.2, cubic-bezier(0.25

**Hover Patterns:** px
