---
name: MyBotica Instagram Carousels
description: A warm editorial social system that makes one everyday AI scenario concrete, honest, and easy to follow.
colors:
  deep-green: "#0f2a24"
  warm-cream: "#f6f2ee"
  paper-white: "#fffdf9"
  burgundy-signal: "#8c1d26"
  soft-green: "#dfe9e4"
  blush-highlight: "#f3c7ca"
  muted-ink: "#66716d"
  quiet-line: "#cdd7d2"
  pure-white: "#ffffff"
typography:
  display:
    fontFamily: "Unbounded, sans-serif"
    fontSize: "76px"
    fontWeight: 590
    lineHeight: 1.02
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Unbounded, sans-serif"
    fontSize: "64px"
    fontWeight: 590
    lineHeight: 1.04
    letterSpacing: "-0.035em"
  title:
    fontFamily: "Unbounded, sans-serif"
    fontSize: "34px"
    fontWeight: 560
    lineHeight: 1.12
    letterSpacing: "-0.03em"
  body:
    fontFamily: "Golos, Arial, sans-serif"
    fontSize: "31px"
    fontWeight: 400
    lineHeight: 1.36
    letterSpacing: "normal"
  label:
    fontFamily: "Golos, Arial, sans-serif"
    fontSize: "19px"
    fontWeight: 720
    lineHeight: 1.2
    letterSpacing: "0.03em"
rounded:
  compact: "8px"
  card: "14px"
  soft-card: "16px"
  speech: "15px 15px 15px 4px"
  circle: "50%"
spacing:
  micro: "8px"
  compact: "18px"
  control: "24px"
  content: "30px"
  cluster: "34px"
  section: "48px"
  slide-inset: "76px"
components:
  action-primary:
    backgroundColor: "{colors.deep-green}"
    textColor: "{colors.pure-white}"
    typography: "{typography.label}"
    rounded: "{rounded.card}"
    padding: "28px 30px"
  action-secondary:
    backgroundColor: "{colors.warm-cream}"
    textColor: "{colors.deep-green}"
    typography: "{typography.label}"
    rounded: "{rounded.card}"
    padding: "28px 30px"
  chat-message:
    backgroundColor: "{colors.soft-green}"
    textColor: "{colors.deep-green}"
    typography: "{typography.title}"
    rounded: "{rounded.speech}"
    padding: "28px 30px"
  editorial-card:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.deep-green}"
    rounded: "{rounded.soft-card}"
    padding: "38px"
  cta-chip:
    backgroundColor: "{colors.burgundy-signal}"
    textColor: "{colors.pure-white}"
    typography: "{typography.label}"
    rounded: "{rounded.card}"
    padding: "24px 30px"
---

# Design System: MyBotica Instagram Carousels

## Overview

**Creative North Star: "The Friendly Editorial Guide"**

MyBotica carousels turn one ordinary, repeated task into a compact editorial story. The system is warm and approachable rather than futuristic: generous paper-colored space, decisive dark type, physical objects, and a friendly mascot make the technology feel understandable. Each slide advances one thought, and the sequence moves from a familiar friction to a concrete interaction before asking for action.

The system is expressive through scale, contrast, and composition rather than decorative effects. Deep-green and burgundy full-bleed slides punctuate a cream reading rhythm; crisp grids and rules explain mechanisms; transparent cutouts of the canonical dragon girl and physical source objects enter only when they can participate in that mechanism. Product uncertainty is labeled in the visual hierarchy instead of being hidden in fine print.

**Key Characteristics:**

- Fixed 4:5 editorial canvases with a persistent branded header and ten-step progress rail.
- Cream, deep-green, and burgundy surfaces alternating to control pace and emphasis.
- Wide geometric Unbounded headlines paired with highly readable Golos supporting copy.
- Transparent mascot and physical-object cutouts integrated into paths, grids, and UI messages rather than isolated in generic cards.
- Compact cards with modest radii, strong borders, and selective ambient shadows.
- One everyday scenario per carousel, expressed before the underlying technology.

## Colors

The palette feels like warm printed paper marked with dark botanical ink and a single wine-red editorial signal.

### Primary

- **Deep Botanical Green:** The default ink, primary action surface, and full-slide dark background. It gives the system authority without looking like generic software blue.
- **Burgundy Signal:** The sole high-attention accent for key words, progress, calls to action, state changes, and occasional full-slide interruption.

### Secondary

- **Soft Botanical Wash:** A quiet message or status fill inside light cards; it supports explanation without competing with burgundy.
- **Blush Highlight:** A light emphasis color reserved for important phrases and oversized proof on dark backgrounds.

### Neutral

- **Warm Editorial Cream:** The default slide canvas and the system's dominant negative space.
- **Paper White:** A lifted inner surface for message windows and cards; physical objects remain transparent cutouts against the slide field.
- **Muted Ink:** Supporting copy, annotations, timestamps, and header notes on light surfaces.
- **Quiet Line:** Rules, inactive progress segments, and empty states where a softer boundary is needed.
- **Pure White:** Text and marks on saturated surfaces, plus the strongest inner-card contrast.

