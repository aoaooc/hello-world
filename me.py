import requests
from bs4 import BeautifulSoup
import codecs
import csv

def getHTML(url):
    r = requests.get(url)
    return r.content

def parseHTML(html,class_tag,text_tag):
    soup = BeautifulSoup(html,'html.parser')
    
    body = soup.body
    html_list = body.find('div',attrs={'class':class_tag})
                          
    rlist = []
    for l in html_list.find_all(text_tag):
        list_url = l.attrs['href']
        list_info = l.get_text()
        if list_info.strip() != '':
            rlist.append([list_info.encode('utf-8'),list_url])
            #print list_info,list_url
    return rlist

def writeCSV(file_name,data_list):
    with open(file_name,'wb') as f:
        writer = csv.writer(f)
        for data in data_list:
            writer.writerow(data)

url2 = 'http://172.17.7.8/'
html2 = getHTML(url2)
list2 = parseHTML(html2,'content','a')

writeCSV('test.csv',list2)
