# wq-skills

一套用于公众号内容生产的 Claude Code / Codex skill 集合。覆盖从选题、写作、标题、封面图、排版到上传公众号的完整流程。

---

## 包含哪些 skill

| Skill | 功能 |
|-------|------|
| `wq-gzh-article` | 公众号文章写作全流程（选题→大纲→草稿→检查） |
| `wq-gzh-title` | 标题生成，匹配爆款公式 |
| `wq-gzh-opening` | 开头生成与检查 |
| `wq-gzh-ending` | 结尾生成（非营销型） |
| `wq-gzh-topic` | 选题系统，常规选题 + 热点选题 |
| `wq-gzh-post` | 排版检查 + 上传公众号 |
| `wq-gzh-cover` | 封面图生成（Gemini/ChatGPT web 通道） |
| `wq-gzh-images` | 正文配图制作（HTML→截图） |
| `wq-gzh-cards` | 贴图号卡片图生成 |
| `wq-gzh-marketing` | 营销植入（软植入/强转化） |
| `wq-gzh-story` | 故事案例引擎 |
| `wq-gzh-viewpoint` | 观点重构与金句化 |
| `wq-gzh-humanizer` | 去AI味润色 |
| `wq-gzh-fact-check` | 文章事实检测 |
| `wq-gzh-argument-check` | 文章论证拆解 |
| `wq-gzh-analytics` | 公众号数据分析（读截图） |
| `wq-rike` | 日课写作（知识星球） |
| `wq-video-script` | 短视频脚本写作 |
| `wq-brand-position` | 三层定位系统 |
| `wq-content-diagnosis` | 内容诊断（两轨法） |

---

## 安装方式

### Claude Code

```bash
# 把仓库 clone 到 ~/.claude/skills/
git clone https://github.com/sungwong/wq-skills.git /tmp/wq-skills

# 把每个 skill 文件夹复制到 ~/.claude/skills/
cp -r /tmp/wq-skills/wq-* ~/.claude/skills/
```

### Codex

```bash
git clone https://github.com/sungwong/wq-skills.git /tmp/wq-skills
cp -r /tmp/wq-skills/wq-* ~/.agents/skills/
```

---

## 使用前提：内容系统目录结构

这套 skill 依赖一套固定的文件夹结构。**用 Claude Code / Codex 打开你的内容系统根目录**（而不是其他文件夹），skill 里的相对路径才能正确找到素材库和方法论文件。

推荐目录结构（与[学员安装包](https://github.com/sungwong/wq-skills)配套）：

```
内容系统根目录/
├── CLAUDE.md（Claude Code）/ AGENTS.md（Codex）
├── 想法记录.md
├── 01-素材/
│   ├── 核心概念/
│   ├── 金句库/
│   └── 案例库/
├── 02-方法论/
│   ├── AI指令库/写作指令/写作风格.md   ← 必须存在
│   ├── 写作系统/开头方法论.md           ← 必须存在
│   └── 标题系统/标题方法论.md           ← 必须存在
└── 03-产出/
    └── 文章库/
```

---

## 配置你自己的账号

这套 skill 默认以「破局邦 / 惟乔内容获客 / 写作有光」三个账号为示例。你需要替换成自己的账号：

1. **写作风格**：修改 `wq-gzh-humanizer/references/style-weiqi.md`，按文件顶部说明提取你自己的风格 DNA
2. **账号定位**：在 `04-品牌/定位系统/03-账号定位/` 下建立你自己的账号定位文件
3. **排版规范**：在 `02-方法论/AI指令库/写作指令/` 下建立你自己的账号排版规范
4. **公众号上传**：`wq-gzh-post` 依赖 `~/.wq-skills/upload-wechat.sh`，需单独配置微信公众号 API 凭据

---

## 主要流程

### 写一篇公众号文章

```
/wq-gzh-article
```

或直接说：「帮我写一篇公众号文章，主题是XXX」

流程：确认账号 → 检索素材库 → 生成候选标题 → 确认大纲 → 写正文 → 去AI味 → 事实检测 → 论证检查

### 上传公众号

```
上传到[账号名]
```

### 写日课

```
/wq-rike
```

或说：「写日课，今天聊XXX」

---

## License

MIT
