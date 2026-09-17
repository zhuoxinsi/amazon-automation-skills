# Amazon Listing Creator 🌹

基于 A9 + A10 + COSMO + Alexa + Rufus 多算法的亚马逊 Listing 智能生成工具。

---

## 功能特点

- ✅ 多算法全覆盖（A9 + A10 + COSMO + Alexa + Rufus）
- ✅ 关键词与场景词分列（C列关键词=A9/A10, D列场景词=COSMO/Alexa）
- ✅ 关键词列严格限定数据来源（MCP/用户提供的竞品词，禁止AI联想）
- ✅ 2026 年 7 月标题新规适配（Item Name ≤75字符 + Item Highlights ≤125字符）
- ✅ 支持 SIF MCP 全自动拆解竞品 ASIN
- ✅ 无 MCP 时支持用户上传关键词列表
- ✅ 关键词埋入主框架（P0-P3 分级 + 品牌词去除）
- ✅ 认证信息默认不写入前端文案
- ✅ 强制联网搜索近 6 个月亚马逊新规合规排查
- ✅ 自然流量 + 链接权重最终审核优化
- ✅ 合规黑名单自动校验
- ✅ 数据驱动，拒绝空洞描述
- ✅ 分阶段交互引导，差评/Refus 复核确认

---

## 安装方法

### 方法一：从 GitHub 安装（推荐）

```bash
# 克隆仓库到 OpenClaw skills 目录
git clone https://github.com/zhuoxinsi/amazon-automation-skills.git %USERPROFILE%\.qclaw\skills\amazon-listing-creator

# Windows PowerShell 用户也可以用：
git clone https://github.com/zhuoxinsi/amazon-automation-skills.git "$env:USERPROFILE\.qclaw\skills\amazon-listing-creator"

# 重启 OpenClaw Gateway
openclaw gateway restart
```

> 📌 安装后 skill 路径：`%USERPROFILE%\.qclaw\skills\amazon-listing-creator\`

### 方法二：ClawHub 安装（如已上架）

```bash
openclaw skills install amazon-listing-creator
```

---

## 使用方法

安装完成后，直接在 OpenClaw 中说：

> "帮我生成 THKVESN BGL091 降临节日历的 Listing，竞品 ASIN：B0FBW9NQJT"

AI 会自动拆解竞品数据并引导你完成整个流程。

---

## 文件结构

```
amazon-listing-creator/
├── SKILL.md                          # Skill 定义文件
├── AGENTS.md                         # AI 交互流程指南
├── amazon_compliance_blacklist.txt   # 违禁词黑名单
├── prompts/
│   └── generate_listing.md           # Listing 生成 Prompt
├── scripts/
│   └── gen_listing_excel.py          # Excel 生成脚本
└── README.md                         # 本文件
```

---

## 输入方式

### 方式一：SIF MCP 自动拆解（推荐）

| 输入 | 说明 |
|------|------|
| 品牌名称 | 用于 Item Name 开头 |
| 产品型号 | 用于 Excel 标题栏 |
| 产品名称 | 一句话描述 |
| 3-5 个竞品 ASIN | Agent 自动调用 SIF MCP 拆解 |

### 方式二：用户上传关键词列表

无 SIF MCP 对接时，用户上传关键词列表文件（xlsx/csv/txt），包含关键词、搜索量/流量占比等。

---

## 输出内容

| 模块 | 说明 |
|------|------|
| **Item Name** | 商品名称，A9 优化，≤75字符 |
| **Item Highlights** | 商品亮点，A9 优化，≤125字符 |
| **Bullet Points** | 五点描述，数据驱动，≤500字符/条 |
| **Search Terms** | 后台搜索词，≤250 bytes |
| **Validation Summary** | 13项合规校验 |
| **主图设计建议** | 7条视觉表达建议 |
| **合规排查报告** | 近6个月新规排查结果 |
| **流量权重优化报告** | 自然流量+链接权重优化逻辑 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0.0 | 2026-04-27 | 初始版本 |
| v1.1.0 | 2026-04-29 | 添加可选署名行、Excel格式框架 |
| v2.0.0 | 2026-04-29 | 强制合规声明 + 脚本校验 + 禁止AI自编代码 |
| **v3.0.0** | **2026-08-17** | **标题新规适配 + SIF MCP全自动拆解 + 关键词埋入主框架 + 认证信息默认不写 + 强制联网合规排查 + 自然流量权重最终审核** |
| **v3.1.0** | **2026-08-19** | **Excel 列名全局统一（模块/内容/场景-关键词/中文翻译/规格校验），删除空白行，脚本结构写死，validate_output 强化校验** |
| **v3.2.0** | **2026-08-20** | **关键词/场景词分列（C=关键词A9/A10, D=场景词COSMO/Alexa）+ 6列结构 + 新增Alexa算法 + 关键词列禁止AI联想 + 校验增加关键词非空检查** |
| **v3.2.1** | **2026-08-20** | **新增中英同步校验（标点/句式不一致报错）+ BP标点合规（无结尾.!?) + 中文翻译同步 + 校验增至11项** |
| **v3.3.0** | **2026-08-20** | **新增Description模块(三段HTML) + BP强制FBE结构(Benefit→Feature→Evidence) + 真实性质检(竞品事实移植检测) + 竞品文案结构拆解 + 校验增至13项/Validation16项** |

---

> 💡 **提示**：推荐使用 SIF MCP 自动拆解模式，只需输入品牌和竞品 ASIN 即可全自动生成。