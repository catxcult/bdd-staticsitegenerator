def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if not line.startswith("# "):
            continue

        return line.removeprefix("# ")
    
    raise Exception(f"Invalid/No Title found!")

import re
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches