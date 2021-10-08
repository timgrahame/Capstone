import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { artistFormComponent } from './artist-form.component';

describe('artistFormComponent', () => {
  let component: artistFormComponent;
  let fixture: ComponentFixture<artistFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ artistFormComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(artistFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
