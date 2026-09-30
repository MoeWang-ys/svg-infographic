# SVG Infographic

[English](./README.md)

**不用 AI 生图，让编码 agent 直接给你画图。**

架构图、流程图、对比图、README 配图。字全对、矢量清晰、单张约 8 KB。

说一声，图就出来了：

![svg-infographic 总览](assets/hero.svg)

## 为什么不用生图模型

生图模型的好处是**替你画 —— 代价是字会画错**，中文尤其糟糕。而信息图的价值 100% 在字上，错一个字整张就废了。

本 skill 干脆不用生图模型。agent 手写 SVG，所以**你写的每个字就是图上的每个字**；改一个标签不用重新生成整张图。

| | 生图 AI | 本 skill |
|---|---|---|
| **要用生图模型** | 要，这是前提 | **不要** |
| 文字准确性 | 经常画错字，中文更差 | **100% 可控** |
| 改一个字 | 整张重新生成 | 改一行 |
| 文件体积 | 几百 KB 到几 MB | **约 8 KB，矢量** |
| 风格一致性 | 每次飘 | 每次完全一致 |
| 版本管理 | ❌ 二进制 | ✅ 文本 diff |
| API key / 每张费用 | 必须，要花钱 | **都不要** |

**文字重要时用它。** 插画、氛围图用生图模型；纯逻辑关系图用 Mermaid，GitHub 原生渲染，零成本。

## 你能得到什么

- **每个字都写对** —— 中文也不会错，而这正是生图模型最常翻车的地方。
- **永远可改** —— 改一个字，不用重画整张。随时重跑，结果一样。
- **约 8 KB 矢量文件** —— 放多大都清晰，提交不心疼，git 里能直接 diff。
- **不要 API key，不花钱** —— 就是 SVG 和 Chrome，你机器上早就有。
- **验证过的，不是感觉** —— 每张图出货前都会查文本溢出、空白区域、色差。
- **看起来是特意设计的** —— 暖砂 / 赤陶橙 / 墨青配色，避开深蓝底霓虹和紫渐变的 AI 味。
- **自带中英双语** —— 中英排版分别量边界盒，因为英文更宽。
- **一个暗色 HTML 模板** —— 带复制 / 导出 PNG / 导出 PDF 按钮。

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

## 它会对自己的图做质检

图出货前会被**量一遍，不是看一眼**。下面是本仓库脚本的真实输出：

```
标签溢出画布        34 个里 0 个
空白区域            没有（6/6 横带都有内容）
文件体积            138 KB → 51 KB，看不出偏色
在 GitHub 上能显示   能（1800 × 930 加载成功）
```

## 来源与致谢

- 架构图结构技法吸收自 [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)（MIT）。其暗色霓虹配色不是本 skill 的默认配色。
- `references/dark-template.html` 版权归 Cocoon AI，MIT —— 见 `references/dark-template-LICENSE`。
- 配色禁区规则来自 `huashu-design`。

## 许可

MIT
