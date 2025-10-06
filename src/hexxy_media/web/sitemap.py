import logging
import xml.etree.cElementTree as etree
from pathlib import Path
from typing import Literal

from hexxy_media.common.data import (
    GITHUB_PAGES_MOD_BOOKS,
    GITHUB_PAGES_RECORDS,
    LINK_RECORDS,
)

logger = logging.getLogger(__name__)


# https://www.sitemaps.org/protocol.html

Changefreq = Literal[
    "always",
    "hourly",
    "daily",
    "weekly",
    "monthly",
    "yearly",
    "never",
]


def build_sitemap(output_dir: Path):
    logger.info("Building sitemap.")

    root = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    _sitemap_url(root, loc="https://hexxy.media")
    for record in LINK_RECORDS + GITHUB_PAGES_RECORDS + GITHUB_PAGES_MOD_BOOKS:
        _sitemap_url(root, loc=record.url)

    output_path = output_dir / "sitemap.xml"
    logger.info(f"Writing sitemap to {output_path}.")
    etree.ElementTree(root).write(
        output_path,
        encoding="utf-8",
        xml_declaration=True,
    )


def _sitemap_url(
    root: etree.Element,
    *,
    loc: str,
    lastmod: str | None = None,
    changefreq: Changefreq | None = None,
    priority: float | None = None,
):
    url = etree.SubElement(root, "url")
    etree.SubElement(url, "loc").text = loc
    if lastmod is not None:
        etree.SubElement(url, "lastmod").text = lastmod
    if changefreq is not None:
        etree.SubElement(url, "changefreq").text = changefreq
    if priority is not None:
        etree.SubElement(url, "priority").text = str(priority)
    return url
