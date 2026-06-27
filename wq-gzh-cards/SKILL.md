---
name: wq-gzh-cards
description: |
  公众号贴图号卡片图生成。将日课、文章观点做成一组 HTML 卡片并截图，用于微信公众号贴图（newspic）格式发布。触发方式：/wq-gzh-cards、「做成卡片图」「生成贴图」「做贴图号图片」。上传步骤另见 /wq-gzh-post。
---

# wq-gzh-cards：公众号贴图卡片图生成

---

## 一、通用规范

### 封面文字排版（最高优先级·所有账号通用）

封面标题字**必须充分利用版面，左右对齐、撑满空间**。这是常识，做不到就是不合格。

- **字号要够大**：以"最长那一行基本顶到左右内边距"为准，不要用固定小字号留一大片空白。下方各账号写的字号（如 92px）只是参考下限，**短文案必须按比例放大**，通常落在 130–170px 区间，直到撑满为止。
- **左右留白匀称**：左对齐时，要靠放大字号让最长行贴近右边距，使左右留白视觉平衡；右边大片空、左边贴边就是错的。
- **三行字数尽量接近**（如 6-5-5、8-6-8），减少各行右端的参差。
- **做完自检**：截图后看封面，最长行有没有逼近右边距？左右留白是否对称？字是不是显小、版面是不是发空？任一不满足就加大字号重截。

### 卡片尺寸

所有卡片尺寸一致，不区分"封面卡"与"内容卡"：

| 设计稿 | 截图实际（@2x） |
|--------|------------|
| 1080×1440px（3:4） | 2160×2880px |

文件命名：`card-00-主题.png`、`card-01-主题.png`……
存放位置：`_workspace/[主题]/`

### 截图脚本（screenshot.js）

```javascript
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1440, deviceScaleFactor: 2 });

  const file = 'file://' + path.resolve(__dirname, 'cards.html');
  await page.goto(file, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));

  const cards = await page.$$('.card');
  const labels = ['00-主题', '01-xxx', '02-xxx'];

  for (let i = 0; i < cards.length; i++) {
    const box = await cards[i].boundingBox();
    await page.screenshot({
      path: path.join(__dirname, `card-${labels[i] || i}.png`),
      clip: { x: box.x, y: box.y, width: box.width, height: box.height }
    });
  }

  await browser.close();
})();
```

运行：`node screenshot.js`（需在项目目录安装 puppeteer）

截图完用 Preview 打开确认效果，再交给 `/wq-gzh-post` 上传。

---

## 二、账号规范：惟乔内容获客（weijiaoip）

### 配色

```css
--grad: linear-gradient(135deg, #16C96B 0%, #06B6A0 100%);
--grad-soft: linear-gradient(135deg, #E8F8EE 0%, #E2F4EF 100%);
--ink: #1C231E;
--ink-soft: #33403A;
--ink-mute: #7C8A82;
--line: rgba(28,35,30,0.12);
background: linear-gradient(180deg, #F4FAF3 0%, #EAF4E9 55%, #E6F2E6 100%);
```

### 第一张卡（标题卡）

- 只放标题文字，无其他元素
- 文字左对齐，垂直居中
- 三行，字数均衡（如 8-6-8）
- 字号 92px 起步（仅下限），**按通用规范放大到撑满版面**，短文案通常 130–170px，字重 900，行高 1.4
- 最后一行绿色渐变（`em` 标签）
- 两侧内边距 88px

```css
.card.cover { justify-content:center; align-items:flex-start; padding:80px 88px; }
.cover .hero { font-size:162px; /* 下限92px，放大至撑满 */ font-weight:900; line-height:1.4; letter-spacing:2px; color:var(--ink); }
.cover .hero em { font-style:normal; background:var(--grad); -webkit-background-clip:text; background-clip:text; color:transparent; }
```

### 内容卡结构（第二张起）

1. 顶栏：账号名（绿渐变，`letter-spacing:5px`）+ 页码圆圈（右）
2. 分隔线：`height:2px`
3. kicker：`26px`，绿渐变
4. 节标题：`62px`，字重 900，关键词用 `em`（绿渐变）
5. 正文：`34px`，行高 1.85，`color:var(--ink-soft)`
6. 金句框（可选）：绿色左竖条 + 淡绿底
7. 对比表（可选）：旧认知划线灰底 + 新认知淡绿底
8. 优先级列表（可选）：绿渐变圆形数字
9. 底栏：账号名（左）+ 话题（右），`margin-top:auto`

内边距：`padding: 80px 88px 72px`

---

## 三、账号规范：破局邦（pojubang）

### 配色

```css
--red: #C00000;
--ink: #1a1a1a;
--bg: #FAFAF8;
--highlight: rgba(255,220,80,0.45);  /* 黄色荧光划线 */
--quote-bg: #FFF5F5;
--quote-border: #C00000;
```

### 第一张卡（标题卡）

- 无顶部账号栏
- 超大标题：黑色，72-80px 起步（仅下限），**按通用规范放大到撑满版面**，字重 900，左对齐
- 标题下方：`全文约XXXX字 | 阅读需X分钟`，16px 灰色
- 底部：`破局邦·[话题分类]`（左）+ `01/0X` 红色（右）

### 内容卡结构（第二张起）

1. 顶栏：`● 破局邦`（红点+文字，左）+ `0X/0X` 红色（右）
2. 节标题：60-70px，字重 900，1-2 个关键词红色（`#C00000`）
3. 正文：26-30px，字重 700，行高 1.7
4. 黄色划线：重要短句 `background:rgba(255,220,80,0.45)`（inline）
5. 引用块：`4px solid #C00000` 左线 + `#FFF5F5` 底
6. 底栏：本节主题词（左，灰）+ `0X/0X` 红色（右）

内边距：`padding: 80px 72px 72px`，背景 `#FAFAF8`
