from gensim.models import Phrases


from services.libs.utils import logger
import os


class PhraseExtractor():

    __PREPROCESS_FOLDER = 'preprocess'

    __PHRASER_FILE = 'phrases'

    def __init__(self):
        if not(os.path.isdir(self.__PREPROCESS_FOLDER)):
            os.mkdir(self.__PREPROCESS_FOLDER)

    def build_phrases(self, tokenized_texts, tokenized_titles, load_id):

        phrases = Phrases(tokenized_texts + tokenized_titles,
                          scoring='npmi', threshold=0.2, min_count=50, progress_per=1000)
        try:
            self.__save_phrase_model(phrases, load_id)
        except Exception as e:
            logger.info(e)

        return [phrases[phrases[tokens]] for tokens in tokenized_texts], [phrases[phrases[tokens]] for tokens in tokenized_titles]

    def build_phrases_update(self, tokenized_texts, tokenized_titles, old_load_id: str, new_load_id: str):

        phrases: Phrases = None

        phrases = self.__get_phrase_model(old_load_id)
        phrases.add_vocab(tokenized_texts + tokenized_titles)
        try:
            self.__save_phrase_model(phrases, new_load_id)
        except Exception as e:
            logger.info(e)

        return [phrases[phrases[tokens]] for tokens in tokenized_texts], [phrases[phrases[tokens]] for tokens in tokenized_titles]

    def __get_phrase_model(self, load_id):
        return Phrases.load(self.__phrase_model_path(load_id))

    def __save_phrase_model(self, phrase: Phrases, load_id: str):
        os.mkdir(self.__folder_path(load_id))
        phrase.save(self.__phrase_model_path(load_id))

    def __folder_path(self, load_id: str):
        return '{}/{}'.format(self.__PREPROCESS_FOLDER, load_id)

    def __phrase_model_path(self, load_id):
        return '{}/{}.pkl'.format(self.__folder_path(load_id), self.__PHRASER_FILE)
