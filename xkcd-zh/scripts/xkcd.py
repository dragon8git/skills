#!/usr/bin/env python3
"""Fetch official xkcd assets and package a localized image as offline HTML."""
import argparse
import base64
import html
import json
import mimetypes
import re
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen


def read_url(url):
    with urlopen(url, timeout=30) as response:
        return response.read()


def fetch(args):
    url = urlsplit(args.url)
    if url.scheme not in ('http', 'https') or url.netloc not in ('xkcd.com', 'www.xkcd.com'):
        raise ValueError('Provide an official xkcd.com URL')
    match = re.fullmatch(r'/(\d+)?/?', url.path or '/')
    if not match:
        raise ValueError('Use the homepage or a numbered comic URL')
    number = match.group(1)
    endpoint = f'https://xkcd.com/{number}/info.0.json' if number else 'https://xkcd.com/info.0.json'
    metadata = json.loads(read_url(endpoint))
    image_url = urlsplit(metadata['img'])
    if image_url.scheme != 'https' or image_url.netloc != 'imgs.xkcd.com':
        raise ValueError('Unexpected image host')
    suffix = Path(image_url.path).suffix.lower()
    if suffix not in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
        raise ValueError('Unsupported image format')
    image_bytes = read_url(metadata['img'])
    directory = Path(args.workdir).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    metadata['source_url'] = f"https://xkcd.com/{metadata['num']}/"
    metadata['original_file'] = 'original' + suffix
    (directory / metadata['original_file']).write_bytes(image_bytes)
    (directory / 'metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'num': metadata['num'], 'source_url': metadata['source_url'], 'metadata': str(directory / 'metadata.json'), 'image': str(directory / metadata['original_file'])}, ensure_ascii=False))


def image_uri(path):
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in ('image/png', 'image/jpeg', 'image/gif', 'image/webp'):
        raise ValueError('Unsupported image format')
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


def render(args):
    metadata_path = Path(args.metadata).resolve()
    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    localized = image_uri(Path(args.image))
    original = image_uri(metadata_path.parent / metadata['original_file'])
    title = html.escape(f"xkcd {metadata['num']} · {metadata['title']} · 中文版")
    source = f"https://xkcd.com/{int(metadata['num'])}/"
    notes = html.escape(Path(args.notes).read_text(encoding='utf-8')) if args.notes else ''
    alt = html.escape(metadata.get('alt', ''))
    page = f'''<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>body{{margin:0;background:#f5f3ef;color:#222;font:16px/1.7 system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:24px 16px}}h1{{font-size:22px}}img{{display:block;max-width:100%;height:auto;margin:20px auto;background:white}}details{{margin:20px 0}}summary{{cursor:pointer}}.notes{{white-space:pre-wrap}}footer{{font-size:13px;color:#555}}a{{color:#315c85}}</style>
<main><h1>{title}</h1><img src="{localized}" alt="中文化漫画">
<details><summary>彩蛋与翻译说明</summary><p class="notes">{notes}</p><p>原文彩蛋：{alt}</p></details>
<details><summary>查看英文原图</summary><img src="{original}" alt="英文原漫画"></details>
<footer>原作：Randall Munroe · <a href="{source}">xkcd 原作</a> · <a href="https://creativecommons.org/licenses/by-nc/2.5/">CC BY-NC 2.5</a><br>非官方中文翻译与图片编辑。译作按同一许可提供，仅供非商业使用。</footer></main></html>'''
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding='utf-8')
    print(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    fetch_parser = commands.add_parser('fetch')
    fetch_parser.add_argument('--url', required=True)
    fetch_parser.add_argument('--workdir', required=True)
    render_parser = commands.add_parser('render')
    render_parser.add_argument('--metadata', required=True)
    render_parser.add_argument('--image', required=True)
    render_parser.add_argument('--notes')
    render_parser.add_argument('--output', required=True)
    args = parser.parse_args()
    (fetch if args.command == 'fetch' else render)(args)


if __name__ == '__main__':
    main()
