from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle

from .logger import logger

import json
from pathlib import Path
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
import en_core_web_sm
nlp = en_core_web_sm.load(disable=['ner', 'parser'])
from gensim.utils import simple_preprocess
import multiprocessing
cores = multiprocessing.cpu_count()
from gensim.models.phrases import Phrases, Phraser
from math import ceil
from typing import List


class ArticlePreprocessor: 
       
    def preprocess_articles(self, articles: List[Article]) -> List[ProcessedArticle]:
        return self.__get_tagged_data(articles)

    def __remove_stopwords(self, text: List[str]) -> List[str]:
        return [word for word in text if word not in stop_words]

    def __lemmatization(self, text: List[str], allowed_postags: List[str]) -> List[str]:
        texts_out = []
        doc = nlp(" ".join(text)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

        
    def __get_tagged_data(self, articles: List[Article]) -> List[ProcessedArticle]:
        logger.info('Getting tagged data')
        self.texts = [self.__extract_text_from_html(res.body) for res in articles]
        logger.info('Extracted from HTML')
        self.preprocessed_docs = self.__preprocess_docs(self.texts)
        logger.info('Docs preprocessed and tokenized')
        self.phrase_texts = self.__build_phrases(self.preprocessed_docs);    
        logger.info('Phrases built')
        self.processed_articles: List[ProcessedArticle] = []
        for i, article in enumerate(articles):
            pa = ProcessedArticle(article.id, article.article_load_id, self.phrase_texts[i])
            self.processed_articles.append(pa)
        return self.processed_articles

    def __extract_text_from_html(self, res: str) -> str:
        soup = BeautifulSoup(res, features="lxml")
        
        for f in soup.find_all('figure'):
            f.decompose()
        
        text = soup.get_text().lower();
        
        return text

    def __preprocess_docs(self, results, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV', 'PROPN']):
        
        out = []
        
        l = len(results)
        
        step = ceil(l / 20)

        def pick_token(token):
            return token.pos_ in allowed_postags and len(token.lemma_) > 1
        
        i = 0;

        for res in nlp.pipe(results):
            
            out.append([token.lemma_ for token in res if pick_token(token)])
            
            i += 1
            if i % step == 0:
                logger.info('Preprocess - {:d}% completed'.format(ceil(100 * i / l)))
            
        return out;

    def __build_phrases(self, tokenized_texts):
        
        phrases = Phrases(tokenized_texts)
        
        return [phrases[phrases[tokens]] for tokens in tokenized_texts]