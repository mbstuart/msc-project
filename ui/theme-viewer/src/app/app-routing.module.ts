import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { ArticlesPageComponent } from './pages/articles-page/articles-page.component';
import { ThemesPageComponent } from './pages/themes-page/themes-page.component';


const routes: Routes = [
  {
    path: '',
    children: [
      {
        path: 'articles', 
        component: ArticlesPageComponent
      },
      {
        path: 'themes', 
        component: ThemesPageComponent
      },
      {
        path: '',
        redirectTo: '/articles',
        pathMatch: 'full'
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
