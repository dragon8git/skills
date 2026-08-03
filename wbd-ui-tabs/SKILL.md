---
name: wbd-ui-tabs
description: Build or refine count-aware status tabs in WBD UniApp X (.uvue) list pages. Use when a tab represents a business status and should display its live record count inline while retaining WBD's compact segmented-control hierarchy.
---

# WBD Tab Counts

Use this pattern for a small, mutually exclusive set of status filters on a mobile WBD list page. The count is supporting information, not a separate badge: render it inline after the label so the tab remains compact and easy to scan.

## Implement

1. Derive every tab count from the same already-filtered source collection that the tab will filter. Never hardcode counts or invent a status when its data is unavailable.
2. Keep `全部` first. Use short status labels and normally keep the set to 2–5 tabs; split a separate high-level category switch into its own control above the status tabs.
3. Render the count only when it is greater than zero. Format it as `({{ item.count }})` directly after the label.
4. Keep the selected tab valid when its source changes. If a selected non-default tab reaches zero or disappears, reset it to `all`.
5. Reuse the page's existing data-loading and filtering flow. Do not introduce a global tab component or a second source of truth for a one-page filter.

```vue
<view class="tabs">
  <view
    v-for="item in statusTabs"
    :key="item.value"
    :class="status == item.value ? 'tab active' : 'tab'"
    @tap="setStatus(item.value)"
  >
    <text>{{ item.label }}</text>
    <text v-if="item.count > 0" class="tab-count">({{ item.count }})</text>
  </view>
</view>
```

```ts
const statusTabs = computed(() => {
  const source = typeRecords.value
  return [
    { value: 'all', label: '全部', count: source.length },
    { value: 'processing', label: '进行中', count: source.filter((item) => isProcessing(item)).length },
    { value: 'done', label: '已完成', count: source.filter((item) => item.status == 99).length }
  ]
})

watch([statusTabs], () => {
  if (status.value == 'all') return
  const current = statusTabs.value.find((item) => item.value == status.value)
  if (current == null || current.count == 0) status.value = 'all'
})
```

## Style

Use the existing WBD segmented-control treatment. In `.uvue`, retain `rpx` values and flex layout; do not replace it with web-only DOM or CSS behavior.

```css
.tabs {
  margin-top: 20rpx;
  padding: 6rpx;
  flex-direction: row;
  background-color: #eef2f7;
  border-radius: 22rpx;
}
.tab {
  flex: 1;
  height: 64rpx;
  border-radius: 22rpx;
  color: #6e6e73;
  font-size: 25rpx;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.tab text { color: inherit; font-size: 25rpx; font-weight: inherit; }
.tab-count { margin-left: 4rpx; font-size: 22rpx; }
.active {
  color: #0071e3;
  font-weight: 650;
  background-color: #fbfcff;
  box-shadow: 0 4rpx 12rpx rgba(34, 58, 94, 0.08);
}
```

Keep count text in the tab's inherited color. Do not turn it into a pill, alert color, or separate badge unless the count itself has verified business severity.

## Verify

- Change the backing records or filters and confirm every count changes with the visible result set.
- Select a non-default tab, then make its count zero; confirm selection returns to `全部`.
- Check mobile-width layout: all labels and nonzero counts remain on one line without crowding.
- Run the repository's HBuilderX web compilation. For a WeChat-targeted change, also compile and verify in the WeChat developer tools.
