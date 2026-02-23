# Two-Column Layout - Visual Guide

## Overall Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│                     PAGE HEADER                         │
│                   (Full width)                          │
├──────────────────┬──────────────────────────────────────┤
│                  │                                      │
│  SIDEBAR PANEL   │         CONTENT AREA                 │
│  (280px fixed)   │         (Flex: 1)                    │
│  Light grey bg   │         White background            │
│                  │                                      │
│  - Section 1     │      Main Content                    │
│  - Input fields  │      ├─ Questions                    │
│  - Controls      │      ├─ Results                      │
│  - Buttons       │      ├─ Forms                        │
│                  │      └─ Tables                       │
│                  │                                      │
└──────────────────┴──────────────────────────────────────┘
```

---

## Teacher Create Exam Page

```
┌────────────────────────────────────────────────────────────┐
│ Create Exam                                                │
├──────────────┬────────────────────────────────────────────┤
│              │                                            │
│ Exam Setup   │  Configure exam settings in left panel   │
│              │  Click "Generate Preview" to see...       │
│ [Topic ___]  │                                            │
│              │  OR (after preview)                       │
│ Difficulty ▼ │                                            │
│ [ Medium ]   │  Questions Preview                        │
│              │                                            │
│ Questions #  │  Test ID: abc123...                       │
│ [   5     ]  │  Topic: History                           │
│              │  Total: 5 questions                       │
│              │                                            │
│ [Generate]   │  ┌─────────────────────────────┐          │
│ [Copy Link]  │  │ Q1: Question text here...   │          │
│ [Create]     │  │ A. Option 1                 │          │
│              │  │ B. Option 2                 │          │
│              │  │ C. Option 3                 │          │
│              │  └─────────────────────────────┘          │
│              │                                            │
│              │  ┌─────────────────────────────┐          │
│              │  │ Q2: Question text here...   │          │
│              │  │ A. Option 1                 │          │
│              │  │ B. Option 2                 │          │
│              │  └─────────────────────────────┘          │
│              │                                            │
│              │  ✅ Test created! Share link:             │
│              │  http://localhost:5173/exam/abc123        │
│              │                                            │
└──────────────┴────────────────────────────────────────────┘
```

---

## Student Exam - Start Screen

```
┌────────────────────────────────────────────────────────────┐
│ Exam Details                                               │
├──────────────┬────────────────────────────────────────────┤
│              │                                            │
│ Test Info    │  Topic: History                           │
│              │  Difficulty: Medium                       │
│ Your Name    │  Total Questions: 5                       │
│ [John Doe]   │                                            │
│              │  Enter your name and click                │
│              │  Start Test to begin.                     │
│              │                                            │
│ [Start Test] │                                            │
│              │                                            │
└──────────────┴────────────────────────────────────────────┘
```

---

## Student Exam - During Exam

```
┌────────────────────────────────────────────────────────────┐
│ Exam                                                       │
├──────────────┬────────────────────────────────────────────┤
│              │                                            │
│ Student Info │  Question 1 of 5                         │
│              │                                            │
│ Progress:    │  What is the capital of India?           │
│ 0 / 5        │                                            │
│              │  ◯ New Delhi                              │
│              │  ◯ Mumbai                                 │
│              │  ◯ Kolkata                                │
│              │  ◯ Delhi Cantonment                       │
│              │                                            │
│              │  ─────────────────────────────────────   │
│              │                                            │
│              │  Question 2 of 5                         │
│              │                                            │
│              │  What year did India become independent?  │
│              │                                            │
│              │  ◯ 1947                                   │
│              │  ◯ 1950                                   │
│              │  ◯ 1952                                   │
│              │                                            │
│              │  ─────────────────────────────────────   │
│              │                                            │
│              │  [Submit Exam]                            │
│              │                                            │
└──────────────┴────────────────────────────────────────────┘
```

---

## Results Page

```
┌────────────────────────────────────────────────────────────┐
│ Results                                                    │
├──────────────┬────────────────────────────────────────────┤
│              │                                            │
│ Result       │  PASSED                                  │
│              │                                            │
│ Status:      │  ┌──────────┐                             │
│ Passed       │  │   80%    │                             │
│              │  └──────────┘                             │
│ Score:       │                                            │
│ 80%          │  Student         John Doe                 │
│              │  Total Questions 5                        │
│ [Back Home]  │  Correct         4                        │
│              │  Wrong           1                        │
│              │  Percentage      80.0%                    │
│              │                                            │
│              │  ┌───────────────────────────────┐        │
│              │  │ Great job! You passed.        │        │
│              │  └───────────────────────────────┘        │
│              │                                            │
└──────────────┴────────────────────────────────────────────┘
```

---

## Teacher Dashboard

```
┌────────────────────────────────────────────────────────────┐
│ Dashboard                                                  │
├──────────────┬────────────────────────────────────────────┤
│              │                                            │
│ Actions      │  Last Created Test                       │
│              │                                            │
│ [Create Test]│  Test ID: abc123...                      │
│ [Refresh]    │                                            │
│              │  Share Link:                              │
│              │  http://localhost:5173/exam/abc123        │
│              │  [Copy Link]                              │
│              │                                            │
│              │  Student Submissions                      │
│              │  Total: 3 submission(s)                  │
│              │                                            │
│              │  ┌──────────┬────┬────┬────┬────┐        │
│              │  │ Student  │Scr │Corr│Wrng│Stat│        │
│              │  ├──────────┼────┼────┼────┼────┤        │
│              │  │ John Doe │ 80%│ 4  │ 1  │PASS│        │
│              │  │ Jane Doe │ 60%│ 3  │ 2  │PASS│        │
│              │  │ Bob Smith│ 40%│ 2  │ 3  │FAIL│        │
│              │  └──────────┴────┴────┴────┴────┘        │
│              │                                            │
└──────────────┴────────────────────────────────────────────┘
```

---

## Mobile View (≤ 768px)

All elements stack vertically in single column:

```
┌─────────────────────────────────────────┐
│          Page Header                    │
├─────────────────────────────────────────┤
│          SIDEBAR PANEL                  │
│          (Full Width)                   │
│  ┌──────────────────────────────────┐  │
│  │ Section 1                        │  │
│  │ [Input fields]                   │  │
│  │ [Buttons]                        │  │
│  └──────────────────────────────────┘  │
├─────────────────────────────────────────┤
│       CONTENT AREA                      │
│       (Full Width)                      │
│  ┌──────────────────────────────────┐  │
│  │ Main Content                     │  │
│  │ ├─ Questions                     │  │
│  │ ├─ Forms                         │  │
│  │ └─ Results                       │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## Color Reference

