import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArticleListComponent } from './article-list.component';
import { ThemeTagModule } from 'src/app/theme-tag/theme-tag.module';



@NgModule({
  declarations: [ArticleListComponent],
  imports: [
    CommonModule,
    ThemeTagModule
  ],
  exports: [
    ArticleListComponent
  ]
})
export class ArticleListModule { }
