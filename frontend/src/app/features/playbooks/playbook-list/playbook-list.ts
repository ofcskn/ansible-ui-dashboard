import { Component } from '@angular/core';
import { Playbook } from '../../../core/models/playbook.model';
import { MatTableModule } from '@angular/material/table';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-playbook-list',
  imports: [RouterModule, MatTableModule],
  templateUrl: './playbook-list.html',
  styleUrl: './playbook-list.scss',
})
export class PlaybookList {
  displayedColumns: string[] = ['id', 'title', 'description', 'actions'];

  playbooks: Playbook[] = [
    { id: 1, name: 'Playbook One', description: 'Description of playbook one' },
    { id: 2, name: 'Playbook Two', description: 'Description of playbook two' },
  ];
}
