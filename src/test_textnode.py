import unittest

from textnode import TextNode, TextType
import htmlnode as html


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)

        node_eq = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node_eq)

        node_dif_1 = TextNode("This is a text node",
                              TextType.BOLD, 'https://www.something.com')
        self.assertNotEqual(node, node_dif_1)

        node_dif_2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node_dif_2)

        node_dif_3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node_dif_3)

    def test_repr(self):
        node = TextNode("This is a text node",
                        TextType.BOLD, 'https://www.something.com')
        self.assertEqual(
            "TextNode(This is a text node, bold, https://www.something.com)",
            str(node))

    def test_url_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(None, node.url)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node(self):

        normal_node = TextNode("This is normal text", TextType.NORMAL)
        italic_node = TextNode("This is italic text", TextType.ITALIC)
        bold_node = TextNode("This is bold text", TextType.BOLD)
        code_node = TextNode("This is code text", TextType.CODE)
        link_node = TextNode("This is a link", TextType.LINK, "www.url.com")
        image_node = TextNode("This is an image", TextType.IMAGE, "dir/path")

        self.assertEqual(html.text_node_to_html_node(normal_node).to_html(),
                         "This is normal text")
        self.assertEqual(html.text_node_to_html_node(italic_node).to_html(),
                         "<i>This is italic text</i>")
        self.assertEqual(html.text_node_to_html_node(bold_node).to_html(),
                         "<b>This is bold text</b>")
        self.assertEqual(html.text_node_to_html_node(code_node).to_html(),
                         "<code>This is code text</code>")
        self.assertEqual(html.text_node_to_html_node(link_node).to_html(),
                         '<a href="www.url.com">This is a link</a>')
        self.assertEqual(html.text_node_to_html_node(image_node).to_html(),
                         '<img alt="This is an image" src="dir/path">')


if __name__ == "__main__":
    unittest.main()
