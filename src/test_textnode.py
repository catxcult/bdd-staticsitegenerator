import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()