### Main Colors
- **Text:** #333 (dark grey)
- **Background:** #fff (white)
- **Sidebar:** #fafafa (very light grey)
- **Borders:** #ddd (light grey)

### Accent Colors
- **Primary:** #333 (black)
- **Success:** #2e7d32 (dark green)
- **Error:** #d32f2f (dark red)
- **Secondary Text:** #666 (medium grey)

### Buttons
```
.btn-primary: #333 background, white text
.btn-secondary: #f5f5f5 background, #333 text
.btn-success: #2e7d32 background, white text
```

---

## Spacing Scale

```
xs: 0.5rem (8px)   - Tight spacing
sm: 1rem (16px)    - Standard spacing
md: 1.5rem (24px)  - Loose spacing
lg: 2rem (32px)    - Very loose spacing
```

---

## Typography Hierarchy

```
h1: 1.8rem - Page titles (largest)
h2: 1.4rem - Section headers
h3: 1.2rem - Subsection headers
h4: 1rem   - Card/item titles
p:  0.95rem - Body text
label: 0.95rem - Form labels
small: 0.85rem - Secondary/metadata (smallest)
```

---

## Key CSS Classes for Layout

### Container Layout
- `.container` - Main flex container (display: flex)
- `.sidebar-panel` - Left sidebar (flex: 0 0 280px)
- `.content-area` - Main content (flex: 1)

### Content Sections
- `.page-header` - Top section with title
- `.content-wrapper` - Padded content container
- `.sidebar-section` - Groups within sidebar

### Form Elements
- `.form-group` - Wrapper for label + input
- `.input-field` - Input/select/textarea element
- `.form-row` - Multi-column form row (grid)

### Components
- `.question-section` - Single question
- `.options-group` - Options container
- `.option-label-container` - Radio button wrapper
- `.result-details` - Results table
- `.status-badge` - Status indicator

### Messages
- `.error-message` - Error (red accent)
- `.success-message` - Success (green accent)
- `.empty-state` - Empty state
- `.loading-state` - Loading state

---

## Responsive Breakpoints

```css
Desktop:    > 768px (sidebar visible)
Tablet:     768px - 1024px (sidebar at top)
Mobile:     < 768px (sidebar at top, full width)
```

Media query:
```css
@media (max-width: 768px) {
  .container { flex-direction: column; }
  .sidebar-panel { width: 100%; }
}
```

---

## Design Philosophy

✅ **Clean and minimal** - No unnecessary decorations  
✅ **Focused on functionality** - Simple, clear hierarchy  
✅ **Exam-oriented** - Designed for student exams  
✅ **Easy to navigate** - Sidebar for controls, center for content  
✅ **Accessible** - High contrast, readable fonts  
✅ **Responsive** - Works on all devices  
✅ **No distractions** - Flat design, no animations  

