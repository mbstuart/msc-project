import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArticlesPageComponent } from './articles-page.component';
import { LatestArticlesModule } from 'src/app/latest-articles/latest-articles.module';



@NgModule({
  declarations: [ArticlesPageComponent],
  imports: [
    CommonModule,
    LatestArticlesModule
  ],
  exports: [
    ArticlesPageComponent
  ]
})
export class ArticlesPageModule { }
