#! -*- coding: utf-8 -*-
#
# created by giginet on 2013/11/15
#
__author__ = 'giginet'
import os
import urllib2
import urlparse
import datetime
import re
import itertools
import ConfigParser

import tweepy
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
        dom = fromstring(unicode(html, 'utf-8'))
        release_elems = dom.cssselect('table.rankList tr')[1:]
        self.releases = [Release(tr) for tr in release_elems]

class BandBrosBot(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    CACHE = os.path.join(basedir, 'cache.dat')
    MAX_RELEASES = 10
    CONFIG_PATH = r'twitter.conf'
    CONFIG_SECTION = r'Twitter'

    def __init__(self):
        self.parser = Scraper()
        cache = open(self.CACHE, 'a+')
        cache.close()

        keys = self._parse_config(self.CONFIG_PATH)
        auth = tweepy.OAuthHandler(*keys[:2])
        auth.set_access_token(*keys[2:])
        self.tw = tweepy.API(auth)

    def _parse_config(self, config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        keys = map(lambda option: config.get(self.CONFIG_SECTION, option), config.options(self.CONFIG_SECTION))
        return keys

    def _tweet_release(self, release):
        text = "NEW RELEASE : %(title)s (%(author)s) %(url)s" % {'title' : release.title, 'author' : release.author, 'url' : release.url}
        self.tw.update_status(text)

    def check_new_release(self):
        releases = self.parser.releases
        def is_not_release(release):
            return not self._is_released(release.id)
        new = list(itertools.takewhile(is_not_release, releases))
        new = new[:self.MAX_RELEASES]
        new.reverse()
        for release in new:
            try:
                self._tweet_release(release)
                self._write_cache(release.id)
            except:
                pass

    def _write_cache(self, id):
        cache = open(self.CACHE, 'a+')
        cache.write('%s\n' % id)
        cache.close()

    def _is_released(self, id):
        cache = open(self.CACHE, 'r')
        for line in cache.readlines():
            if str(id) == line.strip():
                cache.close()
                return True
        cache.close()
        return False

if __name__ == '__main__':
    bot = BandBrosBot()
    bot.check_new_release()
