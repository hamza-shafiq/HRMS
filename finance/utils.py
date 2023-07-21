

def normalize_header(headers):
    return [
        str(head)
        .replace(" – ", "_")
        .replace('/', '_')
        .replace(" - ", "_")
        .replace("–", "_")
        .replace("-", "_")
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .lower()
        for head in headers
    ]
