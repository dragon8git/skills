---
name: theme-cases
description: Create 3-5 clearly distinct visual themes for an existing frontend component, add a temporary in-component switcher so users can compare them live, then retain the selected theme and remove preview code. Use when a user asks for multiple UI directions, component theme cases, visual alternatives, or a switchable style preview.
---

# Theme Cases

Create comparison-ready component themes without turning preview plumbing into product code.

## Workflow

1. Inspect the target component, its caller, and the local design guidance. Preserve functional props, events, validation, accessibility, and platform behavior.
2. State the visual problem in one sentence. Design 3 to 5 cases that differ by a primary axis, such as boundary treatment, metadata placement, surface layering, or focus-state behavior. Do not produce cosmetic color-only variations.
3. Add a temporary, clearly labeled segmented switcher adjacent to or inside the target component. Render it only for the nominated preview caller.
4. Keep preview selection state inside the component whenever possible. A local state change must update the rendered class directly; do not require a parent event round trip merely to switch previews.
5. Give every case a stable internal key and a short user-facing label. Keep all cases within the existing design system; do not introduce a new visual language just to make variants look different.
6. Preserve the component's behavioral contract across all cases. If the component supports content growth, resize, counters, disabled state, or validation, every preview case must retain it.
7. When the user selects a case, make it the only default implementation. Remove the switcher, preview-only props, selection state, unused styles, temporary event handlers, and preview caller code.

## Design Rules

- Let the component itself carry attention through hierarchy, boundary, surface, or state. Do not add redundant labels merely to create emphasis.
- Keep enterprise and form interfaces restrained. Favor a single clear anchor over stacked banners, heavy shadows, or multiple competing accents.
- Make information strips and separators earn their space: provide visible breathing room and adequate contrast.
- Prefer existing component and icon conventions. Do not introduce new assets for preview-only decoration.
- Do not leave a visual selector visible to production users unless the user explicitly asks for a permanent preference setting.

## Verification

- Run the repository's required compile or build check after code changes.
- Run the repository's diff or formatting check when available.
- Perform browser interaction checks only when requested or when the switcher behavior cannot be confirmed statically.
- Report which theme was retained and confirm preview code was removed after selection.

## Example Invocation

`$theme-cases 为 wbd-textarea 生成四种提升视觉锚点的方案，在任务表单中加入临时切换预览。`
