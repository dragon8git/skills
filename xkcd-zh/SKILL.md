---
name: xkcd-zh
description: 将 xkcd 链接对应漫画的英文直接替换为中文，输出中文图片与离线 HTML。用于用户提供 xkcd URL 并希望中文化、翻译或阅读中文漫画；仅询问链接内容时不自动编辑图片。
---

# xkcd 中文漫画

默认简体中文。交付主角是**图中文字已替换的漫画**，不能用原图加图外翻译代替。每个指定 URL 对应一幅漫画；首页解析为当前漫画并记录固定编号，不扩大为整站抓取。

## 获取与翻译

运行此技能的助手（`<skill-dir>` 使用实际绝对路径）：

```bash
python3 <skill-dir>/scripts/xkcd.py fetch --url https://xkcd.com/1779/ --workdir <workspace>/work/xkcd-1779
```

助手获取官方 JSON 和图片，保存 `metadata.json` 与 `original.<扩展名>`。失败时读官方页面核对，不猜图片地址或编号。

用 `view_image` 实际查看原图，按顺序识别对白、旁白、标题和图表标注。JSON 的 `transcript` 常为空，不代表没有图中文字。读不清的文字先核对原图，不补写。

先整理原文与中文对应，保持人物归属、笑点、数字和单位。双关优先采用自然简洁的中文，无法保留的含义在图外注释。`alt` 是悬停彩蛋，翻译后放在 HTML 可展开说明中，不擅自加进画面。

## 图片编辑

按可用的 `imagegen` 技能指导，使用内置 `image_gen` 图片编辑工具。原图作为 edit target，本地原图先用 `view_image` 查看，再用 `referenced_image_paths` 提供。不要只重画相似漫画，也不要用 HTML 浮层代替最终中文图片。

提示词模板：

> Use case: text-localization. Replace only the in-image English text with the exact Simplified Chinese strings listed below. Preserve characters, poses, objects, panel boundaries, speech connectors, black-and-white artwork, and reading order. Fit readable Chinese lettering into the original text regions; adapt wrapping without cropping. Remove replaced English lettering. Do not add titles, commentary, watermarks, or extra objects. [逐段列出位置、说话者及准确中文文本。]

公式、代码、数字和必要标识保持准确。不能承诺生成式编辑逐像素保留原图。

检查每段文字、人物归属、数字、有无裁切和构图变化。发现问题后针对性修正，最多额外编辑两次；仍不合格时报告具体未解决项，不把它当完成品。内置工具不可用时说明，只有用户授权 CLI/API 替代方案后才切换。

## 交付

复制选定图片到当前工作区 `outputs/xkcd-<编号>-zh.<真实扩展名>`，保留原图。将实际提示词保存到 outputs 的文本文件。把中文彩蛋、必要双关注释及实际编辑局限写到工作目录的 `notes.txt`，运行：

```bash
python3 <skill-dir>/scripts/xkcd.py render --metadata <workdir>/metadata.json --image <outputs>/xkcd-1779-zh.png --notes <workdir>/notes.txt --output <outputs>/xkcd-1779-zh.html
```

助手生成精简阅读页：中文漫画居中，适应手机宽度，原图与说明折叠，图片内嵌支持离线阅读。保留 Randall Munroe 署名、固定原作链接与 CC BY-NC 2.5，标明非官方翻译。

核对 HTML 已生成且图片已嵌入，尽可能打开预览。最终链接 HTML 与中文图片的绝对路径，简短报告核验结果与实质局限。用户只给 URL 并要求中文化时，直接完成，不重复询问格式。
