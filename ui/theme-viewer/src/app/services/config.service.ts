import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  public dataURL = 'http://localhost:5000'

  constructor() { }


}
