import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LatestArticlesComponent } from './latest-articles.component';
import { ArticleListModule } from './article-list/article-list.module';
import { ScrollingModule } from '@angular/cdk/scrolling';



@NgModule({
  declarations: [LatestArticlesComponent],
  imports: [
    CommonModule,
    ArticleListModule,
    ScrollingModule
  ],
  exports: [
    LatestArticlesComponent
  ]
})
export class LatestArticlesModule { }
