from typing import cast, List, Any, Union, Dict, Match
from datetime import datetime
import json, inspect

import maid_manga_id

class PrettyObject:
    __slots__: List[str] = []
    QUALNAME = "Types"

    @staticmethod
    def default(obj: "PrettyObject") -> Union[str, Dict[str, str]]:
        if isinstance(obj, bytes):
            return repr(obj)

        return {
            "_": obj.QUALNAME,
            **{
                attr: getattr(obj, attr)
                for attr in obj.__slots__
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return json.dumps(self, indent=4, default=PrettyObject.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "types.{}({})".format(
            self.QUALNAME,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in self.__slots__
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: Any) -> bool:
        for attr in self.__slots__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __len__(self) -> int:
        return len(self.write())

    def __getitem__(self, item: Any) -> Any:
        return getattr(self, item)

    def __setitem__(self, key: Any, value: Any) -> Any:
        setattr(self, key, value)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass


class Meta(type, metaclass=type("", (type,), {"__str__": lambda _: "~hi"})):
    def __str__(self):
        return f"<class 'maid_manga_id.types.{self.__name__}'>"

class Object(metaclass=Meta):
    def __init__(self, maid: "maid_manga_id.MaidManga" = None):
        self._maid = maid

    def bind(self, maid: "maid_manga_id.MaidManga"):
        self._maid = maid

    @staticmethod
    def default(obj: "Object"):
        if isinstance(obj, bytes):
            return repr(obj)

        if isinstance(obj, Match):
            return repr(obj)

        if isinstance(obj, datetime):
            return str(obj)

        return {
            "_": obj.__class__.__name__,
            **{
                attr: (
                    getattr(obj, attr)
                )
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return json.dumps(self, indent=4, default=Object.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "maid_manga_id.types.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: "Object") -> bool:
        for attr in self.__dict__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getstate__(self):
        new_dict = self.__dict__.copy()
        new_dict.pop("_maid", None)
        return new_dict

class Listing(list):
    __slots__ = []

    def __str__(self):
        return Object.__str__(self)

    def __repr__(self):
        return f"maid_manga_id.object.Listing([{','.join(Object.__repr__(i) for i in self)}])"