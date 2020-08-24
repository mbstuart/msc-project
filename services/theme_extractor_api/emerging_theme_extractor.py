
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import extract
from sqlalchemy import func

from services.theme_extractor.base_job import BaseJob
from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle
from services.libs.data_model.theme import Theme
from services.libs.data_model.theme_article_link import ThemeArticleLink
from services.theme_extractor.logger import logger


from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import List

class EmergingThemeExtractor(BaseJob):

    def __init__(self): 
        super().__init__()


    def get_emerging_themes(self, frequency='month'):

        theme_ids = self.__extract_emerging_themes_table(frequency);
        # logger.info('Getting themes information from DB')
        themes = self.__get_theme_information_from_db(theme_ids);
        # logger.info('Themes information retrieved from DB')
        return themes;
        
    def get_theme(self, theme_ids: List[str]):
        return self.__get_theme_information_from_db(theme_ids)

    def __get_theme_information_from_db(self, theme_ids: List[int]):
        session: Session = self.get_session();

        subquery = session.query(Theme.id, Theme.name, Theme.theme_words, Article.id, Article.publish_date, Article.title, func.rank().over(
                order_by=Article.publish_date.desc(),
                partition_by=(Theme.article_load_id, Theme.id)
            ).label('rank')).\
            filter(Theme.id.in_([int(id) for id in theme_ids])).\
            join(ThemeArticleLink).\
            join(ProcessedArticle).\
            join(Article).\
            subquery()

        q = session.query(subquery).\
            filter(subquery.c.rank <= 10)

        themes = q.all()

        collated_themes: List[Theme] = []

        last_theme_id = -1;

        collated_theme: {} = None;

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

    def extract_themes_table(self, frequency='month'):
        load_id: UUID = str(self.get_latest_article_load().id)

        tod = datetime.now()
        if frequency == 'month':
            d = timedelta(days = 30 * 10)
        elif frequency == 'week':
            d = timedelta(days = 7 * 10) 
        from_date = tod - d;

        session: Session = self.get_session()

        emerging_themes_agg = session.query(Theme.id).\
        join(ThemeArticleLink).\
        join(ProcessedArticle).\
        join(Article).\
        filter_by(article_load_id = load_id).\
        filter(Theme.id != -1).\
        filter(Article.publish_date >= from_date).\
        add_columns(extract('year', Article.publish_date).label("year"), extract(frequency, Article.publish_date).label(frequency), func.count(Article.id).label("num_articles")).\
        group_by(Theme.id, extract('year', Article.publish_date), extract(frequency, Article.publish_date))
        
        df = pd.read_sql(emerging_themes_agg.statement, emerging_themes_agg.session.bind)

        return df

    def __extract_emerging_themes_table(self, frequency='month'):

        # logger.info('Starting emerging theme extraction. Getting data from db.')

        df = self.extract_themes_table(frequency=frequency)

        # logger.info('Themes extracted from db. Getting latest.')

        yms = np.unique(df[['year', frequency]].to_numpy(), axis=0)

        themes = np.unique(df['ThemeId'])

        avg_count = df.groupby('ThemeId').mean().reset_index()

        df_with_avg = df.join(avg_count.set_index('ThemeId'), on='ThemeId', rsuffix='_avg')
        df_with_avg['rel_count'] = df_with_avg['num_articles'] / df_with_avg['num_articles_avg']
        
        filtered_df = df_with_avg[df_with_avg[frequency] == yms[-1][1]][df_with_avg['year'] == yms[-1][0]][df_with_avg['rel_count'] > 1]

        # logger.info('Latest themes extrfacted')

        return np.unique(filtered_df['ThemeId']).astype(int)
