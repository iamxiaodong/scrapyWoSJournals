#/bin/python
# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from sys import argv
import locale
import os
import glob
import time
from wos_crawl import WOSCrawl

# set up all the journals you want to download as a python list
aList = ['Annals of Statistics', 'Biometrika']

# iteratively download the all papers in above journals, each journal as an individual folder 
for i in range(len(aList)):
    crawl = WOSCrawl(aList[i])
    crawl.set_querystring("SO=" + aList[i])
    crawl.run()
