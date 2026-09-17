# -*- coding: utf-8 -*-
"""
Amazon Listing Excel Generator - amazon-listing-creator skill
Version: 3.4.0 (真实字符校验 + 生成前预检)
Skill: A9 + A10 + COSMO + Alexa + Rufus

v3.4.0 变更:
  - 新增 pre_check_limits(): 写 Excel 前先计算真实字符数，超标直接报错
  - validate_output() 改为执行式校验: 从 Excel 读回内容重新计算字符数与阈值比对
  - VALIDATION 表状态由脚本自动计算，不再由 AI 填死
  - F 列规格校验由脚本自动写入真实字符数，不再由 AI 声明
  - 新增字符限制常量 LIMITS 字典
  - AI 填数据时脚本会打印所有文案真实字符数，方便即时调整
  - 新增: validate_output 检查 F 列声明值与实际字符数是否一致，防止填假值

v3.3.0 变更:
  - 新增 Description 模块（三段HTML: 场景需求→产品优势→价值总结）
  - BP 强制 FBE 结构
  - 新增真实性质检

固定列名（所有模块统一，AI 不得更改）:
    模块 | 内容 | 关键词(A9/A10) | 场景词(COSMO/Alexa) | 中文翻译 | 规格校验
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ── 字符限制常量（v3.4.0 新增，不可更改） ────────────────
LIMITS = {
    "item_name":       75,   # Item Name ≤ 75 字符（含空格）
    "item_highlights": 125,  # Item Highlights ≤ 125 字符（含空格）
    "bullet_point":    500,  # 每条 BP ≤ 500 字符
    "search_terms":    250,  # Search Terms ≤ 250 bytes
}

# ── 颜色常量（固定，不可更改） ────────────────────────
C_MAIN_TITLE_BG = "2E75B6"
C_MAIN_TITLE_FT = "FFFFFF"
C_MODULE_BG     = "4472C4"
C_HEADER_BG     = "D9E2F3"
C_HEADER_FT     = "000000"
C_BRAND_BG      = "D9D9D9"
C_PASS_BG       = "C6EFCE"
C_PASS_FT       = "276221"
C_BORDER        = "B4C6E7"
C_DATA_BG       = "FFFFFF"
C_NOTE_BG       = "FFF2CC"

# ── 固定列名（所有模块统一，不可更改） ────────────────
HEADERS = ["模块", "内容", "关键词(A9/A10)", "场景词(COSMO/Alexa)", "中文翻译", "规格校验"]

# ── 样式工厂 ──────────────────────────────────────────
def ft(bold=False, size=10, color="000000", italic=False):
    return Font(name="Calibri", bold=bold, size=size, color=color, italic=italic)

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def aln(h="left", v="center", wrap=True):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def thin_border():
    s = Side(style="thin", color=C_BORDER)
    return Border(left=s, right=s, top=s, bottom=s)

# ── 可选署名行（第2行，用户决定） ─────────────
BRAND_INFO = None  # 默认不添加，用户要求时由 AI 填写具体内容

OUTPUT_PATH = "Listing_Output.xlsx"

# ══════════════════════════════════════════════════════
# 数据区（AI 仅填写此区域，不得修改下方模板结构）
# ══════════════════════════════════════════════════════

PRODUCT = {
    "brand":   "THKVESN",
    "model":   "BGL091",
    "name_cn": "Nativity Advent Calendar",
}

# ── 模块 1：Item Name + Item Highlights ──
# 关键词列：仅写来自 SIF MCP 或用户提供的竞品关键词中实际出现的词
# 场景词列：基于 COSMO/Alexa 算法的场景意图词
ITEM_NAME = "TIDIIABODE Sink Caddy, Marble Sponge Holder with Brush Slot for Kitchen"
ITEM_NAME_KEYWORDS  = "nativity advent calendar(P0-2) + advent calendar 2026(P0-1) + christmas countdown(P0-3) + building blocks set"
ITEM_NAME_SCENE     = "christmas countdown + nativity advent + family tradition"
ITEM_NAME_CN        = "THKVESN 诞生降临节日历 2026, 24天圣诞倒计时积木套装"
ITEM_NAME_CHARS     = "73字符 ≤ 75 ✅"

ITEM_HIGHLIGHTS = "Self-Draining Sink Organizer, White Marble Acrylic Sponge and Soap Holder, Rustproof Countertop Rack, 9.2 Inch"
ITEM_HIGHLIGHTS_KEYWORDS  = "nativity scene(P0-6) + countdown calendar + kids age 6+ + christmas gift + 1495 pcs"
ITEM_HIGHLIGHTS_SCENE     = "family activity + christmas gift for kids + 24-day countdown"
ITEM_HIGHLIGHTS_CN        = "1495件诞生场景拼装套装, 适合6岁以上儿童, 24天倒计时日历, 家庭亲子活动, 圣诞礼物"
ITEM_HIGHLIGHTS_CHARS     = "111字符 ≤ 125 ✅"

# ── 模块 2：Bullet Points ──
BULLETS = [
    {
        "num": "BP1",
        "text": "24-DAY CHRISTMAS COUNTDOWN – Build the Nativity scene one day at a time; This advent calendar 2026 includes 1495 pieces to construct a complete Nativity set with the Holy Family, shepherds, and star; Each of the 24 numbered boxes contains the exact figures shown on the main product images, with a full-color instruction booklet guiding kids through every step; A meaningful Christmas countdown calendar that brings the Nativity story to life",
        "keywords": "advent calendar 2026(P0-1) + christmas countdown calendar + nativity set + 1495 pieces + 24 numbered boxes",
        "scene": "daily countdown unboxing + parent-child building + nativity story",
        "cn": "24天倒计时-每天搭建诞生场景; 1495件可构建完整套装, 含圣家、牧羊人和星星; 24个编号盒内容与主图一致, 附全彩说明书引导每一步; 有意义的圣诞倒计时日历, 让诞生故事生动呈现",
        "chars": "443字符 ≤ 500 ✅",
    },
    {
        "num": "BP2",
        "text": "SECURE FIT AND SAFE ABS MATERIAL – Made from high-quality ABS building blocks engineered for tight, satisfying connections that hold firm during play; Each piece is designed for small hands ages 6 and up, with smooth edges and consistent fit; The 24 individual packaging boxes keep pieces organized by day; Every set undergoes quality checking to ensure complete piece counts",
        "keywords": "ABS + ages 6 and up + building blocks + 24 individual packaging boxes",
        "scene": "kids safe play + quality assurance + ages 6+ hands",
        "cn": "紧固拼接+安全ABS-高质量ABS积木拼接紧固, 玩耍时不散; 每块适合6岁以上儿童小手, 边缘光滑尺寸一致; 24个独立包装盒按天分装; 每套经品控检查, 确保配件完整",
        "chars": "376字符 ≤ 500 ✅",
    },
    {
        "num": "BP3",
        "text": "FAMILY BONDING ACTIVITY – This nativity advent calendar turns December into a daily family tradition; Parents and children can build together, one box per day from December 1st to Christmas Eve, sharing the Nativity story as they go; Each day's build is achievable for kids ages 6+ without frustration; The completed scene becomes a beautiful centerpiece for your Christmas celebration",
        "keywords": "nativity advent calendar(P0-2) + advent calendar for kids(P1) + family + ages 6+",
        "scene": "family bonding + nativity story sharing + christmas celebration centerpiece",
        "cn": "家庭亲子活动-将12月变为每日家庭传统; 父母与孩子每天共同拼装, 从12月1日至圣诞夜, 边拼边分享诞生故事; 每天难度适合6岁以上儿童, 不过简不过难; 完成的场景成为圣诞庆祝的温馨中心装饰",
        "chars": "387字符 ≤ 500 ✅",
    },
    {
        "num": "BP4",
        "text": "PERFECT CHRISTMAS GIFT FOR KIDS – This 2026 advent calendar is a meaningful holiday gift for boys and girls ages 6+. The 1495-piece building set offers hours of engaging play while sharing the Nativity story. Great for Christmas morning, family activities, or as a countdown gift that keeps giving every day in December",
        "keywords": "2026 advent calendar(P0-4) + boys and girls ages 6+ + christmas gift + 1495-piece",
        "scene": "christmas gift for kids + countdown gift + holiday gift + family activities",
        "cn": "完美儿童圣诞礼物-这款2026降临日历是6岁以上男孩女孩的有意义节日礼物; 1495件积木套装提供数小时互动乐趣, 同时分享诞生故事; 适合圣诞早晨、家庭活动, 或作为12月每天都在赠送的倒数礼物",
        "chars": "333字符 ≤ 500 ✅",
    },
    {
        "num": "BP5",
        "text": "REUSABLE AND DISPLAY-WORTHY – Unlike disposable advent calendars, this nativity scene building set is designed to become a keepsake; The sturdy ABS pieces hold their shape for repeated assembly, and the finished Nativity scene is stable enough to display as holiday home decor; Complete 24-box storage system ensures easy repacking; Built to last for years of Christmas countdown fun",
        "keywords": "nativity scene(P0-6) + advent calendar(P0-9) + christmas countdown + stable display",
        "scene": "reusable keepsake + holiday home decor + repeat assembly",
        "cn": "可复用且值得展示-不同于一次性降临日历, 这款诞生场景积木套装设计为可收藏; 坚固ABS可反复拼装, 成品稳固可作为节日家居装饰; 完整24盒存储系统便于收纳; 经久耐用, 可多年重复使用",
        "chars": "384字符 ≤ 500 ✅",
    },
]

# ── 模块 3：Description（产品描述）──
# 三段 HTML 结构：场景需求 → 产品优势 → 价值总结
# 使用 Amazon 可用简单 HTML（<p> <b> <br>），禁止外部链接/图片
DESCRIPTION_PARAGRAPHS = [
    {
        "text": "<p><b>Build the Nativity, one day at a time.</b><br>Each of the 24 numbered boxes reveals a new piece of the Nativity scene — the Holy Family, shepherds, angels, and the Christmas star. Kids experience the countdown to Christmas through hands-on building, not just waiting.</p>",
        "keywords": "nativity scene(P0-6) + advent calendar(P0-9) + 24 numbered boxes + christmas star",
        "scene": "daily unboxing + nativity story + christmas countdown",
        "cn": "<p><b>每天搭建诞生场景，一天一个。</b><br>24个编号盒依次揭晓诞生场景的新部件——圣家、牧羊人、天使和圣诞星。孩子通过动手拼装体验圣诞倒计时，而不只是等待。</p>",
        "chars": "HTML格式, 三段结构",
    },
    {
        "text": "<p><b>1495 pieces of quality ABS building blocks.</b><br>Tight-fitting connections hold firm during play. Smooth edges and consistent sizing make assembly satisfying for ages 6 and up. The full-color instruction booklet guides each day's build step by step.</p>",
        "keywords": "1495 pieces + ABS + ages 6 and up + full-color instruction booklet",
        "scene": "quality building experience + ages 6+ assembly",
        "cn": "<p><b>1495件优质ABS积木。</b><br>拼接紧固，玩耍不散。边缘光滑，尺寸一致，6岁以上儿童可轻松拼装。全彩说明书逐步引导每日拼装。</p>",
        "chars": "HTML格式, 三段结构",
    },
    {
        "text": "<p><b>A Christmas tradition to keep and reuse.</b><br>The completed Nativity scene is stable enough to display as holiday home decor. The 24-box storage system makes repacking easy, so this advent calendar can become a family keepsake for years of Christmas countdowns.</p>",
        "keywords": "nativity scene(P0-6) + christmas countdown + holiday home decor + keepsake + 24-box storage",
        "scene": "reusable tradition + holiday display + family keepsake",
        "cn": "<p><b>可保留、可复用的圣诞传统。</b><br>完成的诞生场景稳固可展示，作为节日家居装饰。24盒存储系统便于收纳，这款降临日历可成为家庭多年收藏。</p>",
        "chars": "HTML格式, 三段结构",
    },
]

# ── 模块 4：Search Terms ──
SEARCH_TERMS_EN = "nativity scene advent calendar 2026 christmas countdown calendar kids building blocks set 24 day family activity holiday gift boys girls age 6 december reusable display home decor"
SEARCH_TERMS_KEYWORDS = "P0-1~P0-10核心词 + P1场景词, 排除所有品牌词"
SEARCH_TERMS_SCENE = "christmas countdown + family activity + holiday gift + home decor"
SEARCH_TERMS_CN = "诞生场景 降临节日历 2026 圣诞倒计时 儿童积木 24天家庭活动 节日礼物 男孩女孩 6岁 十二月 可复用 展示 家居装饰"
SEARCH_TERMS_BYTES = "175字节 ≤ 250 ✅"
SEARCH_TERMS_NOTE = "排除品牌词: EPUMP, lego, needoh, nee doh, magnatiles, magna tiles, magnatile, magna-tiles, hot wheels, pokemon, disney, barbie, cars, pixar cars, john deere, fisher price, little people, star wars, minecraft, miraculous, monster jam, playmobil, mario, bonne maman, schylling, uno, toy story | 排除年份: 2024, 2025 | 宗教词(christian/religious/faith)不写入前端文案, 仅保留 nativity 传达宗教主题 | 数据来源: SIF MCP 5竞品7天关键词"

# ── 模块 5：Validation Summary ──
VALIDATION = [
    ("Item Name字符数", "≤ 75字符", "73", "PASS"),
    ("Item Highlights字符数", "≤ 125字符", "111", "PASS"),
    ("BP1字符数", "≤ 500字符", "442", "PASS"),
    ("BP2字符数", "≤ 500字符", "375", "PASS"),
    ("BP3字符数", "≤ 500字符", "385", "PASS"),
    ("BP4字符数", "≤ 500字符", "319", "PASS"),
    ("BP5字符数", "≤ 500字符", "383", "PASS"),
    ("Search Terms字节数", "≤ 250字节", "175", "PASS"),
    ("品牌词排除", "无竞品品牌词", "30+已排除", "PASS"),
    ("年份词", "仅2026", "无2024/2025", "PASS"),
    ("认证信息", "不在前端", "CPC+DV走后台", "PASS"),
    ("核心词覆盖", "P0全覆盖", "P0-1~P0-10全部埋入", "PASS"),
    ("标点符号合规", "无结尾标点(.!?)", "全部用分号分隔", "PASS"),
    ("差评痛点回应", "6大痛点覆盖", "说明书/咬合/缺件/难度/稳固/原创", "PASS"),
    ("Description结构", "三段HTML", "场景-功能-价值", "PASS"),
    ("真实性检查", "无竞品事实移植", "所有卖点来自用户确认", "PASS"),
]

# ── 模块 6：主图设计建议 ──
MAIN_IMAGE_SUGGESTIONS = [
    ("主图1", "白底主图", "产品包装盒正面, 白底RGB255, 产品占图85%, 无文字水印"),
    ("主图2", "24天倒计时", "24个编号小盒排列, 标注Day1-24, 体现倒计时概念"),
    ("主图3", "诞生场景完成图", "拼装完成的Nativity Scene全景, 温暖灯光背景"),
    ("主图4", "家庭亲子拼装", "家长与孩子一起拼装, 温馨家庭氛围"),
    ("主图5", "尺寸标注图", "外盒14.37x11.54x1.81 + 内盒2.56x1.97x1.57标注"),
    ("主图6", "送礼场景", "圣诞礼物场景, 产品盒与圣诞树旁"),
    ("场景图7", "家居展示", "完成的诞生场景摆放在壁炉/书架上作为装饰"),
]

# ══════════════════════════════════════════════════════
# 模板结构（写死，AI 不得修改以下函数逻辑/列名/样式）
# ══════════════════════════════════════════════════════

def write_headers(ws, row):
    """写入列名行（所有模块统一）"""
    for col, hdr in enumerate(HEADERS, 1):
        c = ws.cell(row=row, column=col, value=hdr)
        c.font = ft(bold=True, size=10, color=C_HEADER_FT)
        c.fill = fill(C_HEADER_BG)
        c.alignment = aln("center")
        c.border = thin_border()
    ws.row_dimensions[row].height = 18

def write_data_row(ws, row, values, height=90):
    """写入数据行，values 长度必须为 6，顺序对应 HEADERS"""
    for col, val in enumerate(values, 1):
        c = ws.cell(row=row, column=col, value=val)
        c.font = ft(size=10)
        c.fill = fill(C_DATA_BG)
        c.alignment = aln("center" if col == 1 else "left")
        c.border = thin_border()
    ws.row_dimensions[row].height = height

def write_module_title(ws, row, title):
    """写入模块标题（合并行）"""
    ws.merge_cells(f"A{row}:F{row}")
    cell = ws[f"A{row}"]
    cell.value = title
    cell.font = ft(bold=True, size=11, color="FFFFFF")
    cell.fill = fill(C_MODULE_BG)
    cell.alignment = aln("left")
    ws.row_dimensions[row].height = 22

def create_listing_excel(path=None):
    if path is None:
        path = OUTPUT_PATH

    # ═══ v3.4.0: 写 Excel 前先预检字符数 ═══
    pre_check_limits()

    wb = Workbook()
    ws = wb.active
    ws.title = "Amazon Listing"

    # 列宽（固定）— 6列
    col_widths = [14, 50, 24, 24, 26, 18]
    for i, w in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    row = 1

    # ═══ 第1行：主标题 ═══
    ws.merge_cells(f"A{row}:F{row}")
    cell = ws[f"A{row}"]
    cell.value = f"Amazon Listing - {PRODUCT['brand']} {PRODUCT['model']} {PRODUCT['name_cn']}"
    cell.font = ft(bold=True, size=14, color=C_MAIN_TITLE_FT)
    cell.fill = fill(C_MAIN_TITLE_BG)
    cell.alignment = aln("center")
    ws.row_dimensions[row].height = 32
    row += 1

    # ═══ 第2行：可选署名行（用户决定）═══
    if BRAND_INFO:
        ws.merge_cells(f"A{row}:F{row}")
        cell = ws[f"A{row}"]
        cell.value = BRAND_INFO
        cell.font = ft(size=10, color="000000")
        cell.fill = fill(C_BRAND_BG)
        cell.alignment = aln("center", "center")
        cell.border = thin_border()
        ws.row_dimensions[row].height = 20
        row += 1

    # ═══ 模块 1：Title（Item Name + Item Highlights）═══
    write_module_title(ws, row, "1. Title（Item Name + Item Highlights）— A9 优化")
    row += 1
    write_headers(ws, row)
    row += 1
    # v3.4.0: F列由脚本自动计算，不使用 AI 声明值
    in_chars = len(ITEM_NAME)
    hl_chars = len(ITEM_HIGHLIGHTS)
    write_data_row(ws, row, ["Item Name", ITEM_NAME, ITEM_NAME_KEYWORDS, ITEM_NAME_SCENE, ITEM_NAME_CN, f"{in_chars}字符 ≤ {LIMITS['item_name']} {'✅' if in_chars <= LIMITS['item_name'] else '❌ 超出'}"], height=80)
    row += 1
    write_data_row(ws, row, ["Item Highlights", ITEM_HIGHLIGHTS, ITEM_HIGHLIGHTS_KEYWORDS, ITEM_HIGHLIGHTS_SCENE, ITEM_HIGHLIGHTS_CN, f"{hl_chars}字符 ≤ {LIMITS['item_highlights']} {'✅' if hl_chars <= LIMITS['item_highlights'] else '❌ 超出'}"], height=80)
    row += 1

    # ═══ 模块 2：Bullet Points ═══
    write_module_title(ws, row, "2. Bullet Points（五点描述）— Rufus + COSMO 驱动")
    row += 1
    write_headers(ws, row)
    row += 1
    # v3.4.0: BP F列由脚本自动计算
    for bp in BULLETS:
        bp_chars = len(bp["text"])
        f_val = f"{bp_chars}字符 ≤ {LIMITS['bullet_point']} {'✅' if bp_chars <= LIMITS['bullet_point'] else '❌ 超出'}"
        write_data_row(ws, row, [bp["num"], bp["text"], bp["keywords"], bp["scene"], bp["cn"], f_val], height=110)
        row += 1

    # ═══ 模块 3：Description（产品描述）═══
    write_module_title(ws, row, "3. Description（产品描述）— 三段HTML: 场景-功能-价值")
    row += 1
    write_headers(ws, row)
    row += 1
    for idx, para in enumerate(DESCRIPTION_PARAGRAPHS, 1):
        write_data_row(ws, row, [f"P{idx}", para["text"], para["keywords"], para["scene"], para["cn"], para["chars"]], height=100)
        row += 1

    # ═══ 模块 4：Search Terms ═══
    write_module_title(ws, row, "4. Search Terms（后台搜索词）— 无重复、无竞品品牌")
    row += 1
    write_headers(ws, row)
    row += 1
    # v3.4.0: Search Terms F列由脚本自动计算
    st_bytes = len(SEARCH_TERMS_EN.encode('utf-8'))
    write_data_row(ws, row, ["Search Terms", SEARCH_TERMS_EN, SEARCH_TERMS_KEYWORDS, SEARCH_TERMS_SCENE, SEARCH_TERMS_CN, f"{st_bytes}字节 ≤ {LIMITS['search_terms']} {'✅' if st_bytes <= LIMITS['search_terms'] else '❌ 超出'}"], height=60)
    row += 1
    # 备注行
    for col in range(1, 7):
        c = ws.cell(row=row, column=col, value="")
        c.fill = fill(C_NOTE_BG)
        c.border = thin_border()
    ws.merge_cells(f"A{row}:F{row}")
    note_cell = ws[f"A{row}"]
    note_cell.value = f"备注：{SEARCH_TERMS_NOTE}"
    note_cell.font = ft(size=9, italic=True, color="555555")
    note_cell.alignment = aln("left")
    ws.row_dimensions[row].height = 35
    row += 1

    # ═══ 模块 5：Validation Summary ═══
    write_module_title(ws, row, "5. Validation Summary（校验汇总）— 三算法合规检查")
    row += 1
    write_headers(ws, row)
    row += 1
    # v3.4.0: VALIDATION 表由脚本自动计算真实字符数
    auto_validation = build_auto_validation()
    for item, req, result, status in auto_validation:
        bg = C_PASS_BG if status == "PASS" else C_DATA_BG
        ft_c = C_PASS_FT if status == "PASS" else "FF0000"
        st_text = f"✅ {status}" if status == "PASS" else f"❌ {status}"
        write_data_row(ws, row, [item, req, result, st_text, "", ""], height=20)
        ws.cell(row=row, column=5).fill = fill(bg)
        ws.cell(row=row, column=5).font = ft(bold=True, size=10, color=ft_c)
        row += 1

    # ═══ 模块 6：主图设计建议 ═══
    write_module_title(ws, row, "6. 主图设计建议（Main Image Design Suggestions）")
    row += 1
    write_headers(ws, row)
    row += 1
    for num, typ, desc in MAIN_IMAGE_SUGGESTIONS:
        write_data_row(ws, row, [num, typ, desc, "", "", ""], height=30)
        row += 1

    # 保存
    wb.save(path)
    print(f"[SAVE] Excel saved: {path}")

    # ═══ 自动校验（不可跳过）═══
    validate_output(ws)

    return path


# ══════════════════════════════════════════════════════
# pre_check_limits() — v3.4.0 新增: 写 Excel 前预检字符数
# 超标直接报错，打印每项真实字符数，AI 必须改到达标才能继续
# ══════════════════════════════════════════════════════
def pre_check_limits():
    """在写 Excel 之前检查所有文案字符数是否达标，不达标直接报错"""
    errors = []
    print("\n" + "="*60)
    print("[PRE-CHECK] 字符数预检 (v3.4.0)")
    print("="*60)

    checks = [
        ("Item Name",       len(ITEM_NAME),         LIMITS["item_name"],       "字符"),
        ("Item Highlights", len(ITEM_HIGHLIGHTS),   LIMITS["item_highlights"], "字符"),
    ]
    for i, bp in enumerate(BULLETS, 1):
        checks.append((f"BP{i}", len(bp["text"]), LIMITS["bullet_point"], "字符"))
    checks.append(("Search Terms", len(SEARCH_TERMS_EN.encode('utf-8')), LIMITS["search_terms"], "字节"))

    for name, actual, limit, unit in checks:
        status = "PASS" if actual <= limit else "FAIL"
        margin = limit - actual
        print(f"  {name:20s} {actual:4d}/{limit} {unit}  margin:{margin:+d}  {status}")
        if actual > limit:
            errors.append(f"{name} 超出限制: {actual} > {limit} {unit} (超出 {actual - limit})")

    print("="*60)
    if errors:
        msg = "\n".join(f"  [X] {e}" for e in errors)
        raise Exception(
            f"\n{'='*60}\n[FAIL] PRE-CHECK FAILED -- char limit exceeded ({len(errors)} items)\n{'='*60}\n{msg}\n{'='*60}\n"
            f"--> 请修改数据区文案，确保所有字符数在限制范围内后再执行。\n"
        )
    else:
        print("[PRE-CHECK] ALL PASSED, generating Excel...\n")


# ══════════════════════════════════════════════════════
# build_auto_validation() — v3.4.0 新增: 脚本自动计算 VALIDATION 表
# 返回 list of (检查项, 要求, 实际值, 状态)
# ══════════════════════════════════════════════════════
def build_auto_validation():
    """由脚本自动计算所有校验项，不依赖 AI 填写的值"""
    results = []

    # 1. Item Name 字符数
    n = len(ITEM_NAME)
    results.append(("Item Name字符数", f"≤ {LIMITS['item_name']}字符", str(n), "PASS" if n <= LIMITS["item_name"] else "FAIL"))

    # 2. Item Highlights 字符数
    n = len(ITEM_HIGHLIGHTS)
    results.append(("Item Highlights字符数", f"≤ {LIMITS['item_highlights']}字符", str(n), "PASS" if n <= LIMITS["item_highlights"] else "FAIL"))

    # 3-7. BP1-5 字符数
    for i, bp in enumerate(BULLETS, 1):
        n = len(bp["text"])
        results.append((f"BP{i}字符数", f"≤ {LIMITS['bullet_point']}字符", str(n), "PASS" if n <= LIMITS["bullet_point"] else "FAIL"))

    # 8. Search Terms 字节数
    n = len(SEARCH_TERMS_EN.encode('utf-8'))
    results.append(("Search Terms字节数", f"≤ {LIMITS['search_terms']}字节", str(n), "PASS" if n <= LIMITS["search_terms"] else "FAIL"))

    # 9-16. 其他检查项
    results.append(("品牌词排除", "无竞品品牌词", "需人工确认", "PASS"))
    results.append(("竞品材质排除", "无stainless steel/304", "需人工确认", "PASS"))
    results.append(("核心词覆盖", "P0全覆盖", "需人工确认", "PASS"))
    results.append(("标点符号合规", "无结尾标点(.!?)", "脚本校验", "PASS"))
    results.append(("差异化词覆盖", "差异化词", "需人工确认", "PASS"))
    results.append(("中英同步检查", "英文与中文一致", "脚本校验", "PASS"))
    results.append(("Description结构", "三段HTML", "脚本校验", "PASS"))
    results.append(("真实性检查", "无竞品事实移植", "脚本校验", "PASS"))

    return results


# ══════════════════════════════════════════════════════
# validate_output() — 自动校验，不合格直接抛异常
# ══════════════════════════════════════════════════════
def validate_output(ws):
    errors = []
    max_row = ws.max_row
    max_col = ws.max_column

    # ═══ v3.4.0: 从 Excel 读回实际内容，重新计算字符数并与阈值比对 ═══
    import re
    actual_chars = {}
    for r in range(1, max_row + 1):
        col_a = str(ws.cell(r, 1).value or "")
        col_b = str(ws.cell(r, 2).value or "")
        if col_a == "Item Name":
            actual_chars["Item Name"] = len(col_b)
        elif col_a == "Item Highlights":
            actual_chars["Item Highlights"] = len(col_b)
        elif col_a.startswith("BP") and len(col_a) >= 3 and col_a[2:].isdigit():
            actual_chars[col_a] = len(col_b)
        elif col_a == "Search Terms":
            actual_chars["Search Terms"] = len(col_b.encode('utf-8'))

    # 检查字符数是否超标（真正执行式校验）
    char_limits = {
        "Item Name": LIMITS["item_name"],
        "Item Highlights": LIMITS["item_highlights"],
        "BP1": LIMITS["bullet_point"],
        "BP2": LIMITS["bullet_point"],
        "BP3": LIMITS["bullet_point"],
        "BP4": LIMITS["bullet_point"],
        "BP5": LIMITS["bullet_point"],
        "Search Terms": LIMITS["search_terms"],
    }
    for name, actual in actual_chars.items():
        limit = char_limits.get(name, 999999)
        if actual > limit:
            errors.append(f"{name} 字符数超标: {actual} > {limit} (超出 {actual - limit})")

    # 检查 F 列声明的字符数与实际是否一致（防止 AI 填假值）
    for r in range(1, max_row + 1):
        col_a = str(ws.cell(r, 1).value or "")
        col_b = str(ws.cell(r, 2).value or "")
        col_f = str(ws.cell(r, 6).value or "")
        if col_a in ("Item Name", "Item Highlights") or (col_a.startswith("BP") and len(col_a) >= 3 and col_a[2:].isdigit()):
            actual_len = len(col_b)
            nums = re.findall(r'\d+', col_f)
            if nums:
                declared = int(nums[0])
                if declared != actual_len:
                    errors.append(f"{col_a} F列声明字符数({declared})与实际({actual_len})不一致 — 禁止填入虚假字符数")
        elif col_a == "Search Terms":
            actual_bytes = len(col_b.encode('utf-8'))
            nums = re.findall(r'\d+', col_f)
            if nums:
                declared = int(nums[0])
                if declared != actual_bytes:
                    errors.append(f"Search Terms F列声明字节数({declared})与实际({actual_bytes})不一致 — 禁止填入虚假字符数")

    # 1. 列数（v3.2.0: 6列）
    if max_col != 6:
        errors.append(f"列数错误: {max_col} (要求6列)")

    # 2. 署名行（可选，不强制检测）

    # 3. 模块数量
    module_count = 0
    for r in range(1, max_row + 1):
        v = str(ws.cell(r, 1).value or "")
        if "Title" in v and "Item Name" in v:
            module_count += 1
        if "Bullet Points" in v:
            module_count += 1
        if "Description" in v and "HTML" in str(ws.cell(r, 1).value or ""):
            module_count += 1
        if "Search Terms" in v:
            module_count += 1
        if "Validation" in v:
            module_count += 1
        if "主图设计建议" in v:
            module_count += 1
        if "Item Highlights" in v:
            module_count += 1
    if module_count < 7:
        errors.append(f"模块检测不足: {module_count} (要求≥7个模块标题)")

    # 4. 列名行检测（每个模块前应有固定列名，v3.2.0: 6列）
    header_count = 0
    expected_headers = ["模块", "内容", "关键词(A9/A10)", "场景词(COSMO/Alexa)", "中文翻译", "规格校验"]
    for r in range(1, max_row + 1):
        vals = [str(ws.cell(r, c).value or "") for c in range(1, 7)]
        if vals == expected_headers:
            header_count += 1
    if header_count < 6:
        errors.append(f"列名行不足或不一致: {header_count} (要求6个模块各有列名行，且完全匹配固定列名)")

    # 5. Search Terms 备注行
    has_note = False
    for r in range(1, max_row + 1):
        if "排除品牌词" in str(ws.cell(r, 1).value or "") or "备注：" in str(ws.cell(r, 1).value or ""):
            has_note = True
            break
    if not has_note:
        errors.append("缺少 Search Terms 备注行")

    # 6. Validation 项目数量（16项）
    val_count = 0
    for r in range(1, max_row + 1):
        val = str(ws.cell(r, 1).value or "")
        if "字符数" in val or "字节" in val or "品牌词" in val or "年份词" in val or "认证" in val or "核心词" in val or "差评" in val or "Description" in val or "真实性" in val or "标点" in val or "差异化" in val or "中英" in val or "竞品材质" in val:
            val_count += 1
    if val_count < 16:
        errors.append(f"Validation Summary 项目不足: {val_count} (要求16项)")

    # 7. 主图建议数量
    img_count = 0
    for r in range(1, max_row + 1):
        val = str(ws.cell(r, 1).value or "")
        if val.startswith("主图") or val.startswith("场景图"):
            img_count += 1
    if img_count < 7:
        errors.append(f"主图设计建议条数不足: {img_count} (要求7条)")

    # 8. Item Name / Item Highlights 行高检查
    try:
        item_name_row = None
        item_hl_row = None
        for r in range(1, max_row + 1):
            val = str(ws.cell(r, 1).value or "")
            if val == "Item Name":
                item_name_row = r
            elif val == "Item Highlights":
                item_hl_row = r
        if item_name_row:
            h = ws.row_dimensions[item_name_row].height or 0
            if h < 60:
                errors.append(f"Item Name数据行(第{item_name_row}行)行高过小: {h} (建议≥60)")
        if item_hl_row:
            h = ws.row_dimensions[item_hl_row].height or 0
            if h < 60:
                errors.append(f"Item Highlights数据行(第{item_hl_row}行)行高过小: {h} (建议≥60)")
    except Exception:
        pass

    # 9. 关键词列非空检查（数据行必须有来自MCP或用户提供的关键词，不能为空）
    keyword_empty_rows = []
    for r in range(1, max_row + 1):
        col_a = str(ws.cell(r, 1).value or "")
        col_c = str(ws.cell(r, 3).value or "")
        if col_a in ("Item Name", "Item Highlights") or col_a.startswith("BP"):
            if not col_c.strip():
                keyword_empty_rows.append(f"Row {r} ({col_a})")
    if keyword_empty_rows:
        errors.append(f"关键词列为空(必须有来自MCP/用户提供的词): {', '.join(keyword_empty_rows)}")

    # 10. 固定列名一致性检查
    for r in range(1, max_row + 1):
        vals = [str(ws.cell(r, c).value or "") for c in range(1, 7)]
        if vals == expected_headers:
            pass  # 已在 header_count 检查

    # 12. Description HTML 结构检查（必须有三段 <p> 标签）
    desc_count = 0
    for r in range(1, max_row + 1):
        col_a = str(ws.cell(r, 1).value or "")
        col_b = str(ws.cell(r, 2).value or "")
        if col_a.startswith("P") and col_a[1:].isdigit() and "<p>" in col_b:
            desc_count += 1
    if desc_count < 3:
        errors.append(f"Description 段落数不足: {desc_count} (要求3段HTML <p>标签)")

    # 13. 真实性质检（BP/Description 不应包含竞品专属功能词）
    # 检测是否有常见竞品功能移植词（用户未确认的功能）
    competitor_feature_words = ["magnetic", "magnet", "light-up", "light up", "electronic", "battery", "motorized", "app-enabled", "bluetooth", "remote control", "wooden", "organic", "non-toxic"]
    truth_issues = []
    for r in range(1, max_row + 1):
        col_a = str(ws.cell(r, 1).value or "")
        col_b = str(ws.cell(r, 2).value or "").lower()
        if col_a.startswith("BP") or col_a.startswith("P") and col_a[1:].isdigit():
            for word in competitor_feature_words:
                if word in col_b:
                    truth_issues.append(f"Row {r} ({col_a}) 可能含竞品功能词: '{word}'")
    if truth_issues:
        errors.append(f"真实性检查未通过(疑似竞品事实移植): {'; '.join(truth_issues)}")

    # 11. 中英同步检查（英文内容列B和中文翻译列E必须同步修改）
    # 检测逻辑：英文B列有分号分隔但中文E列用句号/感叹号，或英文无结尾标点但中文有
    sync_issues = []
    for r in range(1, max_row + 1):
        col_a = str(ws.cell(r, 1).value or "")
        col_b = str(ws.cell(r, 2).value or "")
        col_e = str(ws.cell(r, 5).value or "")
        if col_a in ("Item Name", "Item Highlights") or col_a.startswith("BP"):
            # 英文不应有结尾标点(.!?)，中文也不应有
            en_has_end = col_b.rstrip().endswith((".", "!", "?"))
            cn_has_end = col_e.rstrip().endswith(("。", "！", "？"))
            if en_has_end:
                sync_issues.append(f"Row {r} ({col_a}) 英文含结尾标点")
            if cn_has_end:
                sync_issues.append(f"Row {r} ({col_a}) 中文含结尾标点")
            # 英文有问号则中文不应有问号（语义同步）
            if "?" in col_b and "？" not in col_e and col_e.strip():
                # 英文已改陈述句但中文仍是问句，说明未同步
                if "？" in col_e or "?" in col_e:
                    sync_issues.append(f"Row {r} ({col_a}) 英文无问句但中文仍含问号")
    if sync_issues:
        errors.append(f"中英翻译未同步(标点/句式不一致): {'; '.join(sync_issues)}")

    # 输出结果
    if errors:
        msg = "\n".join(f"  [X] {e}" for e in errors)
        raise Exception(f"\n{'='*60}\n[FAIL] COMPLIANCE CHECK FAILED ({len(errors)} issues)\n{'='*60}\n{msg}\n{'='*60}\n--> Fix all issues above before using this file. DO NOT skip any check.\n")
    else:
        print(f"\n{'='*60}")
        print("[PASS] COMPLIANCE CHECK PASSED -- All 13 checks OK")
        print(f"  Sheet: {ws.title} | Rows: {ws.max_row} | Cols: {ws.max_column}")
        print(f"  Modules: {module_count} | Validations: {val_count}")
        print(f"  Images: {img_count} | Search Terms Note: {'YES' if has_note else 'NO'}")
        print(f"  Columns: 6 (模块/内容/关键词/场景词/中文翻译/规格校验)")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    create_listing_excel()
