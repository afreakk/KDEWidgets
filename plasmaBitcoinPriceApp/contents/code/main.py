# -*- coding: utf-8 -*-
# Copyright stuff
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import requests
import json

label = None

class hwTempApp(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.Square)

        self.setTheme()
        self.setLayout()
        self.startTimer(10000)
        self.resize(100,50)
    def timerEvent(self,evt):
        setLabel()
    def setTheme(self):
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
    def setLayout(self):
        global label
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        label = Plasma.Label(self.applet)
        setLabel()
        self.layout.addItem(label)
        self.applet.setLayout(self.layout)

def setLabel():
    label.setText(str(getPrice()))

def getPrice():
    r = requests.get("http://data.mtgox.com/api/2/BTCUSD/money/ticker_fast")
    data = r.json()
    return data['data']['last']['display']

def CreateApplet(parent):
    return hwTempApp(parent)
