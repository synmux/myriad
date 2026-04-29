---
version: "alpha"
name: "Nexis Compute - Enterprise AI Infrastructure"
description: "Nexis Compute Dashboard Section is designed for demonstrating application workflows and interface hierarchy. Key features include clear information density, modular panels, and interface rhythm. It is suitable for product showcases, admin panels, and analytics experiences."
colors:
  primary: "#2DD4BF"
  secondary: "#5EEAD4"
  tertiary: "#14B8A6"
  neutral: "#FFFFFF"
  background: "#FFFFFF"
  surface: "#2DD4BF"
  text-primary: "#9CA3AF"
  text-secondary: "#FFFFFF"
  border: "#FFFFFF"
  accent: "#2DD4BF"
typography:
  display-lg:
    fontFamily: "System Font"
    fontSize: "52.5px"
    fontWeight: 200
    lineHeight: "52.5px"
    letterSpacing: "-0.05em"
  body-md:
    fontFamily: "System Font"
    fontSize: "14px"
    fontWeight: 300
    lineHeight: "22.75px"
  label-md:
    fontFamily: "System Font"
    fontSize: "12.25px"
    fontWeight: 400
    lineHeight: "17.5px"
rounded:
  md: "5.25px"
spacing:
  base: "5.25px"
  sm: "1.75px"
  md: "3.5px"
  lg: "5.25px"
  xl: "7px"
  gap: "3.5px"
  card-padding: "14px"
  section-padding: "63px"
components:
  button-primary:
    textColor: "{colors.neutral}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: "7px"
  card:
    rounded: "10.5px"
    padding: "14px"
---

## Overview

- **Composition cues:**
  - Layout: Grid
  - Content Width: Full Bleed
  - Framing: Glassy
  - Grid: Strong

## Colors

The color system uses dark mode with #2DD4BF as the main accent and #FFFFFF as the neutral foundation.

