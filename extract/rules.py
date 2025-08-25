import re

REGEX_CRM = re.compile(r"\bCRM[- ]?(?:[A-Z]{2})?\s?\d{4,7}\b", flags=re.I)

def extract_solicitante(text: str) -> FieldSpan:
    m = REGEX_CRM.search(text)
    if not m:
        return FieldSpan(text="", bbox=None, score=0.0)
    return FieldSpan(text=m.group(0), bbox=None, score=0.95)