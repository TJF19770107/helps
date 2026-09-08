# Design Details — The Craft of Visual Polish

The difference between "good enough" and "memorable" is in the details. This reference covers the micro-level design decisions that compound into exceptional UI.

## 1. Visual Hierarchy Beyond Font Size

**The #1 beginner mistake**: relying solely on font size for hierarchy. Professional hierarchy uses multiple dimensions simultaneously.

### The Hierarchy Toolkit

| Dimension | Strong Signal | Subtle Signal |
|-----------|---------------|---------------|
| **Size** | 3:1+ ratio between levels | <2:1 ratio |
| **Weight** | Bold (700) vs Light (300) | Semi-bold vs Regular |
| **Color** | High contrast (dark vs muted) | Slight tone variation |
| **Saturation** | Vibrant accent vs desaturated body | — |
| **Spacing** | Generous whitespace around key element | Tight grouping |
| **Position** | Top-left (primary in LTR) | Bottom-right (tertiary) |

**Golden rule**: Combine 2-3 dimensions. A heading that's larger AND bolder AND surrounded by more whitespace creates unmistakable hierarchy.

### De-emphasize by reducing, not hiding

To de-emphasize secondary content:
- Use lighter color (not smaller size) for metadata
- Use normal weight (not bold) for less important text
- Reduce saturation for secondary labels
- **Never** use tiny font size (<12px) to indicate "less important"

### Labels are a last resort

