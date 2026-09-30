# SVG Infographic

[English](./README.en.md)

**不用 AI 生图，让你的编码 agent 直接画图。**

架构图、流程图、对比图、README 配图。字全对、矢量清晰、单张约 8 KB。

说一声，图就出来了：

![svg-infographic 总览](assets/hero.svg)

## 你有没有遇到过这种事

让 AI 画张架构图，画得挺好看，**结果图里的字是错的**——「用户中心」写成「用户中芯」，或者干脆变成一堆乱码。

中文尤其严重。改一个错别字？只能整张重新生成，然后**另一个地方又错了**。

而一张信息图的价值，100% 就在字上。字错了，图再好看也是废的。

这个 skill 换了个思路：**不让 AI 画图，让它写 SVG 代码。**

于是每个字都是你写的字。

## 装上之后

| | 生图 AI | 装上它 |
|---|---|---|
| **要不要生图模型** | 要，这是前提 | **不要** |
| 文字准确性 | 常画错字，中文更差 | **100% 可控** |
| 改一个字 | 整张重新生成 | 改一行 |
| 文件体积 | 几百 KB 到几 MB | **约 8 KB，矢量** |
| 风格一致性 | 每次飘 | 每次完全一致 |
| git 里能看 diff | ❌ 二进制 | ✅ 文本 |
| API key / 每张费用 | 必须，要花钱 | **都不要** |

还有一个副作用：**它不瞎猜**。每张图出货前都会自动量一遍——标签有没有溢出画布、有没有空白区域、颜色有没有跑偏。因为模型看不见自己的输出，所以只能靠量。

真实输出：

```
标签溢出画布        31 个里 0 个
异常颜色            没有（解析错误会渲染成粉色块）
空白区域            没有（7/7 横带都有内容）
文件体积            135 KB → 46 KB，看不出偏色
在 GitHub 上能显示   能（1800 × 960 加载成功）
```

## 什么时候用它

- **要字对** —— 架构图、流程图、对比图、README 首屏横幅
- **要能改** —— 改一个标签不用重画整张
- **要能进 git** —— 矢量、文本、能 diff

这些场景**别用它**：

- 插画、氛围图、写实场景、人物 → 用生图模型
- 纯逻辑关系图（不在乎排版）→ 用 Mermaid，GitHub 原生渲染，免费

## 怎么装

把 `SKILL.md` 丢进 agent 的 skills 目录：

```bash
# pi
mkdir -p ~/.pi/agent/skills/svg-infographic
cp SKILL.md ~/.pi/agent/skills/svg-infographic/

# Claude Code（项目级）
mkdir -p .claude/skills/svg-infographic
cp SKILL.md .claude/skills/svg-infographic/
```

要装的东西：

```bash
Google Chrome              # 渲染、截图、量文字边界
python3
pip install pillow numpy   # 像素分析 + PNG 压缩
```

然后直接跟 agent 说：

- 「给这个 README 画张架构图」
- 「画个流程图说明一下」
- 「做个前后对比图」
- "draw an architecture diagram for this README"

## 仓库里有什么

```
SKILL.md                      方法论本体
scripts/
  svg2png.sh                  SVG → PNG（Chrome headless + Pillow）
  check_overflow.py           查文本溢出
  check_pixels.py             查墨迹占比、亮度、空白带
  check_colors.py             查解析错误（HTML 实体误用等）
references/
  dark-template.html          暗色 HTML 模板，带导出按钮
assets/                       示例图
```

踩过的坑和硬规则（命令行参数、字体栈、压缩、配色）都在 [`RULES.md`](RULES.md)。发布相关（多语言、图片配对）见 [`github-release`](https://github.com/MoeWang-ys/github-release) skill。

## 出处

- 架构图结构技法参考 [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)（MIT）。它的暗色霓虹配色不是本 skill 的默认配色。
- `references/dark-template.html` 版权归 Cocoon AI，MIT —— 见 `references/dark-template-LICENSE`。
- 配色禁区规则来自 `huashu-design`。

## 许可

MIT
