import re


def mask_emails(text: str) -> tuple[str, int]:
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    cleaned_text, instance_count = re.subn(email_pattern, "|||EMAIL_ADDRESS|||", text)
    return cleaned_text, instance_count


def mask_phone_numbers(text: str) -> tuple[str, int]:
    phone_pattern = r"(?<!\w)(?:\+?1[-.\s]?)?(?:\(\s*\d{3}\s*\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}(?!\w)"
    cleaned_text, instance_count = re.subn(phone_pattern, "|||PHONE_NUMBER|||", text)
    return cleaned_text, instance_count


def mask_ips(text: str) -> tuple[str, int]:
    ipv4_pattern = r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
    cleaned_text, instance_count = re.subn(ipv4_pattern, "|||IP_ADDRESS|||", text)
    return cleaned_text, instance_count
