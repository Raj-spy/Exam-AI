# 🎨 Academic Design System Specification

## Overview
Complete design system for the Exam AI frontend with clean, professional, academic styling.

---

## Color Palette

### Primary Colors
```
Primary Blue:     #4a90e2  (Soft blue for main actions)
Secondary Grey:   #718096  (For secondary text)
Dark Text:        #2c3e50  (Primary text)
Darkest Text:     #1a202c  (Headings)
```

### Neutral Colors
```
White:            #ffffff  (Cards, sections)
Off-white:        #f8f9fb  (Page background)
Light Grey:       #f0f4f8  (Light backgrounds)
Medium Grey:      #e2e8f0  (Borders)
Medium-Dark Grey: #cbd5e0  (Input borders)
```

### Status Colors
```
Success Green:    #22c55e  (Passing, correct)
Error Red:        #ef4444  (Failing, wrong)
Warning Orange:   #f97316  (Alerts - if needed)
```

### Usage Guidelines
- Use primary blue for main buttons and highlights
- Use grey for secondary text and borders
- Use green for success states
- Use red for error states
- Keep backgrounds light (white or off-white)
- Use sufficient contrast (WCAG AA minimum)

---

## Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
```

### Font Sizes
```
h1:  2.2rem  (Page titles)
h2:  1.5rem  (Section headings)
h3:  1.1rem  (Sub-headings)
p:   1rem    (Body text)
small: 0.85rem or 0.9rem (Helper text, labels)
```

### Font Weights
```
Normal:  400
Medium:  500 (labels, secondary headings)
Bold:    600 (headings, buttons)
Heavy:   700 (rarely used)
```

### Line Height
```
1.6  (Default for all text)
```

### Letter Spacing
```
-0.3px  (Headings - slight tightening)
0       (Body text)
```

---

## Spacing System

### Padding
```
0.5rem   = 8px   (Small)
0.75rem  = 12px  (Medium)
1rem     = 16px  (Default)
1.5rem   = 24px  (Large)
2rem     = 32px  (Extra large)
2.5rem   = 40px  (XXL - for page headers)
3rem     = 48px  (XXXL)
```

### Margins
```
Same as padding scale
0.5rem gap between form fields
1rem gap between sections
2rem gap between major sections
```

### Padding Guidelines
- Form inputs: 0.75rem
- Buttons: 0.65rem 1.5rem (vertical, horizontal)
- Cards: 2rem
- Page header: 2.5rem 2rem
- Container padding: 2rem 1.5rem

---

## Border System

### Border Radius
```
3px   - Small (inline elements like code)
4px   - Default (inputs, cards, sections)
6px   - Large (major containers)
50%   - Circle (badges, avatars)
```

### Border Thickness & Style
```
1px solid #e2e8f0     - Standard borders
1px solid #cbd5e0     - Input borders (unfocused)
2px solid #4a90e2     - Input borders (focused)
3px solid #4a90e2     - Left accent borders (cards)
```

---

## Shadows

### Philosophy
Minimal shadows - replaced with clean borders

### Usage
```
None                    - Cards use borders instead
0 2px 4px rgba(0,0,0,0.05)  - Hover states only
```

### Never Use
- Heavy box-shadows
- Drop shadows
- Glow effects
- Multiple layered shadows

---

## Buttons

### Primary Button
```css
background: #4a90e2
color: white
padding: 0.65rem 1.5rem
border: 2px solid #4a90e2
border-radius: 4px
font-weight: 500
transition: background-color 0.2s ease
hover: background: #3a7bc8
```

### Secondary Button
```css
background: #f0f4f8
color: #2c3e50
padding: 0.65rem 1.5rem
border: 2px solid #cbd5e0
border-radius: 4px
font-weight: 500
transition: background-color 0.2s, border-color 0.2s
hover: background: #e2e8f0; border-color: #a0aec0
```

### Button Sizes
```
Small:   0.5rem 1rem
Normal:  0.65rem 1.5rem  (Default)
Large:   0.8rem 2rem
Full:    100% width
```

---

## Form Elements

### Inputs, Textareas, Selects
```css
background: #f8f9fb
color: #2c3e50
padding: 0.75rem
border: 1px solid #cbd5e0
border-radius: 4px
font-size: 0.95rem
font-family: inherit
transition: border-color 0.2s ease
focus: {
  outline: none
  border-color: #4a90e2
  background: white
}
```

### Labels
```css
display: block
margin-bottom: 0.5rem
color: #2c3e50
font-weight: 500
font-size: 0.9rem
```

### Form Field Container
```css
margin-bottom: 1.5rem
```

---

## Cards & Sections

### Standard Card
```css
background: white
border: 1px solid #e2e8f0
border-radius: 6px
padding: 2rem
```

### Card with Accent
```css
border: 1px solid #e2e8f0
border-left: 4px solid #4a90e2
```

### Light Background Section
```css
background: #f8f9fb
border: 1px solid #e2e8f0
border-radius: 4px
padding: 1rem
```

---

## Tables

### Header Row
```css
background: #f0f4f8
color: #1a202c
padding: 1rem
font-weight: 600
border-bottom: 2px solid #cbd5e0
```

### Data Rows
```css
padding: 1rem
border-bottom: 1px solid #e2e8f0
hover: background: #f8f9fb
```

---

## Status Messages

### Error Message
```css
background: #fef2f2
border: 1px solid #fecaca
border-left: 4px solid #ef4444
border-radius: 4px
padding: 1rem
color: #991b1b
font-size: 0.9rem
```

### Success Message
```css
background: #f0fdf4
border: 1px solid #86efac
border-left: 4px solid #22c55e
border-radius: 4px
padding: 1.5rem
color: #166534
text-align: center
```

### Loading State
```css
background: #f8f9fb
border: 1px solid #e2e8f0
padding: 2rem
text-align: center
color: #4a5568
border-radius: 6px
```

---

## Responsive Breakpoints

```css
Mobile:    < 640px   (Extra small)
Tablet:    640px-768px (Small)
Large:     768px-1024px (Medium)
Desktop:   > 1024px  (Large)
```

### Key Breakpoints
```css
@media (max-width: 768px) {
  /* Tablet & mobile changes */
  - Reduce padding
  - Stack layouts vertically
  - Reduce font sizes slightly
  - Adjust spacing
}

