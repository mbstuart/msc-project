import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArticleListComponent } from './article-list.component';
import { ThemeTagModule } from 'src/app/theme-tag/theme-tag.module';
import { ThemeDateModule } from 'src/app/services/theme-date.module';



@NgModule({
  declarations: [ArticleListComponent],
  imports: [
    CommonModule,
    ThemeTagModule,
    ThemeDateModule
  ],
  exports: [
    ArticleListComponent
  ]
})
export class ArticleListModule { }
