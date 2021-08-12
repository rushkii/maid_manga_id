from bs4 import BeautifulSoup as bsoup
from dateutil import parser
import re

from maid_manga_id.scaffold import Maid
from maid_manga_id import types
from maid_manga_id import http
from maid_manga_id import utils
from maid_manga_id.object import Listing

class MangaInfo(Maid):
    async def info(self, title):

        # cek jika argumennya menggunakan url
        # jika tidak maka menggunakan jalur endpoint

        # check if the argument passing the url
        # else using endpoint path
        if bool(re.match(r'((http|https):\/\/)?(www.)?maid.my.id/manga/(.*)', title)):
            url = title
        else:
            url = f"/manga/{title.replace(' ', '-')}"

        manga: bsoup = await http.scrape(url) # request ke url lalu me-return BeautifulSoup objek
                                              # requested to the url then return BeautifulSoup object
        
        cover = manga.find('div', class_='series-thumb').img.get('src')
        title = {
                'japanese': manga.find('div', class_='series-title').h2.text,
                'english': manga.find('div', class_='series-title').span.text
            }
        genre = manga.find('div', class_='series-genres')
        synopsis = manga.find('div', class_='series-synops')
        published = manga.find('span', class_='published')
        author = manga.find('span', class_='author')
        rating = manga.find('div', class_='series-infoz score')
        chapters = manga.find_all('div', class_='flexch-infoz')

        if bool(genre):
            genre = [a.text for a in genre.find_all('a')]
        else:
            genre = []

        if bool(synopsis):
            synopsis = synopsis.text
        else:
            synopsis = None

        if bool(published):
            published = parser.parse(published.text)
        else:
            published = None

        if bool(author):
            author = author.text
        else:
            author = None

        if bool(rating):
            rating = float(rating.text)
        else:
            rating = float(0)

        # menguraikan types.Chapter objek agar bekerja dengan baik
        # parsing types.Chapter object in order to work well
        if bool(chapters):
            chapters = Listing(sorted([
                await types.Chapters._parse(self,
                    title = title,
                    chapter = a.find("span", class_="ch").text,
                    released = parser.parse(utils.recognize_indo_month(
                        a.find("span", class_="date").text)),
                    url = a.a['href']
                ) for a in manga.find_all('div', class_='flexch-infoz')],
                key=lambda _: list((_).__dict__.values())[-1]))
        else:
            chapters = Listing()

        if url.startswith('/'):
            url = f'https://maid.my.id/manga{url}'
        else:
            url

        # menguraikan types.Manga object agar bekerja dengan baik
        # parsing the types.Manga object in order to work well
        parsed = await types.Manga._parse(
            self,
            cover = cover,
            title = title,
            genre = genre,
            synopsis = synopsis,
            published = published,
            author = author,
            rating = rating,
            url = url,
            chapters = chapters)
        return parsed