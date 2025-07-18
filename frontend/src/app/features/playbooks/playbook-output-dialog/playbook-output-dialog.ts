import { ChangeDetectorRef, Component, Inject, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogModule,
} from '@angular/material/dialog';
import { SocketService } from '../../../core/services/socket.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-playbook-output-dialog',
  imports: [MatDialogModule, MatButtonModule, CommonModule],
  templateUrl: './playbook-output-dialog.html',
  styleUrl: './playbook-output-dialog.scss',
})
export class PlaybookOutputDialog implements OnInit {
  logs: string[] = [];

  constructor(
    private _cdr: ChangeDetectorRef,
    @Inject(MAT_DIALOG_DATA)
    public data: { playbookId: number; error?: boolean },
    private _socketService: SocketService
  ) {}

  ngOnInit(): void {
    if (this.data.error) {
      this.logs.push('Error running playbook.');
      return;
    }

    this._socketService.getPlaybookLogs().subscribe((logLine: string) => {
      this.logs.push(logLine);
      this._cdr.detectChanges();
    });
  }
}
