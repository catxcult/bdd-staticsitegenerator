from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    PICTURE = "picture"

class TextNode():
    def __init__(self, text: str, type: TextType, url: str=None):
        self.text = text
        self.text_type = type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text == other.text
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
