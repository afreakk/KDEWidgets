# -*- coding: utf-8 -*-
# Copyright stuff
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import json
import feedparser

labels = []
usrName = "hihmUserName"
password = "hihmPassword"
showTitle=False
updateEvery = 20
cycle = updateEvery-1
feed = None

class rssWidget(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.setLayout()
        self.startTimer(10000)

    def timerEvent(self,evt):
        setLabels(self.applet)

    def setLayout(self):
        global labels
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        setLabels(self.applet)
        for label in labels:
            self.layout.addItem(label)
        self.applet.setLayout(self.layout)

def setLabels(applet):
    global labels
    global showTitle
    global cycle
    global feed
    cycle += 1
    if cycle == updateEvery:
        feed = getFeed()
        cycle = 0
    i=0
    showTitle = not showTitle
    for entry in feed:
        if i == len(labels):
            labels.append(Plasma.Label(applet))
        if showTitle == True:
            entryString = entry.title
        else:
            entryString = entry.description
        labels[i].setText(entryString)
        i+=1

def getFeed():
    r = feedparser.parse("https://"+usrName+":"+password+"@fronter.com/hihm/rss/get_today_rss.php?elements=default&LANG=en")
    data = []
    for entry in r.entries:
        data.append(entry)
    return data

def CreateApplet(parent):
    return hwTempApp(parent)
