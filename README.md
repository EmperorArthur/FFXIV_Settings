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
    * GEARSET.DAT:  0x73
    * GS.DAT:       0x73
    * UISAVE.DAT:   0x31
    * HOTBAR.DAT:   0x31
* GEARSET.DAT:
    * General game gearset info:
        * There are 14 item slots (counting the optional soul gems)
        * Gearsets have a max name of 15 characters (Not counting the probable 0x00 at the end of the segment)
        * The game only cares about if the items are in the armory chest, not their position within the chest.
        * The game warns when a particular item can't be found
        * The game warns when a particular item is of a different color
        * Does the game warn or fail if there is an item, but it's glamored differently?
        * Does the game warn, fail, or silently succeed when substituting a non bonded item for a bonded item?
            * If both are in the armory chest, is the bonded item always chosen?
        * Does the game warn or fail a regular is substituted w/ high quality or the other way around?
        * How many gearsets can a character have?
            * Seems to vary with no good explanation:
            * https://www.reddit.com/r/ffxiv/comments/391kfk/maximum_gear_set_count/
    * Know from looking at the file:
        * Each entry takes 444 bytes (Measured from start of each gear set name)
        * Count byte before each gear set name
            * Starts at 0x00, and counts up
        * Empty entries have a 0x18 exactly 51 bytes after the count byte
            * Non empty entries have something else there
*HOTBAR.DAT:
    *General game info:
        * Each hotbar has 12 entries
        * Hotbars can be shared between classes or not
