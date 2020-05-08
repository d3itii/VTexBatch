#!/usr/bin/python3.7
from classes import Palette, SVG
import copy, argparse, os


def main(args):

    # Import palette file
    palette = Palette(args.palette)

    # Import files / get possible directory
    if args.inputfile:
        inputFiles = [SVG(args.inputfile)]
        outputDir = os.path.split(os.path.abspath(args.inputfile))[0] + "/"
    elif args.inputdir:
        inputFiles = [SVG(f"{os.path.abspath(args.inputdir)}/{x}") for x in os.listdir(args.inputdir) if ".svg" in x]
        outputDir = args.inputdir + "/"

    # Overwrite output dir if supplied
    if args.output:
        outputDir = args.output + "/"

    # Move all file operations to output dir
    os.chdir(outputDir)

    # Make dir for all files
    for variant in palette.variants:
        if not os.path.exists(variant.tag):
            os.mkdir(variant.tag)

    for svg in inputFiles:
        svgTags = svg.getSVGLabels()

        for variant in palette.variants: # Iterate between variants
            
            # Get palette elements for variant
            paletteElements = palette.getVariantElementList(variant)
            # Common elements between SVG and variant
            commonLabels = set(paletteElements) & set(svgTags)
            # Create a dupe to modify
            svgMod = copy.deepcopy(svg)

            print(f"Found {len(commonLabels)} variation(s) to change in {variant.tag}:")

            # Every shared label
            for label in list(commonLabels):

                svgLabel = svgMod.getByLabel(label)

                print(f"   * Changing {len(svgLabel)} instance(s) of '{label}'")

                paletteMatch = palette.getByLabel(variant, label)

                for match in svgMod.getByLabel(label):

                    svgMod.modStyleElements(match,paletteMatch)

            svgMod.export(variant)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Batch create SVG variants.")

    inGroupHeader = parser.add_argument_group(title='Input')
    
    inGroup = inGroupHeader.add_mutually_exclusive_group(required=True)

    inGroup.add_argument('-f', action="store",
                        dest="inputfile",
                        help="Path to single input SVG")
    inGroup.add_argument('-i', action="store",
                        dest="inputdir",
                        help="Path to directory of SVGs")

    inGroupHeader.add_argument('-x', action="store",
                        dest="palette", help="Path to palette XML",
                        required=True)

    parser.add_argument('-o', action="store",
                        dest="output",
                        help="Path to output directory; defaults to input directory")

    main(parser.parse_args())