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

## Native modal and Toast timing

H5, 微信小程序, and the emulator do not prove that a physical Android device has the same native-window timing. On a physical Android device, `uni.showModal` can invoke its confirmation callback before its native window has finished being destroyed. If that callback sends a request which fails quickly, an immediate `uni.showToast` can be dismissed by the modal teardown and appear as a brief flash.

When diagnosing this pattern:

1. Add a temporary Toast outside any modal with `duration: 5000`. If it stays visible, the Toast API itself is not the cause; remove the probe after the test.
2. Reproduce on the affected physical device and correlate the business error, `PopupWindow`, and `DecorViewImmersiveImpl.onDetachedFromWindow` logs. A filtered capture can use:

```bash
app_pid="$(/Users/lee/Library/Android/sdk/platform-tools/adb -s "$device_id" shell pidof io.dcloud.uniappx | tr -d '\r')"
/Users/lee/Library/Android/sdk/platform-tools/adb -s "$device_id" logcat -T 1 --pid="$app_pid" -v threadtime \
  JSConsole:I console:I ViewRootImpl:I DecorViewImmersiveImpl:D WindowOnBackDispatcher:W '*:S'
```

3. Do not infer a failed-request reload from the symptom. Check that data reload/navigation remains only in the success path.

For a confirmed collision, route every Toast caused by that confirmation path (success, failure, or immediate local feedback) through a shared helper such as `app/utils/modal-toast.uts` `showToastAfterModal()`. It waits about `400ms` only on `APP-ANDROID`, while H5 and 微信小程序 remain immediate. Direct/dev-tool paths that bypass the confirmation dialog must keep normal `uni.showToast`. Retain normal request-lock cleanup, do not delay the request, and do not reload on failure. Re-test on the affected physical device after the change.

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

## Gradient fidelity

Do not simplify Android gradients to two colors merely for compatibility. Android UTS CSS supports multi-stop `linear-gradient`; removing H5/微信中间色标 makes the transition wash out early and visibly changes the design.

Audit all app-owned gradient branches before changing them:

```bash
rg -n -C 3 --glob '*.uvue' 'linear-gradient' \
  "$project/pages/wbd" "$project/components" "$project/windows"
```

For each `WEB || MP-WEIXIN` / `APP-ANDROID` pair, preserve the same colors, stop positions, and stop count. Use Android-compatible direction keywords instead of copying an angle when needed:

```css
/* WEB || MP-WEIXIN */
background-image: linear-gradient(180deg, #0071e3 0%, #2b94ff 46%, #d9ecff 92%, #f6f7fb 100%);

/* APP-ANDROID */
background-image: linear-gradient(to bottom, #0071e3 0%, #2b94ff 46%, #d9ecff 92%, #f6f7fb 100%);
```

Use `to bottom right` for the established diagonal Android fallback. Preserve every intermediate stop, including transparent overlay stops such as `rgba(...) 0%, rgba(...) 56%, rgba(...) 100%`. Two-stop gradients with the same endpoints are already equivalent; do not add speculative stops.

After the source audit, visually inspect one emulator page for each distinct gradient family (for example, vertical hero, diagonal hero, and image shade). If a system permission dialog covers a target page, do not change the permission state without user instruction; report that visual check as blocked while still recording the source and compile evidence.

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