- **Primary (#2DD4BF):** Main accent and emphasis color.
- **Secondary (#5EEAD4):** Supporting accent for secondary emphasis.
- **Tertiary (#14B8A6):** Reserved accent for supporting contrast moments.
- **Neutral (#FFFFFF):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Background: #FFFFFF; Surface: #2DD4BF; Text Primary: #9CA3AF; Text Secondary: #FFFFFF; Border: #FFFFFF; Accent: #2DD4BF

- **Gradients:** bg-gradient-to-r from-teal-500 to-teal-300, bg-gradient-to-b from-transparent to-transparent via-teal-200, bg-gradient-to-b from-transparent to-teal-400/0 via-teal-500/10, bg-gradient-to-b from-transparent to-teal-300/10 via-teal-400/40

## Typography

Typography relies on System Font across display, body, and utility text.

- **Display (`display-lg`):** System Font, 52.5px, weight 200, line-height 52.5px, letter-spacing -0.05em.
- **Body (`body-md`):** System Font, 14px, weight 300, line-height 22.75px.
- **Labels (`label-md`):** System Font, 12.25px, weight 400, line-height 17.5px.

## Layout

Layout follows a grid composition with reusable spacing tokens. Preserve the grid, full bleed structural frame before changing ornament or component styling. Use 5.25px as the base rhythm and let larger gaps step up from that cadence instead of introducing unrelated spacing values.

Treat the page as a grid / full bleed composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Grid
- **Content width:** Full Bleed
- **Base unit:** 5.25px
- **Scale:** 1.75px, 3.5px, 5.25px, 7px, 8.75px, 10.5px, 14px, 17.5px
- **Section padding:** 63px
- **Card padding:** 14px, 21px
- **Gaps:** 3.5px, 7px, 10.5px, 14px

## Elevation & Depth

Depth is communicated through glass, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as glass first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Glass
- **Borders:** 1px #FFFFFF
- **Shadows:** rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 1px 2px 0px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgb(45, 212, 191) 0px 0px 12px 0px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(45, 212, 191, 0.5) 0px 0px 20px 0px
- **Blur:** 12px, 4px, 64px

### Techniques

- **Gradient border shell:** Use a thin gradient border shell around the main card. Wrap the surface in an outer shell with 0px padding and a 19px radius. Drive the shell with linear-gradient(105deg, rgba(0, 0, 0, 0) 15%, rgba(255, 255, 255, 0.03) 25%, rgba(0, 0, 0, 0) 35%) so the edge reads like premium depth instead of a flat stroke. Keep the actual stroke understated so the gradient shell remains the hero edge treatment. Inset the real content surface inside the wrapper with a slightly smaller radius so the gradient only appears as a hairline frame.

## Shapes

Shapes rely on a tight radius system anchored by 5.25px and scaled across cards, buttons, and supporting surfaces. Icon geometry should stay compatible with that soft-to-controlled silhouette.

Use the radius family intentionally: larger surfaces can open up, but controls and badges should stay within the same rounded DNA instead of inventing sharper or pill-only exceptions.

- **Corner radii:** 5.25px, 10.5px, 19px, 9999px
- **Icon treatment:** Linear
- **Icon sets:** Solar

## Components

Anchor interactions to the detected button styles. Reuse the existing card surface recipe for content blocks.

### Buttons

- **Primary:** text #FFFFFF, radius 5.25px, padding 7px, border 0px solid rgb(229, 231, 235).

### Cards and Surfaces

- **Card surface:** border 1px solid rgba(255, 255, 255, 0.1), radius 10.5px, padding 14px, shadow none.
- **Card surface:** background rgba(8, 4, 16, 0.95), border 1px solid rgba(255, 255, 255, 0.08), radius 19px, padding 21px, shadow rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(45, 212, 191, 0.15) 0px 20px 50px -10px, blur 64px.

### Iconography

- **Treatment:** Linear.
- **Sets:** Solar.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do

- Do use the primary palette as the main accent for emphasis and action states.
- Do keep spacing aligned to the detected 5.25px rhythm.
- Do reuse the Glass surface treatment consistently across cards and controls.
- Do keep corner radii within the detected 5.25px, 10.5px, 19px, 9999px family.

### Don't

- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't mix unrelated shadow or blur recipes that break the current depth system.
- Don't exceed the detected moderate motion intensity without a deliberate reason.

## Motion

Motion feels controlled and interface-led across text, layout, and section transitions. Timing clusters around 150ms and 2000ms. Easing favors ease and cubic-bezier(0.4. Hover behavior focuses on color and text changes. Scroll choreography uses GSAP ScrollTrigger for section reveals and pacing.

**Motion Level:** moderate

**Durations:** 150ms, 2000ms, 1000ms, 6000ms

**Easings:** ease, cubic-bezier(0.4, 0, 1), 0.2, ease-in-out

**Hover Patterns:** color, text

**Scroll Patterns:** gsap-scrolltrigger

## WebGL

Reconstruct the graphics as a full-bleed background field using canvas-backed effect. The effect should read as technical, meditative, and atmospheric: dot-matrix particle field with teal on black and sparse spacing. Build it from dot particles + soft depth fade so the effect reads clearly. Animate it as slow breathing pulse. Interaction can react to the pointer, but only as a subtle drift. Preserve dom fallback.

**Id:** webgl

**Label:** WebGL

**Stack:** WebGL

**Insights:**

- **Scene:**
  - **Value:** Full-bleed background field
- **Effect:**
  - **Value:** Dot-matrix particle field
- **Primitives:**
  - **Value:** Dot particles + soft depth fade
- **Motion:**
  - **Value:** Slow breathing pulse
- **Interaction:**
  - **Value:** Pointer-reactive drift
- **Render:**
  - **Value:** Canvas-backed effect

**Techniques:** Dot matrix, Breathing pulse, Pointer parallax, DOM fallback

**Code Evidence:**

- **HTML reference:**
  - **Language:** html
  - **Snippet:**

    ```html
    <body
      class="bg-[#030108] text-white font-sans antialiased overflow-x-hidden selection:bg-teal-400/40 relative min-h-screen flex flex-col font-light scroll-smooth"
    >
      <canvas
        id="particle-canvas"
        class="absolute inset-0 w-full h-full pointer-events-none opacity-60 z-0"
      ></canvas>

      <nav
        class="relative z-20 w-full max-w-7xl mx-auto px-6 py-6 flex justify-between items-center"
      ></nav>
    </body>
    ```

- **JS reference:**
  - **Language:** js
  - **Snippet:**

    ```
    // 1. Canvas Particle System for WebGL-like background feel
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    function resize() {
        width = canvas.width = window.innerWidth;
    …
    ```
