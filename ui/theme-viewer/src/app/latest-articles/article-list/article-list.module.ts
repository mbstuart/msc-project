import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArticleListComponent } from './article-list.component';
import { ThemeTagModule } from 'src/app/theme-tag/theme-tag.module';
import { ThemeDateModule } from 'src/app/services/theme-date.module';
import { ScrollingModule } from '@angular/cdk/scrolling';



@NgModule({
  declarations: [ArticleListComponent],
  imports: [
    CommonModule,
    ThemeTagModule,
    ThemeDateModule,
    ScrollingModule
  ],
  exports: [
    ArticleListComponent
  ]
})
export class ArticleListModule { }
