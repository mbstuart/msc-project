import { Pipe, PipeTransform } from '@angular/core';
import * as moment from 'moment'


@Pipe({
  name: 'themeDate'
})
export class ThemeDatePipe implements PipeTransform {

  transform(value: Date, ...args: unknown[]): unknown {
    const mdate = moment(value);
    const today = moment();
    const dayDiff = today.diff(mdate, 'day');
    if (mdate.isSame(today, 'day')) {
      return mdate.format('HH:mm A')
    }
    else if (dayDiff < 7) {
      return mdate.format('ddd HH:mm A')
    }
    else {
      return mdate.format('YYYY-MM-DD')
    }
  }

}
