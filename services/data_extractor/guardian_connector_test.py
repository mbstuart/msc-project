import pytest
from .guardian_connector import GuardianConnector


def test_guardian_connector():

    gc = GuardianConnector()

    arts = gc.get_results('random', 1, None)

    assert(True)


def test_guardian_articles():

    gc = GuardianConnector()

    arts = gc.get_guardian_articles(max_pages=2)

    assert(len(arts) > 0)
