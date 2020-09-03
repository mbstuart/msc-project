from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from typing import List
from services.libs.data_model.processed_article import ProcessedArticle

class WVModelBuilder:

    cores = 4

    def build_wv_model(self, processed_articles: List[ProcessedArticle]):
        tagged_docs = [self.__get_tagged_doc(article) for article in processed_articles] + [self.__get_tagged_doc_title(article) for article in processed_articles]
        model = self.__build_model(tagged_docs)
        return model;

    def __get_tagged_doc(self, processed_article: ProcessedArticle):
        return TaggedDocument(words=processed_article.words, tags=[processed_article.id])
    
    def __get_tagged_doc_title(self, processed_article: ProcessedArticle):
        return TaggedDocument(words=processed_article.title_words, tags=[processed_article.id + '_title'])

    def __build_model(self, tagged_data):
        vec_size = 400

        model = Doc2Vec(vector_size=vec_size,
                    workers = self.cores,
                    min_count=5,
                        dm =1)

        model.build_vocab(tagged_data)

        model.train(tagged_data,
                        total_examples=model.corpus_count,
                    epochs = model.epochs
                        )


        
        return model