from textnode import TextNode, TextType

def main():
    node = TextNode("Test Node", TextType.LINK, "http://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()