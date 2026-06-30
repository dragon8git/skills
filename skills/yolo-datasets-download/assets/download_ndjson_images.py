#!/usr/bin/env python3
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def load_ndjson_files(ndjson_paths: list[Path]):
    dataset_meta = {}
    records = []

    for ndjson_path in ndjson_paths:
        with ndjson_path.open("r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"[warn] {ndjson_path}:{lineno}: invalid json: {e}", file=sys.stderr)
                    continue

                kind = record.get("type")
                if kind == "dataset":
                    if not dataset_meta:
                        dataset_meta = record
                    elif dataset_meta.get("class_names") != record.get("class_names"):
                        print(
                            f"[warn] class_names mismatch in {ndjson_path}, using the first dataset header",
                            file=sys.stderr,
                        )
                    continue
                if kind != "image":
                    continue

                url = record.get("url")
                name = record.get("file")
                if not url or not name:
                    print(f"[warn] {ndjson_path}:{lineno}: missing url/file", file=sys.stderr)
                    continue

                records.append(
                    {
                        "line": lineno,
                        "url": url,
                        "file": name,
                        "stem": Path(name).stem,
                        "split": record.get("split") or "unsplit",
                        "boxes": record.get("annotations", {}).get("boxes", []),
                    }
                )

    return dataset_meta, records


def split_dirs(out_dir: Path, split: str):
    return out_dir / "images" / split, out_dir / "labels" / split


def dedupe_records(records: list[dict]):
    seen = set()
    unique = []
    skipped = 0
    for record in records:
        key = (record["split"], record["file"])
        if key in seen:
            skipped += 1
            continue
        seen.add(key)
        unique.append(record)
    return unique, skipped


def write_label_file(label_path: Path, boxes: list):
    label_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for box in boxes:
        if len(box) != 5:
            continue
        cls_id, x, y, w, h = box
        lines.append(f"{int(cls_id)} {x} {y} {w} {h}")
    label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def download_one(record: dict, out_dir: Path, flat: bool, timeout: int, retries: int):
    split = "all" if flat else record["split"]
    image_dir, label_dir = split_dirs(out_dir, split)
    image_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)

    image_path = image_dir / record["file"]
    label_path = label_dir / f"{record['stem']}.txt"
    write_label_file(label_path, record["boxes"])

    if image_path.exists() and image_path.stat().st_size > 0:
        return "skipped", image_path

    headers = {"User-Agent": "Mozilla/5.0"}
    last_error = None
    for attempt in range(retries + 1):
        try:
            req = Request(record["url"], headers=headers)
            with urlopen(req, timeout=timeout) as resp, image_path.open("wb") as f:
                f.write(resp.read())
            return "downloaded", image_path
        except (HTTPError, URLError, TimeoutError, OSError) as e:
            last_error = e
            if image_path.exists():
                image_path.unlink(missing_ok=True)
            if attempt < retries:
                time.sleep(1 + attempt)

    return f"failed: {last_error}", image_path


def write_dataset_yaml(out_dir: Path, dataset_meta: dict, flat: bool, splits: set[str]):
    class_names = dataset_meta.get("class_names", {})
    names = [name for _, name in sorted(class_names.items(), key=lambda item: int(item[0]))]

    lines = [
        f"path: {out_dir.resolve()}",
        "train: images/all" if flat else "train: images/train",
        "val: images/all" if flat else "val: images/val",
    ]
    if not flat and "test" in splits:
        lines.append("test: images/test")
    lines.append(f"names: {json.dumps(names, ensure_ascii=False)}")
    (out_dir / "dataset.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert an Ultralytics NDJSON export into a YOLO dataset."
    )
    parser.add_argument("ndjson", nargs="+", type=Path, help="One or more .ndjson files")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("yolo_dataset"),
        help="Output directory (default: yolo_dataset)",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=8,
        help="Concurrent downloads (default: 8)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Per-request timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retries per file after the first attempt (default: 2)",
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        help="Put everything under images/all and labels/all",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Only process the first N images for a quick check (default: 0 means all)",
    )
    return parser.parse_args()


def print_progress(done: int, total: int, counts: dict):
    percent = (done / total * 100) if total else 100.0
    print(
        (
            f"\rprogress: {done}/{total} ({percent:5.1f}%) "
            f"downloaded={counts['downloaded']} "
            f"skipped={counts['skipped']} "
            f"failed={counts['failed']}"
        ),
        end="",
        file=sys.stderr,
        flush=True,
    )


def main():
    args = parse_args()
    dataset_meta, records = load_ndjson_files(args.ndjson)
    if not records:
        print("No image records found.", file=sys.stderr)
        return 1
    records, duplicates = dedupe_records(records)
    if duplicates:
        print(f"[warn] skipped {duplicates} duplicate image records", file=sys.stderr)
    if args.limit > 0:
        records = records[: args.limit]

    args.output.mkdir(parents=True, exist_ok=True)
    write_dataset_yaml(args.output, dataset_meta, args.flat, {record["split"] for record in records})

    total = len(records)
    counts = {"downloaded": 0, "skipped": 0, "failed": 0}
    print_progress(0, total, counts)

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [
            pool.submit(download_one, record, args.output, args.flat, args.timeout, args.retries)
            for record in records
        ]
        for done, future in enumerate(as_completed(futures), 1):
            status, image_path = future.result()
            if status == "downloaded":
                counts["downloaded"] += 1
            elif status == "skipped":
                counts["skipped"] += 1
            else:
                counts["failed"] += 1
                print(f"\n[error] {image_path.name}: {status}", file=sys.stderr)
            print_progress(done, total, counts)

    print(file=sys.stderr)
    print(
        f"done: downloaded={counts['downloaded']} skipped={counts['skipped']} "
        f"failed={counts['failed']} output={args.output}"
    )
    return 0 if counts["failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
