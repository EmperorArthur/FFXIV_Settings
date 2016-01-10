# FFXIV Settings Extractor/Editor

Used this research as a jumping off point:
    http://ffxivexplorer.fragmenterworks.com/research.php

Currently Completed:
* FFXIV Macro Extractor:
    * A python script to decompress the FFXIV macro file, and display the results
* FFXIV Keybind Extractor:
    * A python script to decompress the FFXIV keybind file, and display the results

Research Notes:
* All files seem to be using a similar header structure, with the data itself xored.
    * 0x04 is an integer with a value of (file_size - 32)
* xor value per file:
    * MACRO.DAT:    0x73
    * KEYBIND.DAT:  0x73
    * UISAVE.DAT:   0x31