---
name: send-email
description: Download an HTTP(S) file to Downloads, compress it as ZIP, and send it by SMTP when the user asks to deliver a file by email.
---

# Send Email

Use this skill when the user provides an HTTP(S) download URL and wants the downloaded file delivered as a ZIP attachment by email.

## Defaults and limits

- Save the downloaded file and ZIP to `/Users/lee/Downloads/` unless the user specifies another local output directory.
- Default recipient: `18692055330@163.com`. Use a different recipient only when the user explicitly names it in the current request.
- Do not copy SMTP credentials from source code into this skill, logs, or chat. The sender configuration comes from environment variables at send time.
- Before the external send, report the recipient, subject, and ZIP path, then obtain an explicit confirmation. Use `--confirm-send` only after that confirmation.

## Workflow

1. Resolve the URL, recipient, and optional subject from the user request. Ask only if the URL is absent or the intended recipient is unclear.
2. Run the script without `--confirm-send`; it downloads the file, creates the ZIP, and prints the exact delivery summary.
3. Present that summary to the user and wait for confirmation.
4. Run it again with `--confirm-send` and the same inputs. Report only the message ID and local artifact paths; never print SMTP secrets.

## Script

`scripts/download_zip_send.js` uses the existing `nodemailer` installation at `/Users/lee/project/dls-scams-ui` by default. It configures `SEND_EMAIL_SMTP_HOST` as `smtp.qq.com` and `SEND_EMAIL_SMTP_USER` as `928532756@qq.com` when they are absent. The QQ authorization code is read from the macOS default keychain item `SEND_EMAIL_SMTP_PASS`; it can also be overridden for one invocation with the same environment variable.

Optional variables are `SEND_EMAIL_SMTP_HOST`, `SEND_EMAIL_SMTP_USER`, `SEND_EMAIL_SMTP_PASS`, `SEND_EMAIL_SMTP_PORT` (default `465`), `SEND_EMAIL_SMTP_SECURE` (default `true`), `SEND_EMAIL_FROM`, and `SEND_EMAIL_NODE_MODULES_ROOT`.

Example preparation command:

```bash
node /Users/lee/.codex/skills/send-email/scripts/download_zip_send.js \
  --url 'https://example.com/build/download/id' \
  --to '18692055330@163.com'
```

After confirmation, repeat the command with `--confirm-send`.
