# -*- coding: utf-8 -*-
'''
The purpose of this script is to store RuneScape quests locally into word documents for entertainment as a reminder of past gameplay experiences.
The copyright of the quests' content belongs of Jagex.
'''
import requests
import re
import sys
import os
from docx import Document
from docx.shared import Pt

from quests import questParser
from links import linkParser

# Check encoding
cencode = sys.getdefaultencoding()
if sys.stdout.encoding != cencode:
  cencode = sys.stdout.encoding

'''
# main function 
# Step 1: Get two pages of quest names:
allTranscripts = requests.get('https://runescape.fandom.com/wiki/Category:Quest_transcript')
webObj = linkParser()
webObj.feed(allTranscripts.text)
for link in range(len(webObj.links)):
  if "runescape.fandom.com" in webObj.links[link]:
    webObj.links = webObj.links[0:link] + webObj.links[link+1]
    moreTranscripts = requests.get(webObj.links[link])
    webObj.feed(moreTranscripts.text)
webObj.links = webObj.links[-1]

# Intermediate I: Store links
(open("links.txt", "w", encoding="utf8")).write("\n".join(webObj.links))

# Intermediate II: Reading from links
text = ((open("links.txt", "r", encoding="utf8")).read()).split("\n")

# Step 2: Get quest info from link
for t in text:
  questText = questParser()
  res = requests.get("https://runescape.fandom.com" + t)
  questText.feed(res.text)
'''