---
name: wq-gzh-images
description: |
  公众号文章正文配图制作。将框架、流程、对比、数据等用 HTML 做成图片插入文章。触发方式：/wq-gzh-images、「给文章配图」「做正文图」「做一张图解释XX」。
---

# wq-gzh-images：公众号正文配图

---

## 配图优先级判断

先通读文章，标出两类位置再动手：

1. **适合做图的位置**：文章在讲框架、流程、对比、路径、模型、步骤——读者需要一张图帮他理解结构
2. **需要截图的位置**：文章在证明一件事是真的——聊天记录、后台数据、客户反馈、平台截图

**做图和截图不能互换：**
- 没有真实截图时，不用 AI 生成图或插画伪装证据，只标注"待补截图"
- 解释方法/模型用 HTML 做图；证明真实性用截图

---

## 主流程：HTML → 截图

**所有需要"做出来"的配图，默认用 HTML 制作，再用 puppeteer 截图。**

工作流：
1. 用 HTML/CSS 写配图，存到 `_workspace/[主题]/images/[名称].html`
2. 用 puppeteer 截图，输出到同目录 `[名称].png`
3. 用 Preview 打开确认效果
4. 插入文章对应段落（Markdown `![](相对路径.png)`）

### 截图脚本（单图版）

```javascript
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 800, height: 600, deviceScaleFactor: 2 });

  const file = 'file://' + path.resolve(__dirname, '[文件名].html');
  await page.goto(file, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 1000));

  // 截取 body 或指定元素的实际高度
  const el = await page.$('.chart'); // 或 body
  const box = await el.boundingBox();
  await page.screenshot({
    path: path.resolve(__dirname, '[输出名].png'),
    clip: { x: box.x, y: box.y, width: box.width, height: box.height }
  });

  await browser.close();
  console.log('done');
})();
```

宽度常用值：
- 数据表格图（手机阅读）：`560px`、deviceScaleFactor `3`
- 正文配图（框架/流程等）：`800px`、deviceScaleFactor `2`
- 全屏宽大图：`1080px`

**数据表格图必须用 560px + 3x 缩放**，否则在手机上字太小看不清、图太宽需缩放。

---

## 配图类型与 HTML 模板参考

### 对比图（旧认知 vs 新认知）

```html
<div class="compare" style="display:flex; gap:16px; font-family:sans-serif;">
  <div class="old" style="flex:1; background:#F5F5F5; border-radius:8px; padding:24px; color:#999;">
    <div style="font-size:12px; margin-bottom:8px; text-decoration:line-through;">旧认知</div>
    <div style="font-size:18px;">……</div>
  </div>
  <div class="new" style="flex:1; background:#FFF5EE; border-left:4px solid #C94F0C; border-radius:8px; padding:24px;">
    <div style="font-size:12px; margin-bottom:8px; color:#C94F0C;">新认知</div>
    <div style="font-size:18px; font-weight:700;">……</div>
  </div>
</div>
```

### 流程图（步骤列表）

```html
<div class="steps" style="font-family:sans-serif; padding:32px; background:#FAFAF8;">
  <div class="step" style="display:flex; align-items:flex-start; margin-bottom:24px;">
    <div class="num" style="width:40px; height:40px; border-radius:50%; background:#C00000; color:#fff; display:flex; align-items:center; justify-content:center; font-weight:900; flex-shrink:0; margin-right:16px;">1</div>
    <div>
      <div style="font-size:18px; font-weight:700; margin-bottom:6px;">步骤标题</div>
      <div style="font-size:15px; color:#666;">补充说明</div>
    </div>
  </div>
  <!-- 重复 .step -->
</div>
```

### 数据图（横向条形）

```html
<div style="font-family:sans-serif; padding:32px; background:#fff;">
  <div style="margin-bottom:16px;">
    <div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:6px;">
      <span>标签A</span><span>78%</span>
    </div>
    <div style="background:#eee; border-radius:4px; height:12px;">
      <div style="background:#C94F0C; width:78%; height:100%; border-radius:4px;"></div>
    </div>
  </div>
</div>
```

