import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_raw_text
)


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
    '''
        self.assertListEqual(
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                '''* This is the first list item in a list block
* This is a list item
* This is another list item'''
            ],
            markdown_to_blocks(text)
        )

    def test_block_to_block_type(self):
        headings = '''# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6'''
        result = []
        for block in markdown_to_blocks(headings):
            result.append(block_to_block_type(block))
        self.assertEqual([
                         "h1",
                         "h2",
                         "h3",
                         "h4",
                         "h5",
                         "h6"
                         ],
                         result)
        ul = '''* Item 1
* Item 2
* Item 3'''
        self.assertEqual(block_to_block_type(ul), 'ul')

        ul = '''- Item 1
- Item 2
- Item 3'''
        self.assertEqual(block_to_block_type(ul), 'ul')

        ol = '''1. Item 1
2. Item 2
3. Item 3'''
        self.assertEqual(block_to_block_type(ol), 'ol')

        quote = "> This is a quote."
        self.assertEqual(block_to_block_type(quote), 'quote')

        code = '''```
This is code
```'''
        self.assertEqual(block_to_block_type(code), 'code')

        paragraph = 'Just a normal phrase.'
        self.assertEqual(block_to_block_type(paragraph), 'p')

    def test_block_raw_text(self):
        headings = '''# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6'''
        result = []
        for block in markdown_to_blocks(headings):
            result.append(block_raw_text(block))
        self.assertEqual([
                         ["Heading 1"],
                         ["Heading 2"],
                         ["Heading 3"],
                         ["Heading 4"],
                         ["Heading 5"],
                         ["Heading 6"]
                         ],
                         result)
        ul = '''* Item 1
* Item 2
* Item 3'''
        self.assertEqual(block_raw_text(ul), ['Item 1', 'Item 2', 'Item 3'])

        ul = '''- Item 1
- Item 2
- Item 3'''
        self.assertEqual(block_raw_text(ul), ['Item 1', 'Item 2', 'Item 3'])

        ol = '''1. Item 1
2. Item 2
3. Item 3'''
        self.assertEqual(block_raw_text(ol), ['Item 1', 'Item 2', 'Item 3'])

        quote = "> This is a quote."
        self.assertEqual(block_raw_text(quote), ['This is a quote.'])

        code = '''```
This is code
and another one
```'''
        self.assertEqual(block_raw_text(code), [
                         'This is code ', 'and another one'])

        paragraph = 'Just a normal phrase.'
        self.assertEqual(block_raw_text(paragraph), ['Just a normal phrase.'])


if __name__ == "__main__":
    unittest.main()
