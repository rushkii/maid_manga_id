from typing import List, Dict
from dataclasses import dataclass

from maid_manga_id.object import Object

@dataclass
class Manga(Object):
    cover: str = None
    title: Dict[str, str] = None
    genre: List[str] = None
    synopsis: str = None
    published: int = None
    author: str = None
    rating: float = None
    url: str = None
    chapters: List[dict] = None

    async def _parse(self, **kwargs):
        return Manga(**kwargs)