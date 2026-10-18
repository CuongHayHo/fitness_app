#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_mermaid.py - Kết xuất toàn bộ 9 sơ đồ Mermaid ra PNG độ phân giải cao.
Sử dụng mermaid-cli (puppeteer) với:
- Nền trắng (-b white)
- Scale factor = 2 (-s 2)
- Cấu hình mermaid-config.json (font Segoe UI, cỡ chữ 18-20px)
"""

import os
import subprocess
import sys
from PIL import Image

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
MERMAID_DIR = os.path.join(REPORT_DIR, "mermaid")
IMG_DIR = os.path.join(REPORT_DIR, "img")
CONFIG_PATH = os.path.join(REPORT_DIR, "mermaid-config.json")
PUPPETEER_CONFIG = os.path.join(REPORT_DIR, "puppeteer-config.json")

MMD_FILES = [
    "so-do-kien-truc-sensor-android.mmd",
    "so-do-platform-channel.mmd",
    "so-do-use-case.mmd",
    "kien-truc-tong-the.mmd",
    "erd-sqlite.mmd",
    "luong-dieu-huong.mmd",
    "so-do-step-counter.mmd",
    "so-do-platform-bridge.mmd",
    "ci-cd-pipeline.mmd",
]

def render_all():
    print("=" * 80)
    print("BẮT ĐẦU KẾT XUẤT 9 SƠ ĐỒ MERMAID ĐỘ PHÂN GIẢI CAO")
    print("=" * 80)

    results = []

    for mmd_name in MMD_FILES:
        base_name = os.path.splitext(mmd_name)[0]
        in_path = os.path.join(MERMAID_DIR, mmd_name)
        out_path = os.path.join(IMG_DIR, f"{base_name}.png")

        if not os.path.isfile(in_path):
            print(f"[LỖI] Không tìm thấy: {in_path}")
            continue

        cmd = [
            "npx", "-y", "@mermaid-js/mermaid-cli",
            "-p", PUPPETEER_CONFIG,
            "-c", CONFIG_PATH,
            "-i", in_path,
            "-o", out_path,
            "-b", "white",
            "-s", "2",
        ]

        print(f"\n--> Đang render: {mmd_name} -> {base_name}.png ...")
        proc = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        if proc.returncode != 0:
            print(f"[FAIL] Render thất bại cho {mmd_name}:")
            print(proc.stderr)
            results.append((mmd_name, False, (0, 0), 0.0))
        else:
            with Image.open(out_path) as im:
                w, h = im.size
                aspect = w / h if h > 0 else 0
            size_kb = os.path.getsize(out_path) / 1024
            print(f"[OK] Kích thước: {w} x {h} px | Tỷ lệ: {aspect:.2f} | Dung lượng: {size_kb:.1f} KB")
            results.append((mmd_name, True, (w, h), aspect))

    print("\n" + "=" * 80)
    print("TỔNG KẾT KẾT XUẤT 9 SƠ ĐỒ MERMAID:")
    print("=" * 80)
    all_ok = True
    for name, ok, size, aspect in results:
        status = "THÀNH CÔNG" if ok else "THẤT BÀI"
        if not ok:
            all_ok = False
        print(f"  {name:35s}: [{status}] {size[0]:4d} x {size[1]:4d} px (aspect {aspect:.2f})")

    return all_ok

if __name__ == "__main__":
    success = render_all()
    sys.exit(0 if success else 1)
