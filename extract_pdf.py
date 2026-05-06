#!/usr/bin/env python3
"""
PDF教材提取与清洗工具
用法: python3 extract_pdf.py <input.pdf> [--title "书名"] [--author "作者"] [--publisher "出版社"] [--isbn "ISBN"] [--lang "zh/en"]
"""

import fitz
import re
import sys
import os
import json
import argparse
from collections import Counter


def check_pdf_type(pdf_path):
    """判断PDF是文字型还是扫描型"""
    doc = fitz.open(pdf_path)
    text_blocks = 0
    image_blocks = 0

    # 随机取5页检测
    sample_pages = list(range(min(5, len(doc)))) + list(range(max(0, len(doc)-5), len(doc)))
    sample_pages = list(set(sample_pages))[:8]

    for i in sample_pages:
        page = doc[i]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                text_blocks += 1
            elif block["type"] == 1:
                image_blocks += 1

    doc.close()
    return {
        "type": "text" if text_blocks > 5 else "scanned",
        "text_blocks": text_blocks,
        "image_blocks": image_blocks,
        "pages_sampled": len(sample_pages),
    }


def extract_text(pdf_path):
    """从PDF提取全文"""
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    meta = doc.metadata
    page_count = len(doc)
    doc.close()
    return "\n".join(pages), meta, page_count


def detect_repeated_phrases(lines, min_freq=3, min_len=3, max_len=40):
    """检测重复出现的短文本（页眉页脚）"""
    # 只取每页的首行和末行
    first_lines = []
    last_lines = []

    # 按空行分"页"
    page_start = 0
    for i, line in enumerate(lines):
        if not line.strip() and i > page_start + 2:
            if page_start < len(lines):
                first_lines.append(lines[page_start].strip())
            if i - 1 > page_start:
                last_lines.append(lines[i - 1].strip())
            page_start = i + 1

    # 统计频率
    candidates = Counter()
    for line_list in [first_lines, last_lines]:
        for line in line_list:
            if min_len <= len(line) <= max_len and not line.strip().isdigit():
                candidates[line] += 1

    # 返回高频短语
    return {phrase for phrase, count in candidates.items() if count >= min_freq}


def clean_lines(lines, repeated_phrases):
    """清洗文本行"""
    cleaned = []
    removed_page_nums = 0
    removed_headers = 0
    prev_empty = False

    for line in lines:
        s = line.rstrip()
        ss = s.strip()

        # 1. 去页码：独立数字行 (1-999)
        if ss.isdigit() and 1 <= int(ss) <= 999:
            removed_page_nums += 1
            continue

        # 2. 去页眉页脚
        if ss in repeated_phrases:
            removed_headers += 1
            continue

        # 3. 合并连续空行
        if not ss:
            if not prev_empty:
                cleaned.append("")
                prev_empty = True
            continue

        cleaned.append(s)
        prev_empty = False

    return cleaned, removed_page_nums, removed_headers


def fix_symbols(text):
    """修复常见符号映射问题"""
    fixes = 0

    # ∆ (U+2206 Increment) → Δ (U+0394 Greek Delta)
    n = text.count('∆')
    if n > 0:
        text = text.replace('∆', 'Δ')
        fixes += n

    # △ (U+25B3 Triangle) → Δ (仅在数学上下文中)
    # 判断：△ 后面跟 G, T, H, S 等大写字母 = 数学符号
    triangle_fixes = len(re.findall(r'△(?=[A-Z])', text))
    if triangle_fixes > 0:
        text = re.sub(r'△(?=[A-Z])', 'Δ', text)
        fixes += triangle_fixes

    return text, fixes


def build_metadata_header(meta, page_count, args):
    """构建元数据头"""
    title = args.title or meta.get("title", "") or os.path.splitext(os.path.basename(args.input))[0]
    author = args.author or meta.get("author", "")
    publisher = args.publisher or ""
    isbn = args.isbn or ""
    lang = args.lang or "auto"

    # 从文件名推断语言
    if lang == "auto":
        if any('\u4e00' <= c <= '\u9fff' for c in title):
            lang = "Chinese"
        else:
            lang = "English"

    # 主题标签
    topic = args.topic or ""

    header = f"# {title}\n\n"
    if topic:
        header += f"**Topic**: {topic}\n"
    header += f"**Source**: {os.path.basename(args.input)}\n"
    if author:
        header += f"**Author**: {author}\n"
    if publisher:
        header += f"**Publisher**: {publisher}\n"
    if isbn:
        header += f"**ISBN**: {isbn}\n"
    header += f"**Pages**: {page_count}\n"
    header += f"**Language**: {lang}\n"
    header += "\n---\n\n"

    return header


