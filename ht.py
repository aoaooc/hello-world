# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import codecs
import csv
import re

DOWNLOAD_URL = 'http://www.yxccb.com.cn'

def getHTML(url):
    r = requests.get(url)
    r.connection.close()
    return r.content

def parseHTML(html,class_tag,href_tag,href):
    soup = BeautifulSoup(html,'html.parser')
    body = soup.body
    
    page_soup = body.find('div',attrs={'class':class_tag})
    
    for page_li in page_soup.find_all(href_tag):
        if page_li.get_text().encode('utf-8') == '下一页' and page_li[href] != '[NEXTPAGE]':
            return DOWNLOAD_URL+page_li[href]
        else: return None
    
def parseURL(html,class_tag,li_tag,page_tag):
    soup = BeautifulSoup(html,'html.parser')
    body = soup.body
    
    fin_soup = body.find('div',attrs={'class':class_tag})
    fin_list = []
    for fin_li in fin_soup.find_all(li_tag):
        fin_list.append(fin_li.attrs['href'])

    return fin_list

HTML = getHTML('http://www.yxccb.com.cn/ynhtyh/tzlc34/lccpfxgg18/ee50069b-1.html')
FIN_LIST = parseHTML(HTML,'list_feny','a','tagname')

def main():
    url = DOWNLOAD_URL

    with codecs.open('ht', 'wb', encoding='utf-8') as fp:
        while url:
            html = getHTML(url)
            movies, url = parse_html(html)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))


if __name__ == '__main__':
    main()
