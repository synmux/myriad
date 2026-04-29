---
version: "alpha"
name: "Spatial Interface Systems"
description: "Spatial Interface Dashboard Section is designed for demonstrating application workflows and interface hierarchy. Key features include clear information density, modular panels, and interface rhythm. It is suitable for product showcases, admin panels, and analytics experiences."
colors:
  primary: "#3B82F6"
  secondary: "#22C55E"
  tertiary: "#2563EB"
  neutral: "#FFFFFF"
  background: "#FFFFFF"
  surface: "#3B82F6"
  text-primary: "#FFFFFF"
  text-secondary: "#FFFFFF"
  border: "#FFFFFF"
  accent: "#3B82F6"
typography:
  display-lg:
    fontFamily: "Inter"
    fontSize: "72px"
    fontWeight: 500
    lineHeight: "75.6px"
    letterSpacing: "-0.025em"
  body-md:
    fontFamily: "Inter"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: "21px"
  label-md:
    fontFamily: "Inter"
    fontSize: "10.5px"
    fontWeight: 400
    lineHeight: "14px"
    letterSpacing: "0.21px"
    textTransform: "uppercase"
rounded:
  md: "0px"
spacing:
  base: "5.25px"
  sm: "1px"
  md: "1.75px"
  lg: "3.5px"
  xl: "5.25px"
  gap: "3.5px"
  card-padding: "8.75px"
  section-padding: "28px"
components:
  button-link:
    textColor: "{colors.neutral}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: "0px"
  card:
    rounded: "11px"
    padding: "14px"
---

## Overview

- **Composition cues:**
  - Layout: Grid
  - Content Width: Full Bleed
  - Framing: Glassy
  - Grid: Strong

## Colors

The color system uses dark mode with #3B82F6 as the main accent and #FFFFFF as the neutral foundation.

