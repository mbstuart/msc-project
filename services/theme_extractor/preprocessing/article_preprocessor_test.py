import pytest
from .article_preprocessor import ArticlePreprocessor, RUN_LEMMATIZATION, RUN_PHRASING, RUN_POS_TAGGING
from pytest_mock import MockFixture
from mock import MagicMock
from services.libs.data_model import Article
from datetime import datetime
from services.theme_extractor.preprocessing.transformation import HTMLStripper, PhraseExtractor, PosLemma


def test_article_preprocessor_inits():

    ap = ArticlePreprocessor()

    assert(ap is not None)


def test_article_preprocess_calls_html_stripper(mocker: MockFixture):

    articles = [
        Article('mock-1', '<p>The cat sat on the mat</p>',
                'Cat sits on mat', 'cat', datetime.now(), '12345')
    ]

    mock_html_stripper = HTMLStripper()

    spy: MagicMock = mocker.spy(mock_html_stripper, 'strip_html')

    ap = ArticlePreprocessor(html_stripper=mock_html_stripper)
    ap.preprocess_articles(articles, '12345')

    spy.assert_called_once_with(articles)


def test_article_preprocess_calls_phraser(mocker: MockFixture):

    articles = [
        Article('mock-1', '<p>The cat sat on the mat</p>',
                'Cat sits on mat', 'cat', datetime.now(), '12345')
    ]

    mock_phrase_extractor = PhraseExtractor()

    spy: MagicMock = mocker.spy(mock_phrase_extractor, 'build_phrases')

    ap = ArticlePreprocessor(phrase_extractor=mock_phrase_extractor)
    ap.preprocess_articles(articles, '12345')

    spy.assert_called_once()


def test_article_preprocess_calls_pos_lemma(mocker: MockFixture):

    articles = [
        Article('mock-1', '<p>The cat sat on the mat</p>',
                'Cat sits on mat', 'cat', datetime.now(), '12345')
    ]

    mock_pos_lemma_extractor = PosLemma()

    spy: MagicMock = mocker.spy(mock_pos_lemma_extractor, 'pos_tag_docs')

    ap = ArticlePreprocessor(pos_lemma=mock_pos_lemma_extractor)
    ap.preprocess_articles(articles, '12345')

    spy.assert_called()


def test_article_preprocess_phrasing_not_run_if_excluded(mocker: MockFixture):

    articles = [
        Article('mock-1', '<p>The cat sat on the mat</p>',
                'Cat sits on mat', 'cat', datetime.now(), '12345')
    ]

    mock_phrase_extractor = PhraseExtractor()

    spy: MagicMock = mocker.spy(mock_phrase_extractor, 'build_phrases')

    ap = ArticlePreprocessor(phrase_extractor=mock_phrase_extractor, steps=[
        RUN_LEMMATIZATION, RUN_POS_TAGGING])
    ap.preprocess_articles(articles, '12345')

    spy.assert_not_called()
