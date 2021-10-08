import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { artistMenuPage } from './artist-menu.page';

describe('artistMenuPage', () => {
  let component: artistMenuPage;
  let fixture: ComponentFixture<artistMenuPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ artistMenuPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(artistMenuPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
