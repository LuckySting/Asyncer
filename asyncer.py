import aiohttp
import asyncio
from multiprocessing import Pool, freeze_support


class OverrideException(Exception):
    pass


class Asyncer:

    def __init__(self, func):
        self.func = func

    async def _a_func(self, *args):
        await asyncio.sleep(1)
        return self.func(*args)

    async def _async_tasker(self, args):
        tasks = [asyncio.ensure_future(self._a_func(*arg)) for arg in args]
        return await asyncio.gather(*tasks)

    @classmethod
    async def _fetch(cls, session, url):
        async with session.get(url) as response:
            return await response.text()

    @classmethod
    async def _fetcher(cls, urls):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                tasks.append(asyncio.ensure_future(cls._fetch(session, url)))
            return await asyncio.gather(*tasks)

    @classmethod
    def async_fetch(cls, urls):
        try:
            ioloop = asyncio.get_event_loop()
        except RuntimeError:
            ioloop = asyncio.new_event_loop()
        return ioloop.run_until_complete(cls._fetcher(urls))

    def async_run(self, args):
        try:
            ioloop = asyncio.get_event_loop()
        except RuntimeError:
            ioloop = asyncio.new_event_loop()
        return ioloop.run_until_complete(self._async_tasker(args))

