import re
import time
import datetime
import sys
import pyperclip

class CodexScans():
    def __init__(self):
        self.starsystem = "No System Recorded"
        self.cmdr = ""
        self.nspsyscount = 0
        self.atnsp = 0
        self.nspscanscurrent = set()
        self.nspscans1 = set()
        self.nspscans2 = set()
        self.nspscans3 = set()
        self.finalstring =""

    def Local2UTC(self, LocalTime):
        # convert local datestamp to Games UTC Timezone
        # TODO make this return full and correct string?
        EpochSecond = time.mktime(LocalTime.timetuple())
        utcTime = datetime.datetime.utcfromtimestamp(EpochSecond)
        return utcTime
        
    def addnsp(self):
        self.nspsyscount += 1

    def atnextnsp(self):
        # Todo automate this for double entry checks - player returning to same NSP
        self.atnsp += 1
     
    def addsystem(self, s):
        self.starsystem = s

    def addcodexscan(self, scan, c, s): # TODO check for additional NSP sites against nspsyscount
        self.cmdr = c
        self.starsystem = s

        if self.atnsp == 0:
            # Uh-oh, we have a problem, lets ignore it and add it to NSP 1
            self.atnsp += 1
            self.nspscans1.add(scan)
        elif self.atnsp == 1:
            self.nspscans1.add(scan)
        elif self.atnsp == 2:
            self.nspscans2.add(scan)
        elif self.atnsp == 3:
            self.nspscans3.add(scan)

        self.finalstring = self.makestring()
        pyperclip.copy(self.finalstring)

    def getfinalstring(self):
        self.finalstring = self.makestring()
        return self.finalstring

    def makesitestring(self, s):
        molluscspecies = '' # bullet etc
        mollusctype = ''
        cloudstorm = ''  #storm or not
        cloudtype = ''
        crystals = [] # Storage format (ice, Rubeum, Metallic, Roseum)
        other = []
        
        for x in s:
            if "Mollusc" in x:
                splits = x.split()
                molluscspecies = splits[1]
                mollusctype = splits[0]
            elif "Cloud" in x:
                splits = x.split()
                if "Storm" in x:
                    cloudstorm = "Storm"
                cloudtype = splits[0]
            elif "Crystals" in x:
                splits = x.split()
                crystals.append(splits[1])
                crystals.append(splits[0])
            else:
                if x not in other:
                    other.append(x)

        for x in range(4):
            # quick cheat to ensure 4 crystal entries if none scanned
             crystals.append('')

        entryString = '{molluscspecies}{t}{mollusctype}{t}{cloudtype}{cloudstorm}{t}{c1a}{t}{c1b}{t}{c2a}{t}{c2b}{t}{other}'.format(
            t = '\t',
            molluscspecies = molluscspecies,
            mollusctype = mollusctype,
            cloudtype = cloudtype,
            cloudstorm = cloudstorm,
            c1a = crystals[0],
            c1b = crystals[1],
            c2a = crystals[2],
            c2b = crystals[3],
            other = ", ".join(other)
        )
        return entryString

    def makestring(self):
        nspsite1 = self.makesitestring(self.nspscans1)
        nspsite2 = self.makesitestring(self.nspscans2)
        nspsite3 = self.makesitestring(self.nspscans3)
        returnstring = ''
   
        LocalTime = datetime.datetime.now()
        UTCTime = self.Local2UTC(LocalTime)

        # TODO add correct Timestamp
        returnstring = '{timestamp}{t}{cmdr}{t}{sector}{t}{system}{t}{nspnum}{t}{yes}{t}{blank}{t}{blank}{t}{nsp1}{t}{yes}{t}{blank}{t}{blank}{t}{nsp2}{t}{yes}{t}{blank}{t}{blank}{t}{nsp3}{t}{dot}'.format(
            t = '\t',
            yes = 'Yes',
            blank = '',
            dot = ".",
            timestamp = UTCTime.strftime("%m/%d/%Y %H:%M:%S"), #Create UTC (games timezone) datetimestamp
            cmdr = self.cmdr,
            sector = self.starsystem.split()[0],
            system = self.starsystem.split(' ', 1)[1],
            nspnum = self.nspsyscount,
            nsp1 = nspsite1,
            nsp2 = nspsite2,
            nsp3 = nspsite3,

        )
    
        
        return returnstring
