#!/usr/bin/python3.7
import xml.etree.ElementTree as etree
import os

class Palette(object):
    
    def __init__(self,filename):

        self.__tree = self.__getTree(filename)
        self.variants = self.__getVariants(self.__tree)
    
    def __getTree(self, filename):

        try:
            return etree.parse(filename).getroot()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error opening palette {filename}")

    def __getVariants(self, palette):
        return [elem for elem in palette]
    
    def getVariantElementList(self, tree):
        return [elem.tag for elem in tree]

    def getByLabel(self, tree, label):
        matchingLabel = tree.find(label)
        return matchingLabel

class SVG(object):
    
    def __init__(self, filepath):

        self.tree = self.__getTree(filepath)
        self.filepath = filepath

    def __getTree(self, filepath):

        try:
            return etree.parse(filepath).getroot()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error opening SVG {filepath}")

    # Return value for any labeled element
    def getSVGLabels(self):

        labeledElements = self.tree.iterfind('.//*[@{http://www.inkscape.org/namespaces/inkscape}label]')
        return [element.attrib.get("{http://www.inkscape.org/namespaces/inkscape}label") for element in labeledElements]
    
    # Return list containing elements matching input label
    def getByLabel(self, label):

        matchingLabel = self.tree.findall(".//*[@{http://www.inkscape.org/namespaces/inkscape}label='"+ label + "']")
        return matchingLabel.copy()

    def modStyleElements(self, svgElem, paletteElem):

        if 'style' not in svgElem.attrib:
            return

        styleAttrib = dict(x.split(':') for x in svgElem.attrib['style'].split(';'))

        for palAttrib, palAttribValue in paletteElem.items():

            if palAttribValue:
                styleAttrib[palAttrib] = palAttribValue
        
        attribString = ''.join(f'{key}:{val};'.format(key,val) for key, val in styleAttrib.items())

        svgElem.set('style', attribString)
    
    def export(self,variant):

        filename = os.path.split(os.path.abspath(self.filepath))[1]

        with open(f"{variant.tag}/{filename}", 'w') as out:
            out.write(etree.tostring(self.tree).decode('utf8'))
        out.close()