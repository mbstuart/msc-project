from services.theme_extractor.base_job import BaseJob
from sqlalchemy.orm import Session
from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle
from services.libs.data_model.theme import Theme
from services.libs.data_model.theme_article_link import ThemeArticleLink
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import extract
from sqlalchemy import func
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import List

class EmergingThemeExtractor(BaseJob):

    def __init__(self): 
        super().__init__()


    def get_emerging_themes(self):

        theme_ids = self.__extract_emerging_themes_table();
        themes = self.__get_theme_information_from_db(theme_ids);
        print(themes)
        return themes;
        

    def __get_theme_information_from_db(self, theme_ids: List[str]):
        session: Session = self.sessionmaker();

        subquery = session.query(Theme.id, Theme.name, Theme.theme_words, Article.id, Article.publish_date, Article.title, func.rank().over(
                order_by=Article.publish_date.desc(),
                partition_by=(Theme.article_load_id, Theme.id)
            ).label('rank')).\
            filter(Theme.id.in_(theme_ids)).\
            join(ThemeArticleLink).\
            join(ProcessedArticle).\
            join(Article).\
            subquery()

        themes = session.query(subquery).\
            filter(subquery.c.rank <= 4).\
            all()

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
                'publish_date': theme[4],
                'title': theme[5],
            })


        return collated_themes

    def __extract_emerging_themes_table(self):

        load_id: UUID = str(self.get_latest_article_load().id)

        tod = datetime.now()
        d = timedelta(days = 30 * 10) 
        from_date = tod - d;

        session: Session = self.sessionmaker()

        emerging_themes_agg = session.query(Theme.id).\
        join(ThemeArticleLink).\
        join(ProcessedArticle).\
        join(Article).\
        filter_by(article_load_id = load_id).\
        filter(Article.publish_date >= from_date).\
        add_columns(extract('year', Article.publish_date).label("year"), extract('month', Article.publish_date).label("month"), func.count(Article.id).label("num_articles")).\
        group_by(Theme.id, extract('year', Article.publish_date), extract('month', Article.publish_date))
        
        df = pd.read_sql(emerging_themes_agg.statement, emerging_themes_agg.session.bind)
        
        themes = np.unique(df['ThemeId'])
        years = np.unique(df['year'])
        months = np.unique(df['month'])

        new_data = []

        for theme in themes:
            for year in years:
                for month in months:
                    arr = np.array([theme,year,month])
                    exists = (df[df.columns[1:4]] == arr).all(1).any()
                    if not(exists):
                            new_data.append(arr)


        new_data_df = pd.DataFrame(new_data, columns=df.columns[1:4])
        new_data_df['num_articles'] = 0
        df_with_missing = pd.concat([df, new_data_df], sort=False).reset_index()

        avg_count = df_with_missing.groupby('ThemeId').mean().reset_index()

        df_with_avg = df_with_missing.join(avg_count.set_index('ThemeId'), on='ThemeId', rsuffix='_avg')
        df_with_avg['rel_count'] = df_with_avg['num_articles'] / df_with_avg['num_articles_avg']
        filtered_df = df_with_avg[df_with_avg['month'] == max(months)][df_with_avg['rel_count'] > 1]

        return np.unique(filtered_df['ThemeId'])
