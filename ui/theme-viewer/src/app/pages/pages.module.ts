import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArticlesPageModule } from './articles-page/articles-page.module';
import { ThemesPageModule } from './themes-page/themes-page.module';



@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    ArticlesPageModule,
    ThemesPageModule
  ]
})
export class PagesModule { }
