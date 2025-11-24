import re

def extract_locality(text: str) -> str:
    """
    Very simple parser:
    - Extract last token or capitalized word sequences that look like locality names.
    - Handles patterns like "Analyze Wakad", "Show price for Akurdi", "Compare Aundh and Ambegaon Budruk".
      For compare queries it returns the first locality found (frontend could call the API multiple times).
    """

    text = (text or "").strip()
    if not text:
        return ""

    # try to find quoted locality: "Analyze 'Wakad'"
    m = re.search(r'["\']([^"\']+)["\']', text)
    if m:
        return m.group(1).strip()

    # common verbs to strip
    text = re.sub(r'\b(analyze|show|compare|give|for|price|growth|trend|trends|demand|of|the|last|over|years)\b', ' ', text, flags=re.I)

    # look for capitalized word sequences (e.g., "Ambegaon Budruk")
    tokens = text.split()
    caps = []
    i = 0
    while i < len(tokens):
        if tokens[i][0].isupper():
            j = i
            seq = [tokens[j]]
            j += 1
            while j < len(tokens) and tokens[j][0].isupper():
                seq.append(tokens[j]); j += 1
            caps.append(" ".join(seq))
            i = j
        else:
            i += 1

    if caps:
        return caps[0]

    # fallback: last token
    last = text.split()[-1]
    return last
