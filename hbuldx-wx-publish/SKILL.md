---
name: hbuldx-wx-publish
description: Publish a UniApp X project to WeChat Mini Program with the HBuilderX CLI. Use when the user asks to build, upload, deploy, or release a 微信小程序 and needs safe version bumping, a generated release description, private-key validation, or an auditable upload result.
---

# HBuilderX 微信小程序发行

Use `/Applications/HBuilderX.app/Contents/MacOS/cli publish mp-weixin` for a user-authorized release. An explicit `$hbuldx-wx-publish` invocation is upload authorization: complete the required readiness checks, then upload in the same turn without asking for a second confirmation. Do not upload when the user explicitly asks only for a preflight, build, or release preparation.

## Release workflow

1. Read `<project>/manifest.json` to obtain `mp-weixin.appid`, `versionName`, and `versionCode`.
2. Check `git status --short`; preserve unrelated user edits. Summarize the current meaningful edits from the working tree or latest relevant commit. Do not invent a change summary.
3. Before every upload, increment the last numeric segment of `versionName` by one: `2.0.2` becomes `2.0.3`. When `versionCode` exists, increment it by one too. Update `manifest.json` with the new local version before publishing.
4. Require the caller to provide the WeChat private-key path, or use an explicitly supplied project-local path. Check only that the file exists and is readable; never print its contents.
5. Set the release description to `<verified change summary>；发布于 YYYY-MM-DD HH:mm:ss +0800`. If there is no verified edit summary, use `发布当前工作区版本` rather than fabricating one.
6. Confirm the CLI syntax locally with `cli publish mp-weixin --help`, then publish with `--upload true`, the bumped version, appid, key path, description, and robot number (default `1`). Do not pause for an additional upload confirmation when this skill was explicitly invoked.
7. Capture CLI output to a `mktemp` file outside the repository so the final upload response is not lost to terminal truncation. Report the exact version and description used. Report success only when the command exits successfully and its captured output confirms the upload; otherwise state that platform confirmation is pending or failed.

## Command pattern

```bash
release_log=$(mktemp /tmp/hbuldx-wx-publish.XXXXXX.log)
/Applications/HBuilderX.app/Contents/MacOS/cli publish mp-weixin \
  --project "<absolute-project-path>" \
  --name "<project-name>" \
  --appid "<mp-weixin-appid>" \
  --upload true \
  --version "<bumped-version>" \
  --privatekey "<private-key-path>" \
  --description "<release-description>" \
  --robot 1 >"$release_log" 2>&1
publish_status=$?
tail -n 80 "$release_log"
exit "$publish_status"
```

## Guardrails

- Treat a build success as distinct from a successful WeChat-platform upload.
- Do not expose the private key or commit it to the repository.
- Do not overwrite a user-selected version, appid, robot number, description, or key path.
- Leave source-map and mixed-subpackage options disabled unless the user explicitly requests them.
- After upload, tell the user that WeChat public-platform version management remains the final place to confirm the uploaded version.
