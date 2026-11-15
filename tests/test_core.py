# stdlib
import unittest

# local
import metadata_utils

# ==============================================================================


class TestEscaping(unittest.TestCase):
    text_raw = """foo "' bar"""
    text_escaped = "foo &quot;&apos; bar"
    text_escaped_twice = "foo &amp;quot;&amp;apos; bar"

    def test_escape(self) -> None:
        escaped = metadata_utils.html_attribute_escape(self.text_raw)
        self.assertEqual(escaped, self.text_escaped)

    def test_escape_twice(self) -> None:
        # we don't parse we, just escape, so this will change
        escaped_twice = metadata_utils.html_attribute_escape(self.text_escaped)
        self.assertEqual(escaped_twice, self.text_escaped_twice)

    def test_unescape(self) -> None:
        unescaped = metadata_utils.html_attribute_unescape(self.text_escaped)
        self.assertEqual(unescaped, self.text_raw)

    def test_roundtrip(self) -> None:
        escaped = metadata_utils.html_attribute_escape(self.text_raw)
        self.assertEqual(escaped, self.text_escaped)
        unescaped = metadata_utils.html_attribute_unescape(escaped)
        self.assertEqual(unescaped, self.text_raw)

    def test_roundtrip_preserves_literal_entity(self) -> None:
        escaped = metadata_utils.html_attribute_escape("&quot;")
        self.assertEqual(escaped, "&amp;quot;")
        self.assertEqual(metadata_utils.html_attribute_unescape(escaped), "&quot;")


class TestCleanAscii(unittest.TestCase):
    def test_NFKD(self) -> None:
        text_unicode = "El Ni\xf1o"
        text_clean_a = "El Nino"  # downgrades
        escaped = metadata_utils.force_clean_ascii_NFKD(text_unicode)
        # py3 is a bytes
        self.assertEqual(escaped, text_clean_a.encode())

    def test_NFKC(self) -> None:
        text_unicode = "El Ni\xf1o"
        text_clean_a = "El Nio"  # strips
        escaped = metadata_utils.force_clean_ascii_NFKC(text_unicode)
        # py3 is a bytes
        self.assertEqual(escaped, text_clean_a.encode())

    def test_compatibility_ligature(self) -> None:
        text = "\ufb01 caf\xe9"
        self.assertEqual(metadata_utils.force_clean_ascii_NFKD(text), b"fi cafe")
        self.assertEqual(metadata_utils.force_clean_ascii_NFKC(text), b"fi caf")
