from bs4 import BeautifulSoup
import requests

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
resp = requests.get(url)

print(resp)

soup = BeautifulSoup(resp.text)

#print(soup)

llist = soup.find_all('div', {'class':'lister'})

#print(llist)

for x in llist:
    for y in x.find_all('a'):
        print(y.text)
