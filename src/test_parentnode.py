import unittest

from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_with_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: parent with no children")

        parent_node2 = ParentNode("div", None)
        with self.assertRaises(ValueError) as context2:
            parent_node2.to_html()
        self.assertEqual(str(context2.exception), "invalid HTML: parent with no children")
    
    def test_bad_tag(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: no tag")

    def test_empy_str_child(self):
        child_node = LeafNode("span", "")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span></span></div>")

    def test_sibling_parents(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node2])
        grandparent_node = ParentNode("div", [parent_node, parent_node2])
        self.assertEqual(grandparent_node.to_html(), "<div><div><span>child</span></div><div><p>child2</p></div></div>")

if __name__ == "__main__":
    unittest.main()