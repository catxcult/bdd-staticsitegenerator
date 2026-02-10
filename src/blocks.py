from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    if is_code_block(block):
        return BlockType.CODE
    if is_comment_block(block):
        return BlockType.QUOTE
    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def is_heading(block):
    return block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))

def is_code_block(block):
    lines = block.split("\n")
    return len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")

def is_comment_block(block):
    lines = block.split("\n")
    
    for line in lines:
        if not line.startswith(">"):
            return False
    return True

def is_unordered_list(block):
    lines = block.split("\n")

    for line in lines:
        if not line.startswith("- "):
            return False
    return True

def is_ordered_list(block):
    lines = block.split("\n")

    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            return False
    return True


