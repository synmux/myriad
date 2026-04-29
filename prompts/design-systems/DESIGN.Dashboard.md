---
version: "alpha"
name: "Analytics Dashboard - Remixed"
description: "Analytics Remixed Pricing Section is designed for comparing plans and supporting conversion decisions. Key features include plan comparison blocks and conversion-oriented actions. It is suitable for subscription pricing pages and plan comparison experiences."
colors:
  primary: "#34D399"
  secondary: "#3C82FF"
  tertiary: "#3B82F6"
  neutral: "#050505"
  background: "#050505"
  surface: "#FFFFFF"
  text-primary: "#FFFFFF"
  text-secondary: "#D4D4D4"
  border: "#FFFFFF"
  accent: "#34D399"
typography:
  display-lg:
    fontFamily: "Inter"
    fontSize: "42px"
    fontWeight: 600
    lineHeight: "42px"
    letterSpacing: "-0.025em"
  body-md:
    fontFamily: "Inter"
    fontSize: "10.5px"
    fontWeight: 400
    lineHeight: "14px"
rounded:
  sm: "5.25px"
  lg: "7px"
spacing:
  base: "5.25px"
  sm: "1px"
  md: "1.75px"
  lg: "3.5px"
  xl: "5.25px"
  gap: "3.5px"
  card-padding: "9.63px"
  section-padding: "56px"
components:
  button-primary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: "5.25px"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: "5.25px"
  button-link:
    textColor: "{colors.surface}"
    typography: "{typography.body-md}"
    rounded: "0px"
    padding: "0px"
  card:
    rounded: "{rounded.lg}"
    padding: "9.63px"
---

## Overview

- **Composition cues:**
  - Layout: Grid
  - Content Width: Full Bleed
  - Framing: Glassy
  - Grid: Strong

## Colors

The color system uses dark mode with #34D399 as the main accent and #050505 as the neutral foundation.

- **Primary (#34D399):** Main accent and emphasis color.
- **Secondary (#3C82FF):** Supporting accent for secondary emphasis.
- **Tertiary (#3B82F6):** Reserved accent for supporting contrast moments.
- **Neutral (#050505):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Background: #050505; Surface: #FFFFFF; Text Primary: #FFFFFF; Text Secondary: #D4D4D4; Border: #FFFFFF; Accent: #34D399

- **Gradients:** bg-gradient-to-b from-transparent to-transparent via-white/10, bg-gradient-to-b from-transparent to-transparent via-white/5, bg-gradient-to-b from-white to-white/60, bg-gradient-to-b from-white/30 to-white/5

## Typography

Typography relies on Inter across display, body, and utility text.

- **Display (`display-lg`):** Inter, 42px, weight 600, line-height 42px, letter-spacing -0.025em.
- **Body (`body-md`):** Inter, 10.5px, weight 400, line-height 14px.

## Layout

Layout follows a grid composition with reusable spacing tokens. Preserve the grid, full bleed structural frame before changing ornament or component styling. Use 5.25px as the base rhythm and let larger gaps step up from that cadence instead of introducing unrelated spacing values.

Treat the page as a grid / full bleed composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Grid
- **Content width:** Full Bleed
- **Base unit:** 5.25px
- **Scale:** 1px, 1.75px, 3.5px, 5.25px, 7px, 8.75px, 10.5px, 14px
- **Section padding:** 56px
- **Card padding:** 9.63px, 10.5px, 14px
- **Gaps:** 3.5px, 5.25px, 7px, 8.75px

## Elevation & Depth

Depth is communicated through glass, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as glass first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Glass
- **Borders:** 1px #FFFFFF; 1px #3B82F6; 1px #10B981
- **Shadows:** rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 1px 2px 0px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.4) 0px 4px 24px 0px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 2px 4px 0px inset
- **Blur:** 12px, 40px, 8px

### Techniques

- **Gradient border shell:** Use a thin gradient border shell around the main card. Wrap the surface in an outer shell with 1px padding and a 14px radius. Drive the shell with linear-gradient(rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05), rgba(0, 0, 0, 0)) so the edge reads like premium depth instead of a flat stroke. Keep the actual stroke understated so the gradient shell remains the hero edge treatment. Inset the real content surface inside the wrapper with a slightly smaller radius so the gradient only appears as a hairline frame.

## Shapes

Shapes rely on a tight radius system anchored by 3.5px and scaled across cards, buttons, and supporting surfaces. Icon geometry should stay compatible with that soft-to-controlled silhouette.

Use the radius family intentionally: larger surfaces can open up, but controls and badges should stay within the same rounded DNA instead of inventing sharper or pill-only exceptions.

- **Corner radii:** 3.5px, 5.25px, 7px, 10.5px, 14px, 9999px
- **Icon treatment:** Linear
- **Icon sets:** Solar

## Components

Anchor interactions to the detected button styles. Reuse the existing card surface recipe for content blocks.

### Buttons

- **Primary:** background #FFFFFF, text #FFFFFF, radius 7px, padding 5.25px, border 1px solid rgba(255, 255, 255, 0.1).
- **Secondary:** background #FFFFFF, text #FFFFFF, radius 5.25px, padding 5.25px, border 1px solid rgba(255, 255, 255, 0.1).
- **Links:** text #FFFFFF, radius 0px, padding 0px, border 0px solid rgb(229, 231, 235).

### Cards and Surfaces

- **Card surface:** border 1px solid rgba(255, 255, 255, 0.05), radius 7px, padding 9.63px, shadow none.
- **Card surface:** background rgba(15, 15, 15, 0.95), border 0px solid rgb(229, 231, 235), radius 10.5px, padding 14px, shadow none, blur 40px.

### Iconography

- **Treatment:** Linear.
- **Sets:** Solar.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do

- Do use the primary palette as the main accent for emphasis and action states.
- Do keep spacing aligned to the detected 5.25px rhythm.
- Do reuse the Glass surface treatment consistently across cards and controls.
- Do keep corner radii within the detected 3.5px, 5.25px, 7px, 10.5px, 14px, 9999px family.

### Don't

- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't mix unrelated shadow or blur recipes that break the current depth system.
- Don't exceed the detected expressive motion intensity without a deliberate reason.

## Motion

Motion feels expressive but remains focused on interface, text, and layout transitions. Timing clusters around 150ms and 3000ms. Easing favors ease and cubic-bezier(0.4. Hover behavior focuses on color and text changes. Scroll choreography uses GSAP ScrollTrigger for section reveals and pacing.

**Motion Level:** expressive

**Durations:** 150ms, 3000ms, 300ms, 2000ms, 500ms, 700ms

**Easings:** ease, cubic-bezier(0.4, 0, 1), 0.2, linear

**Hover Patterns:** color, text, stroke, transform

**Scroll Patterns:** gsap-scrolltrigger
