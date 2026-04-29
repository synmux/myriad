---
version: "alpha"
name: "Integration Platform"
description: "Integration Platform Onboarding Section is designed for building reusable UI components in modern web projects. Key features include reusable structure, responsive behavior, and production-ready presentation. It is suitable for component libraries and responsive product interfaces."
colors:
  primary: "#84CC16"
  secondary: "#737373"
  tertiary: "#10DC23"
  neutral: "#737373"
  surface: "#737373"
  accent: "#84CC16"
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

The color system uses dark mode with #84CC16 as the main accent and #737373 as the neutral foundation.

- **Primary (#84CC16):** Main accent and emphasis color.
- **Secondary (#737373):** Supporting accent for secondary emphasis.
- **Tertiary (#10DC23):** Reserved accent for supporting contrast moments.
- **Neutral (#737373):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Surface: #737373; Accent: #84CC16

- **Gradients:** bg-gradient-to-b from-white/20 to-white/0, bg-gradient-to-b from-transparent to-transparent via-white/10, bg-gradient-to-b from-lime-400/60 to-lime-400/0

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

Motion stays restrained and interface-led across text, layout, and scroll transitions. Hover behavior focuses on transform and text changes. Scroll choreography uses GSAP ScrollTrigger for section reveals and pacing.

**Motion Level:** minimal

**Hover Patterns:** transform, text

**Scroll Patterns:** gsap-scrolltrigger
