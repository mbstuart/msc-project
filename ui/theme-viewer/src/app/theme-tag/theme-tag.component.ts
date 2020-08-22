import { Component, OnInit, Input } from '@angular/core';
import { Theme } from '../models/theme';
import { ThemeService } from '../services/theme.service';

@Component({
  selector: 'app-theme-tag',
  templateUrl: './theme-tag.component.html',
  styleUrls: ['./theme-tag.component.scss']
})
export class ThemeTagComponent {

  @Input() theme: Theme

  constructor(
    private readonly themeService: ThemeService
  ) { }

  getColorForTheme({id}: {id: number}) {
    return this.themeService.getColorForTheme({id})
  }


}
