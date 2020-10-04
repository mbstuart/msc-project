from services.libs.data_model import Article
from typing import List
from bs4 import BeautifulSoup


class HTMLStripper():

    def strip_html(self, articles: List[Article]) -> List[str]:
        return [self.__extract_text_from_html(art.body) for art in articles]

    def __extract_text_from_html(self, res: str) -> str:
        soup = BeautifulSoup(res, features="lxml")

        for f in soup.find_all('figure'):
            f.decompose()

        text = soup.get_text().lower()

        return text
