from typing import List
from math import ceil

from services.libs.utils import logger
import en_core_web_sm

nlp = en_core_web_sm.load(disable=['ner', 'parser'])


class PosLemma:

    def pos_tag_docs(self, results: List[str], allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV', 'PROPN'], lemmatize=True, postag=True):

        out = []

        l = len(results)

        step = ceil(l / 20)

        def pick_token(token):
            return (token.pos_ in allowed_postags and len(token.lemma_) > 1) if postag else True

        i = 0

        for res in nlp.pipe(results):

            if lemmatize:
                out.append(
                    [token.lemma_ for token in res if pick_token(token)])
            else:
                out.append(
                    [token.text for token in res if pick_token(token)])

            i += 1
            if i % step == 0:
                logger.info(
                    'Preprocess - {:d}% completed'.format(ceil(100 * i / l)))

        return out
