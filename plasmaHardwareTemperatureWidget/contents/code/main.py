# -*- coding: utf-8 -*-
# Copyright stuff
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import itertools
import subprocess
import string
labels = []
class hwTempApp(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        global labels
        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.Square)

        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)

        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        makeLabels(self.applet)
        for label in labels:
            self.layout.addItem(label)
        self.applet.setLayout(self.layout)
        self.startTimer(8000)
        self.resize(400,200)
    def timerEvent(self,evt):
        strings = getStrings()
        updateLabels(strings)

def getStrings():
    raw = subprocess.check_output(["sensors"]).decode("utf8")
    raw = raw.split("\n")
    formatted = []
    for x in xrange(len(raw)):
        if not ":" in raw[x]:
            continue
        else:
            formatted.append(raw[x].replace("+",""))
    return formatted

def makeLabels(applet):
    global labels
    strings = getStrings()
    for x in xrange(len(strings)):
        labels.append(Plasma.Label(applet))
    updateLabels(strings)

def updateLabels(strings):
    for label, line in itertools.izip(labels,strings):
        label.setText(format(line))

def CreateApplet(parent):
    return hwTempApp(parent)
