import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ThemeTagComponent } from './theme-tag.component';
import { NgbPopoverModule } from '@ng-bootstrap/ng-bootstrap';
import { ThemePopoverModule } from './theme-popover/theme-popover.module';



@NgModule({
  declarations: [ThemeTagComponent],
  imports: [
    CommonModule,
    NgbPopoverModule,
    ThemePopoverModule
  ],
  exports: [
    ThemeTagComponent
  ]
})
export class ThemeTagModule { }
