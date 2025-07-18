import { Component, Inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-playbook-output-dialog',
  imports: [MatDialogModule, MatButtonModule],
  templateUrl: './playbook-output-dialog.html',
  styleUrl: './playbook-output-dialog.scss',
})
export class PlaybookOutputDialog {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { output: string }) {}
}
