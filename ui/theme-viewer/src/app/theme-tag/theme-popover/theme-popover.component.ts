import { Component, OnInit, Input } from '@angular/core';
import { DataService } from '../../services/data.service';
import { tap } from 'rxjs/operators';
import { Theme } from '../../models/theme';

@Component({
  selector: 'app-theme-popover',
  templateUrl: './theme-popover.component.html',
  styleUrls: ['./theme-popover.component.scss']
})
export class ThemePopoverComponent implements OnInit {

  @Input() themeId: number;

  public theme: Theme;

  constructor(
    private readonly dataService: DataService
  ) { }

  ngOnInit(): void {
    this.dataService.getTheme(this.themeId)
      .pipe(tap(theme => {
        this.theme = theme;
      }))
      .subscribe()
  }

}
