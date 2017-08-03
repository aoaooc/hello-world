import requests
from bs4 import BeautifulSoup

def getHTML(url):
    r = requests.get(url)
    return r.content

def parseHTML(html):
    soup = BeautifulSoup(html,'html.parser')
    div_people_list = soup.find('div', attrs={'class': 'story-body'})
    return div_people_list.find_all('p')
	
    

url2 = 'http://www.ftchinese.com/story/001073657'
html2 = getHTML(url2)
ax = parseHTML(html2)


for a in ax:
    name = a.get_text()
    print name
