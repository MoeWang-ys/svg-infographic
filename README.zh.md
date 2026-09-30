# SVG Infographic

[English](./README.md)

一个 agent skill，用**手写 SVG + Chrome headless** 做信息图 —— 架构图、流程图、对比图、README 配图。

它就是一个 `SKILL.md`，任何有文件系统和 shell 权限的编码 agent 都能用（Claude Code、pi、Cursor）。

下面这张图就是用本 skill 画的 —— 34 个文本元素，零溢出：

![svg-infographic 总览](assets/hero.svg)

## 它做什么

**文字准确是信息图的全部价值 —— 而生图模型画不好字，中文尤其糟。** 所以本 skill 不生成图片，它手写 SVG，然后程序化验证结果。

| | 生图 AI | 本 skill |
|---|---|---|
| 文字准确性 | 经常画错字，中文更差 | **100% 可控** |
| 改一个字 | 整张重新生成 | 改一行 |
| 文件体积 | 几百 KB 到几 MB | **约 8 KB，矢量** |
| 风格一致性 | 每次飘 | 每次完全一致 |
| 版本管理 | ❌ 二进制 | ✅ 文本 diff |
| 需要 API key | 要 | **不要** |

**文字重要时用它。** 插画、氛围图用生图模型；纯逻辑关系图用 Mermaid，GitHub 原生渲染，零成本。

### 核心能力

- **程序化验证** —— `getBBox()` 测文本溢出、墨迹占比与亮度分析、定点取色、模拟 GitHub 加载。这一条最关键：多数模型看不见自己的输出。
- **Chrome headless 流水线** —— 渲染 PNG 并量真实文字边界。不碰 cairo，不用跟 `libcairo.2.dylib` 折腾。
- **PNG 压缩** —— 430 KB → 140 KB，附色差校验，不会压出偏色。
- **默认中英双语** —— 中英排版分别量边界盒，因为英文更宽。
- **反 AI 味配色** —— 暖砂、赤陶橙、墨青。取自 `huashu-design` 的审美禁区（深蓝底霓虹、紫渐变，都再见）。
- **附暗色模板** —— 一个带复制 / 导出 PNG / 导出 PDF 按钮的 HTML 外框。

## 给谁用

任何需要 agent 产出**标签准确**的图的人 —— 项目 README、架构文档、内部讲解材料。如果你用中文工作，这几乎是刚需。

## 安装

把 `SKILL.md` 复制到 agent 的 skills 目录：

```bash
# pi
mkdir -p ~/.pi/agent/skills/svg-infographic
cp SKILL.md ~/.pi/agent/skills/svg-infographic/

# Claude Code（项目级）
mkdir -p .claude/skills/svg-infographic
cp SKILL.md .claude/skills/svg-infographic/
```

依赖：

```bash
Google Chrome              # 渲染、截图、量文字边界
python3
pip install pillow numpy   # 像素分析 + PNG 压缩
```

然后直接说：*「给这个 README 画个架构图」*

## 触发词

- 「给 README 配图」
- 「画个架构图」「做个流程图」「画张对比图」
- 「画图说明一下」「整个图看看」
- "illustrate this in a diagram" / "make an infographic"

## 目录结构

```
SKILL.md                      方法论本体
scripts/
  svg2png.sh                  SVG → PNG（Chrome headless + Pillow）
  check_overflow.py           文本溢出检测
  check_pixels.py             墨迹占比、亮度、横带分析
references/
  dark-template.html          暗色 HTML 模板，带导出按钮
assets/                       示例图
```

踩过的坑与硬规则（命令行参数、字体栈、压缩、配色）都收在 [`RULES.md`](RULES.md)。

## 实测数字

下面每个数字都是本仓库脚本的真实输出。

```
文本溢出        34 个文本，0 个溢出
墨迹 / 亮度     占比 2.89%，最暗 56（说明文字渲染了）
横带分析        6/6 横带均有内容
PNG 压缩        138 KB → 51 KB（-63%），色差 0.04/255
GitHub 加载     naturalWidth × naturalHeight = 1800 × 930
```

## 来源与致谢

- 架构图结构技法吸收自 [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)（MIT）。其暗色霓虹配色不是本 skill 的默认配色。
- `references/dark-template.html` 版权归 Cocoon AI，MIT —— 见 `references/dark-template-LICENSE`。
- 配色禁区规则来自 `huashu-design`。

## 许可

MIT
