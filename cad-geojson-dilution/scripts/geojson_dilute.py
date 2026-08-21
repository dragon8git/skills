#!/usr/bin/env python3
"""Stream and simplify a GeoJSON FeatureCollection without loading it all in memory."""

import argparse
import json
import math
import os
import sys
from collections import Counter


def iter_features(path, encoding):
    """Yield Feature objects from a top-level GeoJSON FeatureCollection incrementally."""
    decoder = json.JSONDecoder()
    with open(path, "r", encoding=encoding) as source:
        buffer = ""
        started = False
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk and not buffer:
                if not started:
                    raise ValueError("Top-level features array was not found")
                return
            buffer += chunk
            if not started:
                marker = buffer.find('"features"')
                if marker < 0:
                    if not chunk:
                        raise ValueError("Top-level features array was not found")
                    buffer = buffer[-32:]
                    continue
                array_start = buffer.find("[", marker)
                if array_start < 0:
                    continue
                buffer = buffer[array_start + 1:]
                started = True

            index = 0
            needs_more = False
            while True:
                while index < len(buffer) and buffer[index] in " \t\r\n,":
                    index += 1
                if index >= len(buffer):
                    break
                if buffer[index] == "]":
                    return
                try:
                    feature, end = decoder.raw_decode(buffer, index)
                except json.JSONDecodeError:
                    needs_more = True
                    break
                if not isinstance(feature, dict):
                    raise ValueError("features array contains a non-object entry")
                yield feature
                index = end
            buffer = buffer[index:]
            if not chunk:
                if buffer.strip() and needs_more:
                    raise ValueError("GeoJSON ended in the middle of a feature")
                return


