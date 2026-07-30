---
name: ffmpeg-zip
description: Compress local video files with FFmpeg while balancing visual quality and file size. Use when Codex needs to reduce the size of a MOV, MP4, MKV, or other local video without overwriting its source, especially for screen recordings that should retain readable text.
---

# FFmpeg 视频压缩

使用 `scripts/compress_video.sh` 完成一次压缩。默认输出 HEVC/H.265 MP4；优先使用 macOS 的 `hevc_videotoolbox`，其他环境退回 `libx265`。

## Workflow

1. 先用 `ffprobe` 检查源文件的时长、分辨率、帧率、编码和大小。
2. 默认运行脚本，不覆盖源文件或已有输出：

   ```bash
   bash /Users/lee/.codex/skills/ffmpeg-zip/scripts/compress_video.sh "/absolute/path/input.mov"
   ```

3. 需要明确控制大小时传入输出路径和视频码率：

   ```bash
   bash /Users/lee/.codex/skills/ffmpeg-zip/scripts/compress_video.sh "/absolute/path/input.mov" "/absolute/path/output.mp4" 8M
   ```

4. 检查脚本输出的 HEVC 编码、时长和文件大小后，再报告结果。

## Defaults

- 保留原始分辨率、帧率和首条音频。
- 默认码率按画面高度选择：>=1800px 为 12M，>=1080px 为 7M，>=720px 为 4M，其他为 2M。
- 音频重编码为 AAC 128k，并将 MP4 索引移至文件头。
- HEVC 对 Apple 设备兼容；若交付对象必须使用旧设备或网页浏览器，先说明兼容性取舍，再按要求改用 H.264。
