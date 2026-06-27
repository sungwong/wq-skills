#!/usr/bin/env python3
"""惟乔日课编号计算（按日期递增，不是流水号）

规则：
- 编号跟着日期走，每过一天 +1，没写的那天号留空（所以编号里会有缺口）。
- 取号方法：扫描日课目录，找"编号最大"的那篇作为锚点，取它的编号 N 和日期 D，
  今天的编号 = N + (今天 - D 的天数差)。
- 同一天再写第二篇时，天数差为 0，自动给 N+1。

用法：
  python3 rike_number.py            # 打印今天该用的编号和日期
  python3 rike_number.py --keyword 趋势   # 连开头和文件名一起打印
"""
import os
import re
import sys
import glob
from datetime import date


def get_rike_dir():
    """定位日课目录：先按 skill 相对路径找，找不到再退回绝对路径。"""
    here = os.path.dirname(os.path.abspath(__file__))
    # skills/home-claude-skills/weiqiao-rike -> 上三层是 content-system 根
    candidate = os.path.normpath(
        os.path.join(here, "..", "..", "..", "03-产出", "日课")
    )
    if os.path.isdir(candidate):
        return candidate
    fallback = "/Users/weiqiao/content-system/03-产出/日课"
    if os.path.isdir(fallback):
        return fallback
    return candidate  # 让上层报错提示


def get_anchor(rike_dir):
    """返回编号最大的 (编号, 日期date)。"""
    max_num = -1
    anchor_date = None
    for f in glob.glob(os.path.join(rike_dir, "日课*.md")):
        name = os.path.basename(f)
        m = re.match(r"日课(\d+)-(\d{8})", name)
        if not m:
            continue
        num = int(m.group(1))
        d = m.group(2)
        if num > max_num:
            max_num = num
            anchor_date = date(int(d[:4]), int(d[4:6]), int(d[6:8]))
    return max_num, anchor_date


def next_number():
    rike_dir = get_rike_dir()
    max_num, anchor_date = get_anchor(rike_dir)
    if max_num < 0 or anchor_date is None:
        raise SystemExit(f"未在 {rike_dir} 找到日课文件，无法取号")
    today = date.today()
    diff = (today - anchor_date).days
    nxt = max_num + diff
    if nxt <= max_num:        # 同一天再写 / 异常，至少 +1
        nxt = max_num + 1
    return nxt, today, max_num, anchor_date


def main():
    nxt, today, anchor_num, anchor_date = next_number()
    date_h = f"{today.year}-{today.month}-{today.day}"          # 开头用
    date_f = today.strftime("%Y%m%d")                           # 文件名用
    keyword = None
    if "--keyword" in sys.argv:
        i = sys.argv.index("--keyword")
        if i + 1 < len(sys.argv):
            keyword = sys.argv[i + 1]

    print(f"今天编号: {nxt}")
    print(f"锚点: 第{anchor_num}篇 / {anchor_date}  → 距今 {(today - anchor_date).days} 天")
    print(f"日期(开头): {date_h}")
    print(f"日期(文件名): {date_f}")
    if keyword:
        print(f"开头: #日课 今天是{date_h}，惟乔日课第{nxt}篇，关键词：{keyword}。")
        print(f"文件名: 日课{nxt}-{date_f}-{keyword}.md")


if __name__ == "__main__":
    main()
