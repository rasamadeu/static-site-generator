from enum import Enum
import pdb


def markdown_to_blocks(text):
    texts = text.split('\n\n')
    blocks = []
    for text in texts:
        if text != '':
            blocks.append(text.strip())
    return blocks


def block_is_heading(block):
    i = 0
    while block[i] == '#' and i < 6:
        i += 1

    if i == 0:
        return False, ''

    if block[i] == ' ':
        return True, f'h{i}'
    raise Exception(f'{block} is not a valid heading')


def block_is_code(block):
    lines = block.split('\n')
    if lines[0] == '```' and lines[-1] == '```':
        return True
    return False


def block_lines_start_with(block, char):
    lines = block.split('\n')
    length = len(char)
    for line in lines:
        if len(line) < length or line[0:length] != char:
            return False
    return True


def block_is_ordered_list(block):
    lines = block.split('\n')
    i = 1
    for line in lines:
        if len(line) < 3 or line[0:3] != f'{i}. ':
            return False
        i += 1
    return True


def block_to_block_type(block):
    is_heading, heading_type = block_is_heading(block)
    if is_heading:
        return heading_type

    if block_is_code(block):
        return 'code'

    if block_lines_start_with(block, '>'):
        return 'quote'

    if (block_lines_start_with(block, '* ')
            or block_lines_start_with(block, '- ')):
        return 'ul'

    if block_is_ordered_list(block):
        return 'ol'

    return 'p'


def block_raw_text(block):
    type = block_to_block_type(block)
    if type[0] == 'h':
        num = int(type[1]) + 1
        return [block[num:]]
    lines = block.split('\n')
    if type == 'ol':
        return list(map(lambda x: x[3:], lines))
    if type == 'ul':
        return list(map(lambda x: x[2:], lines))
    if type == 'code':
        lines = lines[1: -1]
        for i in range(len(lines) - 1):
            lines[i] += '\n'
        return lines
    for i in range(len(lines) - 1):
        lines[i] += ' '
    if type == 'p':
        return lines
    return list(map(lambda x: x[2:], lines))
