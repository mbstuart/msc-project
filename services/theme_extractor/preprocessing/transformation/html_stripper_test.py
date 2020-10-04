import pytest
from pytest_mock import MockFixture
from mock import MagicMock
from .html_stripper import HTMLStripper
from services.libs.data_model.article import Article


def test_pos_lemma_extraction():

    hs = HTMLStripper()

    articles = [
        Article('id', '<p>this is a <span class="italicised">test</span> sentence</p>',
                'test', None, None, None)
    ]

    stripped = hs.strip_html(articles)

    assert(stripped[0] == 'this is a test sentence')
