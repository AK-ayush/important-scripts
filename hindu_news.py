import pandas as pd 
import urllib2
from bs4 import BeautifulSoup
from datetime import date, timedelta as td
import os
from collections import deque
import csv
from datetime import date, timedelta

#use your proxy here
#proxy = urllib2.ProxyHandler({'http':'',
#                              'https':''})
#auth = urllib2.HTTPBasicAuthHandler()
#
#opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
#
#urllib2.install_opener(opener)


def crawlArticle(newsLink, uid, currdate):
    page = urllib2.urlopen(newsLink).read()
    soup = BeautifulSoup(page, "html.parser") 
    
    #scrapping title
    Title =""
    title_tag = soup.find('h1', attrs={'class': 'title'})
    if title_tag:
        Title = title_tag.text.strip().replace('\n', ' ').replace('\r', '').encode("utf-8")
        #print Title

    #scrapping Headline
    Headline = ""
    headLine_tag = soup.find('h2', attrs={'class': 'intro'})
    if headLine_tag:
        Headline = headLine_tag.text.strip().replace('\n', ' ').replace('\r', '').encode("utf-8") # strip() is used to remove starting and trailing spaces
        #print Headline

    #scrapping Body  and 
    BodyText = ""
    body_tags = soup.find_all('div', id=lambda x : x and x.startswith('content-body-14269002-'))
    for para in body_tags[0].find_all('p'):
        #print para.text.strip()
        if para:
            BodyText = BodyText + para.text.strip().replace('\n', ' ').replace('\r', '').encode("utf-8")
    #print BodyText
    
    #scrapping image links
    ImageLink = []
    img_links = soup.find_all('div', attrs = {'class':'img-container picture'}) + soup.find_all('div', attrs = {'class':'img-container img-full-w-cont'})
    for img_link in img_links:
        if img_link:
            ImageLink.append(img_link.img['data-proxy-image'].strip().encode("utf-8"))

    #print ImageLink 
    print "Writing row for Uid:"+ str(uid)+"..."   
    with open("hindu_news.csv", "a") as toWrite:
        writer = csv.writer(toWrite, delimiter=",")
        writer.writerow([uid, '['+Title+Headline+']', '['+BodyText+']', str(currdate), newsLink.encode("utf-8"), ImageLink])

def main():
    
    if not os.path.exists(os.getcwd()+'/hindu_news.csv'):
        print "BKG"
        outputfile='hindu_news.csv'
        df=pd.DataFrame([["Uid","Headline","Body","Date","NewsLink","ImageLink"]])
        print df
        df.to_csv(outputfile,header=False,index=False)
        
    lastuid = 'N00000000000'
    startdate = date(2016,12,15)
    enddate = date(2017,01,14)
    delta=enddate-startdate

    for i in range(delta.days+1):
        currdate=startdate+timedelta(i)
        #print("white")
        mainlink='http://www.thehindu.com/archive/web/'+str(currdate.year)+'/'+str("%02d" % currdate.month)+'/'+str("%02d" % currdate.day)+'/'
        print mainlink
        # linkscrawler(mainlink,[currdate.year,currdate.month,currdate.day],lastuid)

        final_date=[currdate.year,currdate.month,currdate.day]
        newslinks = []
        # link='http://www.thehindu.com/archive/web/2016/12/15/'
        try:
            #print mainlink
            page = urllib2.urlopen(mainlink).read()
            #print(page)
        except (KeyboardInterrupt,SystemExit):
            raise
        except:
            print("Unable to Access MainLink "+str(currdate))
        else:
            try:
                soup = BeautifulSoup(page, "html.parser")
        
                for link in soup.find_all('a', href=True):
                    
                    templink=link['href']
                    if (templink.find('http://www.thehindu.com/')==0 and templink.endswith('.ece')):
                        #print (templink.find('http://www.thehindu.com/')==0)
                        newslinks.append(templink)
                        #print templink
                        #return 
                        # print newslinks

            except:
                print("Error in Scraping MainLink "+str(currdate))

        count=1
        for link in newslinks:
            uid='N'+str(final_date[0])+"%02d" % final_date[1]+"%05d" % count
            #print uid
            crawlArticle(link, uid, currdate)
            # print lastuid
            if uid>lastuid:
                print("Last Uid")
                count+=1
            #print("walker")
            if count >= 20:
                return

if __name__ == '__main__':
    main()
    nl = 'http://www.thehindu.com/opinion/op-ed/the-superbugs-of-hyderabad/article20536685.ece'
    nl2 = 'http://www.thehindu.com/entertainment/dance/Dance-and-its-many-dimensions/article16834097.ece'
    uid = 'N000001234'
    #crawlArticle(nl ,uid)
