import { Component, OnInit } from '@angular/core';
import { tap } from 'rxjs/operators';
import { Article } from '../models/article';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-latest-articles',
  templateUrl: './latest-articles.component.html',
  styleUrls: ['./latest-articles.component.scss']
})
export class LatestArticlesComponent implements OnInit {

  public articles: Article[]

  constructor(
    private readonly dataService: DataService
  ) { }

  ngOnInit(): void {

  }


}
