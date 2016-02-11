from EruditArticle import erudit

def print_children(child, indent=None):
    if indent == None:
        indent = ""

    for ch, el in child.children().items():
        print("%s%s: %s" % (indent, ch, el.attr()))
        print_children(el, indent=indent+"    ")


if __name__ == '__main__':


    with open("sample300_02.xml", "rb") as f:
          xmlstring = f.read()

    article = erudit.Article(xmlstring)

    print_children(article)
