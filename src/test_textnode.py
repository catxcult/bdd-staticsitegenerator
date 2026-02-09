import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestTextNode(unittest.TestCase):
    def test_eq_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_no_url(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a italic text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_urls(self):
        node = TextNode("Link Test", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link Test", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_with_urls(self):
        node = TextNode("Link Test", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link Test", TextType.LINK, "https://google.dev")
        self.assertNotEqual(node, node2)

    def test_not_eq_with_url(self):
        node = TextNode("Link Test", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link Test", TextType.LINK)
        self.assertNotEqual(node, node2)

    ## Conversion checks
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("Boots", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boots")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Boots", TextType.IMAGE, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com", "alt": "Boots"})

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

    # The following tests are generated

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
        
if __name__ == "__main__":
    unittest.main()