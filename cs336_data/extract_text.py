from fastwarc.warc import ArchiveIterator, WarcRecordType
from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import bytes_to_str, detect_encoding


def extract_text_from_html_bytes(html_bytes):
    encoding = detect_encoding(html_bytes)
    decoded_text = bytes_to_str(html_bytes, encoding=encoding, fallback_encodings=("utf-8",))
    plain_text = extract_plain_text(decoded_text)
    return plain_text


if __name__ == "__main__":
    warc_file = "../data/CC-MAIN-20260305070756-20260305100756-00000.warc.gz"
    wet_file = "../data/CC-MAIN-20260305070756-20260305100756-00000.warc.wet.gz"
    with open(warc_file, "rb") as stream:
        for record in ArchiveIterator(stream, record_types=WarcRecordType.response):
            payload_bytes = record.reader.read()
            extracted_text = extract_text_from_html_bytes(payload_bytes)

            with open("my_extraction.txt", "w", encoding="utf-8") as f:
                f.write(extracted_text)

            print("URL:", record.headers.get("WARC-Target-URI"))
            print("Record ID:", record.headers.get("WARC-Record-ID"))
            target_record_id = record.headers.get("WARC-Record-ID")
            print("Extracted characters:", len(extracted_text))

            break

    with open(wet_file, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record.headers.get("WARC-Refers-To") == target_record_id:
                wet_text = record.reader.read().decode("utf-8", errors="replace")

                with open("wet_extraction.txt", "w", encoding="utf-8") as f:
                    f.write(wet_text)

                break
