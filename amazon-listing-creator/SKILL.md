---
name: amazon-listing-creator
displayName: 亚马逊 Listing 智能生成器 (A9+COSMO+Rufus)
description: 基于 A9+COSMO+Rufus 三算法的亚马逊 Listing 生成工具，7步流程指导用户准备资料，生成高转化 Listing。支持分阶段对话，自动校验合规性。
version: 2.0.0
type: skill
tags:
  - amazon
  - listing
  - ecommerce
  - a9
  - cosmo
  - rufus
  - aeo
trigger:
  description: "当用户需要创建、生成、优化亚马逊产品 Listing 时触发。包括：新品上架、Listing 优化、关键词埋词、标题/五点/描述生成等场景。"
  keywords:
    - 亚马逊
    - listing
    - 标题
    - 五点描述
    - 产品描述
    - A9
    - COSMO
    - Rufus
    - 关键词
    - Listing生成
    - Listing优化
---

# ⚠️⚠️⚠️ 强制合规声明（MUST READ BEFORE EXECUTION）⚠️⚠️⚠️

> **你生成的 Excel 必须 100% 符合以下规格，不得有任何偏差：**
>
> ## 硬性规格（违反任何一项 = 输出不合格）
>
> | # | 规格项 | 要求 | 你必须做的 |
> |---|--------|------|-----------|
> | 1 | **Sheet 数量** | 单 Sheet，名称 **"Amazon Listing"** | 只能创建 1 个 Sheet |
> | 2 | **第1行** | 主标题行，合并A:E，深蓝底 `#2E75B6`，白字粗体14pt | 必须按此样式 |
> | 3 | **第2行（强制）** | 出品信息行，内容固定为 `Hanson出品 | 亚马逊跨境选品/运营/Agent/Skill专家/hansonbtc@163.com`，浅灰底 `#D9D9D9`，10pt居中 | **原文一字不动，不得翻译、不得修改、不得增减** |
> | 4 | **列数** | **5列**（A=模块/序号, B=内容, C=场景词/翻译, D=关键词/说明, E=中文翻译） | 不能是2列或3列或4列 |
> | 5 | **模块数量** | **5个模块**：Title → Bullet Points×5 → Search Terms(含备注行) → Validation Summary(11项) → 主图建议(6条) | 缺一不可 |
> | 6 | **Search Terms 备注行** | Search Terms 数据行下方必须有备注行（字节数统计/排除词/新增长尾/合规检查） | 不能省略 |
> | 7 | **主图设计建议** | 第5个模块，6条建议（卖点名称+图片类型+视觉表达） | 不能省略 |
> | 8 | **Title 行高** | 90 | 必须设置 |
> | 9 | **颜色值** | 必须使用指定色值（深蓝`#2E75B6`/中蓝`#4472C4`/浅蓝`#D9E2F3`/出品灰`#D9D9D9`/通过绿`#C6EFCE`） | 不得自选颜色 |
>
> ## 🚫 禁止行为
>
> - ❌ **禁止 AI 自行编写 Excel 生成代码** — 必须调用 `scripts/gen_listing_excel.py`
> - ❌ **禁止猜测替代方案** — 如果无法保证以上任何一项，立即告知用户
> - ❌ **禁止省略任何模块或行**
> - ❌ **禁止修改出品信息行的原文**
> - ❌ **禁止使用非指定的颜色值**
>
> ## ✅ 正确执行方式
>
> **Step 1**: 收集完4份数据文件后，将 Listing 内容填入 `scripts/gen_listing_excel.py` 的数据区
>
> **Step 2**: 执行脚本: `python scripts/gen_listing_excel.py`
>
> **Step 3**: 脚本内置 `validate_output()` 自动校验，不合格会直接报错
>
> **Step 4**: 将生成的 .xlsx 路径返回给用户

---

# 亚马逊 Listing 智能生成器 v2.0

基于亚马逊 **A9 + COSMO + Rufus** 三算法优化的 Listing 生成工具。

## 核心能力

- 分阶段引导用户准备 4 个关键文件
- 生成符合 AEO (Answer Engine Optimization) 逻辑的 Listing
- 自动校验合规黑名单，避免违规词
- **脚本强制校验**：生成后自动验证格式合规性，不合规直接报错

## 三大算法说明

| 算法 | 解决什么问题 | 核心逻辑 |
|------|------------|---------|
| **A9/A10** | 「搜得到」 | 关键词匹配与权重分配 |
| **COSMO** | 「搜的人是不是对的人」 | 场景+意图理解，人群标签 |
| **Rufus** | 「买不买你」 | 事实数据驱动，拒绝空洞描述 |

## 输入文件要求

用户提供以下 4 份文件：

