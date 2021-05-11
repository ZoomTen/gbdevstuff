# gbdevstuff

Miscellaneous tools to help with Game Boy development and study.

* **rgbenv** (bash) - RGBDS version manager. Might be useful when dealing with forks of very old disassemblies and random repos. It requires git, curl, as well as the RGBDS build dependencies, since this will not just download binaries.

* **ImportGBSymbols** (python, ghidra) - This script allows importing RGBDS/BGB .sym files into Ghidra. It is meant to be used with the [GhidraBoy][1] extension for Ghidra.

* **ghidra2asm** (python) - This script formats disassembly output *copied* from Ghidra into a neat ASM file suitable for proper disassembly projects. Also meant to be used with [GhidraBoy][1]. Originally, it was used with the "Export Program" output, however there are fatal problems with the output - `ld [hl], 4` can be rendered as `ld hl, 4` (!!!). Copying from the Code Browser is considered safer.
