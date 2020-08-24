import { Article } from './article';

export interface Theme {

    id: number;

    name: string;

    keywords: string[];

    articles: Article[];

}