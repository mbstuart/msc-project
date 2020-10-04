import pytest
from pytest_mock import MockFixture
from mock import MagicMock
from .pos_lemma import PosLemma


def test_pos_lemma_extraction():

    pl = PosLemma()

    docs = ['Boris Johnson’s law-breaking Brexit bill is straight out of the Donald Trump playbook, and leaves justice secretary Robert Buckland looking “a very small figure,” says shadow justice secretary David Lammy.']

    tagged_docs = pl.pos_tag_docs(docs)

    assert(type(tagged_docs[0][0]) == type('str'))


def test_pos_no_lemma():

    pl = PosLemma()

    docs = ['Boris Johnson’s law-breaking Brexit bill is straight out of the Donald Trump playbook, and leaves justice secretary Robert Buckland looking “a very small figure,” says shadow justice secretary David Lammy.']

    tagged_docs = pl.pos_tag_docs(docs, lemmatize=False)

    assert(type(tagged_docs[0][0]) == type('str'))


def test_pos_no_postag():

    pl = PosLemma()

    docs = ['Boris Johnson’s law-breaking Brexit bill is straight out of the Donald Trump playbook, and leaves justice secretary Robert Buckland looking “a very small figure,” says shadow justice secretary David Lammy.']

    tagged_docs = pl.pos_tag_docs(docs, postag=False)

    assert(type(tagged_docs[0][0]) == type('str'))


def test_postag():

    pl = PosLemma()

    docs = ['Boris Johnson’s law-breaking Brexit bill is straight out of the Donald Trump playbook, and leaves justice secretary Robert Buckland looking “a very small figure,” says shadow justice secretary David Lammy.']

    tagged_docs = pl.pos_tag_docs(docs)

    assert(tagged_docs[0][2] == 'law')
