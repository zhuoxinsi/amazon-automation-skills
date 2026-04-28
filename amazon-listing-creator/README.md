<p align="center">
  <h1>🛒 Amazon Listing Creator</h1>
  <strong>基于 A9 + COSMO + Rufus 三算法的亚马逊 Listing 智能生成器</strong><br/>
  <em>让 AI 帮你写出高转化、合规、SEO 友好的专业 Listing</em>
</p>

<p align="center">
  <a href="#-功能特性">功能特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-输出示例">输出示例</a> •
  <a href="#-算法说明">算法说明</a> •
  <a href="#%EF%B8%8F-常见问题">FAQ</a>
</p>

---

## ✨ 功能特性

| 特性 | 说明 |
|------|------|
| 🎯 **三算法驱动** | A9（关键词排名）+ COSMO（场景意图）+ Rufus（事实数据）全覆盖 |
| 📋 **7 步引导流程** | 分阶段对话，从资料准备到 Listing 导出，每一步都有指引 |
| 🛡️ **三层防护机制** | 数据层分离 + 自动校验 + 模板隔离，英文内容绝对纯净 |
| ⚠️ **合规黑名单检测** | 自动拦截 best/premium/guaranteed 等违规词 |
| 📊 **Excel 专业导出** | 标准化格式，含校验汇总、主图建议、中英对照 |
| 🔤 **中英双语输出** | 英文 Listing + 中文翻译，方便团队审核 |

## 🚀 快速开始

### 前置要求

