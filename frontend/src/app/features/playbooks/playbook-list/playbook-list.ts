import { ChangeDetectorRef, Component, NgZone } from '@angular/core';
import { Playbook } from '../../../core/models/playbook.model';
import { MatTableModule } from '@angular/material/table';
import { RouterModule } from '@angular/router';
import { PlaybookService } from '../../../core/services/playbook.service';
import { CommonModule } from '@angular/common';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { PlaybookOutputDialog } from '../playbook-output-dialog/playbook-output-dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-playbook-list',
  imports: [
    RouterModule,
    MatTableModule,
    CommonModule,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatDialogModule,
  ],
  templateUrl: './playbook-list.html',
  styleUrl: './playbook-list.scss',
})
export class PlaybookList {
  displayedColumns: string[] = [
    'id',
    'name',
    'description',
    'filepath',
    'actions',
  ];
  playbookOutput: string | null = '';
  showModal: boolean = false;
  error: string | null = null;
  playbooks: Playbook[] = [];
  loading = true;
  loadingPlaybookId: number | null = null;

  constructor(
    private socket: Socket,
    private playbookService: PlaybookService,
    private cdr: ChangeDetectorRef,
    private dialog: MatDialog,
    private zone: NgZone
  ) {}

  runPlaybook(playbookId: number) {
    if (this.loadingPlaybookId !== null) return;

    this.loadingPlaybookId = playbookId;

    this.playbookService.run(playbookId).subscribe({
      next: () => {
        this.zone.run(() => {
          this.dialog.open(PlaybookOutputDialog, {
            data: { playbookId },
            width: '700px',
          });

          this.loadingPlaybookId = null;
          this.cdr.markForCheck();
        });
      },
      error: (error) => {
        this.zone.run(() => {
          if (error.status === 409) {
            this.dialog.open(PlaybookOutputDialog, {
              data: { playbookId, alreadyRunning: true },
              width: '700px',
            });
          } else {
            this.dialog.open(PlaybookOutputDialog, {
              data: { playbookId, error: true },
              width: '700px',
            });
          }

          this.loadingPlaybookId = null;
          this.cdr.markForCheck();
        });
      },
    });
  }

  ngOnInit(): void {
    this.playbookService.list().subscribe({
      next: (response) => {
        this.playbooks = response.data;
        this.cdr.detectChanges();
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to fetch playbooks', err);
        this.loading = false;
      },
    });
  }
}
