import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service';
import { Article } from '../models/article';
import { Observable, of, Subject, timer, ReplaySubject } from 'rxjs';
import { Theme } from '../models/theme';
import { switchMap, tap, first, catchError } from 'rxjs/operators';
import { ArticleLoad } from '../models/article-load';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private cache: {
    [url: string]: {
      expired: Observable<boolean>,
      response: Observable<any>
    }
  } = {

    }

  constructor(
    private readonly httpClient: HttpClient,
    private readonly config: ConfigService
  ) { }

  public getLatestArticles(pageSize, pageNum = 1): Observable<{ articles: Article[] }> {
    return this.get(`/articles?page_num=${pageNum}&page_size=${pageSize}`) as Observable<{ articles: Article[] }>
  }

  public getEmergingThemes() {
    return this.get(`/emerging-themes`, 60) as Observable<{ themes: Theme[] }>
  }

  public getTheme(themeId: number) {
    return this.get(`/themes/${themeId}`, 60) as Observable<Theme>
  }

  public getArticleLoad() {
    return this.get(`/article-load`, 60) as Observable<ArticleLoad>
  }

  private get(url: string, cacheTime?: number) {

    if (!cacheTime) {
      return this.httpClient.get(`${this.config.dataURL}${url}`)
    }

    const expired = (this.cache[url] && this.cache[url].expired) || of(true);

    return expired.pipe(
      first(),
      switchMap(
        expired => {
          if (expired) {

            const expiry$ = new ReplaySubject<boolean>(1);
            expiry$.next(false);

            const result$ = new ReplaySubject<any>(1);

            this.cache[url] = {
              expired: expiry$.asObservable(),
              response: result$.asObservable()
            }

            return this.httpClient.get(`${this.config.dataURL}${url}`)
              .pipe(
                tap(
                  response => {
                    timer(cacheTime * 1000).subscribe(timer => {
                      console.log(`${url} expired after ${cacheTime} seconds`)
                      expiry$.next(true);
                    })
                    result$.next(response);
                  }
                ),
                catchError(err => {
                  expiry$.next(true);
                  result$.next(null);
                  throw err;
                })
              )
          } else {
            return this.cache[url].response.pipe(first());
          }
        }
      )
    )

  }
}
