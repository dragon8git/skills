---
name: cad-geojson-dilution
description: Stream, simplify, and validate large CAD-derived GeoJSON for coarse Web-map browsing. Use when DWG/DXF exports contain excessive coordinates or GeoJSON is too large to render.
---

# CAD GeoJSON Dilution

Use this skill to reduce a large, top-level GeoJSON `FeatureCollection` without loading the source file fully into memory. It is intended for coarse Web-map display, not CAD editing, surveying, or preserving every source feature.

## Start with evidence

Treat the source file as read-only. Inspect its size, encoding, geometry types, feature count, and coordinate ranges before selecting loss parameters. Never assume a CAD-derived GeoJSON is UTF-8: use `--input-encoding gb18030` when Chinese CAD text prevents UTF-8 decoding. The bundled converter writes UTF-8 output.

Run the deterministic helper from this skill directory:

```sh
python3 scripts/geojson_dilute.py INPUT.geojson output/outline.json \
  --tolerance 0.0002 --precision 4 --drop-points --min-line-length-metres 20
```

`--report PATH.json` is optional and records input/output sizes, feature counts, coordinate counts, and geometry types. Always write outputs to a new path.

## Choose the loss budget

- For visually recognizable corridors and outlines, begin with `--tolerance 0.00005` to `0.0002` degrees, then compare actual renders. Around latitude 23°, `0.0002` is roughly 22m.
- Use `--precision 4` (roughly 11m) as a coarse display baseline. Precision 3 can distort narrow geometry substantially.
- Use `--drop-points` only if labels and point symbols are outside the requested map result.
- If raising tolerance barely reduces file size, inspect short paths. CAD exports often contain many already-two-point fragments. `--min-line-length-metres 20` can remove them, but must be visually checked because it removes real small features too.
- Do not claim a fixed size target is achievable without a trial run. If a detailed single GeoJSON cannot meet the target, explain the trade-off; consider vector tiles only if the user permits changing output format.

## Verify before delivery

Compile the helper, parse the output with `python3 -m json.tool`, and report actual bytes and compression ratio. Validate empty and malformed inputs when changing the script. For Web-map use, load the generated file in a real browser or the target map SDK; a valid JSON document alone does not establish rendering quality.

The converter supports `Point`, `MultiPoint`, line and polygon geometries, and `GeometryCollection`. It removes invalid/empty geometry after simplification. It does not preserve topology across independent CAD features, so use conservative parameters when shared boundaries matter.
