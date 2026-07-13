#!/usr/bin/env python3
"""Extract vulnerability data from a merged Issue and write as a TOML file."""

import os
import re
import unicodedata
from pathlib import Path

DATA_DIR = Path("docs")
ISSUE_BODY = os.environ.get("ISSUE_BODY", "")
ISSUE_NUMBER = os.environ.get("ISSUE_NUMBER", "0")

def extract_field(body, label):
    patterns = [
        rf"###\s*{label}\s*\n(.*?)(?:\n###|\Z)",
        rf"###\s*{label}\s*\n\n(.*?)(?:\n###|\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, body, re.DOTALL)
        if m:
            return m.group(1).strip()
    return ""

def clean(val):
    return val.strip() if val else ""

def toml_val(v):
    return f'"{v.replace(chr(92), chr(92)*2).replace(chr(34), chr(92)+chr(34))}"'

def slug(s):
    s = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff\u3400-\u4dbf_-]', '-', s)
    s = re.sub(r'-+', '-', s).strip('-').lower()
    return s[:100] or "untitled"

def main():
    vendor = extract_field(ISSUE_BODY, "厂商")
    name = extract_field(ISSUE_BODY, "漏洞名称")
    vuln_type = extract_field(ISSUE_BODY, "漏洞类型")
    version = extract_field(ISSUE_BODY, "涉及版本")
    path = extract_field(ISSUE_BODY, "利用路径 / URL")
    detail = extract_field(ISSUE_BODY, "漏洞详情 / POC")
    fix = extract_field(ISSUE_BODY, "处置建议 / 修复方案")
    date = extract_field(ISSUE_BODY, "情报获取时间")

    label = "nday"
    if "- [x] 0day" in ISSUE_BODY or "- [X] 0day" in ISSUE_BODY:
        label = "0day"
    elif "- [x] 1day" in ISSUE_BODY or "- [X] 1day" in ISSUE_BODY:
        label = "1day"

    verifier = extract_field(ISSUE_BODY, "来源 / 验证人")

    year_match = re.search(r"title:\s*\[(\d{4})\]", ISSUE_BODY)
    if not year_match:
        year_match = re.search(r"(20\d{2})", ISSUE_BODY)
    year = year_match.group(1) if year_match else "2025"

    year_dir = DATA_DIR / year
    year_dir.mkdir(parents=True, exist_ok=True)

    # Build TOML content with only non-empty fields
    fields = [
        ("vendor", vendor or "未知"),
        ("name", name or "未知"),
        ("type", vuln_type or "未知"),
    ]
    if version:
        fields.append(("version", clean(version)))
    if path:
        fields.append(("path", clean(path)))
    if detail:
        fields.append(("detail", clean(detail)))
    if fix:
        fields.append(("fix", clean(fix)))
    if date:
        fields.append(("date", clean(date)))
    fields.append(("label", label))
    if year in ("2025",) and verifier:
        fields.append(("verifier", clean(verifier)))

    lines = [f'{k} = {toml_val(v)}' for k, v in fields]
    content = '\n'.join(lines) + '\n'

    vendor_slug = slug(vendor or "unknown")
    name_slug = slug(name or "unknown")
    fname = f"{vendor_slug}_{name_slug}.toml"
    fpath = year_dir / fname

    # Avoid overwriting
    counter = 1
    while fpath.exists():
        fpath = year_dir / f"{vendor_slug}_{name_slug}_{counter}.toml"
        counter += 1

    fpath.write_text(content, encoding="utf-8")
    print(f"Added {fpath.name}")

if __name__ == "__main__":
    main()