- **Primary (#3B82F6):** Main accent and emphasis color.
- **Secondary (#22C55E):** Supporting accent for secondary emphasis.
- **Tertiary (#2563EB):** Reserved accent for supporting contrast moments.
- **Neutral (#FFFFFF):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Background: #FFFFFF; Surface: #3B82F6; Text Primary: #FFFFFF; Text Secondary: #FFFFFF; Border: #FFFFFF; Accent: #3B82F6

- **Gradients:** bg-gradient-to-tr from-accent/5 to-transparent, bg-gradient-to-br from-white/30 to-transparent, bg-gradient-to-b from-accent/10 to-transparent

## Typography

Typography relies on Inter across display, body, and utility text.

- **Display (`display-lg`):** Inter, 72px, weight 500, line-height 75.6px, letter-spacing -0.025em.
- **Body (`body-md`):** Inter, 14px, weight 400, line-height 21px.
- **Labels (`label-md`):** Inter, 10.5px, weight 400, line-height 14px, letter-spacing 0.21px, uppercase.

## Layout

Layout follows a grid composition with reusable spacing tokens. Preserve the grid, full bleed structural frame before changing ornament or component styling. Use 5.25px as the base rhythm and let larger gaps step up from that cadence instead of introducing unrelated spacing values.

Treat the page as a grid / full bleed composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Grid
- **Content width:** Full Bleed
- **Base unit:** 5.25px
- **Scale:** 1px, 1.75px, 3.5px, 5.25px, 7px, 10.5px, 14px, 21px
- **Section padding:** 28px, 63px, 98px
- **Card padding:** 8.75px, 10.5px, 14px, 28px
- **Gaps:** 3.5px, 5.25px, 7px, 10.5px

## Elevation & Depth

Depth is communicated through glass, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as glass first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Glass
- **Borders:** 1px #FFFFFF; 1px #3B82F6; 1px #60A5FA
- **Shadows:** rgba(0, 0, 0, 0.8) -20px 20px 40px 0px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(59, 130, 246, 0.8) 0px 0px 8px 0px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(255, 255, 255, 0.5) 0px 0px 10px 0px
- **Blur:** 24px, 12px, 40px

### Techniques

- **Gradient border shell:** Use a thin gradient border shell around the main card. Wrap the surface in an outer shell with 1px padding and a 8px radius. Drive the shell with linear-gradient(to right bottom, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.01)) so the edge reads like premium depth instead of a flat stroke. Keep the actual stroke understated so the gradient shell remains the hero edge treatment. Inset the real content surface inside the wrapper with a slightly smaller radius so the gradient only appears as a hairline frame.

## Shapes

Shapes rely on a tight radius system anchored by 1.75px and scaled across cards, buttons, and supporting surfaces. Icon geometry should stay compatible with that soft-to-controlled silhouette.

Use the radius family intentionally: larger surfaces can open up, but controls and badges should stay within the same rounded DNA instead of inventing sharper or pill-only exceptions.

- **Corner radii:** 1.75px, 3.5px, 7px, 8px, 12px, 9999px
- **Icon treatment:** Linear
- **Icon sets:** Solar

## Components

Anchor interactions to the detected button styles. Reuse the existing card surface recipe for content blocks.

### Buttons

- **Links:** text #FFFFFF, radius 0px, padding 0px, border 0px solid rgb(229, 231, 235).

### Cards and Surfaces

- **Card surface:** background rgba(9, 9, 11, 0.9), border 1px solid rgba(255, 255, 255, 0.02), radius 11px, padding 14px, shadow none, blur 40px.
- **Card surface:** background #070708, border 1px solid rgba(255, 255, 255, 0.02), radius 15px, padding 14px, shadow none, blur 24px.

### Iconography

- **Treatment:** Linear.
- **Sets:** Solar.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do

- Do use the primary palette as the main accent for emphasis and action states.
- Do keep spacing aligned to the detected 5.25px rhythm.
- Do reuse the Glass surface treatment consistently across cards and controls.
- Do keep corner radii within the detected 1.75px, 3.5px, 7px, 8px, 12px, 9999px family.

### Don't

- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't mix unrelated shadow or blur recipes that break the current depth system.
- Don't exceed the detected minimal motion intensity without a deliberate reason.

## Motion

Motion stays restrained and interface-led across text, layout, and scroll transitions. Timing clusters around 150ms. Easing favors ease and cubic-bezier(0.4. Hover behavior focuses on text changes. Scroll choreography uses GSAP ScrollTrigger for section reveals and pacing.

**Motion Level:** minimal

**Durations:** 150ms

**Easings:** ease, cubic-bezier(0.4, 0, 0.2, 1)

**Hover Patterns:** text

**Scroll Patterns:** gsap-scrolltrigger

## WebGL

Reconstruct the graphics as a wide canvas band using webgl, custom shaders. The effect should read as technical, meditative, and atmospheric: dot-matrix particle field with black and sparse spacing. Build it from dot particles + soft depth fade so the effect reads clearly. Animate it as slow breathing pulse. Interaction can react to the pointer, but only as a subtle drift. Preserve dom fallback.

**Id:** webgl

**Label:** WebGL

**Stack:** WebGL

**Insights:**

- **Scene:**
  - **Value:** Wide canvas band
- **Effect:**
  - **Value:** Dot-matrix particle field
- **Primitives:**
  - **Value:** Dot particles + soft depth fade
- **Motion:**
  - **Value:** Slow breathing pulse
- **Interaction:**
  - **Value:** Pointer-reactive drift
- **Render:**
  - **Value:** WebGL, custom shaders

**Techniques:** Dot matrix, Breathing pulse, Pointer parallax, Shader gradients, Noise fields

**Code Evidence:**

- **HTML reference:**
  - **Language:** html
  - **Snippet:**

    ```html
    <!-- WebGL Lazer Background -->
    <canvas
      id="lazer-canvas"
      class="fixed top-0 left-0 w-full h-[800px] pointer-events-none z-0"
      style="-webkit-mask-image: linear-gradient(to bottom, black 50%, transparent); mask-image: linear-gradient(to bottom, black 50%, transparent);"
    ></canvas>

    <!-- Global Navigation -->
    ```

- **JS reference:**
  - **Language:** js
  - **Snippet:**

    ```
    // WebGL Lazer & FBM Background Implementation
    const canvas = document.getElementById('lazer-canvas');
    const gl = canvas.getContext('webgl');

    if (gl) {
        const resizeCanvas = () => {
            canvas.width = window.innerWidth;
            canvas.height = 800; // Fixed height as per design
    ```

- **Renderer setup:**
  - **Language:** js
  - **Snippet:**

    ```
    // WebGL Lazer & FBM Background Implementation
    const canvas = document.getElementById('lazer-canvas');
    const gl = canvas.getContext('webgl');

    if (gl) {
        const resizeCanvas = () => {
            canvas.width = window.innerWidth;
    ```

- **Draw call:**
  - **Language:** js
  - **Snippet:**
    ```
    // Fragment shader creating vertical beam and subtle noise
        const fragmentShaderSource = `
            precision mediump float;
            uniform vec2 u_resolution;
    …
    ```
