import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):

        node = HTMLNode(
            "p",
            "This is a text node",
            [],
            {
                "href": "https://something.org",
                "target": "_blank"
            }
        )

        self.assertEqual(
            " href=\"https://something.org\" target=\"_blank\"",
            node.props_to_html()
        )

        node_2 = HTMLNode(
            "p",
            "This is a text node",
            [],
        )

        self.assertEqual("", node_2.props_to_html())

        node_3 = HTMLNode(
            "p",
            "This is a text node",
            [],
            {
                "href": "https://something.org",
                "target": "_blank",
                "src": "dir/",
                "another_prop": "some_value"
            }
        )

        self.assertEqual(
            " href=\"https://something.org\" target=\"_blank\" src=\"dir/\" another_prop=\"some_value\"",
            node_3.props_to_html()
        )

        node_4 = HTMLNode(
            "p",
            "This is a text node",
            [],
            {
                "href": "https://something.org",
            }
        )

        self.assertEqual(
            " href=\"https://something.org\"",
            node_4.props_to_html()
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):

        node = LeafNode(
            "p",
            "This is a text node",
            {
                "href": "https://something.org",
                "target": "_blank"
            }
        )
        self.assertEqual(
            "<p href=\"https://something.org\" target=\"_blank\">This is a text node</p>",
            node.to_html()
        )

        node_2 = LeafNode(
            "p",
            "This is a text node",
        )
        self.assertEqual("<p>This is a text node</p>", node_2.to_html())

        node_3 = LeafNode(
            "p",
            "This is a text node",
            {
                "href": "https://something.org",
                "target": "_blank",
                "src": "dir/",
                "another_prop": "some_value"
            }
        )
        self.assertEqual(
            "<p href=\"https://something.org\" target=\"_blank\" src=\"dir/\" another_prop=\"some_value\">This is a text node</p>",
            node_3.to_html()
        )

        with self.assertRaises(ValueError):
            node_4 = LeafNode(
                {
                    "href": "https://something.org",
                },
                "This is a text node"
            )

        with self.assertRaises(ValueError):
            node_5 = LeafNode(
                "This is a text node",
                {
                    "href": "https://something.org",
                }
            )


class TestParentNode(unittest.TestCase):
    def test_to_html(self):

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            node.to_html()
        )

        node_2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            "<p><b>Bold text</b>Normal text</p>",
            node_2.to_html()
        )

        node_3 = ParentNode(
            "p",
            [
                node_2,
                LeafNode(None, "Middle text"),
                node
            ],
        )

        self.assertEqual(
            "<p><p><b>Bold text</b>Normal text</p>Middle text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>",
            node_3.to_html()
        )

        with self.assertRaises(ValueError) as e:
            node_4 = ParentNode(
                None,
                [
                    node_2,
                    LeafNode(None, "Middle text"),
                    node
                ],
            )
            node_4.to_html()
        self.assertEqual(str(e.exception),
                         "Parent Nodes' tag must be a string.")

        with self.assertRaises(ValueError) as e:
            node_5 = ParentNode(
                "p",
                [],
            )
            node_5.to_html()
        self.assertEqual(str(e.exception),
                         "Parent Nodes' children must be a non-empty list.")

        with self.assertRaises(ValueError) as e:
            node_6 = ParentNode(
                "p",
                node_2
            )
            node_6.to_html()
        self.assertEqual(str(e.exception),
                         "Parent Nodes' children must be a non-empty list.")

        with self.assertRaises(ValueError) as e:
            node_6 = ParentNode(
                "p",
                node_2
            )
            node_6.to_html()
        self.assertEqual(str(e.exception),
                         "Parent Nodes' children must be a non-empty list.")


if __name__ == "__main__":
    unittest.main()