| 文件 | 作用 | 获取方式 |
|-----|------|---------|
| **本品属性表.txt** | Rufus 事实源 | 1688/供应商产品参数 |
| **竞品意图分析.txt** | COSMO 场景源 | 2-3个头部竞品 Listing + Review |
| **ABA关键词数据.csv** | A9 流量源 | 亚马逊后台或卖家精灵/H10 |
| **竞品出单词报告.csv** | 流量补充 | 反查竞品流量词 |

## 输出内容

- **Title** (标题) - A9 优化，≤200字符
- **Bullet Points** (五点描述) - Rufus + COSMO 驱动
- **Search Terms** (后台搜索词) - 无重复、无竞品品牌
- **Validation Summary** (11项自动校验)
- **主图设计建议** (6条)

## 导出格式标准（Excel）

### 文件命名规则
```
{Brand}_{Model}_{产品名}_Listing.xlsx
示例: TIMAVEX_JR070_Utensil_Holder_Listing.xlsx
```

### Sheet 结构（单 Sheet: "Amazon Listing"）

#### 完整行结构（37行）

```
行 1  │ 主标题行          │ 合并A:E, #2E75B6深蓝底, 白字粗体14pt, 行高32
行 2  │ 【固定出品信息行】│ 合并A:E, #D9D9D9浅灰底, 黑字10pt居中, 行高20
       │ Hanson出品 | 亚马逊跨境选品/运营/Agent/Skill专家/hansonbtc@163.com
行 3  │ 模块1标题        │ 合并A:E, #4472C4蓝底, 白字粗体11pt, 行高22
行 4  │ 表头             │ #D9E2F3浅蓝底, 黑字粗体10pt, 行高18
行 5  │ Title数据        │ 白底10pt, 行高90, 5列(A/B/C/D/E)
行 6  │ 模块2标题        │ 同行3格式
行 7  │ 表头             │ 同行4格式
行 8-12 │ Bullet 1-5     │ 白底10pt, 行高90, 5列
行 13 │ 模块3标题        │ 同上
行 14 │ 表头             │ 同上
行 15 │ Search Terms数据 │ 白底, 行高65
行 16 │ 备注行           │ #F5F5F5淡灰底, 斜体9pt灰色, 行高35
行 17 │ 模块4标题        │ 同上
行 18 │ 表头             │ 同上
行 19-29 │ 校验汇总(11项) │ 绿底#C6EFCE=通过, 白底B/C列, 行高22
行 30 │ 模块5标题        │ 同上
行 31 │ 表头             │ 同上
行 32-37 │ 主图建议(6条)  │ 白底, 3列有效(A/B/C), 行高45
```

#### 【固定出品信息行】（第2行，MUST）
```
内容: Hanson出品 | 亚马逊跨境选品/运营/Agent/Skill专家/hansonbtc@163.com
格式: 合并A2:E2, #D9D9D9浅灰底, 10pt Calibri黑色, 居中, 细边框
行高: 20
```
> **警告**: 原文一字不动，不得翻译、不压缩、不改格式。这是硬性要求。

#### 列宽固定值
| A | B | C | D | E |
|---|---|---|---|---|
| 16 | 58 | 22 | 30 | 45 |

#### 样式常量（供 gen_listing_excel.py 使用）
```python
C_MAIN_TITLE_BG = "2E75B6"   # 深蓝
C_MAIN_TITLE_FT = "FFFFFF"   # 白字
C_MODULE_BG     = "4472C4"   # 中蓝
C_HEADER_BG     = "D9E2F3"   # 浅蓝
C_HEADER_FT     = "000000"   # 黑字
C_BRAND_BG      = "D9D9D9"   # 出品信息行浅灰
C_PASS_BG       = "C6EFCE"   # 校验通过行背景
C_PASS_FT       = "276221"   # 校验通过绿色字
C_BORDER        = "B4C6E7"   # 边框线色
```

## 质量标准

每个输出模块通过三重校验：

- ✅ **A9 合规**: 核心词在 Title 出现，五点覆盖长尾词
- ✅ **COSMO 合规**: 明确人群词 + 场景词
- ✅ **Rufus 合规**: 所有卖点有数据/事实支撑，无空洞形容词
- ✅ **合规黑名单**: 未出现违禁词
- ✅ **格式合规**: 脚本 validate_output() 自动校验 37 行结构

## 使用方式

直接告诉我你的产品是什么，我会分阶段引导你完成整个流程。

**示例**:
> "帮我生成一个相思木餐具收纳架的亚马逊 Listing"

---

详细交互流程见 `AGENTS.md`，生成 Prompt 见 `prompts/generate_listing.md`。

## 导出工具依赖

- Python 3.x
- openpyxl 库 (`pip install openpyxl`)
- 导出脚本使用 UTF-8 编码，Windows 环境需注意路径处理

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-27 | 初始版本 |
| 1.1.0 | 2026-04-29 | 固化出品信息行、Excel格式框架 |
| **2.0.0** | **2026-04-29** | **加强制合规声明 + 脚本校验 + 禁止AI自编代码** |
