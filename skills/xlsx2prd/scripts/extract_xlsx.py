#!/usr/bin/env python3
"""Extract XLSX sheet values and hierarchy into auditable JSON and Markdown."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN, "r": REL, "p": PKG_REL}


def column_index(reference: str) -> int:
    match = re.match(r"([A-Z]+)", reference.upper())
    if not match:
        return 0
    value = 0
    for char in match.group(1):
        value = value * 26 + ord(char) - 64
    return value - 1


def cell_text(cell: ET.Element, shared_strings: list[str]) -> object:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//m:t", NS))
    value_node = cell.find("m:v", NS)
    if value_node is None:
        formula = cell.find("m:f", NS)
        return f"={formula.text}" if formula is not None and formula.text else ""
    raw = value_node.text or ""
    if cell_type == "s":
        try:
            return shared_strings[int(raw)]
        except (ValueError, IndexError):
            return raw
    if cell_type == "b":
        return raw == "1"
    if cell_type in {"str", "e"}:
        return raw
    try:
        number = float(raw)
        return int(number) if number.is_integer() else number
    except ValueError:
        return raw


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return [
        "".join(node.text or "" for node in item.findall(".//m:t", NS))
        for item in root.findall("m:si", NS)
    ]


def workbook_sheets(archive: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {
        rel.get("Id"): rel.get("Target", "")
        for rel in rels.findall("p:Relationship", NS)
    }
    result = []
    for sheet in workbook.findall("m:sheets/m:sheet", NS):
        rel_id = sheet.get(f"{{{REL}}}id")
        target = targets.get(rel_id, "")
        if target.startswith("/"):
            target = target.lstrip("/")
        elif not target.startswith("xl/"):
            target = f"xl/{target}"
        result.append((sheet.get("name", "Sheet"), target))
    return result


def parse_sheet(
    archive: zipfile.ZipFile, target: str, shared_strings: list[str]
) -> dict[str, object]:
    root = ET.fromstring(archive.read(target))
    rows: dict[int, dict[int, object]] = {}
    formulas: dict[str, str] = {}
    max_col = -1
    max_row = -1
    for row in root.findall("m:sheetData/m:row", NS):
        row_index = int(row.get("r", "1")) - 1
        max_row = max(max_row, row_index)
        row_values: dict[int, object] = {}
        for cell in row.findall("m:c", NS):
            reference = cell.get("r", "A1")
            col = column_index(reference)
            max_col = max(max_col, col)
            row_values[col] = cell_text(cell, shared_strings)
            formula = cell.find("m:f", NS)
            if formula is not None and formula.text:
                formulas[reference] = formula.text
        rows[row_index] = row_values

    matrix = []
    for row_index in range(max_row + 1):
        row_values = rows.get(row_index, {})
        matrix.append([row_values.get(col, "") for col in range(max_col + 1)])

    merged_ranges = [
        node.get("ref", "")
        for node in root.findall("m:mergeCells/m:mergeCell", NS)
        if node.get("ref")
    ]
    normalized = [list(row) for row in matrix]
    for merged in merged_ranges:
        start, _, end = merged.partition(":")
        end = end or start
        start_col = column_index(start)
        end_col = column_index(end)
        start_row = int(re.search(r"\d+", start).group()) - 1
        end_row = int(re.search(r"\d+", end).group()) - 1
        value = matrix[start_row][start_col]
        for row_index in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                normalized[row_index][col] = value

    return {
        "rows": len(matrix),
        "columns": max_col + 1,
        "values": matrix,
        "normalizedMergedValues": normalized,
        "mergedRanges": merged_ranges,
        "formulas": formulas,
    }


def markdown_cell(value: object) -> str:
    text = str(value).replace("\n", "<br>").replace("|", "\\|")
    return text[:160]


def write_inventory(data: dict[str, object], output_path: Path) -> None:
    lines = [
        "# Workbook Inventory",
        "",
        f"- Source: `{data['source']}`",
        f"- Sheets: {len(data['sheets'])}",
        "",
    ]
    for sheet in data["sheets"]:
        lines.extend(
            [
                f"## {sheet['name']}",
                "",
                f"- Used shape: {sheet['rows']} rows x {sheet['columns']} columns",
                f"- Merged ranges: {len(sheet['mergedRanges'])}",
                f"- Formula cells: {len(sheet['formulas'])}",
                "",
            ]
        )
        values = sheet["values"]
        preview = values[: min(12, len(values))]
        if preview and sheet["columns"]:
            width = min(sheet["columns"], 10)
            lines.append("| " + " | ".join(f"C{i + 1}" for i in range(width)) + " |")
            lines.append("| " + " | ".join("---" for _ in range(width)) + " |")
            for row in preview:
                lines.append(
                    "| " + " | ".join(markdown_cell(value) for value in row[:width]) + " |"
                )
            lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.input.suffix.lower() != ".xlsx":
        raise SystemExit("Input must be an .xlsx file")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.input) as archive:
        shared_strings = read_shared_strings(archive)
        sheets = []
        for name, target in workbook_sheets(archive):
            sheet = parse_sheet(archive, target, shared_strings)
            sheet["name"] = name
            sheets.append(sheet)

    data = {"source": str(args.input.resolve()), "sheets": sheets}
    (args.output_dir / "workbook.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_inventory(data, args.output_dir / "inventory.md")
    print(
        json.dumps(
            {
                "source": data["source"],
                "sheets": [
                    {
                        "name": sheet["name"],
                        "rows": sheet["rows"],
                        "columns": sheet["columns"],
                    }
                    for sheet in sheets
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
