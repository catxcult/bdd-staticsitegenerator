from htmlnode import LeafNode
from textnode import TextNode, TextType
from helpers import extract_markdown_images, extract_markdown_links

def markdown_to_blocks(markdown):
    markdown = markdown.replace("\r\n", "\n")
    blocks = []
    sections = markdown.split("\n\n")
    for section in sections:
        section = section.strip()
        if section == "":
            continue
        blocks.append(section)
    return blocks

def text_node_to_html_node(text_node):
    tag = None
    value = None
    props = None
    match text_node.text_type:
        case TextType.TEXT:
            value = text_node.text
        case TextType.BOLD:
            tag = "b"
            value = text_node.text
        case TextType.ITALIC:
            tag = "i"
            value = text_node.text
        case TextType.CODE:
            tag = "code"
            value = text_node.text
        case TextType.LINK:
            tag = "a" ######
            value = text_node.text
            props = {"href": text_node.url}
        case TextType.IMAGE:
            tag = "img"
            value = ""
            props = {"src": text_node.url, "alt": text_node.text}
        case _:
            raise Exception(f"Unknown TextType: '{text_node.text_type.value}'")
        
    node = LeafNode(tag, value, props)
    return node

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Unmatched delimiter!")
            
        split_nodes = []
        for i in range(len(split_text)):
            node_type = TextType.TEXT if i % 2 == 0 else text_type
            if split_text[i] == "":
                continue
            split_nodes.append(TextNode(split_text[i], node_type))


        new_nodes.extend(split_nodes)
    
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_helper(old_nodes, True)

def split_nodes_link(old_nodes):
    return split_nodes_helper(old_nodes, False)

def split_nodes_helper(old_nodes, is_image):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text) if is_image else extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        match_type = TextType.IMAGE if is_image else TextType.LINK
        
        working_text = node.text
        split_nodes = []
        for match in matches:
            split_string = f"[{match[0]}]({match[1]})"
            if is_image:
                split_string = f"!{split_string}"
            split_text = working_text.split(split_string, 1)
            if split_text[0] != "":
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(match[0], match_type, match[1]))
            working_text = split_text[1]
        if working_text != "":
            split_nodes.append(TextNode(working_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes