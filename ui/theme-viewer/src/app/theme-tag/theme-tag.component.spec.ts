import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ThemeTagComponent } from './theme-tag.component';

describe('ThemeTagComponent', () => {
  let component: ThemeTagComponent;
  let fixture: ComponentFixture<ThemeTagComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ThemeTagComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ThemeTagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
