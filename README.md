# Maid Manga ID Wrapper
Maid Manga Indonesia wrapper using Python BeautifulSoup.
You can contact me on [LINE](https://line.me/ti/p/~your.bae_) or [Telegram](https://t.me/nekoha).

### Instalation
```sh
$ pip install maid_manga_id --upgrade
```
or
```sh
$ python setup.py install
```
### Features
- Search manga
- Get manga
- Download manga for each chapter (still development)
- and more.

### Usage
#### Get manga information
```python
from maid_manga import MaidManga
import asyncio

if __name__ == '__main__':
    maid = MaidManga()

    async def main():
        manga = await maid.info('kanojo mo kanojo')
        print(manga)

    asyncio.get_event_loop().run_until_complete(main())
```
#### Search manga
```python
from maid_manga import MaidManga
import asyncio

if __name__ == '__main__':
    maid = MaidManga()

    async def main():
        manga = await maid.search('kanojo mo kanojo')
        print(manga)

    asyncio.get_event_loop().run_until_complete(main())
```
#### Download manga each chapter
```python
from maid_manga import MaidManga
import asyncio

if __name__ == '__main__':
    maid = MaidManga()

    async def main():
        manga = await maid.info('kanojo mo kanojo')
        chapter = 1
        print(await manga.chapters[chapter-1].download())

    asyncio.get_event_loop().run_until_complete(main())
```

### Release note:
This project is under development, any meaningful pull request are opened.

### DISCLAIMER:
OOP (Object Oriented Programming) design is inspired from [this library](https://github.com/pyrogram/pyrogram)