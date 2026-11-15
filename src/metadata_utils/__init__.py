# stdlib
import unicodedata
from typing import Dict
from xml.sax.saxutils import escape
from xml.sax.saxutils import unescape

__VERSION__ = "1.0.0"


# ==============================================================================


# https://wiki.python.org/moin/EscapingHtml
# escape() and unescape() takes care of "&" , "<" and ">"
# we need to handle quotes, so we don't break things
html_attribute_escape_table: Dict[str, str] = {'"': "&quot;", "'": "&apos;"}
html_attribute_unescape_table: Dict[str, str] = {
    v: k for (k, v) in html_attribute_escape_table.items()
}


def html_attribute_escape(text: str) -> str:
    """Escape text for insertion into a quoted HTML attribute."""
    return escape(text, html_attribute_escape_table)


def html_attribute_unescape(text: str) -> str:
    """Decode the five named entities emitted by html_attribute_escape."""
    return unescape(text, html_attribute_unescape_table)


def force_clean_ascii_NFKD(text: str) -> bytes:
    """Apply NFKD, then return ASCII bytes, dropping non-ASCII characters."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore")


def force_clean_ascii_NFKC(text: str) -> bytes:
    """Apply NFKC, then return ASCII bytes, dropping non-ASCII characters."""
    return unicodedata.normalize("NFKC", text).encode("ascii", "ignore")
