"""Generate Open Graph preview PNGs for the .dev and .cc Astro sites.

Usage:
    uv run --extra og python scripts/generate-og-images.py
    uv run --extra og python scripts/generate-og-images.py --site dev
    uv run --extra og python scripts/generate-og-images.py --site cc
    uv run --extra og python scripts/generate-og-images.py --check

Visual identity follows tmp/si-briefing-skill.md:
  bg #08080e, accent #00ffa3, corner brackets, DejaVu Sans Mono for EN,
  NotoSansCJK-Bold.ttc with index=0 for JP glyphs.

The --check mode compares regenerated PNGs against existing files and exits 1
on drift. Useful for future CI wiring; not enforced anywhere yet.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- visual identity ---------------------------------------------------------

WIDTH = 1200
HEIGHT = 630

BG = "#08080e"
ACCENT = "#00ffa3"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#b0b0c0"
TEXT_MUTED = "#8888a0"
BAR_BG = "#14141a"

BAR_HEIGHT = 44
CORNER_BRACKET_LEN = 36
CORNER_BRACKET_STROKE = 3
CORNER_INSET = 28
ACCENT_UNDERLINE_WIDTH = 180
ACCENT_UNDERLINE_STROKE = 3

# Font candidates — resolved in order; first hit wins.
FONT_EN_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
]
FONT_EN_REGULAR_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]
# Noto Sans CJK TTC files require index=0 for the JP variant (avoids 文字化け).
FONT_JP_BOLD_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]
FONT_JP_REGULAR_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]


@dataclass(frozen=True)
class SiteConfig:
    """Per-site rendering config."""

    footer_url: str
    out_dir: Path


SITE_CONFIG: dict[str, SiteConfig] = {
    "dev": SiteConfig(
        footer_url="spiritualintelligence.dev",
        out_dir=REPO_ROOT / "site" / "public" / "images" / "og",
    ),
    "cc": SiteConfig(
        footer_url="spiritualintelligence.cc",
        out_dir=REPO_ROOT / "site-cc" / "public" / "images" / "og",
    ),
}

FOOTER_TAGLINE = "OPEN SOURCE // LOCAL-ONLY // NON-JUDGEMENTAL"


@dataclass(frozen=True)
class Card:
    """A single og:image to render."""

    site: Literal["dev", "cc"]
    filename: str
    title: str
    subtitle: str
    section: str  # top-left label, e.g. "DOCS" or "HOME"


# Inventory. Keep titles short enough that EN fits on one line at 60pt;
# JP pages are sized down slightly to account for wider glyphs.
CARDS: tuple[Card, ...] = (
    # --- .dev ---
    Card(
        site="dev",
        filename="default.png",
        title="Spiritual Intelligence",
        subtitle="Cybersecurity for the Soul",
        section="HOME",
    ),
    Card(
        site="dev",
        filename="blog-default.png",
        title="Blog",
        subtitle="Field notes on spiritual disinformation",
        section="BLOG",
    ),
    Card(
        site="dev",
        filename="docs-quickstart.png",
        title="Quickstart",
        subtitle="Install, scan your first text, read the score",
        section="DOCS",
    ),
    Card(
        site="dev",
        filename="docs-library.png",
        title="Library Reference",
        subtitle="Python API for the threat filter and topology module",
        section="DOCS",
    ),
    Card(
        site="dev",
        filename="docs-api.png",
        title="REST API Reference",
        subtitle="HTTP endpoints, request shapes, response schema",
        section="DOCS",
    ),
    Card(
        site="dev",
        filename="docs-architecture.png",
        title="Architecture",
        subtitle="Hybrid NLP plus heuristic layers, CVP topology",
        section="DOCS",
    ),
    # --- .cc ---
    Card(
        site="cc",
        filename="default.png",
        title="Spiritual Intelligence",
        subtitle="Why critical thinking matters in spiritual spaces",
        section="HOME",
    ),
    Card(
        site="cc",
        filename="why-spiritual-intelligence-matters.png",
        title="Why Spiritual Intelligence Matters",
        subtitle="The gap conventional media leaves open",
        section="ESSAY // 01",
    ),
    Card(
        site="cc",
        filename="threat-modelling.png",
        title="Threat Modelling for Spiritual Spaces",
        subtitle="Borrowing a security mindset for vulnerable states",
        section="ESSAY // 02",
    ),
    Card(
        site="cc",
        filename="common-threats.png",
        title="Common Threats in Spiritual Spaces",
        subtitle="Patterns that recur across traditions and languages",
        section="ESSAY // 03",
    ),
    Card(
        site="cc",
        filename="common-misconceptions.png",
        title="Common Misconceptions",
        subtitle="What analysis is not doing, and why that matters",
        section="ESSAY // 04",
    ),
    Card(
        site="cc",
        filename="cybersecurity-and-privacy.png",
        title="Cybersecurity and Privacy",
        subtitle="Local-only analysis, data sovereignty, your own machine",
        section="ESSAY // 05",
    ),
    Card(
        site="cc",
        filename="mapping-claims-and-patterns.png",
        title="Mapping Claims and Patterns",
        subtitle="From single phrases to structural intelligence",
        section="ESSAY // 06",
    ),
    Card(
        site="cc",
        filename="the-virtualisation-model.png",
        title="The Virtualisation Model",
        subtitle="CVP: consciousness layers as infrastructure",
        section="ESSAY // 07",
    ),
    Card(
        site="cc",
        filename="egregores.png",
        title="Egregores",
        subtitle="When containers harvest their hosts",
        section="ESSAY // 08",
    ),
)


# --- font resolution ---------------------------------------------------------


def _resolve_font(candidates: list[str], label: str) -> str:
    for path in candidates:
        if Path(path).is_file():
            return path
    sys.stderr.write(
        f"error: could not find a {label} font. Tried: {', '.join(candidates)}\n"
        f"hint: sudo apt install fonts-dejavu fonts-noto-cjk\n"
    )
    sys.exit(2)


def _has_cjk(text: str) -> bool:
    return any(0x3000 <= ord(ch) <= 0x9FFF or 0xFF00 <= ord(ch) <= 0xFFEF for ch in text)


def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    # index=0 is mandatory for NotoSansCJK TTC files; harmless for other fonts.
    if path.endswith(".ttc"):
        return ImageFont.truetype(path, size, index=0)
    return ImageFont.truetype(path, size)


# --- rendering ---------------------------------------------------------------


def _draw_corner_brackets(draw: ImageDraw.ImageDraw) -> None:
    stroke = CORNER_BRACKET_STROKE
    span = CORNER_BRACKET_LEN
    inset = CORNER_INSET
    # Top-left
    draw.line([(inset, inset), (inset + span, inset)], fill=ACCENT, width=stroke)
    draw.line([(inset, inset), (inset, inset + span)], fill=ACCENT, width=stroke)
    # Top-right
    draw.line(
        [(WIDTH - inset - span, inset), (WIDTH - inset, inset)],
        fill=ACCENT,
        width=stroke,
    )
    draw.line(
        [(WIDTH - inset, inset), (WIDTH - inset, inset + span)],
        fill=ACCENT,
        width=stroke,
    )
    # Bottom-left
    draw.line(
        [(inset, HEIGHT - inset - span), (inset, HEIGHT - inset)],
        fill=ACCENT,
        width=stroke,
    )
    draw.line(
        [(inset, HEIGHT - inset), (inset + span, HEIGHT - inset)],
        fill=ACCENT,
        width=stroke,
    )
    # Bottom-right
    draw.line(
        [
            (WIDTH - inset - span, HEIGHT - inset),
            (WIDTH - inset, HEIGHT - inset),
        ],
        fill=ACCENT,
        width=stroke,
    )
    draw.line(
        [
            (WIDTH - inset, HEIGHT - inset - span),
            (WIDTH - inset, HEIGHT - inset),
        ],
        fill=ACCENT,
        width=stroke,
    )


def _text_size(
    draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont
) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _fit_title_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: str,
    max_width: int,
    start_size: int,
    min_size: int,
) -> ImageFont.FreeTypeFont:
    size = start_size
    while size > min_size:
        font = _load_font(font_path, size)
        w, _ = _text_size(draw, text, font)
        if w <= max_width:
            return font
        size -= 2
    return _load_font(font_path, min_size)


def render_card(card: Card, site_cfg: SiteConfig) -> Image.Image:
    font_en_bold = _resolve_font(FONT_EN_BOLD_CANDIDATES, "DejaVu Sans Mono Bold")
    font_en_reg = _resolve_font(FONT_EN_REGULAR_CANDIDATES, "DejaVu Sans Mono")
    font_jp_bold = _resolve_font(FONT_JP_BOLD_CANDIDATES, "Noto Sans CJK JP Bold")

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (WIDTH, BAR_HEIGHT)], fill=BAR_BG)
    header_font = _load_font(font_en_reg, 16)
    header_left = f"SI-PROTOCOLS // {card.section}"
    draw.text((inset_x := 36, 14), header_left, fill=TEXT_MUTED, font=header_font)
    header_right = "CLASSIFICATION: OPEN"
    w_right, _ = _text_size(draw, header_right, header_font)
    draw.text((WIDTH - w_right - 36, 14), header_right, fill=ACCENT, font=header_font)
    _ = inset_x

    # Footer bar
    draw.rectangle([(0, HEIGHT - BAR_HEIGHT), (WIDTH, HEIGHT)], fill=BAR_BG)
    footer_font = header_font
    footer_left = site_cfg.footer_url
    draw.text(
        (36, HEIGHT - BAR_HEIGHT + 14),
        footer_left,
        fill=TEXT_MUTED,
        font=footer_font,
    )
    w_right, _ = _text_size(draw, FOOTER_TAGLINE, footer_font)
    draw.text(
        (WIDTH - w_right - 36, HEIGHT - BAR_HEIGHT + 14),
        FOOTER_TAGLINE,
        fill=ACCENT,
        font=footer_font,
    )

    _draw_corner_brackets(draw)

    # Title — choose font family by script, fit width
    title_is_cjk = _has_cjk(card.title)
    title_font_path = font_jp_bold if title_is_cjk else font_en_bold
    title_start = 72 if title_is_cjk else 64
    title_min = 44 if title_is_cjk else 36
    title_font = _fit_title_font(
        draw, card.title, title_font_path, WIDTH - 2 * 80, title_start, title_min
    )
    tw, th = _text_size(draw, card.title, title_font)
    title_y = (HEIGHT - th) // 2 - 20
    draw.text(((WIDTH - tw) // 2, title_y), card.title, fill=TEXT_PRIMARY, font=title_font)

    # Accent underline
    underline_y = title_y + th + 28
    draw.line(
        [
            ((WIDTH - ACCENT_UNDERLINE_WIDTH) // 2, underline_y),
            ((WIDTH + ACCENT_UNDERLINE_WIDTH) // 2, underline_y),
        ],
        fill=ACCENT,
        width=ACCENT_UNDERLINE_STROKE,
    )

    # Subtitle
    subtitle_is_cjk = _has_cjk(card.subtitle)
    subtitle_font_path = font_jp_bold if subtitle_is_cjk else font_en_reg
    subtitle_font = _fit_title_font(
        draw, card.subtitle, subtitle_font_path, WIDTH - 2 * 120, 24, 18
    )
    sw, sh = _text_size(draw, card.subtitle, subtitle_font)
    draw.text(
        ((WIDTH - sw) // 2, underline_y + 24),
        card.subtitle,
        fill=TEXT_SECONDARY,
        font=subtitle_font,
    )
    _ = sh

    return img


def encode_png(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def generate(site_filter: str | None = None, check_only: bool = False) -> int:
    """Generate (or compare) PNGs. Returns 0 on success, nonzero on drift."""
    drift = False
    for card in CARDS:
        if site_filter and card.site != site_filter:
            continue
        site_cfg = SITE_CONFIG[card.site]
        site_cfg.out_dir.mkdir(parents=True, exist_ok=True)
        out_path = site_cfg.out_dir / card.filename

        img = render_card(card, site_cfg)
        new_bytes = encode_png(img)

        if check_only:
            if not out_path.is_file():
                sys.stderr.write(f"drift: missing {out_path}\n")
                drift = True
                continue
            old_bytes = out_path.read_bytes()
            if hashlib.sha256(old_bytes).digest() != hashlib.sha256(new_bytes).digest():
                sys.stderr.write(f"drift: {out_path} differs from regenerated output\n")
                drift = True
        else:
            out_path.write_bytes(new_bytes)
            print(f"wrote {out_path.relative_to(REPO_ROOT)} ({len(new_bytes)} bytes)")

    if check_only and drift:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site",
        choices=["dev", "cc"],
        help="restrict generation to one site (default: both)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare against existing PNGs; exit 1 if drift detected",
    )
    args = parser.parse_args()
    return generate(site_filter=args.site, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
