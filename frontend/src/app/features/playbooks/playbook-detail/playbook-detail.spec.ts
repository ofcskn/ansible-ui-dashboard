import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaybookDetail } from './playbook-detail';

describe('PlaybookDetail', () => {
  let component: PlaybookDetail;
  let fixture: ComponentFixture<PlaybookDetail>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlaybookDetail]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlaybookDetail);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
