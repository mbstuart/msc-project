from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import extract
from sqlalchemy import func

from typing import List

from services.theme_extractor.base_job import BaseJob
from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle
from services.libs.data_model.theme import Theme
from services.libs.data_model.theme_article_link import ThemeArticleLink
from services.libs.utils import logger


class ThemeBase(BaseJob):

    def __init__(self):
        super().__init__()

    def get_theme_information_from_db(self, theme_ids: List[int]):
        session: Session = self.get_session()

        load_id = self.get_latest_article_load().id

        subquery = session.query(Theme.id, Theme.name, Theme.theme_words, Article.id, Article.publish_date, Article.title, func.rank().over(
            order_by=Article.publish_date.desc(),
            partition_by=(Theme.id)
        ).label('rank')).\
            filter(Theme.id.in_([int(id) for id in theme_ids])).\
            join(ThemeArticleLink).\
            join(ProcessedArticle).\
            join(Article).\
            filter(Theme.article_load_id == load_id).\
            subquery()

        q = session.query(subquery).\
            filter(subquery.c.rank <= 10)

        themes = q.all()

        collated_themes: List[Theme] = []

        last_theme_id = -1

        collated_theme: {} = None

        for theme in themes:
            if theme[0] != last_theme_id:
                last_theme_id = theme[0]
                collated_theme = {
                    'id': theme[0],
                    'name': theme[1],
                    'keywords': theme[2],
                    'articles': []
                }
                collated_themes.append(collated_theme)

            collated_theme['articles'].append({
                'id': theme[3],
                'publishDate': theme[4],
                'title': theme[5],
                'theme': {
                    'id': theme[0],
                    'name': theme[1],
                }
            })

        return collated_themes
