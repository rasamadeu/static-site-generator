import unittest

from textnode import TextNode, TextType
from markdown_inline import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):

        bold_node = TextNode(
            "This is text with a **bold block** word", TextType.NORMAL)
        self.assertEqual(
            split_nodes_delimiter([bold_node], "**"),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.NORMAL)
            ]
        )

        italic_node = TextNode(
            "This is text with a *italic_node block* word", TextType.NORMAL)
        self.assertEqual(
            split_nodes_delimiter([italic_node], "*"),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("italic_node block", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL)
            ]
        )

        code_node = TextNode(
            "This is text with a `code_node block` word", TextType.NORMAL)
        self.assertEqual(
            split_nodes_delimiter([code_node], "`"),
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code_node block", TextType.CODE),
                TextNode(" word", TextType.NORMAL)
            ]
        )

        several_inline_node = TextNode(
            "This *is* text with a `code block` word and **bold** text",
            TextType.NORMAL
        )
        result = split_nodes_delimiter([several_inline_node], "**")
        result = split_nodes_delimiter(result, '*')
        result = split_nodes_delimiter(result, '`')
        self.assertEqual(
            result,
            [
                TextNode("This ", TextType.NORMAL),
                TextNode("is", TextType.ITALIC),
                TextNode(" text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word and ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.NORMAL)
            ]
        )

        missing_matching = TextNode(
            "This *is italic text",
            TextType.NORMAL
        )

        with self.assertRaises(Exception) as e:
            split_nodes_delimiter([missing_matching], "*")
        self.assertEqual(str(e.exception),
                         'No matching closing delimiter found')

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text),
                         [
                         ("to boot dev", "https://www.boot.dev"),
                         ("to youtube", "https://www.youtube.com/@bootdotdev")
                         ])

    def test_extract_markdown_images(self):

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text),
                         [
                         ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                         ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
                         ])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE,
                         "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another link", TextType.LINK,
                         "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
