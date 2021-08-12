# Maid Manga ID API
Maid Manga Indonesia API Using Python Web Scraper.
You can contact me on [LINE](https://line.me/ti/p/~your.bae_).

### Instalation
```sh
$ pip install maid_manga_id --upgrade
```
or
```sh
$ python setup.py install
```
### Features
- Search
- Top Manga based-on genres
- Get Manga Full Info
- Get Chapter Image Page
- and more.

### Usage
#### Get Manga but Extended Version
```python
from maid_manga.api import MaidMangaID

if __name__ == '__main__':
    manga = MaidMangaID()
    print(manga.get_manga_extended(title='kanojo mo kanojo'))
```
#### Get Manga Author
```python
from maid_manga.api import MaidMangaID

if __name__ == '__main__':
    manga = MaidMangaID()
    print(manga.get_manga_author(title='kanojo mo kanojo'))
```
