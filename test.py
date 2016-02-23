from EruditArticle import erudit

def print_children(child, indent=None):
    if indent == None:
        indent = ""

    for ch, elemlist in child.children().items():
        for el in elemlist:
            print("%s%s: %s" % (indent, ch, el.attr()))
            print_children(el, indent=indent+"    ")


if __name__ == '__main__':


    with open("samples/sample300_02.xml", "rb") as f:
          xmlstring = f.read()

    article = erudit.Article(xmlstring)
    # print(article.liminaire.grauteur.children())
    # print(article.liminaire.grauteur.auteur)

    print_children(article)