Before adding a label ("Name:", "Email:", "Date:"):
1. Can the format speak for itself? (email@example.com is obviously an email)
2. Can you use placeholder context? ("$49.99" doesn't need "Price:")
3. If you must label, de-emphasize the label, not the value

## 2. Spacing & Whitespace Mastery

### Start with too much whitespace

**Counter-intuitive truth**: It's easier to remove whitespace than to add it later. White space is not "wasted" space—it's active design that creates:
- Focus (guides the eye)
- Breathing room (reduces cognitive load)
- Perceived quality (luxury brands use tons of whitespace)

### Spacing creates grouping (Gestalt proximity)

Instead of borders and cards to group related items, use spacing:
- **Tight spacing** (8-12px) = "these belong together"
- **Medium spacing** (24-32px) = "these are siblings"
- **Large spacing** (48-64px+) = "new section starts here"

### The spacing-before > spacing-after rule

Section headings need **more space above** than below. The heading belongs to the content that follows it:

```css
/* ❌ Wrong: equal spacing */
h2 { margin: 24px 0; }

/* ✅ Right: more space above, less below */
h2 { margin-top: 48px; margin-bottom: 16px; }
```

### Fluid spacing

```css
:root {
  --space-xs: clamp(0.25rem, 0.5vw, 0.5rem);
  --space-sm: clamp(0.5rem, 1vw, 1rem);
  --space-md: clamp(1rem, 2vw, 2rem);
  --space-lg: clamp(2rem, 4vw, 4rem);
  --space-xl: clamp(4rem, 8vw, 8rem);
}
```

## 3. Color System Architecture

### Building a Production Palette (Refactoring UI Method)

Don't rely on color generators. Build manually:

**Step 1: Define three color groups**
- **Grays** (8-10 shades): Text, backgrounds, borders, panels — used everywhere
- **Primary** (5-9 shades): Brand color, CTAs, key navigation
- **Accents** (2-3 shades each): Success (green), Warning (yellow), Danger (red), Info (blue)

**Step 2: Pick the base, then extend**
1. Choose middle shade (500) — should work as a button background
2. Define darkest (900) — works as text color
3. Define lightest (100) — works as tinted background
4. Fill in between (200, 300, 400, 600, 700, 800)

**Step 3: Trust your eyes, not math**
- `darken()` and `lighten()` in CSS preprocessors produce flat, lifeless colors
- Real color shifts change hue, saturation, AND lightness simultaneously
- Blues get more purple as they darken; yellows shift toward orange
- **Always reduce chroma at extremes** (very light or very dark)

### The 60-30-10 Rule Applied

This is about **visual weight**, not pixel count:
- **60%**: Neutral backgrounds, whitespace, base surfaces
- **30%**: Secondary — text, borders, inactive states
- **10%**: Accent — CTAs, highlights, focus states

The most common mistake: using the brand color everywhere because "it's our color." Accent works **because it's rare**. Overuse kills its power.

### Tinted Neutrals (Essential)

Never use pure gray. Add a tiny hint of your brand hue:
```css
/* Dead gray — no personality */
--gray-100: oklch(95% 0 0);

/* Warm-tinted — cohesive and alive */
--gray-100: oklch(95% 0.01 60);

/* Cool-tinted — professional and tech */
--gray-100: oklch(95% 0.01 250);
```

## 4. Borders & Separators

### Use fewer borders

Borders add visual clutter. Prefer these alternatives:
1. **Box shadow** for subtle separation (softer than a border)
2. **Background color difference** between adjacent sections
3. **Extra spacing** to create separation
4. **No separator at all** — let content grouping speak for itself

When you must use borders:
- Use **light, thin** borders (`1px solid oklch(90% 0.01 250)`)
- Never use thick, dark borders for content separation
- Reserve strong borders for focus states and interactive elements

### Box shadow as elevation

```css
/* Subtle card elevation — barely there */
--shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.05);

/* Medium elevation — dropdowns, popovers */
--shadow-md: 0 4px 6px -1px oklch(0% 0 0 / 0.07),
             0 2px 4px -2px oklch(0% 0 0 / 0.05);

/* High elevation — modals, floating panels */
--shadow-lg: 0 10px 15px -3px oklch(0% 0 0 / 0.08),
             0 4px 6px -4px oklch(0% 0 0 / 0.04);
```

**Key insight**: If you can clearly see the shadow, it's too strong. Shadows should create a subtle sense of depth, not be decorative.

## 5. Interactive States

### Every interactive element needs 5 states

| State | Purpose | Techniques |
|-------|---------|------------|
| **Default** | Resting state | Base style |
| **Hover** | "This is interactive" | Subtle background, color shift, cursor change |
| **Active/Pressed** | "You're clicking" | Slight scale-down, darker shade, inset shadow |
| **Focus** | Keyboard navigation | Visible ring/outline (2-3px, contrasting color) |
| **Disabled** | "Not available now" | Reduced opacity (0.4-0.5), cursor: not-allowed |

### Hover states done right

```css
.button {
  background: var(--primary-500);
  transition: all 150ms cubic-bezier(0.25, 1, 0.5, 1);
}

/* ❌ Don't: jarring color jump */
.button:hover { background: var(--primary-800); }

/* ✅ Do: subtle, refined shift */
.button:hover {
  background: var(--primary-600);
  box-shadow: 0 2px 8px oklch(0% 0 0 / 0.12);
  transform: translateY(-1px);
}

/* ✅ Active: ground it */
.button:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px oklch(0% 0 0 / 0.1);
}
```

### Focus rings are non-negotiable

```css
/* Use outline, not border (outline doesn't affect layout) */
:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* Remove focus for mouse users, keep for keyboard */
:focus:not(:focus-visible) {
  outline: none;
}
```

## 6. Loading, Empty, & Error States

### Skeleton screens > spinners

Skeleton screens set spatial expectations. Users perceive faster loading because they see the layout forming:

```css
.skeleton {
  background: linear-gradient(
    90deg,
    oklch(92% 0.01 250) 25%,
    oklch(96% 0.01 250) 50%,
    oklch(92% 0.01 250) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Empty states are an opportunity

An empty state (no data, first use) is NOT just "No items found." It's a chance to:
1. **Explain** what this section will show once populated
2. **Encourage action** with a clear CTA ("Create your first project")
3. **Delight** with thoughtful illustration or copy
4. **Educate** about the feature's value

### Error states need empathy

- Use warm, human language ("Something went wrong" > "Error 500")
- Suggest next steps ("Try refreshing" or "Contact support")
- Preserve user input — never clear a form on validation error
- Inline validation > form-level error banners
- Red is for errors only — don't dilute its meaning

## 7. Micro-interactions

### Feedback loops

Every user action should have immediate visual feedback:

| Action | Feedback | Timing |
|--------|----------|--------|
| Button click | Color shift + scale(0.97) | <100ms |
| Toggle switch | Slide + color change | 200ms |
| Form submit | Button → loading spinner → success checkmark | <300ms each phase |
| Item added to list | Smooth height expansion + fade-in | 300ms |
| Delete | Fade out + collapse | 200ms |
| Drag start | Elevation increase + subtle rotation | 150ms |

### Optimistic UI

Update the interface immediately, handle failures gracefully:
- **Use for**: Likes, bookmarks, toggles, simple state changes
- **Avoid for**: Payments, deletions, anything with real consequences
- Show immediate visual change → sync with server → silently revert on failure

### Progress indication

- **0-1 second**: No indicator needed (instant feel)
- **1-3 seconds**: Skeleton or progress bar
- **3-10 seconds**: Progress bar with percentage + estimated time
- **10+ seconds**: Background processing with notification on completion

## 8. Responsive Design Details

### Content-first breakpoints

Don't use arbitrary breakpoints (768px, 1024px). Instead:
1. Resize your browser until the design **breaks**
2. Add a breakpoint **there**
3. This ensures breakpoints serve your content, not device assumptions

### Container queries for components

```css
.card-container { container-type: inline-size; }

/* Card adapts to its container, not viewport */
@container (min-width: 400px) {
  .card { grid-template-columns: 120px 1fr; }
}
@container (max-width: 399px) {
  .card { grid-template-columns: 1fr; }
}
```

### Mobile-specific details

- **Touch targets**: Minimum 44×44px (even if visual element is smaller)
- **Thumb zones**: Primary actions in bottom half of screen
- **Text size**: 16px minimum body text (prevents iOS auto-zoom on input focus)
- **Padding**: More generous horizontal padding on mobile (16-20px)

## 9. Optical Adjustments

Things that are mathematically correct often look wrong. Trust your eyes:

### Centering icons in circles
A geometric center point ≠ optical center. Play icons need to shift 2-3px right; down arrows need 1-2px down.

### Text alignment
Text at `padding-left: 0` appears indented because of letterform whitespace. Use negative margin (`-0.04em`) to optically align text with elements above.

### Consistent spacing illusion
Padding inside a button with text appears different on top vs bottom due to ascenders/descenders. Add 1-2px more to the top to optically center.

```css
.button {
  /* Visually centered, not mathematically */
  padding: 10px 20px 8px;
}
```

### Color weight
Bright/saturated colors feel "heavier" than desaturated ones. When placing a vivid icon next to muted text, the icon will dominate. Either desaturate the icon slightly or give the text more weight (bolder/larger).

## 10. Dark Mode Done Right

Dark mode is NOT inverted light mode:

| Aspect | Light Mode | Dark Mode |
|--------|-----------|-----------|
| Depth | Shadows (dark below) | Lighter surfaces (no shadows) |
| Text weight | Normal (400) | Slightly lighter (350) |
| Accent colors | Vibrant | Desaturated 10-15% |
| Backgrounds | White/near-white | Dark gray (NEVER pure #000) |
| Images | Normal | Slightly reduce brightness |
| Borders | Gray | Lighter gray or remove entirely |

```css
:root[data-theme="dark"] {
  /* Elevation = lighter, not shadowed */
  --surface-0: oklch(12% 0.01 250); /* Base */
  --surface-1: oklch(17% 0.01 250); /* Cards */
  --surface-2: oklch(22% 0.01 250); /* Elevated */
  --surface-3: oklch(27% 0.01 250); /* Popovers */

  /* Reduce text weight on dark backgrounds */
  --body-weight: 350;

  /* Desaturate accents */
  --primary: oklch(68% 0.12 250); /* vs 60% 0.15 in light */
}
```

## 11. Iconography

- **Consistent style**: Don't mix filled and outlined icons. Pick one system.
- **Optical sizing**: Icons at 16px need thicker strokes than at 24px. Use the font's optical size axis or provide separate icon sets.
- **Meaningful use**: Icons should aid recognition, not decorate. If the icon doesn't immediately communicate meaning, use text instead.
- **Alignment**: Icons next to text should align to the text baseline or center, never float.

## 12. The Polish Checklist

Before shipping, verify:

- [ ] **Hierarchy**: Squint test — can you identify the most important element?
- [ ] **Spacing**: Is the spacing consistent and using a defined scale?
- [ ] **States**: Does every interactive element have hover, active, focus, disabled?
- [ ] **Empty states**: What does the user see with no data?
- [ ] **Error states**: What happens when something goes wrong?
- [ ] **Loading states**: Skeleton screens or appropriate spinners?
- [ ] **Typography**: Is text readable? Line length ≤ 65ch? Proper hierarchy?
- [ ] **Color contrast**: All text meets WCAG AA (4.5:1)?
- [ ] **Touch targets**: All interactive elements ≥ 44px tap area?
- [ ] **Reduced motion**: Animations respect `prefers-reduced-motion`?
- [ ] **Dark mode**: Surfaces, shadows, and accents properly adapted?
- [ ] **Responsive**: Content breaks are smooth, nothing overflows?
- [ ] **Focus management**: Tab order is logical? Focus visible on keyboard nav?
- [ ] **Micro-copy**: Button labels are action-oriented? Error messages helpful?

---

**Sources**: Refactoring UI (Adam Wathan & Steve Schoger), Material Design Guidelines, Apple HIG, WCAG 2.1, Rovertech Micro-interactions Guide, Detail Garden design knowledge collection.
