# svg-infographic

> 做信息图 / 架构图 / 流程图 / 对比图 / README 配图的完整方法论 —— **手写 SVG + Chrome headless**，附程序化验证脚本。

![svg-infographic 方法论总览](assets/hero.svg)

<sub>↑ 这张图本身就是本 skill 画的：34 个文本元素 0 溢出，4 项程序化验证全过。</sub>

给 AI 编码 agent 用的 skill（Claude Code / pi / Cursor 等均可）。核心主张一句话：

**带文字的图，别让文生图 AI 画，手写 SVG。**

---

## 为什么

**生图模型画中文几乎必错**，而信息图的价值 100% 在文字上。

|  | 生图 AI | 手写 SVG |
|---|---|---|
| 要 API key | 要 | **不要** |
| 文字准确性 | **经常画错字**（尤其中文） | 100% 可控 |
| 改一个字 | 重新生成 → 整张全变 | 改一处 → 只变一处 |
| 体积 | 几百 KB ~ 几 MB | **~8KB（矢量）** |
| 风格一致性 | 每次飘 | 完全一致 |
| 可版本管理 | ❌ 二进制 | ✅ 文本 diff |

分界线是**文字是否重要**：

| 要做的东西 | 用什么 |
|---|---|
| 架构图、流程图、对比图、数据流图 | ✅ **本 skill（手写 SVG）** |
| README 首屏 banner（带准确文字） | ✅ 本 skill |
| 插画、氛围图、写实场景、人物、产品图 | ❌ 生图 AI |
| 纯逻辑关系图（无精确排版要求） | 可用 Mermaid（GitHub 原生渲染，零成本） |

---

## 它解决的真问题：AI 看不见自己的图

多数模型不支持图片输入。所以画完不能靠"应该没问题"，**必须靠程序化验证**。

本 skill 提供 4 项实测：

1. **文本溢出检测** — 在 Chrome 里跑 `getBBox()` 量每个 `<text>` 的真实包围盒，越界即报
2. **像素分析** — 墨迹占比 + 最暗亮度 + 横带内容分布，确认"东西真的画出来了"且没空白带
3. **主色采样** — 采样已知位置坐标，确认配色没跑偏
4. **模拟 GitHub 加载** — README 里是 `<img src>`，跟直接打开 SVG 不一样，`naturalWidth = 0` 说明图根本没加载

实测战绩（2026-09-30 给 `pi-web-extensions` 做 README 插图）：
**三张中文图 86 个文本元素 0 溢出**，英文版重排后同样 0 溢出，6 张图全部通过验证后上线。

---

## 安装

把 `SKILL.md` 放到你的 agent skills 目录：

```bash
# pi
cp SKILL.md ~/.pi/agent/skills/svg-infographic/SKILL.md

# Claude Code（项目级）
mkdir -p .claude/skills/svg-infographic && cp SKILL.md .claude/skills/svg-infographic/
```

依赖：

```bash
# 必须
Google Chrome              # 渲染 + 截图 + 量包围盒
python3                    # 验证脚本
pip install pillow numpy   # 像素分析 + PNG 压缩
```

> **别用 cairosvg**：macOS 上缺 `libcairo.2.dylib`，装了也跑不起来。Chrome 本机已经有了，直接用。

---

## 内容

```
SKILL.md                     完整方法论（418 行）
scripts/
  svg2png.sh                 SVG → PNG（Chrome headless + Pillow 压缩）
  check_overflow.py          ① 文本溢出检测
  check_pixels.py            ② 像素分析
references/
  dark-template.html         暗色模板（17KB，含 Copy/PNG/PDF 导出按钮）
  dark-template-LICENSE      上游 MIT 许可
```

### 方法论覆盖面

- **5 步流程**：手写 SVG → Chrome 转 PNG → 压缩 → 程序化验证 → README 引用
- **z-order 铁律**：箭头要画在方框之前（SVG 后画的盖住先画的）
- **中英双语版**：不是翻译一下就能用，英文比中文宽，替换后必须重新量包围盒
- **本地预览**：图片必须 base64 内嵌，否则 Chrome 拦 `file://` 是空白
- **配色**：暖砂 + 赤陶橙 + 墨青默认配色，附审美禁区（深蓝底霓虹 / 紫渐变 / emoji 当图标）
- **架构图专技**：组件间距表、半透明方框遮不住箭头、图例必须在边界框外

### 踩过的坑（都实测过）

| 坑 | 现象 | 解法 |
|---|---|---|
| `file://` 图片被拦 | `naturalWidth = 0`，预览空白 | 图片 base64 内嵌 |
| `fetch()` 被 CORS 拦 | 注入脚本拿不到 SVG | SVG 内容直接内联进 HTML |
| `--window-size` < viewBox | 图被裁 | window ≥ viewBox |
| PNG 压缩开 dither | 体积反而变大 + 噪点 | `dither=Image.NONE` |
| CJK 双宽 | ASCII 算好的对齐，中文一放就歪 | 别用 ASCII 画含中文的图 |
| 中英文字宽不同 | 中文换英文后溢出 | 英文版单独量包围盒；调小 font-size |
| 检查脚本跨 group 误报 | 报"箭头被遮挡"其实没有 | 用 `getBoundingClientRect()` |

---

## 效果示例

实测压缩效果：

```
Chrome 直出 430KB  →  quantize(128, dither=NONE)  →  140KB   (-67%)
色差 0.4~0.8 / 255（肉眼不可见）
```

产出结构（6 张图中英各 3，共 1.1MB，SVG 单张仅 8KB）：

```
docs/assets/
  hero.svg              8.9KB   首屏：before/after 对比
  hero-en.svg           8.9KB
  flow.svg              7.9KB   流程：说一次，以后都记得
  flow-en.svg           7.9KB
  architecture.svg      7.0KB   架构：它由哪几块组成
  architecture-en.svg   7.1KB
  *.png                        各 ~140KB，给本地预览用
```

---

## 与其他 skill 的分工

- **Mermaid**：纯逻辑关系图，GitHub 原生渲染，零成本 —— 本 skill 不抢这活
- **frontend-slides / beautiful-html-templates**：幻灯片整页
- **huashu-design**：本 skill 的审美禁区规则来自它

---

## 致谢

- 架构图结构技法吸收自 [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)（MIT），其暗色霓虹配色不符合本 skill 默认配色，仅取其结构技法
- `references/dark-template.html` 版权归 Cocoon AI，MIT，见 `references/dark-template-LICENSE`

## License

MIT
