---
name: wq-gzh-post
description: |
  公众号文章排版检查与上传。普通文章（news）走完整排版规范再上传；贴图（newspic）走卡片图上传流程。适用于破局邦、惟乔内容获客、写作有光。触发方式：/wq-gzh-post、「上传到破局邦」「上传到惟乔」「发写作有光」「上传公众号」。
---

# wq-gzh-post：公众号排版与上传

---

### 账号配置

| 账号 | alias | theme | color | author | 凭据环境变量 |
|------|-------|-------|-------|--------|--------------|
| 破局邦 | `pojubang` | `pojubang` | `#C00000` | [作者名] | `WECHAT_POJUBANG_APP_ID` / `WECHAT_POJUBANG_APP_SECRET` |
| 惟乔内容获客 | `weijiaoip` | `default` | `#C94F0C` | [作者名] | `WECHAT_WEIJIAOIP_APP_ID` / `WECHAT_WEIJIAOIP_APP_SECRET` |
| 写作有光 | `xiezuoyouguang` | `default` | `#C94F0C` | [作者名] | `WECHAT_XIEZUOYOUGUANG_APP_ID` / `WECHAT_XIEZUOYOUGUANG_APP_SECRET` |

### 本地运行配置

| 项 | 值 |
|----|----|
| 上传入口脚本 | `~/.wq-skills/upload-wechat.sh` |
| 内部上传实现 | `~/.wq-skills/wq-gzh-post-uploader/scripts/wechat-api.ts` |
| 凭据文件 | `~/.wq-skills/.env` |
| SSH 隧道脚本 | `~/.wq-skills/start-wechat-proxy.sh` |
| 代理地址 | `http://127.0.0.1:13128` |

---

## 类型一：普通文章（news）

### 第一步：读取账号排版规范（必做，不可跳过）

上传前必须读取对应规范全文，不凭记忆执行：

- 破局邦：`02-方法论/AI指令库/写作指令/破局邦-排版规范.md`
- 惟乔内容获客：`02-方法论/AI指令库/写作指令/惟乔内容获客-排版规范.md`
- 写作有光：`02-方法论/AI指令库/写作指令/写作有光-排版格式.md`

规范与其他 skill 冲突时，以账号规范为准。

### 第二步：生成上传版文件（-upload.md）

- 去掉 frontmatter（`账号`、`状态`、`日期` 不进正文）
- 正文第一行不含标题（标题只通过 `--title` 传入）
- 追加账号固定结尾（从排版规范取，不手写）
- 用 `awk` 同时去掉末尾标题候选区，不用 `tail`

### 第三步：上传前检查清单

通用：
- [ ] frontmatter 已去除
- [ ] 正文无重复标题行
- [ ] **标题已由用户明确确认，不是 AI 自拟**
- [ ] 所有本地图片路径存在
- [ ] 封面图存在，`--cover` 指向最终封面
- [ ] **正文配图已插入**（若本次创作过程中生成过配图，逐一确认已嵌入正文对应位置；未插入则上传前先插入，不跳过）
- [ ] 节标题颜色、加粗、色块、结尾模板已按规范执行

破局邦额外：
- [ ] 正文第一行是 `12px` 页首关注提示 HTML（不是 `15px`）
- [ ] 上传稿无微信原生公众号名片模拟
- [ ] 结尾含 3 条推荐阅读 + 见面礼 CTA（`#576b95` 蓝色 span）
- [ ] 金句软植入链接保留（footer 的 `[文字](URL)` 不替换为纯文本）

惟乔内容获客额外：
- [ ] 节标题用 `<p style="color:#C94F0C;font-weight:bold;">` 格式
- [ ] 加粗用 `<strong style="color:#C94F0C;">` 不用 markdown `**`
- [ ] 有 1-2 个强观点框（`background:#FFF5EE; border-left:4px solid #C94F0C`）
- [ ] 结尾福利+关于作者+推荐阅读，标签用蓝色 `<span style="color:#576b95;">`

写作有光额外：
- [ ] 主题色 `#C94F0C`
- [ ] 封面文字与文章标题相同

### 第四步：上传命令

**标题来源规则（最高优先级）**：`--title` 必须使用用户原始提供的标题。AI 提议的标题若未经用户明确确认（用户说"用这个"/"就这个"/"好"），不得用于上传。有疑问时回问用户，不擅自决定。

```bash
bash ~/.wq-skills/upload-wechat.sh \
  '[文章-upload.md路径]' \
  --account [alias] \
  --cover '[封面图路径]' \
  --title '[纯标题，去掉文件名NN-前缀]'
```

上传成功确认日志：
- `Account: [账号名] ([alias])`
- `Cover uploaded successfully`
- 返回 `media_id`

---

## 类型二：贴图（newspic）

卡片图生成见 `/wq-gzh-cards`。

### upload.md 格式

```markdown
第一段描述文字。

第二段描述文字。

#话题一 #话题二 #话题三

![](card-00-xxx.png)

![](card-01-xxx.png)
```

规则：
- 描述在图片前，段间空一行
- `#话题` 直接写（描述字段是纯文本）
- 第一张图 = feed 封面，**不加 `--cover`**
- 图片 5-6 张，过多触发 45166

### 上传命令

```bash
bash ~/.wq-skills/upload-wechat.sh \
  '[upload.md路径]' \
  --type newspic \
  --title '[标题，≤20字]' \
  --account [alias] \
  --no-cite
```

注意：标题 ≤ 20 字；不加 `--cover`；`wechat-api.ts` 已打补丁（newspic 自动剥 HTML、`</p>` 转 `\n\n`）

---

## 代理问题

本机 IP 不在白名单时脚本自动启 SSH 隧道。手动启：

```bash
bash ~/.wq-skills/start-wechat-proxy.sh
curl -s -x http://127.0.0.1:13128 https://api.weixin.qq.com/  # 返回404即正常
```

---

## 完成报告

- 账号 + 文章路径 + 上传类型（news / newspic）
- 草稿 `media_id`
- 若中途上传过错版本，提醒删除旧草稿
