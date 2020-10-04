import { Component, OnInit, Input, ViewChild, HostListener } from '@angular/core';
import { NgbPopover } from '@ng-bootstrap/ng-bootstrap';
import { Subject } from 'rxjs';
import { debounceTime, tap } from 'rxjs/operators';
import { Theme } from '../models/theme';
import { ThemeService } from '../services/theme.service';

@Component({
  selector: 'app-theme-tag',
  templateUrl: './theme-tag.component.html',
  styleUrls: ['./theme-tag.component.scss']
})
export class ThemeTagComponent {

  @Input() theme: Theme

  @ViewChild(NgbPopover) popover: NgbPopover;

  private closePopover: Subject<boolean> = new Subject();

  @HostListener('mouseleave') onMouseLeave(event) {
    this.closePopover.next(true)
  }

  @HostListener('mouseover') onMouseEnter(event) {
    this.closePopover.next(false)
  }

  constructor(
    private readonly themeService: ThemeService
  ) { }

  ngAfterViewInit() {
    this.closePopover
      .pipe(
        debounceTime(500),
        tap(enter => {
          if (enter) {
            this.popover.close()
          }
        })
      )
      .subscribe()
    // this.popover.triggers
  }

  getColorForTheme({ id }: { id: number }) {
    return this.themeService.getColorForTheme({ id })
  }


}
