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


class WOSCrawl(object):
    browser = None
    def __init__(self, JournalName):
        self.download_dir=os.getcwd() + '/' + JournalName 
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
        profile = webdriver.FirefoxProfile()
        profile.set_preference('self.browser.download.dir', self.download_dir)
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.dir', self.download_dir)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/x-bibtex')
        profile.set_preference('browser.helperApps.alwaysAsk.force', False)
        profile.set_preference('browser.download.manager.showWhenStarting', False)

        self.browser = webdriver.Firefox(profile)
        self.browser.implicitly_wait(10)
        self.browser.get('http://www.webofknowledge.com')

        #change the language to English
        self.browser.find_element_by_xpath('//*[@class="userCabinet nav-list"]/li[3]/a').click()
        self.browser.find_element_by_xpath('//a[@class="subnav-link" and @title="English"]').click()
        # select the database
        self.browser.find_element_by_id('collectionDropdown').click()
        self.browser.find_element_by_xpath('//a[@title="Search Web of Science Core Collection"]').click()
        #change search types to advanced search
        self.browser.find_element_by_css_selector('i.icon-dd-active-block-search').click()
        self.browser.find_element_by_xpath('//a[@title="Advanced Search"]').click()

    def set_querystring(self, querystring):
        self.browser.find_element_by_id('value(input1)').send_keys(querystring)

        select = Select(self.browser.find_element_by_id("value(input2)"))
        select.deselect_all()
        select.select_by_visible_text("English")

        select = Select(self.browser.find_element_by_id("value(input3)"))
        select.deselect_all()
        select.select_by_visible_text("All document types")

        if(not self.browser.find_element_by_xpath('//input[@value="CCR"]').is_displayed()):
           self.browser.find_element_by_css_selector('.settings-title').click()
        if(self.browser.find_element_by_xpath('//input[@value="CCR"]').is_selected()):
            self.browser.find_element_by_xpath('//input[@value="CCR"]').click()
        if(self.browser.find_element_by_xpath('//input[@value="IC"]').is_selected()):
            self.browser.find_element_by_xpath('//input[@value="IC"]').click()
        #search start
        self.browser.find_element_by_id('searchButton').click()

    def download_bib(self, markFrom, markTo):
        self.browser.find_element_by_xpath('//*[@id="s2id_saveToMenu"]/a/span[2]/b').click()
        self.browser.find_element_by_xpath('//li//div[text()="Save to Other File Formats"]').click()
        self.browser.find_element_by_id('numberOfRecordsRange').click()
        self.browser.find_element_by_name("markFrom").send_keys(str(markFrom))
        self.browser.find_element_by_name("markTo").send_keys(str(markTo))

        select = Select(self.browser.find_element_by_id("bib_fields"))
        select.select_by_visible_text("Author, Title, Source, Abstract")
        #select.select_by_visible_text("Full Record and Cited References ")
        select = Select(self.browser.find_element_by_id("saveOptions"))
        select.select_by_visible_text("HTML")
        self.browser.find_element_by_xpath('//input[@title="Send"]').click()
        self.browser.find_element_by_xpath('//a[@class="quickoutput-cancel-action" and text()="Close"]').click()
        time.sleep(10)

    def concat_files(self):
        output = open(self.download_dir + "/output.html", 'a')
        for f in glob.glob(self.download_dir + "/*.html"):
            output.write(open(f).read())
        output.close()

    def run(self):
        result_link = self.browser.find_element_by_css_selector('div.historyResults > a')
        total_items=locale.atoi(result_link.text)
        print "total %d items" % total_items
        result_link.click()
        download_times = total_items / 500
        print "total %d times to download" % download_times
        for i in range(download_times):
            self.download_bib(i*500+1, (i+1)*500)
            print "%d times download completed."%(i+1)
        self.download_bib(total_items - total_items % 500 +1 , total_items)
        self.concat_files()
        print "done."

# if __name__ == "__main__":
#     crawl = WOSCrawl("Annals of Statistics")
#     #crawl.download_dir = os.getcwd() + '/hahahah' 
#     crawl.set_querystring("SO=Annals of Statistics")
#     crawl.run()
