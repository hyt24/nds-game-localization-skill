# NDS Game Localization Skill

一套面向 Codex / AI Agent 的 Nintendo DS 游戏本地化工作流，来自《天堂独太 2》中文化项目中的真实实践。

An evidence-driven Codex skill for auditing, translating, rebuilding, and validating Nintendo DS game localizations.

它不是针对某一款游戏写死的“一键汉化器”，而是一套可迁移、可审计、可复现的方法：帮助 Agent 从 `.nds` ROM 开始，完成已有汉化检索、资源盘点、文字识别、术语统一、文本与图片回写、ROM 重建、差异审计和模拟器/实机验证。

## 它解决什么问题

NDS 游戏里的文字不一定是普通字符串。它们可能存在于自定义字形流、压缩容器、4bpp/8bpp 图块、调色板图片、ARM9 或 Overlay 中。只做字符串搜索，通常会遗漏菜单、章节标题、卡片标题、图片文字和运行时生成的 UI。

这个 Skill 要求 Agent 把汉化当成一个完整工程，而不是一次翻译任务：

- 开始前联网确认是否已有汉化版、补丁或进行中的项目；
- 保留不可变的原始 ROM，并记录每个候选版本的 SHA-256；
- 盘点 NitroFS、ARM9、Overlay、压缩格式和全部资源族；
- 使用全文 OCR、候选字形匹配和人工校对恢复原文；
- **批量翻译前先建立并审批词汇表**；
- 让对话、菜单、道具/卡片标题和图片使用统一译名；
- 保留控制码、字形容量、图块布局、调色板和 UI 边界；
- 对重建 ROM 做组件级二进制差异审计；
- 将离线检查与模拟器/实机验证明确分开；
- 持续维护资源清单、构建谱系、失败假设和测试进度。

## 推荐流程

```text
联网检索已有汉化
        ↓
确认版本与用户选择
        ↓
ROM / NitroFS / ARM9 / Overlay 资源审计
        ↓
文本、字形、图片与运行时文字分类
        ↓
OCR 与人工识别 → 初始词汇表审批
        ↓
翻译与容量检查 → 文本/图片回写
        ↓
重建 ROM → 二进制差异与回读验证
        ↓
模拟器/实机测试 → 进度与发布记录
```

## 主要能力

- NDS ROM 基础信息与 NitroFS 清单导出
- 原版/候选 ROM 组件差异比较
- 自定义字形流和上下文 OCR 的处理原则
- 4bpp/8bpp 图块、调色板和图片 UI 的审计方法
- 人名、称呼、章节、UI、道具、卡片及专业术语的词汇表门槛
- 可复制的项目清单、资源表、构建记录和运行测试模板
- OCR/翻译服务的手动、本地及 API 三种配置模式
- ARM9/Overlay 运行时 Hook 的证据要求与风险控制
- BPS/xdelta 等合法补丁发布建议

## 安装

将仓库克隆到 Codex 可发现的 Skill 目录：

```bash
git clone https://github.com/hyt24/nds-game-localization-skill.git \
  ~/.agents/skills/nds-game-localization
```

重新启动 Codex 后，可在任务中直接说：

```text
使用 nds-game-localization skill，帮我审计这份 NDS ROM，先检查网上是否已有汉化版。
```

也可以只把仓库作为流程与模板参考使用。

## 环境

基础审计脚本需要：

- Python 3
- [`ndspy`](https://github.com/RoadrunnerWMC/ndspy)

处理项目专用图片时通常还需要 Pillow。OCR 和翻译 API 并非强制：可以选择完全人工模式、本地 OCR 模式，或经用户授权后使用外部 Vision/翻译服务。密钥应保存在项目 `.env` 中，不得提交到版本库。

## 内置模板与检查器

- `assets/project-manifest.yaml`：项目、ROM 和工具配置
- `assets/glossary.csv`：翻译词汇表
- `assets/resource-inventory.csv`：资源发现与处理状态
- `assets/build-ledger.csv`：候选 ROM 谱系、哈希和验证结果
- `assets/hypothesis-log.csv`：发现、失败和已推翻假设
- `assets/runtime-test-matrix.csv`：模拟器/实机测试矩阵
- `scripts/inspect_nds.py`：ROM 与 NitroFS 审计
- `scripts/compare_nds.py`：ROM 组件差异比较
- `scripts/check_glossary.py`：翻译前词汇表门槛检查
- `scripts/check_progress.py`：项目进度完整性检查

## 适用范围与限制

这套方法适用于多数以 NitroFS 为基础的 NDS 本地化项目，但不能保证自动支持所有游戏。不同游戏可能使用私有压缩、加密、脚本虚拟机、运行时字库、特殊 VRAM 管线或反篡改机制。遇到未知格式时，应先证明解析与无修改回写能够字节级往返，再开始翻译。

项目不会替代语言校对、图像人工调整和运行测试。静态检查通过不等于游戏中一定正常。

## 法律与发布边界

只处理用户有权修改的 ROM。不要在仓库、Issue 或发布包中上传商业 ROM、完整提取资源、专有字体、密钥或其他受版权保护的数据。公开发布时应提供工具、源码、校验值和合法的差分补丁，而不是 ROM 本体。

## 致谢

本 Skill 的形成受中文 NDS 汉化社区教程与开源工具启发，包括 fengarea（A9VG 汉化组）的《NDS汉化小白教程》、用户提供的 Bilibili 学习资料，以及 Haroohie Translation Club 的 NitroPacker。完整来源和许可说明见 [references/acknowledgements.md](references/acknowledgements.md)。

## License

[MIT License](LICENSE)
