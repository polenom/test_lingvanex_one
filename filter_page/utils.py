import asyncio
import sys
from asyncio import Queue
from asyncio.exceptions import TimeoutError
import re

import aiohttp
import urllib

from aiohttp import ClientSession, ClientConnectorError


class ParcerApps:
    url = 'https://apps.microsoft.com/store/category/Business'
    _url_filter = 'https://apps.microsoft.com/store/api/Products/GetFilteredProducts/?hl=en-gb&gl=US&NoItems=24&Category=Business'
    _url_cursor = 'https://apps.microsoft.com/store/api/Products/GetFilteredProducts/?hl=en-gb&gl=US&NoItems=24&Category=Business&Cursor='
    _url_product = 'https://apps.microsoft.com/store/api/ProductsDetails/GetProductDetailsById/'

    def __init__(self):
        self._companies = []
        self._run_status = False

    @classmethod
    def run(cls):
        service = cls()
        try:
            asyncio.run(service.main())
        except (ClientConnectorError, TimeoutError) as e:
            print(e)
        return service

    async def main(self):
        q = Queue()
        loop = asyncio.get_running_loop()
        async with aiohttp.ClientSession() as session:
            task_one_products = loop.create_task(self._get_products(session, q))
            task_two_product = loop.create_task(self._get_product(session, q))
            await asyncio.gather(task_one_products, task_two_product)

    async def _request(self, session: ClientSession, url: str):
        timer = [60, 30, 15, 7, 3, 2, 1, 1]
        timeout = aiohttp.ClientTimeout(total=10)
        while True:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    return await response.json()
                if timer:
                    await asyncio.sleep(timer.pop())
                    continue
            raise TimeoutError

    async def _request_from_product(self, session: ClientSession, url: str):
        response = await self._request(session, url)
        company_dict = self._create_company(response)
        self._companies.append(company_dict)

    async def _get_products(self, session: ClientSession, queue: Queue):
        value_cursor = ''
        while True:
            full_url = self._url_cursor + urllib.parse.quote(value_cursor)
            response = await self._request(session, full_url)
            product_ids = [i['productId'] for i in response['productsList']]
            queue.put_nowait(product_ids)
            if not response.get('cursor'):
                queue.put_nowait(None)
                break
            value_cursor = response.get('cursor')

    async def _get_product(self, session: ClientSession, queue: Queue):
        count = 0
        while True:
            products_ids = await queue.get()
            if products_ids is None:
                print(f'Count: {count}')
                break
            print(f'Count: {count}', end='\r')
            tasks = []
            for id in products_ids:
                url = self._url_product + id + '?hl=en-gb&gl=US'
                tasks.append(self._request_from_product(session, url))
            await asyncio.gather(*tasks)
            count += len(products_ids)


    def _get_email(self, text: str) -> str | None:
        index_email = text.rfind('email')
        if index_email >= 0:
            pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
            result_find = re.findall(pattern, text[index_email:])
            if result_find:
                return result_find[0]

    def get_date(self):
        return self._companies

    def _create_company(self, response: dict) -> dict:
        email = self._get_email(response['description'])
        return {
            'title': response['title'],
            'release_year': response['releaseDateUtc'],
            'company': response['publisherName'],
            'email': email
        }