- [OpenClaw](https://github.com/openclaw) 已安装并运行
- 本 Skill 已放入 OpenClaw skills 目录

### 安装步骤

#### 方式一：通过 SkillHub 一键安装（推荐）

```bash
skillhub install amazon-listing-creator
```

#### 方式二：手动安装

1. 将 `amazon-listing-creator` 文件夹复制到你的 OpenClaw skills 目录：
   ```
   {openclaw_skills_dir}/amazon-listing-creator/
   ```

2. 确保目录结构完整：
   ```
   amazon-listing-creator/
   ├── SKILL.md              # Skill 核心配置与指令
   ├── README.md             # 你正在看的这个文件
   ├── AGENTS.md             # Agent 行为规范
   ├── LL.md                 # Listing 逻辑规则
   ├── prompts/              # 分阶段提示词模板
   │   └── ...
   ├── _metadata.json        # 元数据
   └── amazon_compliance_blacklist.txt  # 合规黑名单词库
   ```

3. 重启 OpenClaw Gateway：
   ```bash
   openclaw gateway restart
   ```

### 使用方式

安装完成后，直接对 AI 说以下任意一句话即可触发：

- "帮我生成一个亚马逊 Listing"
- "我要上架一个新产品"
- "帮我优化一下这个产品的标题和五点"
- "写一个餐具收纳架的 Listing"

AI 会自动进入 **7 步引导流程**，逐步收集信息后生成完整 Listing。

## 📦 输入文件

在使用前，请准备好以下 4 份文件（越详细效果越好）：

| 文件 | 作用 | 推荐来源 |
|------|------|---------|
| **本品属性表.txt** | 产品参数、材质、尺寸等事实数据 | 1688 / 供应商规格书 |
| **竞品意图分析.txt** | 头部竞品的卖点、场景、人群洞察 | 竞品 Listing + Review 分析 |
| **ABA关键词数据.csv** | 类目高流量关键词及搜索量 | 亚马逊后台 / 卖家精灵 / Helium 10 |
| **竞品出单词报告.csv** | 竞品实际流量词，补充长尾词 | 反查工具 |

> 💡 **没有全部文件也能用** — AI 会根据已有信息智能补全，但数据越全，Listing 质量越高。

## 📄 输出内容

生成的 Excel 文件包含以下模块：

### Module 1: Title（标题）
- ≤200 字符，A9 关键词优化
- 核心词前置，品牌+品名+卖点+尺寸

### Module 2: Bullet Points（五点描述）
- 5 条结构化卖点，每条 ≤500 字符
- 每条包含：英文正文 + 场景词 + 关键词埋入 + 中文翻译

### Module 3: Search Terms（后台搜索词）
- ≤250 bytes，空格分隔
- 无重复、无竞品品牌、无标点

### Module 4: Validation Summary（校验汇总）
- 字符数/字节数自动统计
- A9 / COSMO / Rufus 三算法合规检查
- 违规词黑名单扫描

### Module 5: 主图设计建议
- 基于产品卖点的视觉表达建议
- 主图 + 辅图组合方案

## 🧠 三大算法说明

本 Skill 的 Listing 生成逻辑基于亚马逊三大核心算法：

| 算法 | 解决什么问题 | 核心逻辑 | 我们怎么做 |
|------|------------|---------|-----------|
| **A9/A10** | 「搜得到」 | 关键词匹配与权重分配 | 核心词前置到 Title 前部，Search Terms 覆盖长尾 |
| **COSMO** | 「搜的人是不是对的人」 | 场景理解 + 人群标签 | 每条 Bullet Point 绑定场景词和人群意图 |
| **Rufus** | 「买不买你」 | 事实数据驱动，拒绝空洞描述 | 所有卖点必须有产品参数/数据支撑 |

## 🛡️ 英文质量保障

我们深知亚马逊 Listing 的英文质量直接影响转化率。因此内置了 **三层防护机制**：

```
┌─────────────────────────────────────────┐
│ 第 1 层：数据分离                        │
│   _en 字段 = 纯英文                      │
│   _zh 字段 = 纯中文翻译                  │
│   scene/keywords = 永远英文              │
└─────────────────────────────────────────┘
                ↓ 校验通过 ↓
┌─────────────────────────────────────────┐
│ 第 2 层：自动检测                        │
│   导出前正则扫描所有英文字段              │
│   发现中文 → 立即报错中断 + 定位字段      │
└─────────────────────────────────────────┘
                ↓ 校验通过 ↓
┌─────────────────────────────────────────┐
│ 第 3 层：写入隔离                        │
│   英文列只读 _en 字段                    │
│   中文列只读 _zh 字段                    │
│   从结构上杜绝混用可能                   │
└─────────────────────────────────────────┘
```

## 📊 导出示例

导出的 Excel 文件结构预览：

```
Hanson_AMZ001_Utensil_Holder_Listing.xlsx
├── Row 1: 主标题行（品牌 + 产品名）
├── Row 2: 出品信息行
├── Module 1: Title（5列：模块/内容/场景词/关键词/中文翻译）
├── Module 2: Bullet Points × 5（5列：#/内容/场景词/关键词/中文翻译）
├── Module 3: Search Terms（英文 + 中文翻译，合并宽列显示）
├── Module 4: Validation Summary（11项合规检查结果）
└── Module 5: 主图设计建议
```

## ❓ 常见问题

<details>
<summary><b>Q: 必须提供 4 份输入文件才能用吗？</b></summary>

不是的。4 份文件是「最佳实践」，但即使只有产品基本信息，AI 也能生成可用的 Listing。数据越全，Listing 的 SEO 表现和转化率通常越好。
</details>

<details>
<summary><b>Q: 支持哪些类目的产品？</b></summary>

通用设计，支持所有类目。Skill 本身不限制类目，算法逻辑（A9/COSMO/Rufus）适用于所有亚马逊站点。
</details>

<details>
<summary><b>Q: 生成的 Listing 可以直接用吗？</b></summary>

生成的 Listing 可以作为高质量初稿使用。建议根据实际产品和运营经验做微调后再上架。
</details>

<details>
<summary><b>Q: 英文部分会不会出现中文？</b></summary>

不会。三层防护机制会在导出前自动校验所有英文字段，一旦发现中文字符会立即报错中断，不会生成含有中文的英文 Listing。
</details>

---

## 🌟 Star 支持

如果这个 Skill 对你有帮助，欢迎给一个 ⭐ Star 支持一下！

你的支持是我们持续更新的动力：
- 🔧 更多类目的模板优化
- 🌍 多语言 Listing 支持（德语、日语等）
- 📈 A/B 测试对比功能
- 🤖 与更多亚马逊工具集成

<a href="https://github.com/zhuoxinsi/amazon-automation-skills">
  <img src="https://img.shields.io/github/stars/zhuoxinsi/amazon-automation-skills?style=social" alt="GitHub Stars"/>
</a>

---

## 📝 License

MIT License © [zhuoxinsi](https://github.com/zhuoxinsi)

## 🤝 贡献

欢迎 Issue 和 PR！如果你在使用中发现问题或有改进建议，欢迎提 [Issue](https://github.com/zhuoxinsi/amazon-automation-skills/issues)。
