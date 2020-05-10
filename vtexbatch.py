#!/usr/bin/python3.7
import copy
import argparse
import os
from classes import Palette, SVG


def main(args):
    """Main"""

    # Import palette file
    palette = Palette(args.palette)

    # Import files / get possible directory
    # Overwrite output dir if supplied
    if args.inputfile:
        input_files = [SVG(args.inputfile)]
        output_dir = f"{os.path.split(os.path.abspath(args.inputfile))[0]}/"
    elif args.inputdir:
        input_files = [SVG(f"{os.path.abspath(args.inputdir)}/{x}")
                       for x in os.listdir(args.inputdir) if ".svg" in x]
        output_dir = f"{args.inputdir}/"
    if args.output:
        output_dir = f"{args.output}/"

    # Move all file operations to output dir
    # Make any non-existant subdirs
    os.chdir(output_dir)
    for variant in palette.variants:
        if not os.path.exists(variant.tag):
            os.mkdir(variant.tag)

    for svg in input_files:
        svg_tags = svg.get_svg_labels()

        for variant in palette.variants:
            palette_elements = palette.getVariantElementList(variant)
            common_labels = set(palette_elements) & set(svg_tags)
            modified_svg = copy.deepcopy(svg)

            for label in list(common_labels):
                palette_match = palette.get_by_label(variant, label)
                for match in modified_svg.get_by_label(label):
                    modified_svg.mod_elements(match, palette_match)

            modified_svg.export(variant)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Batch create SVG variants.")

    inGroupHeader = parser.add_argument_group(title='Input')
    inGroup = inGroupHeader.add_mutually_exclusive_group(required=True)
    inGroupHeader.add_argument('-x', action="store",
                               dest="palette", help="Path to palette XML",
                               required=True)

    inGroup.add_argument('-f', action="store",
                         dest="inputfile",
                         help="Path to single input SVG")
    inGroup.add_argument('-i', action="store",
                         dest="inputdir",
                         help="Path to directory of SVGs")

    parser.add_argument('-o', action="store",
                        dest="output",
                        help="Path to output directory; defaults to input directory")

    main(parser.parse_args())
