from bs4 import BeautifulSoup
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import csv, os
from datetime import date, timedelta
from bs4 import BeautifulSoup

newspaper_base_url = 'http://www.prothom-alo.com/'
newspaper_archive_base_url = 'http://www.prothom-alo.com/archive/'


start_date = date(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
end_date = date(int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
delta = end_date - start_date


def process_article(url):
    content = urllib.urlopen(url).read()
    article_soup = BeautifulSoup(content, "html5lib")
    title = article_soup.title.text.decode("utf-8")
    print title
    paragraphs = article_soup.article.find('div', {'class': 'viewport'}).find('noscript').children

    news = "".decode("utf-8")
    for c in paragraphs:
        ps = BeautifulSoup(c, "html5lib")
        for p in ps.find_all('p'):
            news = news + p.text.decode("utf-8")


    return title,news







outcsv = open('./data/ProthomAlo_{}_{}.csv'.format(start_date, end_date), mode='w')
csvwritter = csv.writer(outcsv, delimiter = ',', dialect = 'excel', lineterminator = '\n')
csvwritter.writerow(["DATE", "TITLE", "NEWS"])

news_index = 1


for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)
    
    for index in range(0, 15, 1):
        print '--------------------'
        print 'checking archive page: {id} and date {d}'.format(id=index+1, d=date_str)
        print '--------------------'

        url = newspaper_archive_base_url + str(date_str) + '?edition=print&page=' + str(index + 1)
        print url

        archive_soup = BeautifulSoup(urllib.urlopen(url), "html5lib")
        all_links = archive_soup.find_all("a", attrs={"class": "link_overlay"})

        print "total links found: "+str(len(all_links))
        # check if this archive page contains any article
        if len(all_links) != 0:
            for link in all_links:
                article_url = newspaper_base_url + link.get('href')
                title, news = process_article(article_url)

                csvwritter.writerow([date_str, title, news])
                news_index += 1







print "total news saved: "+str(news_index)
outcsv.close()
