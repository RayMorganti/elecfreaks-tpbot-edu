# elecfreaks-tpbot-edu

A MicroPython module for TPBot Edu, based on the MIT-licensed **pxt-TPBot** TypeScript project by **ELECFREAKS** and revisions of the MIT-licensed **TPBot.py** implementation by **lionyhw**.

## Overview

This repository provides a MicroPython implementation of TPBot Edu functionality for educational and embedded use.

It is partially based on upstream MIT-licensed work from:

### ELECFREAKS TypeScript source for TPBot Edu
- Project: **pxt-TPBot**
- Repository: https://github.com/elecfreaks/pxt-TPBot
- Source file: **V2.ts**
- File URL: https://github.com/elecfreaks/pxt-TPBot/blob/master/V2.ts
- Author: **ELECFREAKS**
- License: **MIT**
- Copyright year: **2020**

### lionyhw MicroPython source for standard TPBot
- Project: **EF_Produce_MicroPython**
- Repository: https://github.com/lionyhw/EF_Produce_MicroPython
- Source file:  **TPBot.py**
- File URL: https://github.com/lionyhw/EF_Produce_MicroPython/blob/master/TPBot.py
- Author: **lionyhw**
- License: **MIT**
- Copyright year: **2020**

Credit for the original upstream designs and implementations belongs to their respective authors.

The integration, adaptation, revision, and additional MicroPython porting work in this repository was done by **Ray Morganti**.

This repository contains only the resulting MicroPython module and related project files for TPBot Edu.  
It does **not** include the original upstream source files.

## Files

- [`tpbot_edu.py`](tpbot_edu.py.py) — the main MicroPython module
- [`examples/`](examples/) — example programs
- [`docs/changes_from_upstream_modules.md`](docs/changes_from_upstream_modules.md) — summary of key changes from the original module
- [`LICENSE`](LICENSE) — license information

## Installation

Copy [`tpbot_edu.py`](tpbot_edu.py) and [`examples/`](examples/) to your BBC micro:bit using your preferred MicroPython file transfer method.

## Development note

This revised version was developed with AI assistance. Generated code and documentation were reviewed, edited, and tested on actual Elecfreaks TPBot Edu and BBC micro:bit v2 hardware by the repository author.

## Differences from upstream modules

See [`docs/changes_from_upstream_modules.md`](docs/changes_from_upstream_modules.md)

## Compatibility

Supported:

- Elecfreaks TPBot Edu
- BBC micro:bit v2

The module in this repository has not been tested on the standard TPBot, and was not designed to be compatible with that robot.

If you are looking for a module compatible with the standard TPBot, see:

- **lionyhw / TPBot.py**  
  https://github.com/lionyhw/EF_Produce_MicroPython/blob/master/TPBot.py

## License

This project is licensed under the **MIT License**.

Because this repository is based on MIT-licensed upstream work, it preserves attribution to the original authors and includes copyright for the additional work in this repository.

See the [LICENSE](LICENSE) file for details.
