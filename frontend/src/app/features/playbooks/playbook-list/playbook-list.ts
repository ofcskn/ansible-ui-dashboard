import { ChangeDetectorRef, Component } from '@angular/core';
import { Playbook } from '../../../core/models/playbook.model';
import { MatTableModule } from '@angular/material/table';
import { RouterModule } from '@angular/router';
import { PlaybookService } from '../../../core/services/playbook.service';

@Component({
  selector: 'app-playbook-list',
  imports: [RouterModule, MatTableModule],
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
  playbooks: Playbook[] = [];
  loading = true;

  constructor(
    private playbookService: PlaybookService,
    private cdr: ChangeDetectorRef
  ) {}

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
