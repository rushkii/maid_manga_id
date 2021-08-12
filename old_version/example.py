from maid_manga.api import MaidMangaID
import json, re

if __name__ == '__main__':
    manga = MaidMangaID()
    print(json.dumps(manga.top_manga('romance'), indent=4))