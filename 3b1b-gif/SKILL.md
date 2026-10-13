---
name: 3b1b-gif
description: Create mathematically accurate, 3Blue1Brown-inspired explanatory animations and export looping GIFs. Use for requests such as 3b1b 数学动画、向量相加动图、线性变换 GIF, or animated explanations of geometry and calculus. Applies to procedural mathematical animation rather than general image generation or video summarization.
---

# 3b1b GIF

Produce an original mathematical animation with the visual clarity of a 3Blue1Brown-style explanation, then deliver an actual playable GIF. Do not imply official affiliation or exact reproduction of an existing video.

## Choose the smallest useful scene

- Identify the mathematical object and the one relationship to explain. For a broad request such as “线性代数相加的简单动画”, state that you are using 2D vector addition and proceed. Ask only if competing interpretations would materially change the intended lesson.
- Use the user's language for captions. Useful defaults are a dark background, subtle coordinate grid, distinct stable object colors, concise formulas, and smooth movement with pauses for reading. These are defaults, not restrictions on explicit requests.
- Sketch the teaching sequence before rendering: introduce objects → perform one operation → hold the result. A simple GIF usually fits in 8–15 seconds at 15–24 fps, with roughly 960 × 640 pixels. Fit aspect ratio and complexity to the request.

## Render from mathematical geometry

Use code to control coordinates, shapes, labels, and timing. Pillow is sufficient for simple 2D scenes; use an available Manim or other suitable renderer when transformations, 3D, or complex formula layout warrant it. Do not require Manim/LaTeX installation for a simple arrow animation. Generative raster images should not determine mathematical positions or formulas.

Check the actual runtime and dependencies. If the desktop workspace dependency tool is available, it can locate bundled Python/Pillow; otherwise use an existing interpreter or a project-local environment. Avoid hardcoded user-specific runtime paths. Resolve fonts on the host, especially for Chinese; do not silently accept missing glyphs.

For the already-demonstrated vector example, run [scripts/vector_addition.py](scripts/vector_addition.py):

```bash
python /absolute/path/to/3b1b-gif/scripts/vector_addition.py \
  --output /absolute/workspace/outputs/vector-addition.gif \
  --preview-dir /absolute/workspace/work/vector-preview
```

This script requires Pillow. It automatically checks common macOS/Linux/Windows Chinese fonts; use `--font /path/to/cjk-font.ttc` and optionally `--latin-font /path/to/font.ttf` to override. It renders the fixed example **(3, 1) + (1, 2) = (4, 3)**. Other values, framing, languages, or topics require adapting a copy in the task workspace; the script is a starter scene, not a general mathematical renderer. Update geometry, equations, label placement, and bounds together.

## Mathematical and visual invariants

- Derive displayed values from the same mathematics as the drawing. Use equal axis scales when geometry depends on angles or lengths.
- For vector addition, translate b without rotating or scaling it; its tail travels from the origin to the endpoint of a. The sum runs from the original origin to the translated endpoint of b. Keep a faint original b if it helps explain translation.
- Keep object colors consistent between diagrams and equations. Reveal the result after the operation, rather than showing all steps at once.
- Offset labels from arrow shafts, tips, and other text. Reserve caption space outside the plot; ensure all animated positions remain inside the frame.
- Render with antialiasing (for example, 2× supersampling), ease motion, and pause on the final equation. Provide an intentional reset or fade for looping.
- Use a consistent palette sampled from representative frames or a palette-generation pass to limit GIF color flicker. Preserve enough final-result pause for reading. Do not optimize file size at the expense of legibility unless the user requests a size limit.

## Verify and deliver

Reopen the encoded GIF and verify dimensions, multiple frames, total duration, loop metadata, and file size. GIF encoders may merge identical frames: validate summed frame durations instead of equating frame count with playback time.

Inspect the actual GIF when playback is available; otherwise inspect decoded frames at introduction, mid-transition, and final result, and report that limitation if relevant. Check mathematical endpoints, preserved lengths/directions, readable Chinese glyphs, label collisions, clipping, and correct equations. The bundled script also writes three PNG previews; these help inspect layout but do not alone verify encoded playback.

Keep intermediate scripts and previews in the workspace scratch directory. Save the final GIF in the user-facing output directory and embed it with an absolute-path Markdown image, followed by a download link and a short explanation of the demonstrated operation. Report only verified media properties. Do not substitute a still image, a plan, or source code for the requested GIF.
