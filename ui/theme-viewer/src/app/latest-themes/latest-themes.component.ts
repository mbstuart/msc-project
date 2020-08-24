import { Component, OnInit } from '@angular/core';
import { Theme } from '../models/theme';
import { DataService } from '../services/data.service';
import { tap } from 'rxjs/operators';

@Component({
  selector: 'app-latest-themes',
  templateUrl: './latest-themes.component.html',
  styleUrls: ['./latest-themes.component.scss']
})
export class LatestThemesComponent implements OnInit {

  themes: Theme[]

  constructor(
    private readonly dataService: DataService
  ) { }

  ngOnInit(): void {
    this.dataService.getEmergingThemes()
      .pipe(tap(res => {
        this.themes = res.themes
      }))
      .subscribe()
  }

  formatKeyword(keyword: string) {
    return keyword.split('_').map(word => {
      word = word[0].toLocaleUpperCase() + word.substr(1);
      return word;
    }).join(' ')
  }

}
