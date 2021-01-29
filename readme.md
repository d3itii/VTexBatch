# VTexBatch

VTexBatch a command-line script for automation of creating SVG variant creation. It currently only supports SVG files created in [Inkscape](https://gitlab.com/inkscape/inkscape).

- [VTexBatch](#vtexbatch)
  - [Installation / Usage](#installation--usage)
    - [Input Formatting](#input-formatting)
  - [Contributing](#contributing)
    - [Todo](#todo)
  - [License / Credit](#license--credit)

## Installation / Usage

VTexBatch runs on Python 3.7 and requires no dependencies.

```
python3 vtexbatch.py -x [PATH TO PALETTE] [INPUT]

optional arguments:
  -h, --help    Show this help message and exit
  -o OUTPUT     Path to output directory; defaults to input directory

Input:
  -f INPUTFILE  Path to single input SVG
        OR
  -i INPUTDIR   Path to directory of SVGs

  -x PALETTE    Path to palette XML
```

An example is included in the `sample` directory, and can be tested by running:

```bash
python3 vtexbatch.py -x sample/palette.xml -f sample/sample.svg
```

### Input Formatting

Variants are defined in `Palette.xml`, and are saved to corresponding directories. Child elements, corresponding to SVG labels, may define attributes to be modified.

```xml
<palette>
    <variant1>

        <!-- Modifies the fill color of any SVG element labeled 'block1' -->
        <block1 fill="#FF0000"/>

        <!-- Modifies the stroke color of any SVG element labeled 'block2' -->
        <block2 stroke="#FF0000"/>

        <!-- Fill and Stroke attributes are present, but not defined.
            These will not be modified.
        -->
        <block3 fill="" stroke=""/>

        <!-- Any standard style attribute can be modified -->
        <block4 stroke-width="3">

    </variant1>
</palette>
```

If a defined element does not match any labels present in the SVG file, it is ignored. Similarly, any element not defined will default to the original's attributes.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Todo

* Add Adobe Illustrator support
* Add error handling for elements defined twice in a variant

## License / Credit

VTexBatch is licensed under [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html). Created by @heyitsdeity with many thanks to @makusu2.

Originally created for use in the Animal Crossing Retexture Project.
