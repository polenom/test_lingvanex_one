import urllib
from asyncio import Queue
import pytest
from aiohttp import ClientSession
from django.core.management import call_command

from filter_page.utils import ParcerApps


class TestParserApp(ParcerApps):

    async def _get_products(self, session: ClientSession, queue: Queue):
        value_cursor = ''
        full_url = self._url_cursor + urllib.parse.quote(value_cursor)
        response = await self._request(session, full_url)
        product_ids = [i['productId'] for i in response['productsList']]
        queue.put_nowait(product_ids)
        value_cursor = response.get('cursor')
        queue.put_nowait(None)


class TestFalseParserApp(TestParserApp):
    _url_cursor = 'https://apps.microsoft12312321.com/'
    _url_product = 'https://apps.microsoft2131312.com/'


@pytest.fixture
def parser_valid():
    return TestParserApp


@pytest.fixture
def parser_bad():
    return TestFalseParserApp


@pytest.fixture(scope='session')
def command(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('init_date')

