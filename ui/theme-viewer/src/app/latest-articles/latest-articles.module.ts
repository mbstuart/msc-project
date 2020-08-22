import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LatestArticlesComponent } from './latest-articles.component';
import { ArticleListModule } from './article-list/article-list.module';



@NgModule({
  declarations: [LatestArticlesComponent],
  imports: [
    CommonModule,
    ArticleListModule
  ],
  exports: [
    LatestArticlesComponent
  ]
})
export class LatestArticlesModule { }
