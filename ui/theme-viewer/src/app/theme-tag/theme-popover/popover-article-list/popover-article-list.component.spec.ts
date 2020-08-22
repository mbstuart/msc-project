import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PopoverArticleListComponent } from './popover-article-list.component';

describe('PopoverArticleListComponent', () => {
  let component: PopoverArticleListComponent;
  let fixture: ComponentFixture<PopoverArticleListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PopoverArticleListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PopoverArticleListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
