import markdown_blocks as mb
from markdown_to_html import markdown_to_html_node
import os
import pdb


def extract_title(markdown):
    heading = mb.markdown_to_blocks(markdown)[0]
    if 'h1' != mb.block_to_block_type(heading):
        raise Exception('Markdown does not contain a h1 heading')
    return mb.block_raw_text(heading)[0]


def generate_page(from_path, template_path, dest_path):

    print(f'Generating page {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as f:
        markdown = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    title = extract_title(markdown)
    template = template.replace('{{ Title }}', title)

    div_node = markdown_to_html_node(markdown).to_html()
    template = template.replace('{{ Content }}', div_node)

    with open(dest_path, 'w') as f:
        f.write(template)


def generate_page_recursive(origin_dir_path, template_path, dest_dir_path):

    for path in os.listdir(origin_dir_path):
        current_origin = os.path.join(origin_dir_path, path)
        current_destiny = os.path.join(
            dest_dir_path,
            path.replace('.md', '.html'))

        if os.path.isfile(current_origin):
            if current_origin.endswith('md'):
                generate_page(
                    current_origin,
                    template_path,
                    current_destiny)
        else:
            os.mkdir(current_destiny)
            generate_page_recursive(
                current_origin, template_path, current_destiny)
