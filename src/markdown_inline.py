import re
import pdb
from htmlnode import HTMLNode
from textnode import TextNode, TextType

DELIMITERS = {
    '**': TextType.BOLD,
    '*': TextType.ITALIC,
    '`': TextType.CODE
}

IMAGE_REGEX = r'!\[([^\[\]]+)\]\(([^\(\)]+)\)'
LINK_REGEX = r'(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)'


# This function does not function correctly if we
# want to split the text into italic blocks if the original
# text contains inline bold blocks
def split_nodes_delimiter(old_nodes, delimiter):

    if delimiter not in DELIMITERS:
        raise Exception('This function only splits normal text.')
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception('No matching closing delimiter found')
            is_normal = True
            for text in split_text:
                if is_normal:
                    new_nodes.append(TextNode(text, TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(text, DELIMITERS[delimiter]))
                is_normal = not is_normal

    return new_nodes


def extract_markdown_images(text):
    return re.findall(IMAGE_REGEX, text)


def extract_markdown_links(text):
    return re.findall(LINK_REGEX, text)


# We assume that there is always normal text, i.e., the text is not composed
# of only images
def split_nodes_image(old_nodes):

    new_nodes = []
    for node in old_nodes:
        image_nodes = extract_markdown_images(node.text)
        if image_nodes == []:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for image in image_nodes:
            text, remaining_text = remaining_text.split(
                f"![{image[0]}]({image[1]})", 1)
            if text != "":
                new_nodes.append(TextNode(text, TextType.NORMAL))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        if remaining_text != '':
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes


# We assume that there is always normal text, i.e., the text is not composed
# of only images
def split_nodes_link(old_nodes):

    new_nodes = []
    for node in old_nodes:
        link_nodes = extract_markdown_links(node.text)
        if link_nodes == []:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for link in link_nodes:
            text, remaining_text = remaining_text.split(
                f"[{link[0]}]({link[1]})", 1)
            if text != "":
                new_nodes.append(TextNode(text, TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        if remaining_text != '':
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], '**')
    new_nodes = split_nodes_delimiter(new_nodes, '*')
    new_nodes = split_nodes_delimiter(new_nodes, '`')
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
