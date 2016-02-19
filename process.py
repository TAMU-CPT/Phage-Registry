from bs4 import BeautifulSoup, Comment
import requests
import json

def getPage(pageNum=1):
    url = '''http://www.ncbi.nlm.nih.gov/genomes/Genome2BE/genome2srv.cgi?action=GetGenomeList4Grid&mode=2&filterText=Caudovirales%5Borgn%5D&page={page}&pageSize=100'''
    r = requests.get(url.format(page=pageNum))
    soup = BeautifulSoup(r.text, 'html.parser')
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    comment_pos = [int(x) for x in comments[0].strip().split(' ')]
    if comment_pos[0] * comment_pos[1] > comment_pos[2]:
        more = False
    else:
        more = True

    return soup, more


def getResults(bs):
    for row in bs.find_all('tr'):
        node = row.find_all('td')[0].a
        yield (node.get('href')[8:], node.text)


def getNcbi():
    md = []
    i = 1
    while True:
        bs, m = getPage(i)
        i += 1
        data = list(getResults(bs))
        md.extend(data)
        if not m:
            break
    return json.dumps(md, indent=2)

def getPhagesdb():
    md = []
    url = '''http://phagesdb.org/ajax/allphages/'''
    d = requests.get(url)
    b = BeautifulSoup(d.text,  'html.parser')
    for i in b.find_all('tr')[1:]:
        j = i.find_all('td')[0].text
        md.append((j, j))
    return json.dumps(md, indent=2)

def getEmbl():
    url = 'https://www.ebi.ac.uk/genomes/phage.html'
    d = requests.get(url)
    b = BeautifulSoup(d.text,  'html.parser')
    q = b.find('table').find_all('tr')
    md = []
    for x in q:
        if len(x.find_all('td')) == 7:
            t = x.find_all('td')
            md.append((t[4].text, t[1].text))
    return json.dumps(md, indent=2)


with open('ncbi.json', 'w') as handle:
    handle.write(getNcbi())

with open('phagesdb.json', 'w') as handle:
    handle.write(getPhagesdb())

with open('embl.json', 'w') as handle:
    handle.write(getEmbl())