### 框架图（矩阵/象限）

```html
<div style="display:grid; grid-template-columns:1fr 1fr; gap:2px; background:#ddd; width:600px; font-family:sans-serif;">
  <div style="background:#fff; padding:24px;">
    <div style="font-size:12px; color:#999; margin-bottom:8px;">高X低Y</div>
    <div style="font-size:16px; font-weight:700;">象限一</div>
  </div>
  <!-- 4个象限 -->
</div>
```

---

## 数据表格图规范（手机端）

数据表格图是公众号文章中最常见的配图类型，有严格的手机端适配要求。

### 核心参数

| 参数 | 值 | 说明 |
|------|-----|------|
| viewport width | `560px` | 手机满屏宽度，不缩放直接看 |
| deviceScaleFactor | `3` | 3x 确保手机上文字清晰锐利 |
| body padding | `28px 20px` | 上下宽松、左右留边 |
| 正文字号 | `17-22px` | 手机上可读的最低字号 |
| 备注小字 | `11-12px` | 辅助信息，紧跟主数据下方 |
| 行间距 | `padding: 8-14px`, `line-height: 1.3` | 紧凑优先，不要大片空白 |

### 配色：纸质黄暖棕系

数据表格图不用红色系（手机上太刺眼），统一用纸质黄暖棕色调：

| 用途 | 色值 | 说明 |
|------|------|------|
| 页面背景 | `#f5f0e1` | 纸质黄底色 |
| 卡片/表格背景 | `#eae5d6` | 比底色稍深 |
| 标题栏/结论栏 | `#dcd4c0` | 暗黄强调区 |
| 边框/分隔线 | `#c9bfa0` | 柔和边线 |
| 高亮行 | `#c9b896` | 重点数据行背景 |
| 强调色（金额/结论） | `#8b4513` | 暗棕色，替代红色 |
| 标题文字 | `#5c4a2a` | 深棕色 |
| 正文文字 | `#7a6b50` | 中棕色 |
| 备注小字 | `#9a8a70` | 浅棕色 |

### 结构：标题 → 引导 → 数据 → 结论

每张数据表格图必须是完整的信息单元，包含四个层次：

1. **标题栏**（深色背景）：表格名称 + 一句副标题说明
2. **引导语**（浅色背景）：1-2 句话说明"为什么看这张表"，用加粗关键词
3. **数据表格**：紧凑排列，金额/数值单行不换行
4. **结论栏**（深色背景）：1 句核心结论 + 补充说明

不要做"没头没尾"的纯表格——读者在手机上快速滑动，需要标题和结论帮他抓住要点。

### 数据列排版：一行能搞定的一行搞定

- 金额/数值用 `white-space: nowrap` 强制单行，如 `≈3,600元/月`
- 备注信息不占独立列，改为金额下方 `11-12px` 小字副标题
- 名称列宽度 `110-120px`，`white-space: nowrap`
- 不要因为列太多导致文字折行成两行——宁可少列，保证单行可读

### 信息量控制：一张图塞太多就拆

- 一张图超过 8-10 行数据或含多个主题 → 拆成两张图
- 只做表格为图片，表格后的文字解释保持 markdown 文字形式，不要塞进图片
- 拆图原则：每张图一个明确主题，有独立标题和结论

### HTML 模板示例（数据表格图）

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#f5f0e1; font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif; padding:28px 20px; width:560px; }

