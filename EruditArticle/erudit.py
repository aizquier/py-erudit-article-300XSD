import sys
import inspect
from lxml import etree
from lxml import html
#from tgconsole import console

class Struct(dict):

    """
    * For internal use *
    dot.notation access to dictionary attributes
    """
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


def _cleantag(tag):
    """
    * For internal use *
    lxml shows tags concatenated with their namespaces in the
    form {http://namespace}tag .  This function returns extracts the
    tag name and removes the "{http://namespace}" part.
    """
    return tag.split('}')[1]


def _select_element(treeobj, tag):
    """
    * For internal use *
    selects the elements with tag 'tag' that article
    children of the element represented by the object
    'treeobj'.
    Returns a list of objtree objects. If there are not
    selected items, returns a list of the form:
        [ None ]
    """
    selected = []
    if treeobj.objtree() is not None:
        for item in treeobj.objtree().iter():
            if _cleantag(item.tag)  == tag:
                selected.append(item)

    if len(selected) == 0:
        selected.append(None)


    return selected



class Element():

    """
    * For internal use *
    The base "element" class.
    """

    def __init__(self, treeobj):
        self._attributes = Struct()
        self._treeobj = treeobj
        self._children = Struct()
        self.ch = self.children

        # * import attributes
        if self._treeobj is not None:
            for attrib in self._treeobj.attrib:
                self.attr(attrib, self._treeobj.attrib[attrib])

    def _addchild(self, tag):
        """
        Adds a child to the object's Struct of children.
        As there could appear many children with the same tag,
        a "child" is in fact a list of "Element" objects tag have the
        same tag.
        For convenience (especially when the child list only has one item),
        the first item of the "child" list is added as an instance
        attribute, so it can be accessed using dot notation.
        """

        self.children()[tag] = [Element(e) for e in _select_element(self, tag)]
        self.__dict__[tag] = self.children()[tag][0]


    def objtree(self):
        """
        Returns the element's etree object
        """
        return self._treeobj

    def children(self):
        """
        Returns the element's children Struct object
        """
        return self._children

    def attr(self, *args):
        """
        Manages element's attributes:
            el.attr()             : Gets all the attributes as a dict
            el.attr('key')        : Gets the value of attribute 'key'
            el.attr('key', 'val') : Sets the value of attribute 'key' to 'val'

        """
        if self._treeobj is not None:
            if len(args) == 0:
                #return self._attributes
                return self._attributes
            if len(args) == 1:
                try:
                    return self._attributes[args[0]]
                except KeyError:
                    return None
            if len(args) == 2:
                #console.debug(self._attributes)
                self._attributes[args[0]] = args[1]
        else:
            return None

    def xml(self):
        """
        Returns the XML contents of the element, including the tag of
        the element itself.
        """
        if self._treeobj is not None:
            return etree.tostring(self._treeobj).decode("utf-8")
        else:
            return None

    def innerxml(self):
        """
        Returns the XML contents of the element, excluding the tag of
        the element itself. (experimental)
        """
        if self._treeobj is not None:
            # * http://stackoverflow.com/questions/6123351/\
            # *    equivalent-to-innerhtml-when-using-lxml-html-to-parse-html
            return (self._treeobj.text or '') +\
              ''.join(\
                [etree.tostring(child).decode("utf-8")\
                  for child in self._treeobj.iterchildren()])
        else:
            return None

    def text(self):
        """
        Returns the contents of the element as unicode text.
        """
        if self._treeobj is not None:
            return ''.join(self._treeobj.itertext())
        else:
            return None



