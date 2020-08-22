import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ThemesPageComponent } from './themes-page.component';
import { LatestThemesModule } from 'src/app/latest-themes/latest-themes.module';



@NgModule({
  declarations: [ThemesPageComponent],
  imports: [
    CommonModule,
    LatestThemesModule
  ]
})
export class ThemesPageModule { }