### Named Rules

**The Burgundy Signal Rule.** Burgundy marks the one idea, state, or action that deserves immediate attention; it is not a decorative wash applied everywhere.

**The Three-Surface Rhythm Rule.** Build the sequence primarily from warm cream, deep green, and burgundy full-slide fields, using white and soft green only inside those fields.

## Typography

**Display Font:** Unbounded (with sans-serif fallback)  
**Body Font:** Golos (with Arial and sans-serif fallbacks)

**Character:** Unbounded gives short Russian headlines a broad, unmistakable silhouette, while Golos keeps explanation friendly and direct. The contrast between compressed headline density and open body rhythm makes each slide readable at feed size.

### Hierarchy

- **Display** (590, 76px, 1.02): Cover questions and the largest sequence-defining statements; keep line breaks few and intentional.
- **Headline** (590, 64px, 1.04): One clear claim per interior slide.
- **Title** (560, 34px, 1.12): Mechanism labels, results, and compact high-emphasis copy inside diagrams.
- **Body** (400, 31px, 1.36): Explanations and transitions; typical text blocks occupy roughly 610–820px of the 1080px canvas.
- **Label** (720, 19px, 0.03em tracking): Header notes, timestamps, metadata, and microcopy; uppercase is optional and used for categorical system labels, not conversational notes.

### Named Rules

**The One Thought Per Slide Rule.** Give every slide one dominant Unbounded statement; supporting Golos copy explains it but never competes at the same scale.

**The Tight Headline Rule.** Unbounded headlines use tight tracking and near-solid leading; body copy never inherits that compression.

## Layout

Every shipping slide is a fixed 1080 × 1350px portrait canvas. The core safe area uses 76px left and right insets, with 68px at the top and approximately 76px at the bottom. A 46–48px header row holds the logo at left and a concise scene note at right; both adapt to light and saturated backgrounds.

Content is deliberately asymmetric. Headlines usually begin about 104–116px below the header and occupy 760–860px, leaving a secondary zone for a physical object, diagram, card, or mascot. Interior modules use simple one-, two-, or seven-column grids with 18–54px gaps. Major transitions typically use 48–76px of vertical space; internal card spacing stays in the 24–38px range. Transparent cutouts may cross a grid edge, sit over a message window, follow a drawn path, or extend slightly beyond the canvas to make the composition feel organic. The face, expression, silhouette-defining features, book title, and other important identity cues stay inside the frame.

The progress rail is anchored about 46px above the bottom edge, spans the safe width, and divides into ten equal 8px segments with 8px gaps. It is navigational rhythm and provenance, so it appears consistently on all slides and reverses contrast on saturated surfaces.

**The Fixed Editorial Frame Rule.** Do not fluidly reflow the composition: exports target the 1080 × 1350 Instagram canvas, and each slide is art-directed within that frame.

**The Safe Identity Rule.** Edge overlap may loosen the composition, but no crop may remove the dragon girl's face, expression, wings, defining silhouette, or the identifying features of a physical source object.

## Elevation & Depth

The system is flat by default. Full-slide color fields, crisp rules, and tonal contrast establish structure. Shadows appear only where an element is meant to feel placed on paper: message windows, speech bubbles, transparent mascot or book cutouts, and the final call to action. Cutouts use silhouette-aware drop shadows rather than rectangular card shadows. All shadows are broad and ambient, never glossy or neon.

### Shadow Vocabulary

- **Dialogue Lift** (`0 24px 44px rgba(0,0,0,.2)`): A large paper card placed over a deep-green slide.
- **Editorial Lift** (`0 16px 30px rgba(15,42,36,.18)`): Speech bubbles and small floating paper elements on light surfaces.
- **Burgundy Action Lift** (`0 18px 34px rgba(140,29,38,.23)`): The final burgundy call to action only.
- **Light Cutout Drop** (`drop-shadow(0 18px 16px rgba(15,42,36,.1))`): Dragon cutouts on cream, preserving the transparent silhouette.
- **Dark Cutout Drop** (`drop-shadow(0 24px 20px rgba(0,0,0,.2))`): Dragon cutouts overlapping white UI on deep green.
- **Object Drop** (`drop-shadow(0 28px 24px rgba(15,42,36,.2))`): Physical book cutouts whose irregular silhouette should remain visible.

### Named Rules

**The Placed-On-Paper Rule.** Use elevation to make a real or conversational object feel physically placed on the slide; transparent cutouts receive silhouette-aware drop shadows, while data grids, lists, and structural panels remain flat.

## Shapes

Most containers use gently rounded 14–16px corners. Speech bubbles carry a signature clipped lower-left corner, producing an asymmetric conversational silhouette. Mascot and physical-object cutouts have no enclosing geometry: their transparent edges, modest rotation, and natural silhouettes provide the shape. Compact labels use 8px corners. Circles are reserved for binary habit states and path nodes; square burgundy or white markers punctuate lists and statuses.

Borders are functional and usually 2px. They divide grids, outline secondary choices, and keep white cards legible on cream. Large decorative blobs, pills, and continuous soft rounding are not part of the shipped system.

