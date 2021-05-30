import pandas as pd 
import urllib2
from bs4 import BeautifulSoup
from datetime import date, timedelta as td
import os
from collections import deque
import csv
from datetime import date, timedelta
#from IPython.display import display, Image

# proxy = urllib2.ProxyHandler({'http':,
#                               'https':})
# auth = urllib2.HTTPBasicAuthHandler()

# opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)

# urllib2.install_opener(opener)

def contentcrawler(link,uid):
    try:
        print("Drogon")
        page = urllib2.urlopen(link)
        print("Bareilly")
        print link, page
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Unable to Access SubLink "+str(uid))
    else:
        #try:

        # page = urllib2.urlopen(link)
        soup = BeautifulSoup(page,"html.parser")
        print(" Ki")
        # print soup
        newshead=soup.find('h1', {"class": 'title'}).text
        # print newshead
        # print barfi
        newstext=""
        textBody =soup.find_all('div', id=lambda x : x and x.startswith('content-body-14269002-'))
        # print len(textBody)
        for para in textBody[0].find_all('p'):
            if para:
                newstext=newstext+para.text.strip().replace('\n', '').replace('\r', '')
        # print newstext
        
        datesoup = soup.find('meta',{"name":'modified-date'})['content']
        print datesoup
        presdate = date(int(datesoup[:4]),int(datesoup[6:7]),int(datesoup[9:10]))
        # print presdate

        ImageLink = []
        img_links = soup.find_all('div', attrs = {'class':'img-container picture'}) + soup.find_all('div', attrs = {'class':'img-container img-full-w-cont'})
        print img_links
        for img_link in img_links:
            if img_link:
                Imglink = img_link.img['data-proxy-image'].strip()
                print Imglink
                ImageLink.append(Imglink)
                print ImageLink
                image=urllib2.urlopen(Imglink).read()
                with open('akak.png','wb') as imgfile:
                    imgfile.write(image)
                return

            
   #          print("Hello")
   #      except (KeyboardInterrupt, SystemExit):
   #          raise
   #      except:
   #          print("Error in Scraping SubLink "+str(uid))
   #      else:
           
   #          imagedir = os.getcwd()+'/hindu_image/'
   #          imagename = imagedir+ str(uid)+'.jpg'
   #          f = open(imagename,'wb')
   #          f.write(image)
   #          f.close()
   #          print("World")
   #          outputfile='hindu_news.csv'
   #          df=pd.DataFrame([[uid,newshead,newstext,presdate,link,imagelink]])
   #          print("GOT")
   #          with open(outputfile, 'a') as f:
   #              print("Night King")
   #              (df).to_csv(f, header=False,index=False,encoding='utf-8')
   #              print(" killed Viserion")
   #          print("Successfully Scraped "+str(uid))
  	# return 

def linkscrawler(link,date,lastuid):

    newslinks = []
    # link='http://www.thehindu.com/archive/web/2016/12/15/'
    try:
        #print link
        page = urllib2.urlopen(link)
        #print(page)
    except (KeyboardInterrupt,SystemExit):
        raise
    except:
        print("Unable to Access MainLink "+str(date))
    else:
        try:
            soup = BeautifulSoup(page,"html.parser")
            #print "here..."
            for link in soup.find_all('a', href=True):
                
                templink=link['href']
                
                if (templink.find('http://www.thehindu.com/')==0 and templink.endswith('.ece')):
                    # print (templink.find('http://www.thehindu.com/')==0)
                    newslinks.append(templink)
                    # print len(newslinks)
                    # print newslinks
                # for j in newslinks:
                #     print j
        except:
            print("Error in Scraping MainLink "+str(date))
    count=1
    for link in newslinks:
        uid='N'+str(date[0])+"%02d" % date[1]+"%05d" % count
        # print link
        # print lastuid
        if uid>lastuid:
            print("shivangi")
            contentcrawler(link,uid)
            return
        count+=1
        print("Aakansha")
        print("walker") 
    return 

def linksgenerator(startdate,enddate,lastuid): 
    delta=enddate-startdate
    for i in range(delta.days+1):
        currdate=startdate+timedelta(i)
        print("white")
        mainlink='http://www.thehindu.com/archive/web/'+str(currdate.year)+'/'+str("%02d" % currdate.month)+'/'+str("%02d" % currdate.day)+'/'
        print mainlink
        # linkscrawler(mainlink,[currdate.year,currdate.month,currdate.day],lastuid)

        # final_date=[currdate.year,currdate.month,currdate.day]
        linkscrawler(mainlink,[currdate.year,currdate.month,currdate.day],lastuid)
    return     

def main():
    
    if not os.path.exists(os.getcwd()+'/hindu_newspaper.csv'):
        print "BKG"
        outputfile='hindu_news.csv'
        df=pd.DataFrame([["Uid","Headline","Body","Date","NewsLink","ImageLink"]])
        print df
        df.to_csv(outputfile,header=False,index=False)
        lastuid = 'N00000000000'

    startdate = date(2016,12,31)
    enddate = date(2017,01,01)
    linksgenerator(startdate,enddate,lastuid)
    return 

main()
