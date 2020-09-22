# -*- coding: utf-8 -*-
#
# BananaLog
#
# Remember to remove logging before release version
#
"""
#TODO add EDMC tick boxes for "other" section example guardian 
#TODO add duplicate checker

"""
from __future__ import print_function

import sys
import pyperclip

import logging
from config import appname

try:
    # Python 2
    import Tkinter as tk
    import ttk
except ModuleNotFoundError:
    # Python 3
    import tkinter as tk
    from tkinter import ttk
from theme import theme
from CodexScans import CodexScans

VERSION = '0.0002'

this = sys.modules[__name__]	# For holding module globals

this.exitsupercruise = False
this.smusiclifecloud = False
this.lastsystemstring = 'No System Recorded'
this.systemnamestring = 'No System Recorded'
this.systemcodexscans = CodexScans()
this.windowlog = []

# Note only compatble with EDMC 3.10+ beta
logger = logging.getLogger(f'{appname}.{"BananaLog"}') 
# logging code for Pre 4.1.0 EDMC
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()
    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)


def plugin_start3(plugin_dir):
    logger.info('BananaLog Started') 
    return plugin_start()

def plugin_start():
    # nothing to do
    return 'BananaLog'
   
   
def plugin_stop():
    """
    EDMC is closing
    """

def update(method):
    # grab button presses
    logger.info('button Press: ' + method)
    if method == 'Curr':
        pyperclip.copy(this.systemcodexscans.getfinalstring())
    elif method == 'Prev':
        pyperclip.copy(this.lastsystemstring)
    elif method == 'LogWin':
        if this.win1.winfo_exists():
            if this.win1.state() == 'withdrawn':
                this.win1.deiconify()
            else:
                this.win1.withdraw()
        else:
            this.win1 = tk.Toplevel()
            this.win1.title('BananaLog Log')
            this.lb1 = tk.Listbox(win1, height = 40, width = 50)
            this.lb1.pack(side = tk.LEFT, fill = tk.BOTH)
            for x in this.windowlog:
                this.lb1.insert(0, x)

            this.scrollbar = tk.Scrollbar(win1)
            this.scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
            this.lb1.config(yscrollcommand = this.scrollbar.set)  
            this.scrollbar.config(command = this.lb1.yview) 



def updatelogwin(log):
    this.lb1.insert(0, log)
    this.lb1.pack()
    this.windowlog.append(log)


def plugin_app(parent):
    # Build base UI
    this.frame = tk.Frame(parent, borderwidth=3)
    headerlabel = tk.Label(this.frame, text="BananaLog:")
    headerlabel.grid(row=0, column=0, sticky=tk.W) 
    currsyslabel = tk.Label(this.frame, text="Curr System:")
    currsyslabel.grid(row=1, column=0, sticky=tk.W)
    this.currsysbutton = tk.Button(this.frame, text="No System Recorded", width=20, command=lambda: update("Curr"))
    this.currsysbutton.grid(row=1, column=1, sticky=tk.W+tk.E)
    prevsyslabel = tk.Label(this.frame, text="Prev System:")
    prevsyslabel.grid(row=2, column=0, sticky=tk.W)
    this.prevsysbutton = tk.Button(this.frame, text="No System Recorded", width=20, command=lambda: update("Prev"))
    this.prevsysbutton.grid(row=2, column=1, sticky=tk.W+tk.E)
    buttonExample = tk.Button(this.frame, text="Show/Hide Log", width=20, command=lambda: update("LogWin"))
    buttonExample.grid(row=3, column=1, sticky=tk.W)

    this.win1 = tk.Toplevel()
    this.win1.title('BananaLog Log')

    this.lb1 = tk.Listbox(win1, height = 40, width = 50)
    this.lb1.pack(side = tk.LEFT, fill = tk.BOTH)
    '''
    for values in range(100): 
        this.lb1.insert(0, values)
        this.lb1.pack()
        this.windowlog.append(values) 
    '''
    this.scrollbar = tk.Scrollbar(win1)
    this.scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
    this.lb1.config(yscrollcommand = this.scrollbar.set)  
    this.scrollbar.config(command = this.lb1.yview) 

    this.win1.withdraw()
    '''
    for x in range(40):
        tst = 'Purpureum Metallic Crystals'
        updatelogwin('Scanned: ' + tst)
    '''

    return this.frame



def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry['event'] == 'FSDJump':
        # jumped to a new system, clear old scans and setup for new
        logger.info('event: FSD Jump') 
        this.lastsystemstring = this.systemcodexscans.finalstring
        this.prevsysbutton["text"] = this.systemnamestring
        this.systemnamestring = system
        this.currsysbutton["text"] = system
        logger.info('lastsystemstring: ' + this.lastsystemstring) 

        updatelogwin('Scans for System: ' + this.systemcodexscans.starsystem)
        nspsites = this.systemcodexscans.getsystemlogwinstring()
        for x in nspsites:
            updatelogwin(x)
        updatelogwin('END Scans for System'

        del this.systemcodexscans
        this.systemcodexscans = CodexScans()
        this.systemcodexscans.addsystem(system)
        
        updatelogwin('FSD Jump to: ' + entry['StarSystem'])
    elif entry['event'] == 'FSSDiscoveryScan':
        # The CMDR has honked, lets update the system
        logger.info('event: FSSDiscoveryScan') 
        this.currsysbutton["text"] = system
        this.systemcodexscans.addsystem(system)
    elif entry['event'] == 'FSSSignalDiscovered' and entry['SignalName_Localised'] == 'Notable stellar phenomena':
        # add to number of NSP system has
        logger.info('event: FSSSignalDiscovered - Notable stellar phenomen') 
        this.systemcodexscans.addnsp()
    elif entry['event'] == 'SupercruiseEntry':
        # currently an extra condition catch for future, may remove.
        logger.info('event: SupercruiseEntry') 
        updatelogwin('Supercruise')
        this.exitsupercruise = False
    elif entry['event'] == 'SupercruiseExit':
        # First check to see if we are in an NSP
        logger.info('event: SupercruiseExit') 
        this.exitsupercruise = True
    elif entry['event'] == 'Music' and entry['MusicTrack'] == 'Lifeform_FogCloud' and this.exitsupercruise:
        # looks like we are at a new NSP (note we can't check if this is an already scanned NSP)
        this.exitsupercruise = False
        this.smusiclifecloud = False
        logger.info('event: Music - Lifeform Cloud & this.exitsupercruise') 
        this.systemcodexscans.atnextnsp()
    elif entry['event'] == 'CodexEntry':
        #TODO stop non-NSP related entries being passed?
        logger.info('event: CodexEntry ' + entry['Name_Localised']) 
        updatelogwin('Scanned: ' + entry['Name_Localised'])
        this.systemcodexscans.addcodexscan(entry['Name_Localised'], cmdr, system)      
    
    



