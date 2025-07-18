import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaybookOutputDialog } from './playbook-output-dialog';

describe('PlaybookOutputDialog', () => {
  let component: PlaybookOutputDialog;
  let fixture: ComponentFixture<PlaybookOutputDialog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlaybookOutputDialog]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlaybookOutputDialog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
