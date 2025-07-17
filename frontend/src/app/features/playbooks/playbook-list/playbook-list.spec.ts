import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaybookList } from './playbook-list';

describe('PlaybookList', () => {
  let component: PlaybookList;
  let fixture: ComponentFixture<PlaybookList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlaybookList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlaybookList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
