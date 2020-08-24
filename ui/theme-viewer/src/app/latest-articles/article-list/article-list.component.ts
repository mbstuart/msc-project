import { Component, OnInit, Input } from '@angular/core';
import { Article } from 'src/app/models/article';
import { ThemeService } from 'src/app/services/theme.service';

@Component({
  selector: 'app-article-list',
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.scss']
})
export class ArticleListComponent {

  @Input() articles: Article[];
  
  constructor(
    private readonly themeService: ThemeService
  ) { }

  getColorForTheme({id}: {id: number}) {
    return this.themeService.getColorForTheme({id})
  }


}
