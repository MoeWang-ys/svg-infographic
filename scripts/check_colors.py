#!/usr/bin/env python3
"""颜色直方图 — 抓 SVG 解析错误。

SVG 是 XML 不是 HTML。`&rarr;` 这类 HTML 命名实体在 XML 里未定义，
Chrome 解析失败后会渲染一块错误样式（粉色 #FFDDDD + #CC7777 + 黑字）。
文本溢出检测完全抓不到这种错——颜色直方图可以。

用法:
    python3 check_colors.py <file.png>

会打印出现最多的颜色。**任何不在你源 SVG 里的颜色，就是解析错误。**
"""
import sys
from collections import Counter

import numpy as np
from PIL import Image

# Chrome 解析错误时的标志性配色
CHROME_ERROR_COLORS = {
    (255, 221, 221): "Chrome 解析错误背景 (#FFDDDD)",
    (204, 119, 119): "Chrome 解析错误边框 (#CC7777)",
    (153, 0, 0): "Chrome 解析错误文字 (#990000)",
}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    path = sys.argv[1]
    a = np.asarray(Image.open(path).convert("RGB"))
    counts = Counter(map(tuple, a.reshape(-1, 3)))

    print(f"  {path}  {a.shape[1]}x{a.shape[0]}")
    print(f"  共 {len(counts)} 种颜色，出现最多的 12 种：")
    for col, n in counts.most_common(12):
        hexc = f"#{col[0]:02X}{col[1]:02X}{col[2]:02X}"
        mark = ""
        if col in CHROME_ERROR_COLORS:
            mark = f"   ← ✗ {CHROME_ERROR_COLORS[col]}"
        print(f"    {hexc}  {n:>9}{mark}")

    hits = [(c, n) for c, n in counts.items() if c in CHROME_ERROR_COLORS]
    if hits:
        print()
        print("  ✗ 检测到 Chrome 解析错误配色！")
        print("    检查 SVG 里有没有 HTML 实体（&rarr; &mdash; &nbsp;），")
        print("    未转义的 & 或 <。SVG 是 XML，只认 &amp; &lt; &gt; &quot; &apos;。")
        return 1

    print()
    print("  ✓ 未发现解析错误标志色")
    print("    （仍需人工确认其余颜色都来自你的调色板）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
