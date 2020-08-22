import { Component } from '@angular/core';
import {faNewspaper, faLightbulb} from '@fortawesome/free-solid-svg-icons';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'theme-viewer';

  articleIcon = faNewspaper;

  themeIcon = faLightbulb;
}
