from bs4 import BeautifulSoup as bSoup
import requests, lxml

class MaidMangaID:
    def __init__(self):
        self.base_url = "https://maid.my.id"

    def read_html_parse(self, title='', chapter='01'):
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

    def get_manga_thumbnail(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            thumb = s.find('div', class_='series-thumb').img['src']
            return thumb
        else:
            raise Exception('Invalid Title!')

    def get_manga_title(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            title = s.find('div', class_='series-title').h2.text
            return title
        else:
            raise Exception('Invalid Title!')

    def get_manga_subtitle(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            subtitle = s.find('div', class_='series-title').span.text
            return subtitle
        else:
            raise Exception('Invalid Title!')

    def get_manga_genres(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            genres = [a.text for a in s.find_all('div', class_='series-genres')]
            return genres
        else:
            raise Exception('Invalid Title!')

    def get_manga_synopsis(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            synopsis = s.find('div', class_='series-synops').text
            return synopsis
        else:
            raise Exception('Invalid Title!')

    def get_manga_rating(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            rating = s.find('div', class_='series-infoz score').text
            return rating
        else:
            raise Exception('Invalid Title!')

    def get_manga_release(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            release = s.find('span', class_='published').text
            return release
        else:
            raise Exception('Invalid Title!')

    def get_manga_author(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            author = s.find('span', class_='author').text
            return author
        else:
            raise Exception('Invalid Title!')

    def get_chapter_info(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            d = s.find_all('div', class_='flexch-infoz')
            data = [{a.find("span", class_="ch").text: {'release-date': a.find("span", class_="date").text, 'read-url': a.a['href']}} for a in d]
            return data
        else:
            raise Exception('Invalid Title!')

    def get_chapter_list(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            d = len(s.find_all('span', class_='ch'))
            return d
        else:
            raise Exception('Invalid Title!')

    def get_all_chapter_release(self, title=''):
        if title != '':
            r = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s = bSoup(r.text, 'lxml')
            d = s.find_all('div', class_='flexch-infoz')
            data = [{a.find("span", class_="ch").text: a.find("span", class_="date").text} for a in d]
            return data
        else:
            raise Exception('Invalid Title!')

    def get_images_by_chapter(self, title='', chapter='01'):
        s = self.read_html_parse(title, chapter)
        reader = s.find_all('img', alt='image host')
        img = [img['src'] for img in reader]
        return img

    def get_manga_extended(self, title=''):
        if title != '':
            r_manga = requests.get(f"{self.base_url}/manga/{title.replace(' ', '-')}")
            s_manga = bSoup(r_manga.text, 'lxml')
            s_ch = self.read_html_parse(title, chapter='01')
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