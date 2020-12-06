from bs4 import BeautifulSoup as bSoup
from urllib.parse import quote
import requests, lxml, re

class MaidMangaID(object):
    def __init__(self):
        self.base_url = "https://maid.my.id"

    def ch_html_parse(self, title='', chapter='01'):
        if chapter == '0':
            chapter = '01'
        if len(chapter) == 1:
            chapter = '0'+chapter
        if title != '':
            r = requests.get(f"{self.base_url}/{title.replace(' ', '-')}-chapter-{chapter}-bahasa-indonesia")
            s = bSoup(r.text, 'lxml')
            return s
        else:
            raise Exception('Invalid Title!')

    def manga_html_parse(self, title=''):
        if chapter == '0':
            chapter = '01'
        if len(chapter) == 1:
            chapter = '0'+chapter
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            return s
        else:
            raise Exception('Invalid Title!')

    def search(self, query=''):
        all_search = []
        r = requests.get(f"{self.base_url}/?s={quote(query)}")
        s = bSoup(r.text, 'lxml')
        mangas = s.find_all('div', class_='flexbox2-item')
        for s in mangas:
            data = {
                'thumbnail': s.find('div', class_='flexbox2-thumb').img['src'],
                'title': {
                    'japanese': s.find('span', class_='title').text
                },
                'genres': [a.text for a in s.find_all('a', rel='tag')],
                'synopsis': s.find('div', class_='synops').text,
                'chapters': re.compile("Ch. ([0-9]+)").search(s.find('div', class_='season').text).group(1).strip() if s.find('div', class_='season') is not None else "",
                'author': s.find('span', class_='studio').text,
                'rating': s.find('div', class_='score').text
            }
            all_search.append(data)
        return all_search

    def top_manga(self, genre=''):
        if genre != '':
            top = []
            r = requests.get(f"{self.base_url}/top-30-manga-{genre.lower()}")
            s = bSoup(r.text, 'lxml')
            mangas = s.find_all('div', class_='flexbox2-item')
            for s in mangas:
                data = {
                    'thumbnail': s.find('div', class_='flexbox2-thumb').img['src'],
                    'title': {
                        'japanese': s.find('span', class_='title').text
                    },
                    'genres': [a.text for a in s.find_all('a', rel='tag')],
                    'synopsis': s.find('div', class_='synops').text,
                    'chapters': re.compile("Ch. ([0-9]+)").search(s.find('div', class_='season').text).group(1).strip() if s.find('div', class_='season') is not None else "",
                    'author': s.find('span', class_='studio').text,
                    'rating': s.find('div', class_='score').text
                }
                top.append(data)
            return top 
        else:
            raise Exception('Top genre not found, available top genre: Romance, Comedy, Harem.')

    def get_manga_thumbnail(self, title=''):
        if title != '':
            s = self.manga_html_parse(title)
            thumb = s.find('div', class_='series-thumb').img['src']
            return thumb
        else:
            raise Exception('Invalid Title!')

    def get_manga_title(self, title=''):
        if title != '':
            s = self.manga_html_parse(title)
            title = s.find('div', class_='series-title').h2.text
            return title
        else:
            raise Exception('Invalid Title!')

    def get_manga_subtitle(self, title=''):
        if title != '':
            s = self.manga_html_parse(title)
            subtitle = s.find('div', class_='series-title').span.text
            return subtitle
        else:
            raise Exception('Invalid Title!')

    def get_manga_genres(self, title=''):
        if title != '':
            s = self.manga_html_parse(title)
            genres = [a.text for a in s.find_all('div', class_='series-genres')]
            return genres
        else:
            raise Exception('Invalid Title!')

    def get_manga_synopsis(self, title=''):
        if title != '':
            s = self.manga_html_parse(title)
            synopsis = s.find('div', class_='series-synops').text
            return synopsis
        else:
            raise Exception('Invalid Title!')

    def get_manga_rating(self, title=''):
        if title != '':
            s = self.manga_html_parse(title)
            rating = s.find('div', class_='series-infoz score').text
            return rating
        else:
            raise Exception('Invalid Title!')

    def get_manga_release(self, title=''):
        if title != '':
            s = self.manga_html_parse(title)
            release = s.find('span', class_='published').text
            return release
        else:
            raise Exception('Invalid Title!')

    def get_manga_author(self, title=''):
        if title != '':
            s = self.manga_html_parse(title)
            author = s.find('span', class_='author').text
            return author
        else:
            raise Exception('Invalid Title!')

    def get_images_by_chapter(self, title='', chapter='01'):
        s = self.ch_html_parse(title, chapter)
        reader = s.find_all('img', alt='image host')
        img = [img['src'] for img in reader]
        return img

    def get_manga_extended(self, title=''):
        if title != '':
            s_manga = self.manga_html_parse(title)
            s_ch = self.ch_html_parse(title, chapter='01')
            data = {
                'title': {
                    'japanese': s_manga.find('div', class_='series-title').h2.text,
                    'english': s_manga.find('div', class_='series-title').span.text
                },
                'genres': [a.text for a in s_manga.find_all('div', class_='series-genres')],
                'synopsis': s_manga.find('div', class_='series-synops').text,
                'chapters': [
                    {a.find("span", class_="ch").text: 
                        {'release-date': a.find("span", class_="date").text, 'read-url': a.a['href']}
                    } for a in s_manga.find_all('div', class_='flexch-infoz')
                ],
                'images': {
                    'thumbnail': s_manga.find('div', class_='series-thumb').img['src'],
                    'pages': [img['src'] for img in s_ch.find_all('img', alt='image host')]
                },
                'publish-date': s_manga.find('span', class_='published').text,
                'author': s_manga.find('span', class_='author').text,
                'rating': s_manga.find('div', class_='series-infoz score').text
            }
            return data
        else:
            raise Exception('Invalid Title!')

    def get_chapter_info(self, title=''):
        if title != '':
            s = self.manga_html_parse(title=title)
            d = s.find_all('div', class_='flexch-infoz')
            data = [{a.find("span", class_="ch").text: {'release-date': a.find("span", class_="date").text, 'read-url': a.a['href']}} for a in d]
            return data
        else:
            raise Exception('Invalid Title!')

    def get_chapter_list(self, title=''):
        if title != '':
            s = self.manga_html_parse(title=title)
            d = len(s.find_all('span', class_='ch'))
            return d
        else:
            raise Exception('Invalid Title!')

    def get_all_chapter_release(self, title=''):
        if title != '':
            s = self.manga_html_parse(title=title)
            d = s.find_all('div', class_='flexch-infoz')
            data = [{a.find("span", class_="ch").text: a.find("span", class_="date").text} for a in d]
            return data
        else:
            raise Exception('Invalid Title!')