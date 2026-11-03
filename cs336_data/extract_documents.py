from extract_text import extract_text_from_html_bytes
from fastwarc.warc import ArchiveIterator, WarcRecordType


def extract_documents(warc_file):
    documents = []

    with open(warc_file, "rb") as stream:
        for record in ArchiveIterator(stream, record_types=WarcRecordType.response):
            payload_bytes = record.reader.read()
            extracted_text = extract_text_from_html_bytes(payload_bytes)

            if extracted_text.strip():
                documents.append(
                    {
                        "url": record.headers.get("WARC-Target-URI"),
                        "record_id": record.headers.get("WARC-Record-ID"),
                        "text": extracted_text,
                    }
                )

    return documents
