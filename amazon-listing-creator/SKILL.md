---
name: amazon-listing-creator
displayName: 亚马逊 Listing 智能生成器 (A9+COSMO+Rufus)
description: 基于 A9+COSMO+Rufus 三算法的亚马逊 Listing 生成工具，7步流程指导用户准备资料，生成高转化 Listing。支持分阶段对话，自动校验合规性。内置三层防护机制确保英文内容纯净。
version: 1.2.0
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

# 亚马逊 Listing 智能生成器

基于亚马逊 **A9 + COSMO + Rufus** 三算法优化的 Listing 生成工具。

## 核心能力

- 分阶段引导用户准备 4 个关键文件
- 生成符合 AEO (Answer Engine Optimization) 逻辑的 Listing
- 自动校验合规黑名单，避免违规词
- **三层防护机制**确保导出的英文 Listing 绝对纯净

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
- **Product Description** (产品描述) - AEO 就绪
- **Search Terms** (后台搜索词) - 无重复、无竞品品牌

## 数据字段命名规范（三层防护 - 第1层）

所有 Listing 数据必须严格遵循以下字段命名约定，从数据源头杜绝中英混用：

### 字段分离规则

```
TITLE_DATA = {
    "en": "...",       # ← 英文标题，纯英文
    "zh": "...",       # ← 中文翻译，纯中文
    "scene": "...",    # ← 场景词，永远纯英文
    "keywords": "...", # ← 关键词，永远纯英文
}
```

### 核心铁律

1. **`_en` 字段** = 纯英文（允许数字、标点），绝不允许出现中文字符
2. **`_zh` 字段** = 纯中文翻译，仅用于中文翻译列
3. **`scene` 字段** = 永远纯英文（如 "farmhouse kitchen, quality living"）
4. **`keywords` 字段** = 永远纯英文（如 "acacia wood, FDA certified"）
5. **Bullet Points** 同理：`title_en` / `content_en` / `scene` / `keywords` / `title_zh` / `content_zh`

### 数据结构示例（Bullet Points）

```python
BULLETS_DATA = [
    {
        "num": "1",
        "title_en": "Premium Acacia Wood Craftsmanship",  # 英文标题
        "title_zh": "优质相思木工艺",                        # 中文翻译
        "content_en": "Crafted from 100% natural...",       # 英文内容
        "content_zh": "采用100%天然相思木...",                # 中文翻译
        "scene": "quality living, farmhouse style",         # 永远英文
        "keywords": "acacia wood, FDA certified"            # 永远英文
    },
    ...
]
```

## 导出格式标准（Excel）

Listing 生成完成后，必须按以下标准格式导出为 `.xlsx` 文件。

### 文件命名规则

```
{Brand}_{Model}_{产品名}_Listing.xlsx
示例: Hanson_AMZ001_Utensil_Holder_Listing.xlsx
```

> **Brand** 和 **Model** 来自 Phase 3.1 本品属性表的首要确认项。

### Sheet 结构（单 Sheet: "Amazon Listing"）

#### 第1行：主标题行

```
Amazon Listing - {Model} {产品中文简称} / {产品英文名}
示例: Amazon Listing - AMZ001相思木餐具收纳架 / Acacia Wood Utensil Holder
```

