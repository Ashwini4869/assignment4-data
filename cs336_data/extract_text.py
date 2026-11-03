from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import bytes_to_str, detect_encoding


def extract_text_from_html_bytes(html_bytes):
    encoding = detect_encoding(html_bytes)
    decoded_text = bytes_to_str(html_bytes, encoding=encoding, fallback_encodings=("utf-8"))
    plain_text = extract_plain_text(decoded_text)
    return plain_text