**The One Clipped Corner Rule.** Conversational surfaces may soften three corners and clip the lower-left; structural panels use even corners or square rules.

**The Organic Cutout Rule.** Never put the canonical dragon or a physical source object inside a generic square, portrait card, or decorative frame. Integrate the transparent cutout with the composition's path, grid, text, or UI message.

## Components

### Branded Slide Header

- **Style:** A 190–196px MyBotica logo at left and a short 18–19px, heavy Golos scene note at right.
- **State:** Use the dark logo asset on light slides and the light logo asset on deep-green or burgundy slides; the note becomes translucent white on saturated fields.
- **Behavior:** The note names the current rhetorical role—such as an example, concept, or stage—rather than repeating the headline.

### Progress Rail

- **Style:** Ten equal rectangular segments, 8px high with 8px gaps, spanning the slide safe width.
- **State:** Quiet-line inactive segments and a burgundy active segment on cream; translucent-white inactive segments on dark slides; a pure-white active segment on burgundy.
- **Behavior:** The active segment advances exactly once per slide and remains fixed near the bottom edge.

### Action Choices

- **Shape:** Gently curved cards with even corners (14px).
- **Primary:** Deep green with white type, 2px deep-green border, and 28px × 30px internal spacing.
- **Secondary:** Transparent cream with a 2px deep-green border and deep-green type.
- **Behavior:** The pair is shown side by side with a concise micro-label above the action phrase; visual hierarchy communicates the lower-friction path.

### Chat / Reminder Card

- **Corner Style:** A 16px outer card and an asymmetric speech bubble inside.
- **Background:** Paper white over a deep-green field, with a soft-green message fill.
- **Shadow Strategy:** Dialogue Lift on the outer window; the inner message remains flat.
- **Internal Padding:** 38px on the window and 28px × 30px on the message.
- **Behavior:** A small burgundy square identifies the bot or scenario; timestamps and disclaimers use muted Golos text.

### Editorial Lists and Grids

- **Style:** Flat rows separated by 2px rules, with Unbounded labels and small square or circular state marks.
- **Behavior:** Use repeated geometry to make a sequence, week, comparison, or set of examples scannable without adding icons.
- **Density:** Row padding typically falls between 22px and 30px.

### Organic Character and Object Cutouts

- **Shape:** Use transparent PNG cutouts with their natural silhouettes; do not add a square, portrait card, or background plate.
- **Placement:** Let the dragon or physical object intersect a burgundy path, overlap a grid edge, or sit partly in front of a UI message so it belongs to the composition.
- **Shadow Strategy:** Apply a soft silhouette-aware drop shadow only when separation is needed; avoid rectangular elevation around the asset.
- **Behavior:** Use the dragon selectively and choose a canonical emotion that participates in the current thought—thoughtful for a question, wink for a prompt, joy for invitation or completion. Slides without a meaningful mascot role remain typographic, diagrammatic, or object-led.
- **Cropping:** Slight edge overlap is welcome, but the face, emotion, wings and spikes, book title, and other identifying features stay within the frame.

### CTA Chip

- **Shape:** A compact 14px rectangle, not a pill.
- **Primary:** Burgundy with white heavy Golos type and 24px × 30px padding.
- **Depth:** Burgundy Action Lift when it is the sole final action.
- **Behavior:** Keep the wording direct and concrete; it sits after the explanatory arc, never on every slide.

## Do's and Don'ts

### Do:

- **Do** preserve the 1080 × 1350px frame, 76px horizontal safe area, branded header, and ten-step progress rail across the carousel.
- **Do** make one familiar life or work task the visual and narrative center before introducing AI capability.
- **Do** alternate cream, deep-green, and burgundy fields to pace the sequence and reserve burgundy for the highest-attention signal.
- **Do** use transparent cutouts of the canonical dragon girl and physical source objects, integrating them into a path, grid, UI message, or another active compositional relationship.
- **Do** use the mascot selectively and choose an emotion that supports the slide's meaning; let some slides remain typographic, diagrammatic, or object-led.
- **Do** allow small organic overlaps at the canvas edge while keeping faces, expressions, wings, spikes, titles, and other identifying features visible.
- **Do** label speculative mechanics, mockups, and illustrative results visibly in the hierarchy.
- **Do** use physical source objects when the story depends on a real book, tool, or other recognizable reference.

### Don't:

- **Don't** turn the carousel into a generic list of AI features, a fabricated user case, or an unqualified product promise.
- **Don't** introduce extra accent hues merely to differentiate slides; use structure, scale, and the established three-surface rhythm.
- **Don't** decorate every panel with shadows; grids, rules, and color fields are the default depth system.
- **Don't** use pills, excessive rounding, glossy gradients, or futuristic interface chrome that weakens the editorial paper character.
- **Don't** place the dragon girl or physical book inside a generic square, portrait card, or decorative frame.
- **Don't** repeat the mascot mechanically on every slide or use her as a corner sticker; she must guide, react, demonstrate, or close the story.
- **Don't** crop important identity cues or object features merely to create edge tension.
