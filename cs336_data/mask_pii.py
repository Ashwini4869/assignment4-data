import re


def mask_emails(text: str) -> tuple[str, int]:
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    cleaned_text, instance_count = re.subn(email_pattern, "|||EMAIL_ADDRESS|||", text)
    return cleaned_text, instance_count
