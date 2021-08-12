from typing import Any, Callable
from functools import wraps, partial
from motor.frameworks.asyncio import _EXECUTOR
import asyncio

def to_async(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(_EXECUTOR, partial(func, *args, **kwargs))
    return wrapper

def recognize_indo_month(month_str):
    month_str = month_str.split()[0]
    ID = [
        'Januari',
        'Februari',
        'Maret',
        'April',
        'Mei',
        'Juni',
        'Juli',
        'Agustus',
        'September',
        'Oktober',
        'November',
        'Desember'
    ]
    EN = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]
    for i in range(len(ID)):
        if month_str == ID[i]:return EN[i]