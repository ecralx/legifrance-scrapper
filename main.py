import requests
import bs4 as BeautifulSoup
from time import sleep
import random
import re

def slugify(value):
  """
  Normalizes string, converts to lowercase, removes non-alpha characters,
  and converts spaces to hyphens.
  """
  chars = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ '
  valid_value = ''
  for c in value:
    if c.upper() in chars:
      valid_value += c
  return valid_value

UA_list = [
  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 ',
  'Chrome/6.0.472.63 Safari/534.3',
  'Firefox/2.0.0.6',
  'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko)',
  'Chrome/6.0.472.63 Safari/534.3',
  'Safari/419.3',
  'Mozilla/5.0',
  'Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522+ (KHTML, like Gecko) ',
  'Opera/9.00 (Windows NT 5.1; U; en)',
  'Version/3.0 Mobile/1A543a Safari/419.3',
  'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko)',
  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
  'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'
]

URL = "https://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006070719"
SLEEP_TIME = 0.25

r = requests.get(url=URL)
data = r.text
soup = BeautifulSoup.BeautifulSoup(data)
pretty_links = []
liv2_PART = False
liv2_pretty_links = []

legis_part = soup.find("ul", attrs={"class":"noType"})
links = legis_part.find_all('a')
for link in links:
  href = link.get('href')
  if href[:len('affichCode.do')] != 'affichCode.do':
    pass
  if href.split('?')[1] == 'idSectionTA=LEGISCTA000006165393&cidTexte=LEGITEXT000006070719&dateTexte=20200302':
    liv2_PART = True
  if href.split('?')[1] == 'idSectionTA=LEGISCTA000006165323&cidTexte=LEGITEXT000006070719&dateTexte=20200302':
    liv2_PART = False
  
  pretty_link = "https://www.legifrance.gouv.fr/affichCode.do?" + href.split('?')[1]
  pretty_links.append(pretty_link)
  if (liv2_PART):
    liv2_pretty_links.append(pretty_link)

# for test
# pretty_links = [pretty_links[0]]

for (i, url) in enumerate(pretty_links):
  sleep(SLEEP_TIME)
  print(f'[{i}/{len(pretty_links)}] Doing {url}')
  try:
    r = requests.get(url=url, headers = {'User-Agent': random.choice(UA_list)})
    data = r.text
    soup = BeautifulSoup.BeautifulSoup(data)
    titre = soup.find('div', attrs={"class":"titreSection"}).text
    print(f'... Found {titre}')
    articles = soup.find_all('div', attrs={"corpsArt"})
    text = '\n'.join([article.text for article in articles])
    print(f'... Saving it')
    f = open(f'outputs/{slugify(titre)}.txt', 'w', encoding='utf-8')
    f.write(text)
    f.close()
    if url in liv2_pretty_links:
      f = open(f'outputs-liv2/{slugify(titre)}.txt', 'w', encoding='utf-8')
      f.write(text)
      f.close()
  except Exception as error:
    print(f'... ERROR {error}')