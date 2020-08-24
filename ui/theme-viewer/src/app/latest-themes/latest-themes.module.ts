import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ThemeTagModule } from '../theme-tag/theme-tag.module';
import { LatestThemesComponent } from './latest-themes.component';



@NgModule({
  declarations: [LatestThemesComponent],
  imports: [
    CommonModule,
    ThemeTagModule
  ],
  exports: [
    LatestThemesComponent
  ]
})
export class LatestThemesModule { }
