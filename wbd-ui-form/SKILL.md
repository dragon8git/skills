---
name: wbd-ui-form
description: Align and polish WBD UniApp X business forms, especially when pickers and shared wbd-input controls look inconsistent. Use for requests to beautify or normalize WBD form fields against an established in-repo form reference while preserving business logic.
---

# WBD UI: Form

Use the nearest named WBD form as the visual source of truth. Treat its UI structure as reusable, but do not copy its API calls, field meanings, validation, or cross-subpackage imports.

## Workflow

1. Read the target form, the named reference form, and relevant shared controls. Follow repository graph-first instructions before code exploration.
2. Identify visual-only differences: field wrappers, picker selected/placeholder states, chevrons, spacing, card treatment, and disabled states.
3. Preserve bindings, option sources, async loading, edit backfill, validation, and save payloads. Change only the template wrappers and local styles required for visual alignment.
4. Use `apply_patch`, then run the required HBuilderX Mini Program compile and `git diff --check`. Do not claim device-level UI verification without testing it.

## Required Field Pattern

For ordinary business-form fields, use the reference form's `field-group` and `field-shell` structure. Keep the shell in the page stylesheet so it matches the page's style isolation.

```uvue
<view class="field-group">
  <text class="label">字段名称</text>
  <picker mode="selector" :range="labels" :value="selectedIndex" @change="changeValue">
    <view class="field-shell field-shell-select">
      <text :class="selectedIndex >= 0 ? 'field-value' : 'field-placeholder'">
        {{ selectedIndex >= 0 ? labels[selectedIndex] : '请选择' }}
      </text>
      <jk-icon color="#c0c4cc" name="material-symbols:chevron-right-rounded" size="30rpx" />
    </view>
  </picker>
</view>
```

Wrap every `wbd-input` in the same shell; do not assume the shared input owns the card-like background, border, or height.

```uvue
<view class="field-group">
  <text class="label">具体位置</text>
  <view class="field-shell">
    <wbd-input v-model="form.location" placeholder="请输入具体位置（选填）" />
  </view>
</view>
```

Use these baseline page-local styles unless the named reference has intentional variants:

```css
.field-group { margin-top:26rpx; }
.label { color:#3a3a3c; font-size:26rpx; }
.field-shell { min-height:84rpx; margin-top:12rpx; padding:0 22rpx; border-radius:22rpx; background-color:#f8fafc; border:1rpx solid #e8edf6; flex-direction:row; align-items:center; justify-content:space-between; }
.field-value { flex:1; color:#1d1d1f; font-size:26rpx; line-height:38rpx; }
.field-placeholder { flex:1; color:#808080; font-size:26rpx; line-height:38rpx; }
```

## Component Rules

- Use `wbd-input` for all business single-line inputs; use `wbd-textarea` for multi-line text.
- Reuse `wbd-building-floor-picker` for building/floor selection. Configure its props for required or optional fields; do not recreate a local picker.
- Preserve valid required-field semantics. A visual alignment must not make an optional field mandatory or erase dependent selections incorrectly.
- Use `material-symbols` icons through `jk-icon`; do not add ad-hoc icon assets.

## Guardrails

- Do not restyle a shared component to solve one page's shell mismatch. The page owns the `field-shell` wrapper.
- Do not replace a selector with a native input or alter its data flow solely for visual parity.
- Do not import runtime code from another WBD subpackage. Copy only the visual structure into the target page.
