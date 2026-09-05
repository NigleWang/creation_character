#!/usr/bin/python3
"""Fetch publicly visible Xiaohongshu note cards (OG tags) via Playwright.

Scope: only URLs you already have. No login, no search crawl, no captcha bypass.
Stops and records failure if the page asks to log in or verify.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

DEFAULT_URL = "https://xhslink.cn/o/9s6VJcV9Lom"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "outputs" / "drafts" / "xhs_public_og.json"

BLOCK_HINTS = (
    "验证",
    "请登录",
    "登录后查看",
    "扫码登录",
    "安全验证",
)


def meta(page, key: str) -> str | None:
    loc = page.locator(f'meta[property="{key}"], meta[name="{key}"]').first
    if loc.count() == 0:
        return None
    value = loc.get_attribute("content")
    return value.strip() if value else None


def blocked_reason(page) -> str | None:
    parsed = urlparse(page.url)
    host_path = f"{parsed.netloc}{parsed.path}".lower()
    qs = parse_qs(parsed.query)
    error_code = (qs.get("error_code") or [None])[0]
    error_msg = unquote((qs.get("error_msg") or [""])[0])

    if "website-login/error" in host_path or error_code:
        if error_code == "300012" or "IP存在风险" in error_msg:
            return "ip_risk"
        if error_msg:
            return f"blocked:{error_code or 'unknown'}:{error_msg}"
        return f"blocked:{error_code or 'website-login-error'}"
    if "/login" in host_path or "passport" in host_path:
        return "login_redirect"
    body = page.locator("body")
    for hint in BLOCK_HINTS:
        if body.get_by_text(hint, exact=False).count() > 0:
            return f"blocked:{hint}"
    return None


def fetch_one(page, url: str) -> dict[str, Any]:
    row: dict[str, Any] = {"url": url, "ok": False}
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(1800)
    except PlaywrightTimeout:
        row["reason"] = "timeout"
        return row

    row["final_url"] = page.url
    reason = blocked_reason(page)
    if reason:
        row["reason"] = reason
        return row

    title = meta(page, "og:title") or page.title()
    if title:
        title = title.replace(" - 小红书", "").strip()

    tags = page.eval_on_selector_all(
        'meta[property="og:article:tag"]',
        "els => els.map(e => e.content).filter(Boolean)",
    )
    keywords = meta(page, "keywords")
    if not tags and keywords:
        tags = [t.strip() for t in keywords.split(",") if t.strip() and t.strip() != "小红书"]

    row.update(
        {
            "ok": True,
            "title": title,
            "description": meta(page, "og:description"),
            "cover": meta(page, "og:image"),
            "site_name": meta(page, "og:site_name"),
            "tags": tags or [],
        }
    )
    if not row["title"] and not row["description"]:
        row["ok"] = False
        row["reason"] = "empty_public_card"
    return row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "urls",
        nargs="*",
        default=[DEFAULT_URL],
        help="Public note or share URLs (default: the test xhslink)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"JSON output path (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show the real Chrome window (needed if headless gets IP-blocked)",
    )
    parser.add_argument(
        "--bundled",
        action="store_true",
        help="Use Playwright's bundled Chromium instead of /Applications/Google Chrome.app",
    )
    parser.add_argument("--delay", type=float, default=3.0, help="Seconds between URLs")
    return parser.parse_args()


def hint_if_blocked(rows: list[dict[str, Any]]) -> None:
    reasons = {r.get("reason") for r in rows}
    if "ip_risk" in reasons:
        print(
            "小红书返回 300012（IP存在风险）。先用 Safari 打开同一链接：\n"
            "  打不开 → 换手机热点后再跑脚本\n"
            "  能打开 → 用本机命令加 --headed 再试（不要加代理/Cookie/指纹伪装）",
            file=sys.stderr,
        )


def main() -> int:
    args = parse_args()
    urls = [u.strip() for u in args.urls if u.strip()]
    for url in urls:
        host = urlparse(url).netloc.lower()
        if "xiaohongshu.com" not in host and "xhslink." not in host:
            print(f"skip non-xhs url: {url}", file=sys.stderr)
            return 2

    launch_kwargs: dict[str, Any] = {"headless": not args.headed}
    if not args.bundled:
        launch_kwargs["channel"] = "chrome"

    rows: list[dict[str, Any]] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        for i, url in enumerate(urls):
            print(f"fetch {i + 1}/{len(urls)} {url}", file=sys.stderr)
            rows.append(fetch_one(page, url))
            if i < len(urls) - 1:
                time.sleep(args.delay)
        browser.close()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"saved {args.out}", file=sys.stderr)
    hint_if_blocked(rows)
    return 0 if all(r.get("ok") for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