def quality_check(text):
    """质量检查"""
    results = {}

    # 希腊字母
    greek = sum(text.count(c) for c in 'αβγδεζηθικλμνξπρστυφχψω')
    results['greek_letters'] = greek

    # [公式] 占位符
    results['formula_placeholders'] = text.count('[公式]')

    # Delta符号
    results['delta_greek'] = text.count('Δ')
    results['delta_increm'] = text.count('∆')
    results['delta_triangle'] = text.count('△')

    # 公式编号
    results['equation_numbers'] = len(re.findall(r'[(（]\d+[-–.]\d+[)）]', text))

    # Unicode下标
    results['unicode_subscripts'] = sum(text.count(c) for c in '₀₁₂₃₄₅₆₇₈₉')

    # 行数和字符数
    lines = text.splitlines()
    results['total_chars'] = len(text)
    results['total_lines'] = len(lines)

    # 短行数（可能是公式碎片）
    results['short_lines'] = sum(1 for l in lines if 0 < len(l.strip()) <= 2)

    return results


def main():
    parser = argparse.ArgumentParser(description='PDF教材提取与清洗工具')
    parser.add_argument('input', help='输入PDF文件路径')
    parser.add_argument('--title', help='书名')
    parser.add_argument('--author', help='作者')
    parser.add_argument('--publisher', help='出版社')
    parser.add_argument('--isbn', help='ISBN')
    parser.add_argument('--lang', default='auto', help='语言 (zh/en/auto)')
    parser.add_argument('--topic', help='主题标签 (逗号分隔)')
    parser.add_argument('--output', help='输出文件路径 (默认: 输入文件名.txt)')
    parser.add_argument('--check-only', action='store_true', help='仅检查PDF类型，不提取')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: 文件不存在 {args.input}")
        sys.exit(1)

    # Step 1: 类型判断
    print(f"[1/5] 检查PDF类型...")
    pdf_info = check_pdf_type(args.input)
    print(f"  类型: {pdf_info['type']}")
    print(f"  文本块: {pdf_info['text_blocks']}, 图片块: {pdf_info['image_blocks']}")

    if pdf_info['type'] == 'scanned':
        print("\n⚠️  这是扫描型PDF，需要OCR处理，本工具不适用。")
        print("  建议使用: 多模态模型 / Mathpix / Tesseract")
        sys.exit(2)

    if args.check_only:
        print("\n检查完成，这是文字型PDF，可以直接提取。")
        sys.exit(0)

    # Step 2: 文本提取
    print(f"\n[2/5] 提取文本...")
    raw_text, meta, page_count = extract_text(args.input)
    raw_lines = raw_text.splitlines()
    print(f"  原始: {len(raw_text):,} 字符, {len(raw_lines):,} 行, {page_count} 页")

    # Step 3: 清洗
    print(f"\n[3/5] 清洗文本...")

    # 检测页眉页脚
    repeated = detect_repeated_phrases(raw_lines)
    if repeated:
        print(f"  检测到页眉页脚: {repeated}")

    # 清洗行
    cleaned_lines, rm_nums, rm_headers = clean_lines(raw_lines, repeated)
    print(f"  移除页码: {rm_nums} 行")
    print(f"  移除页眉页脚: {rm_headers} 行")
    print(f"  清洗后: {len(cleaned_lines):,} 行")

    # 合并为文本并修复符号
    text = "\n".join(cleaned_lines)
    text, symbol_fixes = fix_symbols(text)
    print(f"  修复符号: {symbol_fixes} 处")

    # Step 4: 元数据
    print(f"\n[4/5] 注入元数据...")
    header = build_metadata_header(meta, page_count, args)
    output_text = header + text
    print(f"  标题: {args.title or meta.get('title', '(从文件名推断)')}")

    # Step 5: 输出
    output_path = args.output or os.path.splitext(args.input)[0] + ".txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_text)

    print(f"\n[5/5] 输出完成: {output_path}")
    print(f"  最终: {len(output_text):,} 字符, {len(output_text.splitlines()):,} 行")

    # 质量报告
    qc = quality_check(output_text)
    print(f"\n{'─' * 50}")
    print(f"[质量报告]")
    print(f"  希腊字母: {qc['greek_letters']}")
    print(f"  Δ (Greek Delta): {qc['delta_greek']}")
    print(f"  ∆ (Increment): {qc['delta_increm']} {'✅' if qc['delta_increm'] == 0 else '⚠️'}")
    print(f"  △ (Triangle): {qc['delta_triangle']} {'✅' if qc['delta_triangle'] == 0 else '⚠️'}")
    print(f"  [公式] 占位符: {qc['formula_placeholders']} {'✅' if qc['formula_placeholders'] == 0 else '❌'}")
    print(f"  公式编号: {qc['equation_numbers']}")
    print(f"  Unicode下标: {qc['unicode_subscripts']}")

    # 输出JSON报告
    report_path = os.path.splitext(output_path)[0] + "_report.json"
    report = {
        "input": args.input,
        "output": output_path,
        "pdf_type": pdf_info,
        "pages": page_count,
        "quality": qc,
        "cleaning": {
            "page_numbers_removed": rm_nums,
            "headers_removed": rm_headers,
            "symbols_fixed": symbol_fixes,
            "repeated_phrases": list(repeated),
        },
    }
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  报告: {report_path}")


if __name__ == '__main__':
    main()
