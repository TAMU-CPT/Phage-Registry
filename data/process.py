from bs4 import BeautifulSoup, Comment
import requests
import json
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

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
        yield {
            'url': 'http://www.ncbi.nlm.nih.gov/genome/' + node.get('href')[8:],
            'id': node.text,
            'typ': 'ncbi',
        }


def getNcbi():
    i = 1
    while True:
        bs, m = getPage(i)
        log.info("\tNCBI page %s", i)
        i += 1
        for hit in getResults(bs):
            yield hit

        if not m:
            break


def getPhagesdb():
    url = '''http://phagesdb.org/ajax/allphages/'''
    d = requests.get(url)
    b = BeautifulSoup(d.text,  'html.parser')
    for i in b.find_all('tr')[1:]:
        j = i.find_all('td')[0].text
        yield {
            'url': 'http://phagesdb.org/phages/' + j + '/',
            'id': j,
            'typ': 'phagesdb',
        }


def getEmbl():
    url = 'https://www.ebi.ac.uk/genomes/phage.html'
    d = requests.get(url)
    b = BeautifulSoup(d.text,  'html.parser')
    q = b.find('table').find_all('tr')
    for x in q:
        if len(x.find_all('td')) == 7:
            t = x.find_all('td')
            yield {
                'url': 'http://www.ebi.ac.uk/ena/data/view/' + t[4].text,
                'id': t[1].text,
                'typ': 'embl',
            }

idx = 0

log.info("Started NCBI")
for i in getNcbi():
    idx += 1
    with open('ncbi.%s.json' % idx, 'w') as handle:
        json.dump(i, handle)
log.info("Finished NCBI")

log.info("Started PhagesDB")
for i in getPhagesdb():
    idx += 1
    with open('phagesdb.%s.json' % idx, 'w') as handle:
        json.dump(i, handle)
log.info("Finished PhagesDB")

log.info("Started EMBL")
for i in getEmbl():
    idx += 1
    with open('embl.%s.json' % idx, 'w') as handle:
        json.dump(i, handle)
log.info("Finished EMBL")
