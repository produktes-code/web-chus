---
name: Broadcast Architect
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1b1b1b'
  surface-container: '#1f1f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353535'
  on-surface: '#e2e2e2'
  on-surface-variant: '#e9bcb6'
  inverse-surface: '#e2e2e2'
  inverse-on-surface: '#303030'
  outline: '#b08782'
  outline-variant: '#5f3f3a'
  surface-tint: '#ffb4aa'
  primary: '#ffb4aa'
  on-primary: '#690003'
  primary-container: '#ff5446'
  on-primary-container: '#5c0002'
  inverse-primary: '#c0000c'
  secondary: '#c6c6c7'
  on-secondary: '#2f3131'
  secondary-container: '#454747'
  on-secondary-container: '#b4b5b5'
  tertiary: '#00e639'
  on-tertiary: '#003907'
  tertiary-container: '#00a827'
  on-tertiary-container: '#003205'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad5'
  primary-fixed-dim: '#ffb4aa'
  on-primary-fixed: '#410001'
  on-primary-fixed-variant: '#930006'
  secondary-fixed: '#e2e2e2'
  secondary-fixed-dim: '#c6c6c7'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#454747'
  tertiary-fixed: '#72ff70'
  tertiary-fixed-dim: '#00e639'
  on-tertiary-fixed: '#002203'
  on-tertiary-fixed-variant: '#00530e'
  background: '#131313'
  on-background: '#e2e2e2'
  surface-variant: '#353535'
  terminal-green: '#00FF41'
  signal-red: '#FF1F1F'
  surface-glass: rgba(255, 255, 255, 0.05)
  grid-line: rgba(255, 255, 255, 0.1)
typography:
  headline-xl:
    fontFamily: Anton
    fontSize: 96px
    fontWeight: '400'
    lineHeight: 100%
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Anton
    fontSize: 64px
    fontWeight: '400'
    lineHeight: 110%
  headline-lg-mobile:
    fontFamily: Anton
    fontSize: 40px
    fontWeight: '400'
    lineHeight: 110%
  headline-md:
    fontFamily: Anton
    fontSize: 32px
    fontWeight: '400'
    lineHeight: 120%
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '400'
    lineHeight: 160%
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 160%
  label-tech:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 140%
    letterSpacing: 0.05em
  label-code:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 140%
spacing:
  unit: 8px
  gutter: 24px
  margin-safe: 40px
  section-gap: 120px
  container-max: 1440px
---

## Brand & Style

The brand personality is authoritative, technical, and high-performance, reflecting a bridge between veteran broadcast engineering and modern system architecture. It evokes the feeling of a premium control room or a high-end technical "war room."

The design style is a hybrid of **Minimalism** and **Technical Brutalism**, elevated by **Glassmorphism**. It utilizes high-contrast aesthetics to ensure clarity and a "broadcast-ready" feel. Structural elements are inspired by technical blueprints and terminal interfaces, balanced with expansive, high-quality media to highlight the human aspect of audiovisual craft.

## Colors

The palette is strictly high-contrast, optimized for professional dark-mode environments.

- **Primary (Signal Red):** Used sparingly for high-impact accents, critical status indicators, and branding flourishes that echo the physical "On Air" signal.
- **Secondary (Crisp White):** Reserved for primary typography and essential iconography to ensure maximum legibility against the dark void.
- **Tertiary (Terminal Green):** Used for technical metadata, "Success" states, and active code-like syntax elements.
- **Neutral (Pure Black):** The foundation of the system, providing a deep, immersive stage for media and text.

Backgrounds should utilize the deep black, while secondary containers use "Surface Glass" (low-opacity white) with backdrop blurs to create depth without sacrificing the dark aesthetic.

## Typography

The typographic system pairs industrial impact with technical precision.

- **Headlines:** Use **Anton** for its bold, condensed, and commanding presence. It mirrors the weight of the brand logo and creates a powerful visual rhythm. All headlines should be Uppercase for a more "architectural" feel.
- **Body Text:** **Hanken Grotesk** provides a clean, contemporary feel that is highly readable in long-form technical descriptions.
- **Technical UI:** **JetBrains Mono** is used for status codes, metadata, versioning, and any terminal-style interface elements. It reinforces the "Audiovisual Architect" persona.

## Layout & Spacing

The layout is governed by a **Fixed Grid** system (12 columns on desktop) but punctuated by "technical leaks"—elements like status bars or thin lines that stretch to the screen edges.

- **Grid:** 12 columns with 24px gutters. Use large margins (40px+) to maintain a premium feel.
- **Sectioning:** Vertical rhythm is aggressive, with large gaps (120px) between major content blocks to allow the "system" room to breathe.
- **Technical Patterns:** Overlay a subtle 32px square grid pattern at 5% opacity on background layers to reinforce the architectural theme.
- **Mobile:** Transition to a 4-column grid with 16px margins. Headlines scale down significantly to ensure they remain impactful but readable on small screens.

## Elevation & Depth

This system avoids traditional soft shadows in favor of **Tonal Layering** and **Glassmorphism**.

- **Level 0 (Base):** Pure black `#000000`.
- **Level 1 (Panels):** Surface-glass containers with a 1px white border at 10% opacity. These elements use a 20px backdrop blur to lift content above the background grid.
- **Level 2 (Active Elements):** High-contrast outlines in Primary Red or Secondary White.
- **Visual Depth:** Depth is created through transparency and "stacking" of glass layers rather than ambient lighting. Red accents should appear as if they are self-illuminated "glows" (neon effect) rather than reflected light.

## Shapes

The shape language is strictly **Sharp (0px)**. Roundness is avoided to maintain the industrial, precision-engineered aesthetic of broadcast equipment and architectural blueprints.

Buttons, cards, and input fields must use 90-degree corners. The only exception is for circular "Status" pips which indicate active/inactive systems.

## Components

- **Buttons:** Rectangular blocks with a 1px border. Primary buttons use a solid White fill with Black text; Secondary buttons use a transparent background with a Red border.
- **Technical Chips:** Used for "SYS_STATUS" or category tags. These should look like terminal labels: Mono font, Uppercase, enclosed in `[ ]` brackets or a high-contrast thin border.
- **Cards:** Glassmorphic containers with 0px radius. Use thin white borders (0.5px or 1px) and subtle hover effects that increase the background blur or border opacity.
- **Input Fields:** Bottom-border only, or a full 1px border with a "Terminal" prompt prefix (e.g., `> _`).
- **Dividers:** Use thin, 1px lines that extend across the grid. Occasionally use "Red lines" to denote a major system break, mirroring the logo's structure.
- **Interactive Terminal:** A custom component displaying real-time or simulated "system logs" in Mono font to add technical texture to the narrative sections.