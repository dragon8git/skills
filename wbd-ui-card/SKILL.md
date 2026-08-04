---
name: wbd-ui-card
description: Polish WBD UniApp X list, archive, category, and task cards using the established information hierarchy, continuous icon-and-value metadata rows, semantic status anchors, and card action patterns. Use when a WBD page needs richer card presentation, a card redesign, field-layout alignment, or merged filter and summary UI while preserving existing real data and business behavior.
---

# WBD UI: Card

Use this skill for card-dense WBD list pages. Improve comprehension and scan speed without inventing fields or changing requests, navigation, editing, deletion, permissions, or loading behavior.

## Workflow

1. Read the target page, its item type/API schema, and the nearest named reference. Follow repository graph-first rules before file exploration.
2. List only confirmed fields. Choose the smallest set that answers: what is this, what is its meaningful state or quantity, and where/when or which identifier applies.
3. Preserve the current data flow. Change template wrappers and page-local styles only unless the request explicitly includes behavior.
4. Use `apply_patch`, then run the WBD HBuilderX Mini Program compile and `git diff --check`. Do not claim device visual QA without a device check.

## Card Anatomy

Use this hierarchy when the confirmed fields support it:

```uvue
<view class="item-card">
  <view class="card-head">
    <view class="item-icon"><jk-icon name="material-symbols:assignment-outline-rounded" color="#1677e8" size="36rpx" /></view>
    <view class="card-main">
      <text class="item-title">{{ item.name }}</text>
      <text v-if="subtitle.length > 0" class="item-subtitle">{{ subtitle }}</text>
    </view>
    <view v-if="hasReliableStatus" :class="'status-anchor ' + statusClass">...</view>
  </view>
  <view class="meta">
    <view class="meta-item">
      <view class="meta-label"><jk-icon name="material-symbols:tag-rounded" color="#5d718a" size="28rpx" /><text>编号</text></view>
      <wbd-overflow-scroll-text class="meta-value" align="end" :text="item.code" />
    </view>
  </view>
  <view v-if="hasActions" class="card-actions">...</view>
  <view v-else-if="canNavigateToDetail" class="card-link"><text>查看详情</text><jk-icon color="#8e8e93" name="mdi:arrow-right" size="24rpx" /></view>
</view>
```

- Header: use an icon, primary name, and at most one subordinate context line. Make the title multi-line when hierarchy text is long; use `wbd-overflow-scroll-text` only for values that must stay on one line.
- Status anchor: place a confirmed status, count, or sequence at the right of the header. Use a compact semantic block with a label and emphasized value. Do not create a status from a guessed field.
- Metadata: use continuous rows with `jk-icon + neutral label` left and `font-weight: 600`, right-aligned value right. Default to a breathable rhythm: `min-height: 70rpx` with `padding: 8rpx 4rpx` and thin separators. Only use the denser `58rpx` row when the card has many confirmed fields and space is materially constrained. Use `wbd-overflow-scroll-text align="end"` for long identifiers, locations, and certificate numbers. When a card includes a project address alongside date/person fields, place the address as the final metadata row.
- Dense building-style KV grid: when a card has very many confirmed, short key-value fields and continuous rows would make it excessively tall, use the `/pages/wbd/maintenance/building/building.uvue` `building-card` pattern instead. Keep the normal header, then group fields in a restrained two-column `detail-grid` on a single muted panel; each `detail-cell` places a neutral label above a semibold value. Use this only for compact, comparable values such as counts, floors, areas, and quantities. Keep long addresses, identifiers, and prose as full-width rows; do not force them into a half-width cell or invent placeholder business values.
- Semantic emphasis: color only fields with trustworthy business meaning. For example, use red for an actual nonconforming count and amber for a known deadline. A key count may use a subtle tinted row and left rail, but do not turn every row into a pill or nested card.
- Actions: default to separated, equal-width icon-plus-label buttons with blue primary/edit and red destructive semantics. When actions are secondary, few in number, and should remain visually quiet, choose the optional `/pages/wbd/maintenance/building/building.uvue` `building-actions action-row` style instead: right-align compact muted pill buttons with a light neutral background and border; preserve red icon/text only for destructive actions. Do not mix both action styles in one card. Reserve `wbd-feishu-tabbar` for page-level fixed actions, not card-local actions.
- Detail navigation: when a card has no card-local buttons and the existing card click already navigates to another page, add the `/pages/wbd/detection/index.uvue` `card-link` affordance after metadata: `查看详情` plus a neutral right arrow, separated by a top divider and right-aligned. It is a visual cue only: retain the existing card click handler, URL, parameters, and navigation guards. Do not add it to cards with actions or cards without confirmed navigation behavior.

## Filter and Summary

If filter/search and summary describe the same collection, merge them into one top-level overview card:

1. Header: collection title, context, and a factual total count.
2. Divider: visually separate the header from filtering controls.
3. Search/filter control: retain its bindings and submit behavior.

Do not merge unrelated filters or hide essential selection state. Do not introduce a second card merely to repeat the total.

## Visual Baseline

```css
.item-card { margin-top:18rpx; padding:26rpx; border:1rpx solid #e2eaf5; border-radius:28rpx; background-color:#fff; box-shadow:0 10rpx 28rpx rgba(37,67,112,.06); }
.card-head,.meta-item,.card-actions { flex-direction:row; align-items:center; }
.card-main { flex:1; min-width:0; }
.item-title { color:#18202c; font-size:30rpx; font-weight:700; line-height:40rpx; }
.item-subtitle { margin-top:4rpx; color:#687487; font-size:23rpx; line-height:32rpx; }
.meta { margin-top:20rpx; border-top:1rpx solid #edf1f6; }
.meta-item { min-height:70rpx; padding:8rpx 4rpx; border-bottom:1rpx solid #f0f3f7; justify-content:space-between; }
.meta-label { flex:1; min-width:0; flex-direction:row; align-items:center; }
.meta-label text { margin-left:10rpx; color:#687487; font-size:23rpx; }
.meta-value { max-width:52%; margin-left:24rpx; color:#26384d; font-size:23rpx; font-weight:600; text-align:right; }
.card-actions { margin-top:20rpx; padding-top:18rpx; border-top:1rpx solid #edf1f6; gap:16rpx; }
.card-link { margin-top:14rpx; padding-top:14rpx; border-top:1rpx solid #edf0f5; flex-direction:row; align-items:center; justify-content:flex-end; }
.card-link text { margin-right:6rpx; color:#6e6e73; font-size:23rpx; }
```

## Guardrails

- Use actual API/type fields only. Check OpenAPI when an endpoint or field meaning is uncertain.
- Do not replace empty, missing, or unknown data with a business claim; render a neutral fallback such as `—`.
- Do not duplicate the same field in header, tags, and metadata.
- Do not add colourful chips, individual mini-cards, gradients, or decorative status when the data does not justify them.
- Use `jk-icon`, preferring `material-symbols`; do not add ad-hoc image assets.
- Keep business actions, URLs, parameters, deleting state, and error handling intact.
