import re
import requests
from nanscrapers.scraper import Scraper
import xbmc

class Animetoon(Scraper):
    name = "animetoon"
    domains = ['animetoon.org']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.animetoon.org/'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb):
        try:
            if season == '1':
                url = self.base_link + title.replace(' ', '-').replace('!', '') + '-episode-' + episode
            elif season == '01':
                url = self.base_link + title.replace(' ', '-').replace('!', '') + '-episode-' + episode
            else:
                url = self.base_link + title.replace(' ','-').replace('!', '') +'-season-'+season+'-episode-'+episode
            html=requests.get(url).text
            match = re.compile('"playlist">.+?</span></div><div><iframe src="(.+?)"').findall(html)
            for url2 in match:
                self.get_sources(url2)              
            return self.sources
        except:
            pass

    def scrape_movie(self, title, year, imdb):
        try:
            start_url = 'http://www.animetoon.org/toon/search?key='+title.replace(' ','+').lower()
            html = requests.get(start_url).text
            match = re.compile('<div class="left_col">.+?<a href="(.+?)">',re.DOTALL).findall(html)
            for url in match:
                html2 = requests.get(url).text
                match2 = re.compile('&nbsp;<a href="(.+?)">(.+?)</a>').findall(html2)
                for url2, year_check in match2:
                    if year.lower() in year_check.lower():
                        self.check_for_split_streams(url2)
            return self.sources
        except:
            pass
                                

    def check_for_split_streams(self,url):
        try:
            html3 = requests.get(url).text
            match3 = re.compile('"playlist">.+?</span></div><div><iframe src="(.+?)"').findall(html3)
            for url2 in match3:
                get_sources(url2)
            block = re.compile('<span class="playlist">(.+?)"Report Video">',re.DOTALL).findall(html3)
            for item in block:
                Next = re.compile('<iframe src="(.+?)"').findall(str(item))
                for url in Next:
                    if 'mp4' in url:
                        self.get_sources(url)
        except:
            pass

    def get_sources(self,url):
        try:
            List = []
            if 'panda' in url:
                HTML = requests.get(url).text
                match2 = re.compile("url: '(.+?)'").findall(HTML)
                for url3 in match2:
                    if 'http' in url3:
                        if url3 not in List:
                            self.sources.append({'source': 'playpanda', 'quality': 'SD', 'scraper': self.name, 'url': url3, 'direct': True})
                            List.append(url3)
            elif 'easy' in url:
                HTML2 = requests.get(url).text
                match3 = re.compile("url: '(.+?)'").findall(HTML2)
                for url3 in match3:
                    if 'http' in url3:
                        if url3 not in List:
                            self.sources.append({'source': 'easyvideo', 'quality': 'SD', 'scraper': self.name, 'url': url3, 'direct': True})
                            List.append(url3)
            elif 'zoo' in url:
                HTML3 = requests.get(url).text
                match4 = re.compile("url: '(.+?)'").findall(HTML3)
                for url3 in match4:
                    if 'http' in url3:
                        if url3 not in List:
                            self.sources.append({'source': 'videozoo', 'quality': 'SD', 'scraper': self.name, 'url': url3, 'direct': True})
                            List.append(url3)
        except:
            pass
    

