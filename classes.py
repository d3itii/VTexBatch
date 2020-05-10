#!/usr/bin/python3.7
import xml.etree.ElementTree as etree
import os


class Palette():

    """Palette instance"""

    def __init__(self, filename):

        self.__tree = self.__get_tree(filename)
        self.variants = self.__get_variants(self.__tree)

    def __get_tree(self, filename):

        try:
            return etree.parse(filename).getroot()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error opening palette {filename}")

    def __get_variants(self, palette):
        return [elem for elem in palette]

    def getVariantElementList(self, tree):
        return [elem.tag for elem in tree]

    def get_by_label(self, tree, label):
        matching_label = tree.find(label)
        return matching_label

class SVG():

    """SVG instance"""

    def __init__(self, filepath):
        self.tree = self.__get_tree(filepath)
        self.filepath = filepath

    def __get_tree(self, filepath):
        """Get SVG XML Tree"""
        try:
            return etree.parse(filepath).getroot()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error opening SVG {filepath}")

    def get_svg_labels(self):
        """Return value for any labeled element"""
        labeled_elements = self.tree.iterfind('.//*[@{http://www.inkscape.org/namespaces/inkscape}label]')
        return [element.attrib.get("{http://www.inkscape.org/namespaces/inkscape}label") for element in labeled_elements]

    def get_by_label(self, label):
        """Return list containing elements matching input label"""
        matching_label = self.tree.findall(".//*[@{http://www.inkscape.org/namespaces/inkscape}label='" + label + "']")
        return matching_label.copy()

    def mod_elements(self, svg_elem, palette_elem):
        """Set SVG style element to palette definition"""
        if 'style' not in svg_elem.attrib:
            return

        style_attrib = dict(x.split(':') for x in svg_elem.attrib['style'].split(';'))

        for palette_attrib, palette_attrib_value in palette_elem.items():
            if palette_attrib_value:
                style_attrib[palette_attrib] = palette_attrib_value

        attrib_string = ''.join(f'{key}:{val};'.format(key, val)
                                for key, val in style_attrib.items())

        svg_elem.set('style', attrib_string)

    def export(self, variant):
        """Export SVG variant"""
        filename = os.path.split(os.path.abspath(self.filepath))[1]
        export = f"{variant.tag}/{filename}"

        with open(export, 'w') as out:
            out.write(etree.tostring(self.tree).decode('utf8'))
        out.close()

        print(f"Created {export}")
