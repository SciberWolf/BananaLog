# BananaLog

A Simple Elite: Dangerous Market Connector [EDMC](https://github.com/EDCD/EDMarketConnector) plugin for the Banana Nebula Expedition.
It uses EDMC to read the Elite Dangerous Player Journal to detect when a commander uses the FSS to discover an NSP sites and the composition scanner to scan NSP objects such as Ice Crystals and then creates a string suitable for pasting into the expeditions discovery spread sheet.

###### This is a work in progress, expect bugs and use at you own risk.
###### There are many limitations to the data Elite Dangerous provides in the logs for NSP so BananaLog may produce errors in the data it provides.

## Installation & Uninstall:
Please download the plugin from the [latest release](https://github.com/SciberWolf/BananaLog/releases/latest) section on this page and then refer to the [Plugin Installation wiki](https://github.com/EDCD/EDMarketConnector/wiki/Plugins) on EDMCs own page to install into EDMC.

## Usage:
Once installed BananaLog will start to read the player log entries to try and determine NSP details for the system you are currently in.
The best procedure to follow for accurate results are:
1 - Jump into system
2 - Use your Discovery System Scanner (Honk)
3 - Scan all system objects with the FSS (this should read how many NSP sites are in the system.
4 - Supercruise to your first NSP site and once you drop into realspace use the composition scanner to scan each unique object at the site (there are normally 3 types).
5 - Repeats step 4 with any other NSP sites in the system
6 - As you follow these steps BananaLog will be copying updated data to your clipboard to paste into a blank cell on the expeditions Spreadsheet (currently formated for the "Form Responses 6" tab).

###### Buttons:
There are two buttons in the EDMC interface for BananaLog
Curr System: This button will regenerate the current system data and copy it to your clipboard.
Prev System: This will copy the last systems data to your clipboard if available. Note: After the next jump this will be cleared.

###### Tips:
Keep some notes of your discoveries in case BananaLog fails to record data correctly.
Always double check the data you paste into the spreadsheet for errors.
Avoid back tracking to the same NSP site twice as there is currently no way to see you have done this from the log.
If you leave the game Banalog will not remember the system data so you will need to start from scratch.
If the System name does not populate HONK your DSS (handy if you log into the game in an unexplored system).
If there is missing data for a system you have scanned try clicking the "Curr System" button to regenerate it.

###### Issues:
If you have any issues you can report them here or contact me on the expeditions Discord server. 

###### Acknowledgments:
Uses [Pyperclip](https://github.com/asweigart/pyperclip) by Al Sweigart

