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

VERSION = '0.03'

this = sys.modules[__name__]	# For holding module globals

this.exitsupercruise = False
this.smusiclifecloud = False
this.lastsystemstring = 'No System Recorded'
this.systemnamestring = 'No System Recorded'
this.systemcodexscans = CodexScans()


def plugin_start3(plugin_dir):
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
    if method == 'Curr':
        pyperclip.copy(this.systemcodexscans.getfinalstring())
    elif method == 'Prev':

        pyperclip.copy(this.lastsystemstring)


def plugin_app(parent):
    # Build base UI
    this.frame = tk.Frame(parent, borderwidth=3)

    headerlabel = tk.Label(this.frame, text="BananaLog:")
    headerlabel.grid(row=0, column=0, sticky=tk.W) 

    currsyslabel = tk.Label(this.frame, text="Curr System:")
    currsyslabel.grid(row=1, column=0, sticky=tk.W)
    this.currsysbutton = tk.Button(this.frame, text="No System Recorded", command=lambda: update("Curr"))
    this.currsysbutton.grid(row=1, column=1, sticky=tk.W+tk.E)

    prevsyslabel = tk.Label(this.frame, text="Prev System:")
    prevsyslabel.grid(row=2, column=0, sticky=tk.W)
    this.prevsysbutton = tk.Button(this.frame, text="No System Recorded", command=lambda: update("Prev"))
    this.prevsysbutton.grid(row=2, column=1, sticky=tk.W+tk.E)
    
    return this.frame


def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry['event'] == 'FSDJump':
        # jumped to a new system, clear old scans and setup for new
        this.lastsystemstring = this.systemcodexscans.finalstring
        this.prevsysbutton["text"] = this.systemnamestring
        this.systemnamestring = system
        this.currsysbutton["text"] = system
        del this.systemcodexscans
        this.systemcodexscans = CodexScans()
        this.systemcodexscans.addsystem(system)
    elif entry['event'] == 'FSSDiscoveryScan':
        # The CMDR has honked, lets update the system
        this.currsysbutton["text"] = system
        this.systemcodexscans.addsystem(system)
    elif entry['event'] == 'FSSSignalDiscovered' and entry['SignalName_Localised'] == 'Notable stellar phenomena':
        # add to number of NSP system has
        this.systemcodexscans.addnsp()
    elif entry['event'] == 'SupercruiseEntry':
        # currently an extra condition catch for future, may remove.
        this.exitsupercruise = False
    elif entry['event'] == 'SupercruiseExit':
        # First check to see if we are in an NSP
        this.exitsupercruise = True
    elif entry['event'] == 'Music' and entry['MusicTrack'] == 'Lifeform_FogCloud' and this.exitsupercruise:
        # looks like we are at a new NSP (note we can't check if this is an already scanned NSP)
        this.exitsupercruise = False
        this.smusiclifecloud = False
        this.systemcodexscans.atnextnsp()
    elif entry['event'] == 'CodexEntry':
        #TODO stop non-NSP related entries being passed?
        this.systemcodexscans.addcodexscan(entry['Name_Localised'], cmdr, system)      
    
    



