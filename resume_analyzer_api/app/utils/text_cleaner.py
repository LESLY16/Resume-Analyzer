import re

def clean_text(text: str) -> str:
    """
    Basic cleaner: normalize whitespace.
    Extend with more advanced cleaning if needed.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()
