import unittest

from textnode import TextNode, TextType
from transformers import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node
from helpers import extract_markdown_images, extract_markdown_links
from blocks import BlockType, block_to_block_type

class TestTransformers(unittest.TestCase):
    ## Split Checks
    def test_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(new_nodes),
                         "[TextNode(This is text with a , text, None), TextNode(code block, code, None), TextNode( word, text, None)]")
        
    def test_bold_split(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(new_nodes),
                         "[TextNode(This is text with a , text, None), TextNode(bolded, bold, None), TextNode( word, text, None)]")
    
    def test_italic_split(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(str(new_nodes),
                         "[TextNode(This is text with an , text, None), TextNode(italic, italic, None), TextNode( word, text, None)]")
        
    def test_unmatched_delimiter(self):
        node = TextNode("This is text with an ^bad word", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            new_nodes = split_nodes_delimiter([node], "^", None)
        self.assertEqual(str(context.exception), "Unmatched delimiter!")

    def test_multiple_code_blocks(self):
        node = TextNode("This has `code` and `more code` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)  # text, code, text, code, text

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(new_nodes),
                         "[TextNode(bold, bold, None), TextNode( at start, text, None)]")
        
    def test_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
    
    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First `code` node", TextType.TEXT),
            TextNode("Second `code` node", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 6)  # 3 from each original node

    def test_empty_delimiter_content(self):
        node = TextNode("Empty `` code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(new_nodes),
                         "[TextNode(Empty , text, None), TextNode( code, text, None)]")
        
    ## Image/Link Tests
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [test](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("test", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_with_link(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_link_with_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_link_and_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is text with an [test](https://i.imgur.com/zjjcJKZ.png)"
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)

        link_matches = extract_markdown_links(text)
        self.assertListEqual([("test", "https://i.imgur.com/zjjcJKZ.png")], link_matches)

    def test_no_images(self):
        matches = extract_markdown_images("Just plain text here.")
        self.assertListEqual([], matches)

    def test_no_links(self):
        matches = extract_markdown_links("Just plain text here.")
        self.assertListEqual([], matches)

    ## Image / Link Split Tests
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_linkss(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_basic(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("No images here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_trailing_text(self):
        node = TextNode(
            "Start ![img](url) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode("![img](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("img", TextType.IMAGE, "url")],
            new_nodes,
        )

    def test_split_images_mixed_types_preserved(self):
        nodes = [
            TextNode("![img](url)", TextType.TEXT),
            TextNode("already image", TextType.IMAGE, "old_url"),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertIn(
            TextNode("already image", TextType.IMAGE, "old_url"),
            new_nodes,
        )

    ## Image / Link Split Tests Cont.
    ## The following tests are generated

    def test_split_links_basic(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode(
                    "to boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("No links here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_trailing_text(self):
        node = TextNode(
            "Start [link](url) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode("[link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "url")],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode(
            "![img](imgurl) and [link](linkurl)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![img](imgurl) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "linkurl"),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt(self):
        node = TextNode(
            "Before ![](url) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "url"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_empty_text(self):
        node = TextNode(
            "Before [](url) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("", TextType.LINK, "url"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes_input(self):
        nodes = [
            TextNode("First ![one](url1)", TextType.TEXT),
            TextNode("Second ![two](url2) end", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode("Second ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes_input(self):
        nodes = [
            TextNode("First [one](url1)", TextType.TEXT),
            TextNode("Second [two](url2) end", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.LINK, "url1"),
                TextNode("Second ", TextType.TEXT),
                TextNode("two", TextType.LINK, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    ## Text to TextNodes Tests
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_no_markdown(self):
        text = "This is just some plain old text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just some plain old text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_text_to_textnodes_only_bold(self):
        text = "This is just some **bold** text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    ## Blocks
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_basic_example(self):
        md = """# This is a heading

This is a paragraph of text.

- item 1
- item 2
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text.",
                "- item 1\n- item 2",
            ],
        )

    def test_leading_and_trailing_newlines(self):
        md = """

First block

Second block

"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "First block",
                "Second block",
            ],
        )

    def test_multiple_blank_lines(self):
        md = """Block one


Block two




Block three"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Block one",
                "Block two",
                "Block three",
            ],
        )

    def test_single_paragraph_no_blank_lines(self):
        md = """Line one
Line two
Line three"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Line one\nLine two\nLine three",
            ],
        )

    def test_assignment_example(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        self.assertEqual(
            markdown_to_blocks(md),
            [],
        )

    def test_literal_newlines(self):
        md = """Block one\n\nBlock two

Block three
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Block one",
                "Block two",
                "Block three",
            ],
        )

    def test_windows_newlines(self):
        md = """Block one\r\n\nBlock two

Block three
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Block one",
                "Block two",
                "Block three",
            ],
        )

    def test_block_to_block_types(self):
        # Got lazy - from solution with some added at the end
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. list\n> some cool quote"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    ## Blocks to HTML
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

### this is an h3

###### this is an h6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><h3>this is an h3</h3><h6>this is an h6</h6></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_ul(self):
        md = """
- This is a list
- with items
- and _italic_ help
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>italic</i> help</li></ul></div>",
        )

    def test_ol(self):
        md = """
1. This is an
2. ordered list
3. with **bold** text
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an</li><li>ordered list</li><li>with <b>bold</b> text</li></ol></div>",
        )
        
if __name__ == "__main__":
    unittest.main()