#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil


README_SNIPPET = """# YOLO Dataset Downloader

## Usage

Convert an Ultralytics `.ndjson` export into a local YOLO dataset:

```bash
python3 download_ndjson_images.py /path/to/dataset1.ndjson /path/to/dataset2.ndjson -o output/yolo_dataset
```

The script accepts one or more `.ndjson` files. Quick check with only the first 10 images:

```bash
python3 download_ndjson_images.py /path/to/dataset.ndjson -o output/yolo_dataset_test --limit 10
```

The script generates:

- `images/train|val|test/*.jpg`
- `labels/train|val|test/*.txt`
- `dataset.yaml`
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Install the YOLO NDJSON downloader template into a workspace."
    )
    parser.add_argument("--workspace", type=Path, required=True, help="Workspace root")
    parser.add_argument(
        "--script-name",
        default="download_ndjson_images.py",
        help="Generated Python script name",
    )
    return parser.parse_args()


def upsert_readme(readme_path: Path):
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        if "# YOLO Dataset Downloader" in content:
            return "README unchanged"
        if not content.endswith("\n"):
            content += "\n"
        readme_path.write_text(content + "\n" + README_SNIPPET, encoding="utf-8")
        return "README updated"

    readme_path.write_text(README_SNIPPET, encoding="utf-8")
    return "README created"


def main():
    args = parse_args()
    workspace = args.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    skill_dir = Path(__file__).resolve().parent.parent
    template = skill_dir / "assets" / "download_ndjson_images.py"
    target = workspace / args.script_name
    shutil.copyfile(template, target)

    readme_status = upsert_readme(workspace / "README.md")
    print(f"installed script: {target}")
    print(readme_status)


if __name__ == "__main__":
    main()
