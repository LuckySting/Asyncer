import aiohttp
import asyncio


class OverrideException(Exception):
    pass


class Asyncer:
    """
    Основной и единственный класс в модуле.
    """

    def __init__(self, func):
        """
        Конструктор класса.
        :param func: функция дла асинхронного выполнения.
        """
        self.func = func

    async def _a_func(self, *args):
        """
        Корутина, выполняющая func.
        :param args: аргументы для функции args.
        :return: результат выполнения func от args.
        """
        return self.func(*args)

    async def _async_tasker(self, args):
        """
        Создание списка корутин
        :param args: список списков аргументов для func
        :return: список результатов выполнения func
        """
        tasks = [asyncio.ensure_future(self._a_func(*arg)) for arg in args]
        return await asyncio.gather(*tasks)

    @classmethod
    async def _fetch(cls, url, mode='text'):
        """
        Асинхронный запрос по адресу url.
        :param session: сессия.
        :param url: адрес.
        :return: Адрес и результат запроса.
        """
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(url) as response:
                    if mode == 'json':
                        resp = await response.json()
                    else:
                        resp = await response.text()
                    print('{} - {}'.format(url, 'done'))
                    return {'url': url, 'response': resp}
        except:
            print('{} - {}'.format(url, 'FAIL'))
            return {'url': url, 'response': None}

    @classmethod
    async def _fetcher(cls, urls, mode='text'):
        """
        Создание списка запросов.
        :param: список адресов.
        :return: спискок результатов запросов.
        """
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(cls._fetch(url, mode)))
        return await asyncio.gather(*tasks)

    @classmethod
    def async_fetch(cls, urls, mode='text'):
        """
        Отправка асинхронных запросов по адресам urls.
        :param mode: тип ответа, json или text, по умолчанию text.
        :param urls: список адресов для запросов.
        :return: результаты запросов.
        """
        try:
            ioloop = asyncio.get_event_loop()
        except RuntimeError:
            ioloop = asyncio.new_event_loop()
        return ioloop.run_until_complete(cls._fetcher(urls, mode))

    def async_run(self, args):
        """
        Асинхронное выполнение func с аргументами из args.
        :param args: список списков аргументов.
        :return: список результатов выполнения
        """
        try:
            ioloop = asyncio.get_event_loop()
        except RuntimeError:
            ioloop = asyncio.new_event_loop()
        return ioloop.run_until_complete(self._async_tasker(args))
