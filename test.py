from EruditArticle import erudit
from termcolor import colored as _c


def print_info( child, parent=None, ):
    """
    Prints recursively the 'text' contents and the attributes
    of an 'Article' object
    """

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

                print("- %s: %s" % (_c(elpath, 'yellow'), attrs))
                if len(el.children()) == 0:
                    print(el.text())
                print()

            print_info(el, parent=elpath)


if __name__ == '__main__':

    # * Read an example xml eruditarticle file into a string.
    # * In the real world, such string should come from a
    # * FedoraCommons datastream.
    with open("samples/sample300_03.xml", "rb") as f:
          xmlstring = f.read()

    # * Call py-erudit-article to build the 'article' object
    # * instance from the string 'xmlstring'
    article = erudit.Article(xmlstring)

    # * Do something useful with the created 'article' object.
    print_info(article, parent='article')
