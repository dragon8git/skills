#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
  echo "Usage: $0 INPUT_VIDEO [OUTPUT_MP4] [VIDEO_BITRATE]" >&2
  exit 64
fi

input_file=$1
if [ ! -f "$input_file" ]; then
  echo "Input file does not exist: $input_file" >&2
  exit 66
fi

input_dir=$(dirname "$input_file")
input_name=$(basename "$input_file")
input_stem=${input_name%.*}
output_file=${2:-"$input_dir/${input_stem}_compressed_hevc.mp4"}

if [ -e "$output_file" ]; then
  echo "Refusing to overwrite existing output: $output_file" >&2
  exit 73
fi

for command in ffmpeg ffprobe; do
  command -v "$command" >/dev/null || {
    echo "Required command is unavailable: $command" >&2
    exit 69
  }
done

height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$input_file")
if [ -z "$height" ]; then
  echo "No video stream found: $input_file" >&2
  exit 65
fi

if [ "$#" -eq 3 ]; then
  video_bitrate=$3
elif [ "$height" -ge 1800 ]; then
  video_bitrate=12M
elif [ "$height" -ge 1080 ]; then
  video_bitrate=7M
elif [ "$height" -ge 720 ]; then
  video_bitrate=4M
else
  video_bitrate=2M
fi

if ffmpeg -hide_banner -encoders 2>/dev/null | grep -q 'hevc_videotoolbox'; then
  video_args=(-c:v hevc_videotoolbox -b:v "$video_bitrate" -maxrate "$video_bitrate" -bufsize "$video_bitrate" -tag:v hvc1)
elif ffmpeg -hide_banner -encoders 2>/dev/null | grep -q 'libx265'; then
  video_args=(-c:v libx265 -preset slow -crf 25 -tag:v hvc1)
else
  echo "No supported HEVC encoder found (need hevc_videotoolbox or libx265)." >&2
  exit 69
fi

ffmpeg -hide_banner -i "$input_file" -map 0:v:0 -map '0:a?' \
  "${video_args[@]}" -c:a aac -b:a 128k -movflags +faststart "$output_file"

codec=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$output_file")
duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$output_file")
size=$(stat -f %z "$output_file" 2>/dev/null || stat -c %s "$output_file")

if [ "$codec" != "hevc" ] || [ -z "$duration" ]; then
  echo "Output verification failed: codec=$codec duration=$duration" >&2
  exit 70
fi

echo "Output: $output_file"
echo "Verified: codec=$codec duration=${duration}s size=${size} bytes"
