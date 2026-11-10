---
name: create-raycast-script
description: Create, integrate, or troubleshoot macOS Raycast Script Commands, including wrappers for existing scripts and Chinese clipboard or encoding issues. Use when the user wants to run an automation from Raycast or assign it a hotkey.
---

# Create Raycast Script

Create or update a Raycast Script Command that performs the user's requested action and verify as much of the actual flow as is practical.

1. Inspect the requested script, dependencies, and existing Raycast script directory and conventions. Prefer a directory explicitly supplied by the user; on this machine `/Users/lee/raycast-scripts` is an existing directory, but verify it before use. Do not overwrite an existing command without inspecting it.
2. Choose a small wrapper for an existing executable, or implement a standalone script when needed. Include a valid shebang, executable permission, and Raycast metadata (`schemaVersion`, `title`, and `mode`); choose output mode to fit the task. Use the real executable and dependency paths found on the machine, since Raycast may have a different PATH from an interactive terminal. Do not rely on shell aliases or activated environments.
3. Preserve Chinese and other Unicode input and output. For scripts using `pbcopy` or `pbpaste`, ensure they run in an available UTF-8 locale (for example, `LC_ALL=en_US.UTF-8` on macOS after checking availability); setting only `LANG` does not override an existing `LC_ALL`. Verify a representative Chinese string round-trips exactly when clipboard access is part of the task. A successful `pbcopy` exit code alone does not establish that the content survived. Use explicit UTF-8 encoding/decoding in code where appropriate.
4. Check syntax and executable permissions. Exercise the real command and inspect its results when safe and authorized; distinguish a simulated check from a full Raycast UI run. Clipboard tests replace the current clipboard, and a command may have other side effects: account for these before running it. If real execution would overwrite valuable user data or cause unrelated side effects, use an isolated test or explain what remains unverified.
5. Report the command name, how to find it in Raycast, and how to assign a hotkey. If the directory has not been registered, direct the user to Raycast Settings → Script Commands → Add Script Directory, or configure it through available authorized UI tools. Do not claim registration or a hotkey was configured unless verified.

When troubleshooting, surface the actual error instead of treating exceptions as an empty result. Compare the Raycast environment with the working terminal environment, including interpreter, PATH, locale, permissions, and clipboard behavior. Check the current [Raycast Script Commands documentation](https://manual.raycast.com/script-commands) when metadata or UI details need verification.
