export interface Article {
    id: string;

    title: string;

    theme: {
        id: string;
        name: string;
    }

    publishDate: Date
}
