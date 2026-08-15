---
name: wbd-ui-android
description: Deploy, relaunch, and visually verify a UniApp X WBD app on a local Android Studio/QEMU emulator. Use when an Android-only UI issue needs a real-emulator screenshot, when HBuilderX must launch a particular app page on an emulator, or when checking Android CSS compatibility without clearing emulator state.
---

# WBD UI Android

Use this workflow for the existing Android Studio emulator. It deploys via HBuilderX and captures the emulator framebuffer through ADB, which works even when macOS accessibility cannot read the QEMU window.

## Preconditions

- Set `project` to the UniApp X app directory, normally `/Users/lee/tmp/xf-wbd-app/app`.
- Use HBuilderX CLI at `/Applications/HBuilderX.app/Contents/MacOS/cli`.
- Use ADB at `/Users/lee/Library/Android/sdk/platform-tools/adb`.
- Confirm the target instead of assuming a device ID:

```bash
/Users/lee/Library/Android/sdk/platform-tools/adb devices -l
```

Require a `device` state. For this environment, the Android Studio arm64 QEMU emulator is normally `emulator-5554`.

## Compile and launch

Compile first when diagnosing Android styles:

```bash
/Applications/HBuilderX.app/Contents/MacOS/cli launch app-android \
  --project "$project" --compile true --continue-on-error false
```

Deploy and relaunch the app on an already-running emulator:

```bash
/Applications/HBuilderX.app/Contents/MacOS/cli launch app-android \
  --project "$project" --deviceId emulator-5554 --playground standard \
  --continue-on-error false
```

Launch a specific page for isolated visual QA:

```bash
/Applications/HBuilderX.app/Contents/MacOS/cli launch app-android \
  --project "$project" --deviceId emulator-5554 --playground standard \
  --pagePath pages/wbd/login/index --continue-on-error false
```

`launch` restarts/deploys the app, not the Android virtual device. Do not run `adb reboot`, clear app data, or clear login state unless the user explicitly requests that state-changing operation.

## Android CSS compatibility

Treat an Android compiler warning for `inset` as a functional defect on full-screen or anchored overlays. Android UTS CSS may ignore `inset: 0`, leaving a preview mask, dialog, or thumbnail status overlay without reliable dimensions.

Scan the supported app-owned sources before visual QA:

```bash
rg -n --glob '*.uvue' '\binset\s*:' \
  "$project/pages/wbd" "$project/components" "$project/windows" 2>/dev/null
```

Replace each `inset: 0` with its equivalent explicit edges; preserve `position` and all other layout declarations:

```css
top: 0;
right: 0;
bottom: 0;
left: 0;
```

Use the same replacement for both `position: fixed` screen masks and `position: absolute` in-card overlays. Re-run the scan after editing, then compile Android and visually exercise the affected overlay; a successful compile alone is insufficient.

## Capture and inspect

Wait for HBuilderX to report that the app started, then capture the exact emulator pixels:

```bash
/Users/lee/Library/Android/sdk/platform-tools/adb -s emulator-5554 \
  exec-out screencap -p > /tmp/wbd-android-screen.png
```

Inspect the saved PNG with the local image-viewing tool and provide it as an absolute-path image/link in the result. Do not claim a visual result solely from a successful compile.

## Verification and reporting

1. Run the Android compile and record success/failure plus targeted warnings.
2. Launch the app or requested page on the confirmed emulator.
3. Capture and visually inspect the screenshot.
4. For cross-platform style changes, compile Web and mp-weixin too; preserve their original CSS when Android needs a platform branch.
5. Report separately: compilation outcome, screenshot evidence, and any unrelated warnings.

Keep modifications visual-only unless the user asks for behavior changes. Stop the long-running launch command after capture without terminating the emulator itself.
