---
name: theme-cases
description: Propose at least 10 visual directions for an existing frontend component, let the user select up to 3, then add a temporary in-component switcher so they can compare the selected themes live and choose one to retain. Use when a user asks for multiple UI directions, component theme cases, visual alternatives, or a switchable style preview.
---

# Theme Cases

Create comparison-ready component themes without turning preview plumbing into product code. The user, not the agent, judges visual results by default.

## Workflow

1. Inspect the target component, its caller, and the local design guidance. Preserve functional props, events, validation, accessibility, and platform behavior.
2. State the visual problem in one sentence. Propose at least 10 candidate cases before writing preview code. For each case, provide a stable key, a short user-facing label, its primary design axis, and a concise design overview. Cases must differ structurally, such as boundary treatment, metadata placement, surface layering, or focus-state behavior. Do not produce cosmetic color-only variations.
3. Stop and ask the user to select no more than 3 candidates. Do not implement preview themes until the selection is explicit.
4. Implement only the selected cases. Add a temporary, clearly labeled segmented switcher adjacent to or inside the target component, and render it only for the nominated preview caller.
5. Keep preview selection state inside the component whenever possible. A local state change must update the rendered class directly; do not require a parent event round trip merely to switch previews.
6. Keep each selected case within the existing design system. Preserve the component's functional props, events, validation, accessibility, platform behavior, content growth, resize behavior, counters, and disabled state.
7. When the user selects a final case, make it the only default implementation. Remove the switcher, preview-only props, selection state, unused styles, temporary event handlers, and preview caller code.

## Design Rules

- Let the component itself carry attention through hierarchy, boundary, surface, or state. Do not add redundant labels merely to create emphasis.
- Keep enterprise and form interfaces restrained. Favor a single clear anchor over stacked banners, heavy shadows, or multiple competing accents.
- Make information strips and separators earn their space: provide visible breathing room and adequate contrast.
- Prefer existing component and icon conventions. Do not introduce new assets for preview-only decoration.
- Do not leave a visual selector visible to production users unless the user explicitly asks for a permanent preference setting.

## User-Led Evaluation

- Do not run compile, build, diff, formatting, browser, or interaction checks by default. Visual comparison and judgment belong to the user.
- Perform a verification step only when the user explicitly asks for it.
- After the user selects a final case, report which theme was retained and confirm preview code was removed.

## Example Invocation

`$theme-cases 为 wbd-textarea 提供至少十种提升视觉锚点的方案；我选择三种后，在任务表单中加入临时切换预览。`
