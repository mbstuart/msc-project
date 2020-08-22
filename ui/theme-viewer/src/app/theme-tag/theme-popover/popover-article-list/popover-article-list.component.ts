import { Component, OnInit, Input } from '@angular/core';
import { Article } from 'src/app/models/article';

@Component({
  selector: 'app-popover-article-list',
  templateUrl: './popover-article-list.component.html',
  styleUrls: ['./popover-article-list.component.scss']
})
export class PopoverArticleListComponent {

  @Input() articles: Article[];

}
