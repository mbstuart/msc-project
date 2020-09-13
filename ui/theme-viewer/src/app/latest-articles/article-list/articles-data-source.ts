import { DataSource, CollectionViewer } from '@angular/cdk/collections';
import { Article } from 'src/app/models/article';
import { Observable, Subscription, BehaviorSubject } from 'rxjs';
import { DataService } from 'src/app/services/data.service';

export class ArticlesDataSource extends DataSource<Article> {

    private cachedArticles = Array.from<Article>({ length: 0 });
    private dataStream = new BehaviorSubject<(Article)[]>(this.cachedArticles);
    private subscription = new Subscription();

    private pageSize = 20;
    private lastPage = 0;

    constructor(
        private readonly dataService: DataService
    ) {
        super();
        this.fetchArticlePage(0)
    }


    connect(collectionViewer: CollectionViewer): Observable<Article[] | readonly Article[]> {
        this.subscription.add(collectionViewer.viewChange.subscribe(range => {

            const currentPage = this._getPageForIndex(range.end);

            if (currentPage > this.lastPage) {
                this.lastPage = currentPage;
                this.fetchArticlePage(currentPage);
            }

        }));
        return this.dataStream;
    }

    disconnect(collectionViewer: CollectionViewer): void {
        this.subscription.unsubscribe();
    }

    private fetchArticlePage(pageNum: number): void {
        this.dataService.getLatestArticles(this.pageSize, pageNum + 1).subscribe(res => {
            this.cachedArticles = this.cachedArticles.concat(res.articles);
            this.dataStream.next(this.cachedArticles);
        });

    }

    private _getPageForIndex(i: number): number {
        return Math.floor(i / this.pageSize);
    }

}