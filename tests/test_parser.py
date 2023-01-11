import pytest

from filter_page.models import App


def test_run_true_parametr(parser_valid):
    result = parser_valid.run()
    assert len(result.get_date()) == 20


def test_run_false_url(parser_bad):
    result = parser_bad.run()
    assert len(result.get_date()) == 0


def test_check_valid_date(parser_valid):
    result = parser_valid.run().get_date()[0]
    assert bool(result.get('title'))
    assert bool(result.get('company'))
    assert bool(result.get('release_year'))
    assert bool(result.get('email') or result.get('email') == None)

@pytest.mark.django_db
def test_command(command):
    assert App.objects.all().count() >= 300