class Article(Element):

    """
    An EruditArticle manager. The public interface of the library.
    Inherits the Element class.
    """

    def _populatefrom(self, child, taglist):
        """
        * For internal use *
        Populate an object 'child' with subchilds whose
        tags are listed in 'taglist'
        """
        if child is not None:
            for _m in taglist:
                child._addchild(_m)

    def __init__(self, xmlstring):
        # * initializes ancestor class
        super().__init__(etree.fromstring(xmlstring))
        self.datatree = self._treeobj

        # * Verifies that 'xmlstring' complies with the schema ERUXDS300
        xmlschemaattrib = \
          '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'
        erudit3xsd = \
          'http://www.erudit.org/xsd/article http://www.erudit.org/xsd/article/3.0.0/eruditarticle.xsd'

        if xmlschemaattrib in self.attr():
            if self.attr(xmlschemaattrib) == erudit3xsd:
                iserudit3 = True
            else:
                iserudit3 = False
        else:
            iserudit3 = False

        if not iserudit3:
            print("Not an EruditArticle datastream!")
            sys.exit()

        # * *****************************************************************
        # * Extraction of ERUXDS300 sections . --Work in progress --

        # * /article
        self._populatefrom(self, ['admin', 'liminaire', 'corps', 'partiesann'])

        # * ********** ADMIN *************************************************
        # * /article/admin
        self._populatefrom(self.admin, \
         ['diffnum', 'droitsauteur', 'editeur', 'histpapier', 'infoarticle',
          'numero', 'prod', 'prodnum', 'revue', 'schema'])

        # * /article/admin/infoarticle
        self._populatefrom(self.admin.infoarticle, \
          ['grdescripteur', 'idpublic', 'manifestation', 'nbaudio', 'nbeq', \
           'nbfig', 'nbimage', 'nbmot', 'nbnote', 'nbom', 'nbpage', 'nbpara', \
           'nbrefbiblio', 'nbtabl', 'nbvideo', 'pagination', ])

        # * /article/admin/infoarticle/grdescripteur
        self._populatefrom(self.admin.infoarticle.grdescripteur,\
          [ 'descripteur', 'facette', ] )

        # * /article/admin/revue
        self._populatefrom(self.admin.revue, \
          [ 'directeur', 'grdescripteur', 'idissn', 'idissnnum', \
            'redacteurchef', 'sstitrerev', 'sstitrerevparal', 'titrerev', \
            'titrerevabr', 'titrerevabrparal', 'titrerevparal', ])

        # * /article/admin/revue/grdescripteur
        self._populatefrom(self.admin.revue.grdescripteur,\
          [ 'descripteur', 'facette', ] )

        # * /article/admin/numero
        self._populatefrom(self.admin.numero, \
          [ 'anonumero', 'grtheme', 'idisbn', 'idisbn13', 'idisbnnum', \
            'idisbnnum13', 'nonumero', 'notegen', 'pub', 'pubnum', 'volume', ])

        # * ********** LIMINAIRE ***********************************************
        # * /article/liminaire
        self._populatefrom(self.liminaire, \
         ['erratum', 'grauteur', 'grmotcle', 'grtitre', 'notegen', 'resume'])

        # * /article/liminaire/grtitre
        self._populatefrom(self.liminaire.grtitre, \
         [ 'sstitre', 'sstitreparal', 'surtitre', 'surtitre2', 'surtitre3',\
           'surtitreparal', 'surtitreparal2', 'surtitreparal3', 'titre', \
           'titreparal', 'trefbiblio', ])

        # * /article/liminaire/grauteur
        self._populatefrom(self.liminaire.grauteur, ['auteur'] )

        # * /article/liminaire/grmotcle
        self._populatefrom(self.liminaire.grmotcle, \
          ['motcle', 'titre', 'titreparal'] )

        self._populatefrom(self.liminaire.grtitre, \
          [ 'sstitre', 'sstitreparal', 'surtitre', 'surtitre2', 'surtitre3',
            'surtitreparal', 'surtitreparal2', 'surtitreparal3', 'titre',
            'titreparal', 'trefbiblio', ] )


        # * ********** CORPS     ***********************************************
        # * /article/corps <-- As most of the 'corps' element contents are
        # * text stream markup, is extracted as it *is* without
        # * further processing

        # * ********** PARTIESANN **********************************************
        # * /article/partiesann
        self._populatefrom(self.partiesann, \
          ['grannexe', 'grbiblio', 'grnote', 'grnotebio', 'merci'])

        # * /article/partiesann/grbiblio
        self._populatefrom(self.partiesann.grbiblio, ['biblio']  )

        # * /article/partiesann/grbiblio/biblio
        self._populatefrom(self.partiesann.grbiblio.biblio, ['refbiblio']  )

        # * /article/partiesann/grnote
        self._populatefrom(self.partiesann.grnote, \
          [ 'note', 'titre', 'titreparal', ]  )

        # * /article/partiesann/grnotebio
        self._populatefrom(self.partiesann.grnotebio, \
          [ 'titre', 'titreparal', 'notebio']  )

        # * /article/partiesann/grannexe
        self._populatefrom(self.partiesann.grannexe, \
          [ 'titre', 'titreparal', 'annexe']  )
