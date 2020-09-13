import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ThemeDatePipe } from './theme-date.pipe';



@NgModule({
  declarations: [
    ThemeDatePipe
  ],
  exports: [
    ThemeDatePipe
  ],
  imports: [
    CommonModule
  ]
})
export class ThemeDateModule { }
