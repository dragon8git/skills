---
name: yolo-datasets-download
description: Generate or update a Python script that converts one or more Ultralytics NDJSON dataset exports into a local YOLO dataset with images, labels, and dataset.yaml. Use when the user has one or multiple `.ndjson` exports with image URLs and bbox annotations and wants Codex to create the downloader/converter script, run a real test, and add usage instructions to the workspace root `README.md`.
---

# YOLO Datasets Download

Install the reusable downloader template into the target workspace, test it against the real `.ndjson`, and leave a root `README.md` with usage.

## Workflow

1. Identify the target workspace root.
2. Run `scripts/install_yolo_dataset_downloader.py --workspace <workspace-root>`.
3. Verify that `<workspace-root>/download_ndjson_images.py` exists.
4. Run a real smoke test with `--limit`, writing into a temporary output directory under the workspace.
5. Confirm that the test output contains:
   - `images/<split>/...`
   - `labels/<split>/...`
   - `dataset.yaml`
6. Report the exact command used and any failures.

## Resources

### `scripts/install_yolo_dataset_downloader.py`

Copy the bundled Python template into the workspace as `download_ndjson_images.py`. Create or update the root `README.md` with usage instructions.

### `assets/download_ndjson_images.py`

Template script that:

- reads one or more Ultralytics NDJSON exports
- downloads images from `type == "image"` records
- writes YOLO label files from `annotations.boxes`
- preserves `train` / `val` / `test` split layout
- writes `dataset.yaml`
- shows live progress during download

## Notes

- Prefer the workspace root `README.md`. If it does not exist, create it.
- Keep the generated script dependency-free; use the Python standard library.
- Use `--limit` for the first execution unless the user explicitly asks for full download immediately.
