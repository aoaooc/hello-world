import requests
from bs4 import BeautifulSoup
import codecs
import csv
import re

def getHTML(url):
    r = requests.get(url)
    #s = requests.session()
    #s.config['keep_alive'] = False
    r.connection.close()
    return r.content

def parseUrl(html,class_tag,url_tag):
    soup = BeautifulSoup(html,'html.parser')
    
    body = soup.body
    html_list = body.find('div',attrs={'class':class_tag})
                          
    rlist = []
    for l in html_list.find_all(url_tag):
        list_url = l.attrs['href']
        rlist.append([list_url])
    return rlist

def parseHTML(html,title_tag,text_tag):
    soup = BeautifulSoup(html,'html.parser')
    
    body = soup.body
    title = body.find('div',attrs={'class':title_tag}).get_text()
    text = body.find('div',attrs={'class':text_tag}).get_text()
    
    rlist = []
    rlist.append([title.encode('utf-8'),text.encode('utf-8')]) 
    
    return rlist

def writeCSV(file_name,data_list):
    with open(file_name,'wb') as f:
        writer = csv.writer(f)
        for data in data_list:
            writer.writerow(data)


url = 'http://www.fudian-bank.com'
url2 = 'http://www.fudian-bank.com/html/lccpgg/index.html'
url3 = 'http://www.fudian-bank.com/html/lccpgg/index'
html2 = getHTML(url2)
url_list = parseUrl(html2,'readmain1_body2_text','a')

pattern = re.compile(r'[\d]+')
match = pattern.findall(url_list[-1][0])

tlist = []
for i in range(1,30):
    if i == 1:
        urlx = url3+'.html'
    else: urlx = url3+'_'+str(i)+'.html'
        
    htmlx = getHTML(urlx)
    
    urlx_list = []
    urlx_list = parseUrl(htmlx,'readmain1_body2_text','a')
    
    for j in range(1,len(urlx_list)):
        if re.search('content',urlx_list[j][0]):
            htmly = getHTML(url+urlx_list[j][0])
            tmp = []
            tmp = parseHTML(htmly,'readmain1_body2_texttitle','textall')
            tlist.append([url+urlx_list[j][0],tmp[0][0],tmp[0][1]])
    
writeCSV('test.csv',tlist)
