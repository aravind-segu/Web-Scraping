import urllib2
import threading
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

price = []
title =[]
link = []
modelNumber = []
idNumber = []
threads = []
image = []

def findModel(link):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(link)
    soup = BeautifulSoup(page)
    span = soup.find("span", {"id":"ctl00_CP_ctl00_PD_lblModelNumber"})
    if not span:
        modelNumber.append("none")
    else:
        modelNumber.append(span.text)
class getPages:
    y = 0
    def getPage(self, pageNumber):
            try:
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                url = "http://www.bestbuy.ca/en-ca/category/laptops-macbooks/20352.aspx?type=product&page="+str(pageNumber)+"&pageSize=32"
                print "entered"
                print url
                page = opener.open(url)
                soup = BeautifulSoup(page)
                print "entered"
                return soup
            except:
                y = -1
                return None

class scrapingThread (threading.Thread):
    pageNumber = 0
    page_lock = threading.Lock()
    add_lock = threading.Lock()
    gp = getPages()
    def _init_(self):
        super(scrapingThread, self).__init__()
    def run(self):
        while(True):
            with scrapingThread.page_lock:
                scrapingThread.pageNumber += 1
                soup = getPages.getPage(self.gp,self.pageNumber)
            all_ul = soup.find_all("ul", class_="listing-items util_equalheight clearfix")
            if not all_ul:
                break
            else:
                self.getInformation(soup)
    def getInformation(self, soup):
        x = 0
        try:
            all_ul = soup.find_all("ul" , class_="listing-items util_equalheight clearfix")
            if not all_ul:
                return
            for ul in all_ul:
                imageLink = ul.find("img")
                images = imageLink.get("src")
                for div in ul.findAll("div", {"class":"prod-info"}):
                    h4 = div.find("h4")
                    print h4.text
                    urlLink = ("http://www.bestbuy.ca" + h4.find("a").get("href"))
                    with scrapingThread.add_lock:
                        image.append(images)
                        title.append(h4.text)
                        findModel(urlLink)
                        link.append(urlLink)
                        price.append(div.find("span", {"class": "amount"}).text)
                    print x
                    x = x + 1

        except urllib2.URLError as e:
            return

y = 1

thread1 = scrapingThread()
thread2 = scrapingThread()
thread3 = scrapingThread()
thread4 = scrapingThread()
thread5 = scrapingThread()
thread6 = scrapingThread()
thread7 = scrapingThread()
thread8 = scrapingThread()
thread9 = scrapingThread()
thread10 = scrapingThread()
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
thread10.join()
df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["Link"] = link
df["ModelNumber"] = modelNumber
df["Images"] = image
print modelNumber
df.to_csv("BestBuyLaptops.csv",index=False, encoding='utf-8')

