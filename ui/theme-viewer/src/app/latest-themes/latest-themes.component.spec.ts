import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LatestThemesComponent } from './latest-themes.component';

describe('LatestThemesComponent', () => {
  let component: LatestThemesComponent;
  let fixture: ComponentFixture<LatestThemesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LatestThemesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LatestThemesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
