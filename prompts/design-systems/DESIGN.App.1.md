---
version: "alpha"
name: "Capital Overview Dashboard"
description: "Capital Overview Dashboard Section is designed for demonstrating application workflows and interface hierarchy. Key features include clear information density, modular panels, and interface rhythm. It is suitable for product showcases, admin panels, and analytics experiences."
colors:
  primary: "#818CF8"
  secondary: "#1F2937"
  tertiary: "#34D399"
  neutral: "#FFFFFF"
  background: "#818CF8"
  surface: "#1F2937"
  text-primary: "#9CA3AF"
  text-secondary: "#FFFFFF"
  border: "#374151"
  accent: "#818CF8"
typography:
  headline-lg:
    fontFamily: "Inter"
    fontSize: "31.5px"
    fontWeight: 600
    lineHeight: "35px"
    letterSpacing: "-0.025em"
  body-md:
    fontFamily: "Inter"
    fontSize: "12.25px"
    fontWeight: 400
    lineHeight: "17.5px"
  label-md:
    fontFamily: "Inter"
    fontSize: "10.5px"
    fontWeight: 400
    lineHeight: "14px"
rounded:
  md: "7px"
spacing:
  base: "5.25px"
  sm: "1px"
  md: "1.75px"
  lg: "3.5px"
  xl: "5.25px"
  gap: "3.5px"
  card-padding: "10.5px"
  section-padding: "28px"
components:
  button-primary:
    backgroundColor: "#212126"
    textColor: "{colors.text-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: "5.25px"
  button-secondary:
    textColor: "{colors.neutral}"
    rounded: "0px"
    padding: "5.25px"
  button-link:
    textColor: "{colors.text-primary}"
    rounded: "0px"
    padding: "5.25px"
  card:
    backgroundColor: "#18181C"
    rounded: "14px"
    padding: "21px"
---

## Overview

- **Composition cues:**
  - Layout: Grid
  - Content Width: Full Bleed
  - Framing: Glassy
  - Grid: Strong

## Colors

The color system uses dark mode with #818CF8 as the main accent and #FFFFFF as the neutral foundation.

- **Primary (#818CF8):** Main accent and emphasis color.
- **Secondary (#1F2937):** Supporting accent for secondary emphasis.
- **Tertiary (#34D399):** Reserved accent for supporting contrast moments.
- **Neutral (#FFFFFF):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Background: #818CF8; Surface: #1F2937; Text Primary: #9CA3AF; Text Secondary: #FFFFFF; Border: #374151; Accent: #818CF8

- **Gradients:** bg-gradient-to-tr from-indigo-500/5 to-emerald-500/5

## Typography

Typography relies on Inter across display, body, and utility text.

- **Headlines (`headline-lg`):** Inter, 31.5px, weight 600, line-height 35px, letter-spacing -0.025em.
- **Body (`body-md`):** Inter, 12.25px, weight 400, line-height 17.5px.
- **Labels (`label-md`):** Inter, 10.5px, weight 400, line-height 14px.

## Layout

Layout follows a grid composition with reusable spacing tokens. Preserve the grid, full bleed structural frame before changing ornament or component styling. Use 5.25px as the base rhythm and let larger gaps step up from that cadence instead of introducing unrelated spacing values.

Treat the page as a grid / full bleed composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Grid
- **Content width:** Full Bleed
- **Base unit:** 5.25px
- **Scale:** 1px, 1.75px, 3.5px, 5.25px, 7px, 8.75px, 10.5px, 14px
- **Section padding:** 28px
- **Card padding:** 10.5px, 14px, 21px, 28px
- **Gaps:** 3.5px, 5.25px, 7px, 10.5px

## Elevation & Depth

Depth is communicated through glass, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as glass first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Glass
- **Borders:** 1px #374151; 1px #1F2937; 1px #10B981; 2px #131316
- **Shadows:** rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 1px 2px 0px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(6, 6, 6, 0.591) 0px 0px 58.3423px -12.8342px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 20px 25px -5px, rgba(0, 0, 0, 0.1) 0px 8px 10px -6px
- **Blur:** 4px

## Shapes

Shapes rely on a tight radius system anchored by 5.25px and scaled across cards, buttons, and supporting surfaces. Icon geometry should stay compatible with that soft-to-controlled silhouette.

Use the radius family intentionally: larger surfaces can open up, but controls and badges should stay within the same rounded DNA instead of inventing sharper or pill-only exceptions.

- **Corner radii:** 5.25px, 7px, 10.5px, 14px, 28px, 9999px
- **Icon treatment:** Linear
- **Icon sets:** Solar

## Components

Anchor interactions to the detected button styles. Reuse the existing card surface recipe for content blocks.

### Buttons

- **Primary:** background #212126, text #9CA3AF, radius 7px, padding 5.25px, border 1px solid rgba(55, 65, 81, 0.5).
- **Secondary:** text #FFFFFF, radius 0px, padding 5.25px, border 0px 0px 2px solid #FFFFFF.
- **Links:** text #9CA3AF, radius 0px, padding 5.25px, border 0px solid rgb(229, 231, 235).

### Cards and Surfaces

- **Card surface:** background #18181C, border 1px solid rgba(31, 41, 55, 0.6), radius 14px, padding 21px, shadow none.
- **Card surface:** background #1C1C21, border 1px solid rgba(55, 65, 81, 0.5), radius 10.5px, padding 14px, shadow rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 20px 25px -5px, rgba(0, 0, 0, 0.1) 0px 8px 10px -6px.
- **Card surface:** background #111113, border 1px solid rgba(31, 41, 55, 0.4), radius 10.5px, padding 10.5px, shadow none.

### Iconography

- **Treatment:** Linear.
- **Sets:** Solar.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do

- Do use the primary palette as the main accent for emphasis and action states.
- Do keep spacing aligned to the detected 5.25px rhythm.
- Do reuse the Glass surface treatment consistently across cards and controls.
- Do keep corner radii within the detected 5.25px, 7px, 10.5px, 14px, 28px, 9999px family.

### Don't

- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't mix unrelated shadow or blur recipes that break the current depth system.
- Don't exceed the detected expressive motion intensity without a deliberate reason.

## Motion

Motion feels expressive but remains focused on interface, text, and layout transitions. Timing clusters around 150ms and 300ms. Easing favors ease and cubic-bezier(0.4. Hover behavior focuses on text and stroke changes. Scroll choreography uses GSAP ScrollTrigger for section reveals and pacing.

**Motion Level:** expressive

**Durations:** 150ms, 300ms, 1000ms, 500ms, 2000ms

**Easings:** ease, cubic-bezier(0.4, 0, 1), 0.2, 0.6

**Hover Patterns:** text, stroke, color, brightness, shadow

**Scroll Patterns:** gsap-scrolltrigger