@media (max-width: 640px) {
  /* Mobile only */
  - Single column layouts
  - Smaller paddings
  - Full-width elements
}
```

---

## Animation & Transitions

### Philosophy
Minimal animations only

### Allowed Transitions
```css
transition: background-color 0.2s ease;
transition: border-color 0.2s ease;
transition: color 0.2s ease;
```

### Never Use
- Bounce animations
- Spin animations
- Slide animations
- Transform translations
- Complex keyframes

---

## Accessibility

### Color Contrast
- All text must meet WCAG AA standards
- Minimum 4.5:1 ratio for body text
- Minimum 3:1 ratio for large text

### Focus States
```css
:focus {
  outline: none
  border-color: #4a90e2
}
```

### Labels
- All inputs must have associated labels
- Labels should use `for` attribute

### Semantic HTML
- Use proper heading hierarchy
- Use semantic elements (button, label, table)
- Use proper ARIA labels when needed

---

## Layout Guidelines

### Container
```css
max-width: 900px
margin: 0 auto
padding: 2rem 1.5rem
```

### Grid Layouts
```css
display: grid
grid-template-columns: 1fr 1fr  /* Two columns */
gap: 2rem
```

### Flexbox
```css
display: flex
flex-direction: column
gap: 1.5rem
```

### Max Widths
```
Main container: 900px
Form sections: 600px
Content width:  100%
```

---

## Component Specifications

### Page Header
```css
background: white
padding: 2.5rem 2rem
border-radius: 6px
border-bottom: 3px solid #4a90e2
text-align: center
margin-bottom: 2rem

h1: color #1a202c, size 1.9rem
p: color #718096, size 0.95rem
```

### Score Circle
```css
width: 140px
height: 140px
border-radius: 50%
background: #f0f4f8
border: 3px solid #4a90e2
display: flex
align-items: center
justify-content: center

score-number: color #4a90e2, size 2.5rem
```

### Question Card
```css
background: #f8f9fb
border: 1px solid #e2e8f0
border-left: 4px solid #4a90e2
border-radius: 4px
padding: 1.5rem
margin-bottom: 1rem
```

### Progress Indicator
```css
background: #f8f9fb
border: 1px solid #e2e8f0
border-radius: 4px
padding: 1rem
text-align: center
color: #4a5568
font-size: 0.9rem
```

---

## Do's and Don'ts

### Do's ✅
- Use clean, solid colors
- Use light backgrounds
- Use proper spacing
- Use clear typography
- Use subtle transitions
- Use borders instead of shadows
- Keep it simple
- Make it responsive
- Test for accessibility

### Don'ts ❌
- Don't use gradients
- Don't use heavy shadows
- Don't use bright colors
- Don't use decorative fonts
- Don't use fancy animations
- Don't use emojis in headers/buttons
- Don't overcomplicate
- Don't ignore mobile
- Don't sacrifice contrast

---

## File Organization

```
src/
├── index.css          (Global styles)
├── App.css            (App-level styles)
├── styles/
│   └── pages.css      (Page-specific styles)
└── components/
    └── Navigation.css (Component styles)
```

---

## Implementation Checklist

- [x] Color system defined
- [x] Typography scaled
- [x] Spacing system implemented
- [x] Border system applied
- [x] Buttons styled
- [x] Forms styled
- [x] Cards designed
- [x] Tables styled
- [x] Status messages styled
- [x] Responsive breakpoints set
- [x] Transitions minimal
- [x] Accessibility tested
- [x] Cross-browser compatible

---

**Design System Version**: 1.0
**Last Updated**: December 26, 2025
**Status**: ✅ Complete and Implemented