.card { background:#eae5d6; border-radius:14px; border:1px solid #c9bfa0; overflow:hidden; }

.title-bar { background:#dcd4c0; padding:18px 24px; text-align:center; border-bottom:2px solid #c9bfa0; }
.title-bar h2 { font-size:22px; font-weight:800; color:#5c4a2a; letter-spacing:1px; line-height:1.4; }
.title-bar .sub { font-size:16px; color:#8a7a60; margin-top:6px; font-weight:400; }

.intro { background:#f5f0e1; padding:16px 24px; border-bottom:1px solid #d4ceb8; }
.intro p { font-size:18px; color:#7a6b50; line-height:1.7; text-align:center; }
.intro strong { color:#8b4513; font-weight:700; }

table { width:100%; border-collapse:collapse; }
tr { border-bottom:1px solid #d4ceb8; }
tr:last-child { border-bottom:none; }
td { padding:8px 14px; font-size:17px; color:#5c4a2a; line-height:1.3; vertical-align:middle; }
td.col-name { font-weight:700; color:#3a3632; width:110px; white-space:nowrap; }
td.col-value { text-align:right; }
.amount-main { font-weight:800; font-size:19px; color:#8b4513; white-space:nowrap; }
.amount-note { display:block; font-size:11px; color:#9a8a70; font-weight:400; margin-top:1px; }
tr.row-highlight { background:#c9b896; }

.summary { background:#dcd4c0; padding:20px 24px; text-align:center; border-top:2px solid #c9bfa0; }
.summary p { font-size:20px; font-weight:800; color:#2a1f0e; line-height:1.5; }
.summary .detail { font-size:16px; color:#7a6b50; margin-top:8px; font-weight:400; }
</style>
</head>
<body>
<div class="card">
  <div class="title-bar">
    <h2>标题</h2>
    <div class="sub">副标题说明</div>
  </div>
  <div class="intro">
    <p>引导语，用 <strong>加粗关键词</strong> 说明为什么看这张表</p>
  </div>
  <table>
    <tr><td class="col-name">名称</td><td class="col-value"><span class="amount-main">≈3,600元/月</span><span class="amount-note">备注小字</span></td></tr>
    <tr class="row-highlight"><td class="col-name">合计</td><td class="col-value"><span class="amount-main">≈53,300元/年</span></td></tr>
  </table>
  <div class="summary">
    <p>核心结论一句话</p>
    <div class="detail">补充说明</div>
  </div>
</div>
</body>
</html>
```

---

## 账号配色

| 账号 | 主色 | 底色 |
|------|------|------|
| 破局邦 | `#C00000` | `#FAFAF8` |
| 惟乔内容获客 | `#C94F0C` | `#FFF5EE` |
| 写作有光 | `#C94F0C` | `#0D1B2A`（深蓝） |

---

## 账号正文图默认风格（以「惟乔内容获客」为例）

**可选：优先使用手绘信息图风格。**

稳定参考图：

`02-方法论/AI指令库/视觉规范/参考图/手绘信息图风格参考.png`（按账号规范自行配置）

视觉特征：

- 白色或接近白色背景，整体像白板/手账/课堂板书，不做厚重商务卡片。
- 黑色手绘线稿为主，边框、箭头、分隔线要有轻微不规则感。
- 使用少量淡彩荧光笔涂抹做重点：黄、浅蓝、浅红/粉，颜色必须低饱和、像手工标注，不做大面积纯色块。
- 可使用简单手绘图标辅助理解，如眼睛、对话气泡、放大镜、文件、机器人、太阳、电池、机械臂等；图标服务信息，不做装饰堆砌。
- 信息结构可以是：三列卡片、阶梯、路径箭头、四步流程、分区板书、底部行动步骤。
- 标题要大，正文要短，适合手机端快速扫读；一张图只讲一个明确主题。
- 保留 `#C94F0C` 作为账号识别色，但只用于少量重点文字、序号、下划线或手绘标注，不要让整张图变成橙色系。
- 优先用 HTML/CSS 模拟手绘风格并截图；可以通过圆角不规则边框、轻微旋转、手绘线条 SVG、淡彩高亮背景来实现。

避免：

- 默认的商务卡片 UI、厚阴影、整齐网格、大片浅橙底。
- 过度精致的 SaaS 风、玻璃拟态、渐变、3D、照片人物、AI 感插画。
- 小字过多、复杂表格、颜色太艳、信息塞满没有留白。

---

## 截图后处理

- 截图完用 `open -a "Preview"` 打开确认
- 插入文章时路径相对文章文件，确保路径可解析
- 上传公众号时图片自动随 markdown 转换上传，无需额外操作
