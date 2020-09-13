import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PopoverArticleListComponent } from './popover-article-list.component';
import { ThemeDateModule } from 'src/app/services/theme-date.module';



@NgModule({
  declarations: [PopoverArticleListComponent],
  imports: [
    CommonModule,
    ThemeDateModule
  ],
  exports: [
    PopoverArticleListComponent
  ]
})
export class PopoverArticleListModule { }
