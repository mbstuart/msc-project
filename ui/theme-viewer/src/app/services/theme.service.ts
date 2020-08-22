import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {

  private readonly colors: string[] = [
    "red",
    "pink",
    "purple",
    "deep-purple",
    "indigo",
    "blue",
    "light-blue",
    "cyan",
    "teal",
    "green",
    "light-green",
    "lime",
    "yellow",
  ]

  constructor() { }

  getColorForTheme({id}: {id: number}) {
    return `color-${this.colors[+id % this.colors.length]}`
  }
}
