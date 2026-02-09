import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("tag", "value", {"href": "https://www.google.com", "target": "_blank",})
        node2 = LeafNode("tag", "value", {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = LeafNode("tag", "value", {"href": "https://www.google.com", "target": "_blank",})
        node2 = LeafNode("tag", "value", {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_props(self):
        node = LeafNode("tag", "value", {"href": "https://www.google.com", "target": "_blank",})
        props_text = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), props_text)

    def test_blank_props(self):
        node = LeafNode("tag", "value", {})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = LeafNode("tag", "value", {"href": "https://www.google.com"})
        repr_text = "LeafNode(tag, value, {'href': 'https://www.google.com'})"
        self.assertEqual(repr(node), repr_text)

    def test_p_html(self):
        node = LeafNode("p", "value")
        html_text = "<p>value</p>"
        self.assertEqual(node.to_html(), html_text)

    def test_link_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html_text = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node.to_html(), html_text)
    
    def test_no_tag(self):
        node = LeafNode(None, "value")
        self.assertEqual(node.to_html(), "value")
    
    def  test_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()