def point_distance_sq(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def perpendicular_distance_sq(point, start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if dx == 0 and dy == 0:
        return point_distance_sq(point, start)
    t = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / (dx * dx + dy * dy)
    projection = (start[0] + t * dx, start[1] + t * dy)
    return point_distance_sq(point, projection)


def simplify_line(points, tolerance):
    if len(points) <= 2:
        return points
    tolerance_sq = tolerance * tolerance
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        first, last = stack.pop()
        best_distance, best_index = tolerance_sq, None
        for index in range(first + 1, last):
            distance = perpendicular_distance_sq(points[index], points[first], points[last])
            if distance > best_distance:
                best_distance, best_index = distance, index
        if best_index is not None:
            keep[best_index] = True
            stack.append((first, best_index))
            stack.append((best_index, last))
    return [point for index, point in enumerate(points) if keep[index]]


def normalize_point(point, precision):
    if not isinstance(point, list) or len(point) < 2:
        return None
    try:
        x, y = round(float(point[0]), precision), round(float(point[1]), precision)
    except (TypeError, ValueError):
        return None
    if not (-180 <= x <= 180 and -90 <= y <= 90):
        return None
    return [x, y]


def normalize_line(points, tolerance, precision, ring=False):
    normalized = []
    for point in points if isinstance(points, list) else []:
        clean = normalize_point(point, precision)
        if clean is not None and (not normalized or clean != normalized[-1]):
            normalized.append(clean)
    if ring and len(normalized) > 1 and normalized[0] == normalized[-1]:
        normalized.pop()
    minimum = 3 if ring else 2
    if len(normalized) < minimum:
        return None
    simplified = simplify_line(normalized + ([normalized[0]] if ring else []), tolerance)
    if ring:
        simplified = simplified[:-1]
        if len(simplified) < 3:
            return None
        simplified.append(simplified[0])
    elif len(simplified) < 2:
        return None
    return simplified


def line_length_metres(points):
    total = 0.0
    for start, end in zip(points, points[1:]):
        latitude = math.radians((start[1] + end[1]) / 2)
        dx = (end[0] - start[0]) * 111320 * math.cos(latitude)
        dy = (end[1] - start[1]) * 110574
        total += math.hypot(dx, dy)
    return total


def simplify_geometry(geometry, tolerance, precision, drop_points=False, min_line_length_metres=0):
    if not isinstance(geometry, dict):
        return None
    kind, coordinates = geometry.get("type"), geometry.get("coordinates")
    if kind == "Point":
        if drop_points:
            return None
        point = normalize_point(coordinates, precision)
        return {"type": kind, "coordinates": point} if point else None
    if kind == "MultiPoint":
        if drop_points:
            return None
        points = [point for point in (normalize_point(p, precision) for p in coordinates or []) if point]
        return {"type": kind, "coordinates": points} if points else None
    if kind == "LineString":
        line = normalize_line(coordinates, tolerance, precision)
        return {"type": kind, "coordinates": line} if line and line_length_metres(line) >= min_line_length_metres else None
    if kind == "MultiLineString":
        lines = [line for line in (normalize_line(line, tolerance, precision) for line in coordinates or [])
                 if line and line_length_metres(line) >= min_line_length_metres]
        return {"type": kind, "coordinates": lines} if lines else None
    if kind == "Polygon":
        rings = [ring for ring in (normalize_line(ring, tolerance, precision, True) for ring in coordinates or []) if ring]
        return {"type": kind, "coordinates": rings} if rings else None
    if kind == "MultiPolygon":
        polygons = []
        for polygon in coordinates or []:
            rings = [ring for ring in (normalize_line(ring, tolerance, precision, True) for ring in polygon or []) if ring]
            if rings:
                polygons.append(rings)
        return {"type": kind, "coordinates": polygons} if polygons else None
    if kind == "GeometryCollection":
        geometries = [result for result in (simplify_geometry(item, tolerance, precision, drop_points, min_line_length_metres)
                                             for item in geometry.get("geometries", [])) if result]
        return {"type": kind, "geometries": geometries} if geometries else None
    return None


def count_coordinates(value):
    if not isinstance(value, list):
        return 0
    if value and isinstance(value[0], (int, float)):
        return 1
    return sum(count_coordinates(child) for child in value)


def count_geometry_coordinates(geometry):
    if not isinstance(geometry, dict):
        return 0
    if geometry.get("type") == "GeometryCollection":
        return sum(count_geometry_coordinates(item) for item in geometry.get("geometries", []))
    return count_coordinates(geometry.get("coordinates"))


def run(args):
    input_size = os.path.getsize(args.input)
    counts, output_types = Counter(), Counter()
    input_features = output_features = input_coordinates = output_coordinates = dropped = dropped_points = 0
    with open(args.output, "w", encoding="utf-8") as target:
        target.write('{"type":"FeatureCollection","features":[')
        first = True
        for index, feature in enumerate(iter_features(args.input, args.input_encoding), start=1):
            input_features += 1
            geometry = feature.get("geometry")
            if isinstance(geometry, dict):
                counts[geometry.get("type", "unknown")] += 1
                input_coordinates += count_geometry_coordinates(geometry)
            result = simplify_geometry(geometry, args.tolerance, args.precision, args.drop_points, args.min_line_length_metres)
            if result is None:
                dropped += 1
                if args.drop_points and isinstance(geometry, dict) and geometry.get("type") in {"Point", "MultiPoint"}:
                    dropped_points += 1
                continue
            if not first:
                target.write(",")
            target.write(json.dumps({"type": "Feature", "geometry": result, "properties": {}}, separators=(",", ":"), ensure_ascii=False))
            first = False
            output_features += 1
            output_types[result["type"]] += 1
            output_coordinates += count_geometry_coordinates(result)
            if index % args.progress_every == 0:
                print(f"processed {index:,} features", file=sys.stderr)
        target.write("]}")
    output_size = os.path.getsize(args.output)
    report = {
        "input": args.input,
        "output": args.output,
        "tolerance_degrees": args.tolerance,
        "coordinate_precision_decimal_places": args.precision,
        "minimum_line_length_metres": args.min_line_length_metres,
        "input_encoding": args.input_encoding,
        "input_bytes": input_size,
        "output_bytes": output_size,
        "size_reduction_percent": round((1 - output_size / input_size) * 100, 2) if input_size else 0,
        "input_features": input_features,
        "output_features": output_features,
        "dropped_invalid_or_empty_after_simplification": dropped,
        "dropped_point_features": dropped_points,
        "input_coordinates": input_coordinates,
        "output_coordinates": output_coordinates,
        "coordinate_reduction_percent": round((1 - output_coordinates / input_coordinates) * 100, 2) if input_coordinates else 0,
        "input_geometry_types": dict(counts),
        "output_geometry_types": dict(output_types),
    }
    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="source FeatureCollection GeoJSON")
    parser.add_argument("output", help="simplified GeoJSON output path")
    parser.add_argument("--report", help="optional JSON report output path")
    parser.add_argument("--tolerance", type=float, default=0.001, help="simplification tolerance in degrees (default: 0.001)")
    parser.add_argument("--precision", type=int, default=4, help="coordinate decimal places (default: 4)")
    parser.add_argument("--input-encoding", default="gb18030", help="source text encoding (default: gb18030)")
    parser.add_argument("--drop-points", action="store_true", help="omit Point and MultiPoint features for an outline-only map")
    parser.add_argument("--min-line-length-metres", type=float, default=0, help="omit LineString paths shorter than this value (default: 0)")
    parser.add_argument("--progress-every", type=int, default=10000)
    args = parser.parse_args()
    if args.tolerance < 0 or args.min_line_length_metres < 0 or not 0 <= args.precision <= 12:
        parser.error("tolerance and minimum line length must be non-negative; precision must be 0..12")
    run(args)


if __name__ == "__main__":
    main()
