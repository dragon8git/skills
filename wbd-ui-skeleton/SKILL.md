---
name: wbd-ui-skeleton
description: Build or repair WBD UniApp X detail-page loading states with structural skeletons, concurrent detail and flow requests, and silent refreshes that preserve rendered data. Use for WBD `.uvue` project/detail pages where an initial full-page loading card is abrupt, data becomes stale after returning from child pages, or dynamic detail/flow sections need a mobile-compatible skeleton.
---

# WBD UI Skeleton

Use this skill for WBD UniApp X detail pages, especially project summary + application grid + processing timeline pages.

## Required checks

1. Follow the repository's graph-first exploration rule, then inspect the target page's `onLoad`, `onShow`, `loadDetail`, error state, and flow request.
2. Reuse an existing skeleton when it matches the page structure. For the detection/evaluate project-detail pattern, reuse `app/components/wbd-project-detail-skeleton/wbd-project-detail-skeleton.uvue`.
3. Do not add a new cache merely to avoid a spinner. First preserve already-rendered `detail` state during refresh. Use an existing page cache only when the page already has one.

## Loading contract

Keep these states distinct.

| State | UI behavior |
| --- | --- |
| First load, no `detail` | Render a layout-matched skeleton; do not show a generic whole-page loading card. |
| Refresh, existing `detail` | Keep the full page rendered; fetch silently and replace results when ready. |
| Detail request fails without data | Retain the existing error/retry state. |
| Detail request resolves empty | Retain the existing empty state. |
| Flow request fails | Use an empty timeline fallback if that is the page's existing failure convention; do not make a successful detail page fail solely for flow data. |

## Request and lifecycle pattern

Use the page's existing `loading` guard. Make independent detail and flow requests concurrent, then clear first-load loading only after both settle.

```uts
let skipInitialShowRefresh = true

onLoad((options) => {
  // resolve stable route ID
  loadDetail()
})

onShow(() => {
  if (skipInitialShowRefresh) {
    skipInitialShowRefresh = false
    return
  }
  loadDetail()
})

function loadDetail() {
  if (projectId.value.length == 0 || loading.value) return
  loading.value = true
  errorText.value = ''
  const hadDetail = detail.value != null
  const flowRequest = loadFlowStepDataBySource({ source, sourceId: projectId.value })
    .catch(() => ({ data: [] as FlowStepData[] }))

  getProject(projectId.value)
    .then((res) => {
      detail.value = res.data == null ? null : res.data!
      if (hadDetail && detail.value != null) detailRefreshing.value = true
      return flowRequest
    })
    .then((flowRes) => { timelineItems.value = mapFlow(flowRes) })
    .catch((err) => { errorText.value = errorTextOf(err) })
    .finally(() => {
      loading.value = false
      if (detailRefreshing.value) setTimeout(() => { detailRefreshing.value = false }, 180)
    })
}
```

- Do not set `detail.value = null` before a refresh; that causes a visible reset and defeats silent refresh.
- Skip the first `onShow`: UniApp X normally runs it immediately after `onLoad`, so otherwise the initial request can be duplicated or hidden behind a timing-dependent guard.
- Prefer this page lifecycle refresh policy over a one-off child-page EventChannel when the page is intentionally defined to refresh on every entry.
- Retain a targeted EventChannel only where refresh must occur exclusively after a successful mutation and the page must not refresh for ordinary returns.

## Skeleton structure and motion

- Match the actual hierarchy: overview card, application/icon grid, and flow/timeline card. Do not use uniform anonymous bars for the entire screen.
- Keep app-count, row count, spacing, card radius, and background close to the destination page, so replacement does not jump.
- Use neutral low-contrast blocks and a subtle pulse; include `prefers-reduced-motion` to disable it.
- For an existing-data refresh, animate only the updated top-level detail region with a short opacity transition, around `180ms`. Do not add GSAP, scroll effects, or full-page fades to mobile business pages.

```css
.detail-refreshing { animation: detail-refresh 180ms ease-out; }
@keyframes detail-refresh { from { opacity: .72; } to { opacity: 1; } }
```

## Guardrails

- Keep request endpoints, status logic, page navigation, and form state unchanged unless the task explicitly includes them.
- Do not hide existing data during background refresh.
- Do not add request-local or global caches without a stated invalidation source; in-memory rendered data is enough for silent refresh.
- Do not claim device visual validation from compilation alone.
- After changes run `launch mp-weixin --compile true --continue-on-error false` and `git diff --check`; manually validate first load, slow flow response, child-page return, detail failure, and empty data in WeChat DevTools.
