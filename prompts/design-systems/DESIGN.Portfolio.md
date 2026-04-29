---
version: "alpha"
name: "Portfolio - Technical System"
description: "Portfolio Technical Feature Section is designed for highlighting product capabilities and value points. Key features include reusable structure, responsive behavior, and production-ready presentation. It is suitable for component libraries and responsive product interfaces."
colors:
  primary: "#2563EB"
  secondary: "#737373"
  tertiary: "#7628F3"
  neutral: "#737373"
  surface: "#737373"
  accent: "#2563EB"
typography:
  headline-lg:
    fontFamily: "System Font"
---

## Overview

- **Composition cues:**
  - Layout: Flex
  - Framing: Open
  - Grid: Minimal

## Colors

The color system uses light mode with #2563EB as the main accent and #737373 as the neutral foundation.

- **Primary (#2563EB):** Main accent and emphasis color.
- **Secondary (#737373):** Supporting accent for secondary emphasis.
- **Tertiary (#7628F3):** Reserved accent for supporting contrast moments.
- **Neutral (#737373):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Surface: #737373; Accent: #2563EB

- **Gradients:** bg-gradient-to-b from-white to-transparent, bg-gradient-to-t from-neutral-100/20 to-transparent

## Typography

Typography relies on System Font across display, body, and utility text.

- **Headlines (`headline-lg`):** System Font.

## Layout

Layout follows a flex composition with reusable spacing tokens. Preserve the flex structural frame before changing ornament or component styling.

Treat the page as a flex composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Flex

## Elevation & Depth

Depth is communicated through flat, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as flat first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Flat

## Shapes

Shapes stay consistent across cards, controls, and icon treatments.

- **Icon treatment:** Linear
- **Icon sets:** Solar

## Components

Component styling should inherit the shared button, icon, spacing, and surface rules instead of inventing one-off treatments. Favor a small family of repeatable patterns for actions, content containers, and fields.

### Iconography

- **Treatment:** Linear.
- **Sets:** Solar.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do

- Do use the primary palette as the main accent for emphasis and action states.
- Do reuse the Flat surface treatment consistently across cards and controls.

### Don't

- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't exceed the detected minimal motion intensity without a deliberate reason.

## Motion

Motion stays restrained and interface-led across text, layout, and scroll transitions. Hover behavior focuses on text and color changes. Scroll choreography uses GSAP ScrollTrigger for section reveals and pacing.

**Motion Level:** minimal

**Hover Patterns:** text, color

**Scroll Patterns:** gsap-scrolltrigger
