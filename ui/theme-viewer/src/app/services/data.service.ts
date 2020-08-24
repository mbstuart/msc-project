import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service';
import { Article } from '../models/article';
import { Observable } from 'rxjs';
import { Theme } from '../models/theme';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  

  constructor(
    private readonly httpClient: HttpClient,
    private readonly config: ConfigService
  ) { }

  public getLatestArticles(n=10): Observable<{articles: Article[]}> {
    return this.httpClient.get(`${this.config.dataURL}/articles`) as Observable<{articles: Article[]}>
  }

  public getEmergingThemes() {
    return this.httpClient.get(`${this.config.dataURL}/emerging-themes`) as Observable<{themes: Theme[]}>
  }

  public getTheme(themeId: number) {
    return this.httpClient.get(`${this.config.dataURL}/themes/${themeId}`) as Observable<Theme>
  }
}
