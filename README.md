![Python package](https://github.com/jvanasco/metadata_utils/workflows/Python%20package/badge.svg)

metadata_utils
==============

This package offers lightweight tools for dealing with metadata in HTML.

## Quoted HTML attributes

Use `html_attribute_escape` on text before inserting it into a quoted HTML
attribute.

```python
from metadata_utils import html_attribute_escape, html_attribute_unescape

title = 'Fish & "Chips"'
escaped = html_attribute_escape(title)
assert f'<span title="{escaped}"></span>' == (
    '<span title="Fish &amp; &quot;Chips&quot;"></span>'
)
assert html_attribute_unescape(escaped) == title
```

`html_attribute_unescape` decodes one layer of the five named entities emitted
by the escape function (`&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&apos;`).
Other named and numeric references pass through unchanged.

## ASCII normalization

Both helpers apply Unicode normalization, drop any remaining non-ASCII
characters, and return `bytes`. Both expand the `ﬁ` ligature into `fi`.
NFKD decomposes `é` so the ASCII `e` survives. NFKC keeps the composed
`é`, which is dropped during ASCII encoding.

```python
from metadata_utils import force_clean_ascii_NFKC, force_clean_ascii_NFKD

assert force_clean_ascii_NFKD("ﬁ café") == b"fi cafe"
assert force_clean_ascii_NFKC("ﬁ café") == b"fi caf"
```
