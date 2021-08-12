from typing import List, Dict
from dataclasses import dataclass
from bs4 import BeautifulSoup as bsoup
from datetime import datetime
from humanfriendly import format_size
import re, img2pdf, os


from maid_manga_id.object import Object
from maid_manga_id import http

@dataclass
class Chapters(Object):
    title: Dict[str, str] = None
    chapter: List[dict] = None
    released: int = None
    url: str = None

    async def _parse(self, **kwargs):
        kwargs['chapter'] = int(re.search(r'[\d]+', str(kwargs['chapter']))[0])
        return Chapters(**kwargs)

    async def download(self):
        if not os.path.exists('downloads/'):
            os.mkdir('downloads/')

        if isinstance(self.title, dict):
            title = f"{self.title['japanese']}-{self.title['english']}"
        else:
            title = self.title

        manga: bsoup = await http.scrape(self.url)
        reader = manga.find_all('img', alt='image host')
        img = [img['src'] for img in reader]
        
        _bytes = []

        print(f"Downloading {title}-chapter-{self.chapter} into PDF file...")
        for im,i in zip(img,range(1, len(img)+1)):  # This HTTP requests is slow, help me to make it faster.
            req = await http.new('GET', im)
            if req.status_code == 200:
                _bytes.append(req.content)
                print(f"{i}. Image size: {format_size(len(req.content))}")

        a4inpt = (img2pdf.mm_to_pt(200),img2pdf.mm_to_pt(300))
        layout_fun = img2pdf.get_layout_fun(a4inpt)

        date = datetime.now()
        path = f"downloads/{title}-chapter-{self.chapter}.pdf"

        with open(path, "wb") as f:
            f.write(img2pdf.convert(_bytes, layout_fun=layout_fun))

        print(f"Download complete, path: {path}")
        return path

    async def read(self):
        # TKinter thing
        pass