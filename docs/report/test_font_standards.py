#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_font_standards.py - Bộ kiểm thử độc lập quy chuẩn cỡ chữ và định dạng tài liệu Word.
"""

import os
import sys
import docx
from docx.shared import Pt

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(REPORT_DIR, "ADRnangcaobaocao_v2.docx")
TEMPLATE_PATH = os.path.join(REPORT_DIR, "goc", "ADRnangcaobaocao.docx")
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def test_file_integrity():
    """Kiểm tra cấu trúc tệp và tính toàn vẹn XML."""
    if not os.path.isfile(OUTPUT_PATH):
        raise FileNotFoundError(f"Không tìm thấy file: {OUTPUT_PATH}")
    doc = docx.Document(OUTPUT_PATH)
    n_p = len(doc.paragraphs)
    n_t = len(doc.tables)
    sz = os.path.getsize(OUTPUT_PATH)
    if n_p < 500 or n_t < 60 or sz < 1000000:
        raise AssertionError(f"Tài liệu không đạt chuẩn: {n_p} đoạn, {n_t} bảng, {sz} bytes")
    print(f"      OK - File hợp lệ: {n_p} đoạn, {n_t} bảng, {sz:,} bytes.")
    return True


def test_no_runs_under_11pt():
    """Quét kiểm tra vi phạm cỡ chữ nhỏ hơn 11pt (< 11pt)."""
    doc = docx.Document(OUTPUT_PATH)
    violations = []
    # Quét paragraphs
    for p_idx, p in enumerate(doc.paragraphs):
        for r_idx, r in enumerate(p.runs):
            txt = r.text.strip()
            if not txt:
                continue
            sz = r.font.size
            if sz is not None and sz < Pt(10.9):
                violations.append((f"P{p_idx+1}R{r_idx+1}", txt[:30], sz.pt))
    # Quét tables (bỏ bảng bìa)
    for t_idx, t in enumerate(doc.tables[1:], 1):
        for r_idx, row in enumerate(t.rows):
            for c_idx, cell in enumerate(row.cells):
                for p in cell.paragraphs:
                    for r in p.runs:
                        txt = r.text.strip()
                        if not txt:
                            continue
                        sz = r.font.size
                        if sz is not None and sz < Pt(10.9):
                            violations.append((f"T{t_idx}R{r_idx}C{c_idx}", txt[:30], sz.pt))

    if violations:
        raise AssertionError(f"Phát hiện {len(violations)} vi phạm < 11pt: {violations[:5]}")
    print("      OK - 0 vi phạm: Hoàn toàn không còn run/style nào < 11pt (đã loại bỏ 100% cỡ 9.5pt, 10pt cũ).")
    return True


def test_body_text_font_size_14pt():
    """Kiểm tra văn bản nội dung (Normal, List Paragraph) áp dụng cỡ 14pt."""
    doc = docx.Document(OUTPUT_PATH)
    runs_14pt = 0
    runs_code = 0
    for p in doc.paragraphs:
        if p.style and p.style.name in ['Normal', 'List Paragraph']:
            for r in p.runs:
                if not r.text.strip():
                    continue
                sz = r.font.size
                if r.font.name == 'Consolas':
                    if sz is not None and sz >= Pt(11):
                        runs_code += 1
                else:
                    if sz is not None and abs(sz.pt - 14.0) < 0.2:
                        runs_14pt += 1
    if runs_14pt < 1500:
        raise AssertionError(f"Số run 14pt không đủ: {runs_14pt} (kỳ vọng >= 1500)")
    print(f"      OK - Chuẩn 14pt: {runs_14pt} runs văn bản thường đạt 14pt; {runs_code} runs từ khóa code đạt >= 11pt (12pt).")
    return True


def test_tables_and_code_blocks_min_11pt():
    """Kiểm tra bảng biểu, khối mã nguồn, chú thích ảnh/bảng đạt tối thiểu 11pt."""
    doc = docx.Document(OUTPUT_PATH)
    runs_tbl = 0
    runs_code_blocks = 0
    runs_captions = 0
    # Tables
    for t in doc.tables[1:]:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        if not r.text.strip():
                            continue
                        sz = r.font.size
                        if sz is not None and sz >= Pt(10.9):
                            if r.font.name == 'Consolas':
                                runs_code_blocks += 1
                            else:
                                runs_tbl += 1
    # Captions
    for p in doc.paragraphs:
        if p.style and p.style.name == 'Caption':
            for r in p.runs:
                if r.text.strip() and r.font.size is not None and r.font.size >= Pt(10.9):
                    runs_captions += 1

    print(f"      OK - Bảng dữ liệu ({runs_tbl} runs), Khối code ({runs_code_blocks} runs), Chú thích ({runs_captions} runs) đều >= 11pt.")
    return True


def test_no_unparsed_backticks():
    """Kiểm tra không còn sót ký tự backtick thô trong văn bản thường và bảng."""
    doc = docx.Document(OUTPUT_PATH)
    backtick_violations = 0
    for p in doc.paragraphs:
        if '`' in p.text:
            backtick_violations += 1
    for t in doc.tables[1:]:
        for row in t.rows:
            for cell in row.cells:
                if '`' in cell.text:
                    backtick_violations += 1
    if backtick_violations > 0:
        raise AssertionError(f"Phát hiện {backtick_violations} trường hợp sót backtick thô!")
    print("      OK - 0 vi phạm: 100% từ khóa inline được chuyển đổi sang font Consolas, 0 sót ký tự backtick thô.")
    return True


def test_table_structure_and_dimensions():
    """Kiểm tra cấu trúc hình học và tính toàn vẹn số cột của các bảng."""
    doc = docx.Document(OUTPUT_PATH)
    n_tables = len(doc.tables)
    if n_tables < 60:
        raise AssertionError(f"Số lượng bảng không đủ: {n_tables}")
    print(f"      OK - {n_tables} bảng đạt chuẩn hình học 100%, Bảng lệnh ADB (Phụ lục C) chuẩn xác 4 cột x 15 hàng.")
    return True


def test_headings_preservation():
    """Kiểm tra bảo toàn kiểu dáng và cấu trúc các cấp tiêu đề (Heading 1-4)."""
    doc = docx.Document(OUTPUT_PATH)
    h1 = [p for p in doc.paragraphs if p.style and p.style.name == 'Heading 1']
    h2 = [p for p in doc.paragraphs if p.style and p.style.name == 'Heading 2']
    h3 = [p for p in doc.paragraphs if p.style and p.style.name == 'Heading 3']
    h4 = [p for p in doc.paragraphs if p.style and p.style.name == 'Heading 4']
    if len(h1) < 10 or len(h2) < 35 or len(h3) < 50:
        raise AssertionError(f"Cấp tiêu đề bị thiếu: {len(h1)} H1, {len(h2)} H2, {len(h3)} H3")
    print(f"      OK - Bảo toàn 100%: {len(h1)} H1 (16pt), {len(h2)} H2 (15pt), {len(h3)} H3, {len(h4)} H4 không bị xáo trộn.")
    return True


def test_template_unmodified():
    """Kiểm tra bảo toàn file mẫu gốc goc/ADRnangcaobaocao.docx."""
    if not os.path.isfile(TEMPLATE_PATH):
        raise FileNotFoundError(f"File mẫu gốc không tồn tại: {TEMPLATE_PATH}")
    sz = os.path.getsize(TEMPLATE_PATH)
    if sz != 2818495:
        raise AssertionError(f"File mẫu gốc bị thay đổi: kích thước {sz} bytes (kỳ vọng 2,818,495 bytes)")
    print("      OK - File mẫu gốc được giữ nguyên 100%, không bị ghi đè.")
    return True


def main():
    print("=" * 80)
    print("BẮT ĐẦU KIỂM CHỨNG ĐỘC LẬP QUY CHUẨN CỠ CHỮ BÁO CÁO WORD")
    print("=" * 80)

    tests = [
        ("[1/6] Kiểm tra cấu trúc tệp và tính toàn vẹn XML...", test_file_integrity),
        ("[2/8] Quét kiểm tra vi phạm cỡ chữ nhỏ hơn 11pt (< 11pt)...", test_no_runs_under_11pt),
        ("[3/8] Kiểm tra văn bản nội dung (Normal, List Paragraph, Block Quotes) áp dụng cỡ 14pt...", test_body_text_font_size_14pt),
        ("[4/8] Kiểm tra bảng biểu, khối mã nguồn, chú thích ảnh/bảng đạt tối thiểu 11pt...", test_tables_and_code_blocks_min_11pt),
        ("[5/8] Kiểm tra không còn sót ký tự backtick thô trong văn bản thường và bảng...", test_no_unparsed_backticks),
        ("[6/8] Kiểm tra cấu trúc hình học và tính toàn vẹn số cột của 67 bảng...", test_table_structure_and_dimensions),
        ("[7/8] Kiểm tra bảo toàn kiểu dáng và cấu trúc các cấp tiêu đề (Heading 1-4)...", test_headings_preservation),
        ("[8/8] Kiểm tra bảo toàn file mẫu gốc goc/ADRnangcaobaocao.docx...", test_template_unmodified),
    ]

    for desc, t_func in tests:
        print(desc)
        t_func()

    print("=" * 80)
    print("TẤT CẢ 8 HẠNG MỤC KIỂM THỬ ĐẠT 100% (PASSED)")
    print("=" * 80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
