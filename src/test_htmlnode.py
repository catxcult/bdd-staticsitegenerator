import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("tag", "value", [], {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("tag", "value", [], {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode("tag", "value", [], {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("tag", "value", [], {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_props(self):
        node = HTMLNode("tag", "value", [], {"href": "https://www.google.com", "target": "_blank",})
        props_text = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), props_text)

    def test_blank_props(self):
        node = HTMLNode("tag", "value", [], {})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("tag", "value", [], {"href": "https://www.google.com"})
        repr_text = "HTMLNode(tag, value, [], {'href': 'https://www.google.com'})"
        self.assertEqual(repr(node), repr_text)

if __name__ == "__main__":
    unittest.main()