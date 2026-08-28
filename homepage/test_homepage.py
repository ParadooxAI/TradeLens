#!/usr/bin/env python3
"""Structural checks for the TradeLens project page."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
INDEX = REPO / "index.html"

FORBIDDEN = ("PAPER_TITLE", "AUTHOR_NAMES", "Lorem ipsum", "TODO:", "YOUR REPO HERE", "polyfill.io")
REQUIRED = (
    "Can Agentic Trading Systems Pay for Their Own Intelligence?",
    "TradeLens",
    "EMNLP 2026 Findings",
    "agentic viability",
    "https://arxiv.org/pdf/2607.10286.pdf",
    "https://github.com/ParadooxAI/TradeLens",
    "@article{duan2026can",
    "header-logos",
    "copy-button",
    "homepage/static/images/web-logo.png",
    "homepage/static/images/teaser.png",
    "homepage/static/images/framework.png",
    "homepage/static/images/exp-1.png",
    "homepage/static/images/exp-2.svg",
    "homepage/static/images/exp-3.png",
    "Qiqi Duan",
    "Changlun Li",
    "Chen Wang",
    "Fan Zhang",
    "Mengxiang Wang",
    "Dayi Miao",
    "Peixian Ma",
    "Jiangpeng Yan",
    "Liyuan Chen",
    "Shuoling Liu",
    "Preslav Nakov",
    "Yuyu Luo",
    "Nan Tang",
    "HKUST(GZ)",
    "Paradoox AI",
    "E Fund Management Co., Ltd",
    "MBZUAI",
    "The University of Tokyo",
    "profit-side and cost-side double blind",
    "diagnosing “Why” is challenging",
    "decision-attributed timing value",
    "DeepSeek-V3.2",
    "Claude Sonnet 4.5",
    "Mistral-large-3",
    "AI-Trader",
    "December 1, 2025",
    "January 30, 2026",
    "−388.29",
    "−2554.81",
    "833.52",
)

PAPER_AUTHOR_ORDER = (
    "Qiqi Duan",
    "Changlun Li",
    "Chen Wang",
    "Fan Zhang",
    "Mengxiang Wang",
    "Dayi Miao",
    "Peixian Ma",
    "Jiangpeng Yan",
    "Liyuan Chen",
    "Shuoling Liu",
    "Preslav Nakov",
    "Yuyu Luo",
    "Nan Tang",
)
REQUIRED_FILES = (
    "../index.html",
    "static/css/index.css",
    "static/css/bulma.min.css",
    "static/js/index.js",
    "static/images/teaser.png",
    "static/images/framework.png",
    "static/images/exp-1.png",
    "static/images/exp-2.svg",
    "static/images/exp-3.png",
    "static/images/acl-logo.svg",
    "static/images/web-logo.png",
    "static/images/hkust_logo.png",
    "static/images/icon.jpg",
    "static/images/favicon.svg",
    "LICENSE",
)


def test_required_files_exist() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    assert not missing, f"missing files: {missing}"


def test_index_content() -> None:
    html = INDEX.read_text(encoding="utf-8")
    for token in FORBIDDEN:
        assert token not in html, f"placeholder left in index.html: {token}"
    assert ">arXiv</span>" not in html, "arXiv button should be removed"


def test_local_image_refs_exist() -> None:
    html = INDEX.read_text(encoding="utf-8")
    refs = re.findall(r'(?:src|href)="(homepage/static/[^"]+)"', html)
    assert refs, "no local static references found"
    missing = [ref for ref in refs if not (REPO / ref).is_file()]
    assert not missing, f"broken static refs: {missing}"


def test_author_order_matches_paper() -> None:
    html = INDEX.read_text(encoding="utf-8")
    positions = [html.find(name) for name in PAPER_AUTHOR_ORDER]
    assert all(pos >= 0 for pos in positions), "missing author"
    assert positions == sorted(positions), f"author order drifted: {PAPER_AUTHOR_ORDER}"


def test_header_taller_and_vertically_centered() -> None:
    css = (ROOT / "static/css/index.css").read_text(encoding="utf-8")
    assert "min-height: calc((var(--header-logo-max) + 2 * var(--header-pad)) * 1.3)" in css
    assert ".header-logos {\n  --header-logo-max:" in css
    assert "align-items: center" in css.split(".header-logos {", 1)[1][:400]


if __name__ == "__main__":
    test_required_files_exist()
    test_index_content()
    test_local_image_refs_exist()
    test_author_order_matches_paper()
    test_header_taller_and_vertically_centered()
    print("homepage tests passed")
