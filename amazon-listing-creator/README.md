# Amazon Listing Creator 🌹

基于 A9 + COSMO + Rufus 三算法的亚马逊 Listing 智能生成工具。

---

## 功能特点

- ✅ 三算法全覆盖（A9 + COSMO + Rufus）
- ✅ 分阶段交互引导
- ✅ 合规黑名单自动校验
- ✅ 数据驱动，拒绝空洞描述
- ✅ 支持自定义扩展

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

> "帮我生成一个 [产品名称] 的亚马逊 Listing"

AI 会自动分阶段引导你完成整个流程。

---

## 文件结构

```
amazon-listing-creator/
├── SKILL.md                          # Skill 定义文件
├── AGENTS.md                         # AI 交互流程指南
├── amazon_compliance_blacklist.txt   # 违禁词黑名单
├── prompts/
│   └── generate_listing.md           # Listing 生成 Prompt
└── README.md                         # 本文件
```

---

## 输入文件

用户提供以下 4 份文件：

| 文件 | 作用 | 获取方式 |
|-----|------|---------|
| 本品属性表.txt | Rufus 事实源 | 1688/供应商产品参数 |
| 竞品意图分析.txt | COSMO 场景源 | 竞品 Listing + Review |
| ABA关键词数据.csv | A9 流量源 | 亚马逊后台/卖家精灵 |
| 竞品出单词报告.csv | 流量补充 | 反查竞品流量词 |

---

## 输出内容

| 模块 | 说明 |
|------|------|
| **Title** | A9 优化标题，含核心关键词 |
| **Bullet Points** | 五点描述，数据驱动 |
| **Product Description** | 产品描述，场景化呈现 |
| **Search Terms** | 后台搜索词，A9 算法优化 |

---

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| v2.0.0 | 三层防护机制（数据校验+格式保护+输出验证）、_en/_zh 数据字段分离 |
| v1.1.0 | 初始版本，三算法基础框架 |

---

> 💡 **提示**：首次使用建议先准备好上述 4 份输入文件，AI 会引导你一步步完成 Listing 生成。
