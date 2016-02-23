from EruditArticle import erudit

def print_children(child, indent=None):
    if indent == None:
        indent = ""

    for ch, elemlist in child.children().items():
        for el in elemlist:
            print("%s%s: %s" % (indent, ch, el.attr()))
            print_children(el, indent=indent+"    ")

def print_info( child, parent=None, ):


    if parent == None:
        parent = ""

    for ch, elemlist in child.children().items():
        for el in elemlist:
            elpath = parent + "."+ ch
            if el.attr() is not None:
                if len(el.attr()) != 0:
                    attrs = '( '
                    for attr, val in  el.attr().items():
                        attrs += "%s=\"%s\" " % (attr, val)
                    attrs += ')'
                else:
                    attrs = ''

                print("- %s: %s" % (elpath, attrs))
                if len(el.children()) == 0:
                    print(el.innerxml())

            print_info(el, parent=elpath)


if __name__ == '__main__':


    with open("samples/sample300_03.xml", "rb") as f:
          xmlstring = f.read()

    article = erudit.Article(xmlstring)
    # print(article.liminaire.grauteur.children())
    # print(article.liminaire.grauteur.auteur)

    #print_children(article.liminaire)
    #print_info(article, parent='article')

    print(article.partiesann.grbiblio.biblio.refbiblio.innerxml())
    print()
    print(article.partiesann.grbiblio.biblio.refbiblio.xml())
    print()
    print(article.partiesann.grbiblio.biblio.refbiblio.text())
