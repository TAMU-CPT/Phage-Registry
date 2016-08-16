from bs4 import BeautifulSoup, Comment
import requests
import json
import os
import re
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PHAGE_IN_MIDDLE = re.compile('^(?P<host>.*)\s*phage (?P<phage>.*)$')
BACTERIOPHAGE_IN_MIDDLE = re.compile('^(?P<host>.*)\s*bacteriophage (?P<phage>.*)$')
STARTS_WITH_PHAGE = re.compile('^(bacterio|vibrio|Bacterio|Vibrio|)?[Pp]hage (?P<phage>.*)$')
NEW_STYLE_NAMES = re.compile('(?P<phage>v[A-Z]_[A-Z][a-z]{2}_.*)')


def phage_name_parser(name):
    host = None
    phage = None
    name = name.replace(', complete genome.', '')
    name = name.replace(', complete genome', '')

    m = BACTERIOPHAGE_IN_MIDDLE.match(name)
    if m:
        host = m.group('host')
        phage = m.group('phage')
        return (host, phage)

    m = PHAGE_IN_MIDDLE.match(name)
    if m:
        host = m.group('host')
        phage = m.group('phage')
        return (host, phage)

    m = STARTS_WITH_PHAGE.match(name)
    if m:
        phage = m.group('phage')
        return (host, phage)

    m = NEW_STYLE_NAMES.match(name)
    if m:
        phage = m.group('phage')
        return (host, phage)

    return (host, phage)



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
            'url': 'https://www.ncbi.nlm.nih.gov/genome/' + node.get('href')[8:],
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


def fetch():
    phages = {}

    log.info("Started NCBI")
    for x in getNcbi():
        phages[x['id']] = [
                (x['typ'], x['url'])
        ]
    log.info("Finished NCBI")

    log.info("Started EMBL")
    for x in getEmbl():
        if x['id'] in phages:
            phages[x['id']].append(
                (x['typ'], x['url'])
            )
        else:
            phages[x['id']] = [
                    (x['typ'], x['url'])
            ]
    log.info("Finished EMBL")

    log.info("Started PhagesDB")
    for x in getPhagesdb():
        if x['id'] in phages:
            phages[x['id']].append(
                (x['typ'], x['url'])
            )
        else:
            phages[x['id']] = [
                    (x['typ'], x['url'])
            ]
    log.info("Finished PhagesDB")
    return phages


def cachedFetch():
    cachePath = os.path.join(SCRIPT_DIR, 'data.cache')
    if os.path.exists(cachePath):
        log.info("Using cache")
        with open(cachePath, 'r') as handle:
            data = json.load(handle)
    else:
        log.info("No cached data found")
        data = fetch()
        with open(cachePath, 'w') as handle:
            json.dump(data, handle)
    return data


def main():
    idx = 0
    phages = cachedFetch()
    for (id, data) in phages.iteritems():
        with open(os.path.join(SCRIPT_DIR, '%s.json' % idx), 'w') as handle:
            (host, phage) = phage_name_parser(id)
            x = {
                'id': id,
                'host': host,
                'phage': phage,
                'urls': json.dumps(data)
            }
            json.dump(x, handle)
            idx += 1

main()
