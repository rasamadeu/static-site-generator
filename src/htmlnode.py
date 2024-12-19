from textnode import TextType

NON_CLOSING_TAGS = {"img"}


class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join(
            map(
                lambda item: f'{item[0]}="{item[1]}"',
                self.props.items(),
            )
        )

    def __repr__(self):
        separator = " " * 4
        string = f"{self.__class__.__name__}:\ntag = {self.tag}\nvalue = {self.value}\nprops = {self.props}\nchildren:\n"
        if self.children is None:
            return string
        string += "\n".join(
            map(
                lambda child: "\n".join(
                    map(
                        lambda line: separator + line,
                        str(child).split("\n")
                    )
                ),
                self.children
            )
        )
        return string


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        if tag is not None and not isinstance(tag, str):
            raise ValueError("Leaf Nodes' tag must be a string or None.")
        if not isinstance(value, str):
            raise ValueError("Leaf Nodes' value must be a string")
        super().__init__(tag, value, None, props)

    def to_html(self):

        if self.value is None:
            raise ValueError("Leaf nodes must have a value.")

        if self.tag is None:
            return self.value

        if self.tag in NON_CLOSING_TAGS:
            return f"<{self.tag}{self.props_to_html()}>"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):

        if not isinstance(self.tag, str):
            raise ValueError("Parent Nodes' tag must be a string.")
        if not isinstance(self.children, list) or len(self.children) == 0:
            raise ValueError(
                "Parent Nodes' children must be a non-empty list.")

        return f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda child: child.to_html(), self.children))}</{self.tag}>"


def text_node_to_html_node(text_node):

    value = text_node.text
    url = text_node.url
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, value)
        case TextType.BOLD:
            return LeafNode("b", value)
        case TextType.ITALIC:
            return LeafNode("i", value)
        case TextType.CODE:
            return LeafNode("code", value)
        case TextType.LINK:
            return LeafNode("a", value, {"href": url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"alt": value, "src": url})
        case _:
            raise Exception("Invalid text type.")
