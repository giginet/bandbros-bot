#! -*- coding: utf-8 -*-
#
# created by giginet on 2013/11/15
#
__author__ = 'giginet'
import urllib2
import urlparse
import datetime
import re

import lxml
from lxml.html import fromstring

BASE_URL = r'http://bandbros-p.nintendo.co.jp'

class Release(object):

    def __init__(self, tr_elem):
        tds = tr_elem.cssselect('td')
        date = tds[0].text_content()[:-2]
        self.published = self._parse_data(date)
        like = tds[1].text
        self.like = int(like) if like.isdigit() else 0
        self.title = tds[2].text_content().strip()
        self.lyrics = tds[3].text == u'あり'
        self.author = tds[4].text
        href = tds[2][0].attrib['href']
        href = href.split(';')[0]
        self.url = urlparse.urljoin(BASE_URL, href)
        self.id = re.search(r'[0-9]+', href).group(0)

    def _parse_data(self, date_string):
        date, time = date_string.split(' ')
        y, m, d = map(lambda s: int(s), date.split('-'))
        h, min, s = map(lambda  s: int(s), time.split(':'))
        return datetime.datetime(y, m, d, h, min, s)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return u'%(title)s(%(author)s)' % { 'title' : self.title, 'author' : self.author}

class Scraper(object):

    SOURCE_URL = r'%s/release/newRelease/' % BASE_URL

    def __init__(self):
        html = urllib2.urlopen(self.SOURCE_URL).read()
        dom = fromstring(html)
        release_elems = dom.cssselect('table.rankList tr')[1:]
        self.releases = [Release(tr) for tr in release_elems]


if __name__ == '__main__':
    scp = Scraper()
    #for release in scp.releases:
        #print release
