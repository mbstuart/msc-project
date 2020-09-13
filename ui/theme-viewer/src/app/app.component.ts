import { Component, OnInit } from '@angular/core';
import { faNewspaper, faLightbulb } from '@fortawesome/free-solid-svg-icons';
import { ArticleLoad } from './models/article-load';
import { DataService } from './services/data.service';
import { tap } from 'rxjs/operators';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'theme-viewer';

  articleIcon = faNewspaper;

  themeIcon = faLightbulb;

  articleLoad: ArticleLoad

  constructor(
    private readonly dataService: DataService
  ) {

  }

  ngOnInit() {
    this.dataService.getArticleLoad()
      .pipe(
        tap(load => {
          this.articleLoad = load;
        })
      ).subscribe()
  }
}
