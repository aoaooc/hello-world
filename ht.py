# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import codecs
import csv
import re

DOWNLOAD_URL = 'http://www.yxccb.com.cn'
FIN_URL = 'http://www.yxccb.com.cn/ynhtyh/tzlc34/lccpfxgg18/ee50069b-1.html'

def getHTML(url):
    r = requests.get(url)
    r.connection.close()
    return r.content

def parseHTML(html,fin_tag,li_tag,page_tag,href_tag,href):
    soup = BeautifulSoup(html,'html.parser')
    body = soup.body
    
    fin_soup = body.find('div',attrs={'class':fin_tag})
    fin_list = []
    for fin_li in fin_soup.find_all(li_tag):
        fin_list.append(DOWNLOAD_URL+fin_li.attrs['href'])
    
    page_soup = body.find('ol',attrs={'class':page_tag})
    for page_li in page_soup.find_all(href_tag):
        if page_li.get_text().encode('utf-8') != '下一页':
            continue
        elif page_li[href] != '[NEXTPAGE]': 
            return fin_list,DOWNLOAD_URL+page_li[href]
        else:
            return fin_list,None

def parsePage(html,text_tag):
    soup = BeautifulSoup(html,'html.parser')
    body = soup.body
    
    text = body.find('div',attrs={'class':text_tag}).get_text()
    return text
     
def main():
    url = FIN_URL
    with codecs.open('page', 'wb', encoding='utf-8') as fp:
        while url:
            html = getHTML(url)
            fin, url = parseHTML(html,'news2','a','fl','a','tagname')
            for l in fin:
                hpage = getHTML(l)
                page = parsePage(hpage,'normal')
                fp.write(page)

if __name__ == '__main__':
    main()
