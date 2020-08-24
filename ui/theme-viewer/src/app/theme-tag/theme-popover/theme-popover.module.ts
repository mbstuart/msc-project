import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ThemePopoverComponent } from './theme-popover.component';
import { PopoverArticleListModule } from './popover-article-list/popover-article-list.module';



@NgModule({
  declarations: [ThemePopoverComponent],
  imports: [
    CommonModule,
    PopoverArticleListModule
  ],
  entryComponents: [
    ThemePopoverComponent
  ],
  exports: [
    ThemePopoverComponent
  ]
})
export class ThemePopoverModule { }
