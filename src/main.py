from copy_static_to_public import copy_static_to_public
from generate_page import generate_page_recursive


def main():
    copy_static_to_public()
    generate_page_recursive('./content',
                            './template.html',
                            './public')

    return 0


if __name__ == "__main__":
    main()