> 合并 A1:E1，深蓝色底 (#2E75B6)，白色粗体 14pt

#### 第2行：出品信息行

```
{Brand}出品 | {品牌定位描述} / {联系邮箱}
示例: Hanson出品 | 亚马逊跨境选品/运营/Agent/Skill专家/hansonbtc@163.com
```

> 合并 A2:E2，灰色小字 (9pt, color #666666)，居中对齐

#### 模块 1: Title（5列）

| 列 | 字段名 | 说明 |
|---|--------|------|
| A | 模块 | 固定值 "Title" |
| B | 内容 | 完整英文标题文本（`TITLE_DATA["en"]`） |
| C | 场景词 | 标题覆盖的主要场景（`TITLE_DATA["scene"]`，永远英文） |
| D | 关键词埋入 | 标题中包含的核心关键词（`TITLE_DATA["keywords"]`，永远英文） |
| E | 中文翻译 | 标题中文译文（`TITLE_DATA["zh"]`） |

#### 模块 2: Bullet Points（5列）

| 列 | 字段名 | 说明 |
|---|--------|------|
| A | # | 序号 1-5 |
| B | Bullet Point | 完整英文五点描述（`title_en` + `content_en` 组装） |
| C | 场景词 | 该条描述覆盖的使用场景词（`scene`，永远英文） |
| D | 关键词埋入 | 该条埋入的关键词列表（`keywords`，永远英文） |
| E | 中文翻译 | 五点中文译文（`title_zh` + `content_zh` 组装） |

#### 模块 3: Search Terms（CDE 合并宽列格式）

**表头行**：
| 列 | 字段名 | 说明 |
|---|--------|------|
| A | 字段 | 固定值 "字段" |
| B | English (英文) | 固定值 "English (英文)" |
| C-E | 中文翻译 | **合并 C:E 列**，表头居中显示 |

> ⚠️ 中文翻译列合并 C:E 三列，加宽显示以避免内容截断。

**数据行**：
| 列 | 字段名 | 说明 |
|---|--------|------|
| A | Search Terms | 固定值 |
| B | 英文搜索词 | 空格分隔的搜索词串（`SEARCH_TERMS_DATA["en"]`） |
| C-E | 中文翻译 | **合并 C:E 列**（`SEARCH_TERMS_DATA["zh"]`） |

**备注行**（紧接数据行下方，合并 A:C）：
- 字节数统计（≤250 bytes）
- 已排除词（重复词、竞品品牌词、标点）
- 新增长尾词
- 排序说明（核心词前置）
- 合规检查结果

#### 模块 4: 校验汇总 Validation Summary（3列）

| 列 | 字段名 | 说明 |
|---|--------|------|
| A | 项目 | 校验项名称 |
| B | 要求 | 规则要求 |
| C | 状态 | 实际结果 + 通过/失败标记 |

**必检项目（11项）**：
- Title 字符数 ≤ 200
- Bullet 1-5 各 ≤ 500 字符（5项）
- Search Terms 字节 ≤ 250 bytes
- A9 合规（核心词前置，长尾覆盖）
- COSMO 合规（明确人群词 + 使用场景）
- Rufus 合规（所有卖点有数据支撑）
- 合规黑名单（无 best/premium/guaranteed/eco-friendly 等）

#### 模块 5: 主图设计建议（合并单元格 A:E）

从 Listing 提取的核心卖点 → 主图视觉表达建议，每条包含：
- 卖点名称
- 主图展示方式
- 特写/对比/场景图建议
- 主图+辅图组合建议（白底图、场景图、细节图、信息图、生活方式图）

### 样式规范

- **主标题行**: 合并 A1:E1，深蓝色底 (#2E75B6)，白色粗体 14pt，行高 30
- **出品信息行**: 合并 A2:E2，灰色小字 9pt (#666666)，居中，行高 18
- **模块标题**: 合并行，蓝色底 (#4472C4)，白色粗体 11pt，行高 20
- **表头行**: 浅蓝底 (#D9E2F3)，黑色粗体 10pt
- **所有单元格**: 细边框，自动换行 (wrap_text)
- **列宽参考**: A=16, B=58, C=22, D=30, E=45
- **行高**: Title=55, Bullet=85, Search Terms=60-65, 备注=80, 主图建议=280-380

## 三层防护机制（英文质量保障）

导出 Excel 时，通过三层防护确保英文 Listing 绝对纯净，不会出现中文字符混入：

```
┌─────────────────────────────────────────┐
│ 第 1 层：数据分离                        │
│   所有数据结构使用 _en / _zh 严格分离     │
│   scene / keywords 字段永远纯英文        │
│   从数据源头杜绝混用可能                  │
└─────────────────────────────────────────┘
                ↓ 校验通过 ↓
┌─────────────────────────────────────────┐
│ 第 2 层：校验检测                        │
│   导出前正则扫描所有英文字段              │
│   [\u4e00-\u9fff] 匹配中文字符          │
│   发现中文 → 立即报错中断 + 定位字段     │
└─────────────────────────────────────────┘
                ↓ 校验通过 ↓
┌─────────────────────────────────────────┐
│ 第 3 层：模板隔离                        │
│   英文列只读 _en 字段                    │
│   中文列只读 _zh 字段                    │
│   Excel 写入时严格字段对应               │
│   从结构上杜绝混用可能                   │
└─────────────────────────────────────────┘
```

### 第 2 层校验实现

导出脚本必须包含 `validate_english_only()` 函数：

```python
def validate_english_only(text, field_name):
    """校验文本是否为纯英文，发现中文立即报错"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    if chinese_pattern.search(text):
        raise ValueError(f"字段 '{field_name}' 包含中文，应为纯英文: {text[:100]}")
    return True
```

导出前批量校验所有英文字段（Title、Bullets、Search Terms），任一校验失败则**中断导出**。

## 质量标准

每个输出模块通过三重校验：

- ✅ **A9 合规**: 核心词在 Title 出现，五点覆盖长尾词
- ✅ **COSMO 合规**: 明确人群词 + 场景词
- ✅ **Rufus 合规**: 所有卖点有数据/事实支撑，无空洞形容词
- ✅ **合规黑名单**: 未出现违禁词
- ✅ **英文纯净**: 三层防护校验全部通过

## 使用方式

直接告诉我你的产品是什么，我会分阶段引导你完成整个流程。

**示例**:
> "帮我生成一个相思木餐具收纳架的亚马逊 Listing"

---

详细交互流程见 `AGENTS.md`，生成 Prompt 见 `prompts/generate_listing.md`。

## 导出工具依赖

- Python 3.x
- openpyxl 库 (`pip install openpyxl`)
- 导出脚本使用 `qclaw-text-file` skill 写入（自动处理 UTF-8 BOM 和换行符）
- Windows 环境下路径使用 raw string (`r"C:\path\to\file"`)
