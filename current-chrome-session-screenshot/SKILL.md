---
name: current-chrome-session-screenshot
description: Capture a screenshot of the first available tab in the user's already-open Chrome session without creating a browser, window, or tab. Use when the user asks to see, inspect, or provide a screenshot of their current Chrome browser state and explicitly wants the existing session preserved.
---

# Current Chrome Session Screenshot

Use the Chrome browser-control skill and its persistent Node runtime. Do not use Playwright, Computer Use, or an in-app browser as substitutes.

## Workflow

1. Select the explicit `chrome` browser binding. Initialize it only if absent, then read its complete `documentation()` output.
2. Name the session, then read the screenshot documentation.
3. Call `chrome.user.openTabs()` exactly once. If it returns no tabs, report that Chrome has no readable open tab and stop.
4. Claim the first returned tab object with `chrome.user.claimTab(tabs[0])`. Never call `tabs.new()`, `goto()`, reload, click, type, or navigate.
5. Capture only the current viewport with `tab.screenshot({ fullPage: false })`.
6. Return the screenshot inline in the final Markdown response. Include its title and URL only when useful.

## Constraints

- Treat “first tab” as the first item returned by `chrome.user.openTabs()`; the browser API exposes that current ordering rather than a guaranteed visual left-to-right strip index.
- Keep the user's tab open. Claiming is read-only for browser contents and releases automatically when the task ends.
- Do not read cookies, local storage, history, passwords, or session stores.
- Do not capture a new browser instance if Chrome is unavailable. Tell the user to connect the ChatGPT browser extension instead.
- Save an output PNG only when needed to render it in the final answer, preferably under `/tmp/`.
