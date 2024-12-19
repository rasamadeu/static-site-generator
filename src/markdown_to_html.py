import htmlnode
import markdown_blocks as mb
import markdown_inline as mi


def get_text_block_children(block, block_type):

    raw_texts = mb.block_raw_text(block)
    children = []
    for text in raw_texts:
        text_nodes = mi.text_to_textnodes(text)
        html_nodes = list(map(
            lambda x: htmlnode.text_node_to_html_node(x),
            text_nodes))
        if block_type in {'ul', 'ol'}:
            children.append(html_nodes)
        else:
            for html_node in html_nodes:
                children.append(html_node)
    return children


def text_block_to_html_node(block):

    block_type = mb.block_to_block_type(block)
    children = get_text_block_children(block, block_type)

    match block_type:
        case 'ul':
            children = list(map(
                            lambda child: htmlnode.ParentNode('li', child),
                            children))
            return htmlnode.ParentNode('ul', children)
        case 'ol':
            children = list(map(
                            lambda child: htmlnode.ParentNode('li', child),
                            children))
            return htmlnode.ParentNode('ol', children)
        case 'p':
            return htmlnode.ParentNode('p', children)
        case 'quote':
            return htmlnode.ParentNode('blockquote', children)
        case 'code':
            to_wrap = htmlnode.ParentNode('code', children)
            return htmlnode.ParentNode('pre', [to_wrap])

    # Remaining case is heading
    return htmlnode.ParentNode(block_type, children)


def markdown_to_html_node(markdown_text):
    markdown_blocks = mb.markdown_to_blocks(markdown_text)

    children = []
    for block in markdown_blocks:
        child = text_block_to_html_node(block)
        children.append(child)
    parent_node = htmlnode.ParentNode('div', children)
    return parent_node
