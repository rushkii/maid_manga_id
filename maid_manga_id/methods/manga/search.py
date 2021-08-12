from bs4 import BeautifulSoup as bsoup
from urllib.parse import quote
from urllib.parse import urlparse
import re

from maid_manga_id.scaffold import Maid
from maid_manga_id import types
from maid_manga_id import http
from maid_manga_id.object import Listing

class MangaSearch(Maid):
    async def search(self, title):
        html: bsoup = await http.scrape(f'/?s={quote(title)}')
        result = html.find_all('div', class_='flexbox2-item')

        listed = Listing()
        
        for manga in result:
            cover = manga.find('div', class_='flexbox2-thumb').img.get('src', '').split('?')[0]
            title = manga.find('span', class_='title')
            genre = manga.find_all('a', rel='tag')
            chapter = manga.find('div', class_='season')
            author = manga.find('span', class_='studio')
            rating = manga.find('div', class_='score')
            url = manga.find('a').get('href')

            if bool(title):
                title = title.text
            else:
                title = None

            if bool(genre):
                genre = [a.text for a in genre]
            else:
                genre = []

            if bool(chapter):
                chl = Listing()
                counted = int(re.findall(r'-?\d+\.?\d*', chapter.text)[0])

                for ch in range(1, counted+1):
                    if ch < 10:
                        num = "0"
                    else:
                        num = ""

                    parse = urlparse(url)

                    chl.append(await types.Chapters._parse(
                        self,
                        title = title,
                        chapter = ch,
                        url = f"{parse.scheme}://{parse.netloc}{parse.path.replace('/manga','').rstrip('/')}-chapter-{num}{ch}-bahasa-indonesia/"
                    ))

                chapters = chl
            else:
                chapters = Listing()

            if bool(author):
                author = author.text
            else:
                author = None

            if bool(rating):
                rating = rating.text
            else:
                rating = None

            listed.append(await types.Manga._parse(
                self,
                cover = cover,
                title = title,
                genre = genre,
                author = author,
                rating = rating,
                chapters = chapters
            ))
        return listed