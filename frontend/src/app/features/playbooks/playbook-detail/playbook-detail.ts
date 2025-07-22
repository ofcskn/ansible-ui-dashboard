import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Playbook } from '../../../core/models/playbook.model';
import { PlaybookService } from '../../../core/services/playbook.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-playbook-detail',
  templateUrl: './playbook-detail.html',
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  ],
})
export class PlaybookDetail implements OnInit {
  playbook: Playbook = {
    id: 0,
    name: '',
    description: '',
    filepath: '',
    content: '',
  };
  loading = false;
  isNew = false;
  editorOptions: {} | null = null;
  errorMessage: string | null = '';
  private playbookId: string | null = null;

  constructor(
    public route: ActivatedRoute,
    public router: Router,
    private playbookService: PlaybookService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.editorOptions = { theme: 'vs-dark', language: 'yaml' };
    this.playbookId = this.route.snapshot.paramMap.get('id');

    if (
      !this.playbookId ||
      this.playbookId === 'new' ||
      this.playbookId === '0'
    ) {
      this.isNew = true;
    } else {
      this.isNew = false;
      this.loadPlaybook(this.playbookId);
    }
  }

  loadPlaybook(id: string) {
    this.loading = true;
    this.errorMessage = null;

    this.playbookService.getById(id).subscribe({
      next: (res) => {
        if (res?.data) {
          this.playbook = res.data;

          this.playbookService.getContentById(id).subscribe({
            next: (contentRes) => {
              this.playbook.content = contentRes?.data || '';
              this.loading = false;

              this.cdr.detectChanges();
            },
            error: (error) => {
              this.errorMessage = error.error.message;
              this.loading = false;
              this.cdr.detectChanges();
            },
          });
        } else {
          this.errorMessage = 'Playbook data is empty.';
          this.loading = false;
          this.cdr.detectChanges();
        }
      },
      error: (error) => {
        this.errorMessage = error.error.message;
        this.loading = false;
        this.cdr.detectChanges();
      },
    });
  }

  save() {
    this.errorMessage = null;

    if (!this.playbook.content || this.playbook.content.trim() === '') {
      this.errorMessage = 'YAML content is required';
      return;
    }

    this.loading = true;

    if (this.isNew) {
      this.playbookService.create(this.playbook).subscribe({
        next: () => this.router.navigate(['/playbooks']),
        error: (error) => {
          this.errorMessage = error.error.message;
          this.loading = false;
          this.cdr.detectChanges();
        },
      });
    } else if (this.playbookId) {
      this.playbookService.update(this.playbookId, this.playbook).subscribe({
        next: () => this.router.navigate(['/playbooks']),
        error: (error) => {
          this.errorMessage = error.error.message;
          this.loading = false;
          this.cdr.detectChanges();
        },
      });
    }
  }
}
