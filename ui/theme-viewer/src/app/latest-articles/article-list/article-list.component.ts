import { Component, OnInit, Input, ElementRef } from '@angular/core';
import { Article } from 'src/app/models/article';
import { ThemeService } from 'src/app/services/theme.service';
import { DataService } from 'src/app/services/data.service';
import { ArticlesDataSource } from './articles-data-source';

@Component({
  selector: 'app-article-list',
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.scss']
})
export class ArticleListComponent {

  // @Input() articles: Article[];

  source: ArticlesDataSource;

  constructor(
    private readonly themeService: ThemeService,
    private readonly dataService: DataService,
    private readonly element: ElementRef
  ) {
    this.source = new ArticlesDataSource(this.dataService)
  }

  ngAfterViewInit() {
    const el: HTMLElement = this.element.nativeElement;
    const parentHeight = el.parentElement.offsetHeight;


  }

  getColorForTheme({ id }: { id: number }) {
    return this.themeService.getColorForTheme({ id })
  }


}
