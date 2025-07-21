import { Component } from '@angular/core';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { User } from '../../../core/models/user.model';
import { ApiResponse } from '../../../core/models/api-response.model';
import { UserService } from '../../../core/services/user.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-list',
  imports: [CommonModule, MatTableModule],
  templateUrl: './user-list.component.html',
  styleUrl: './user-list.component.scss',
})
export class UserListComponent {
  displayedColumns: string[] = [
    'id',
    'name',
    'email',
    'username',
    'is_active',
    'role',
  ];
  users = [];
  dataSource = new MatTableDataSource<User>();

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.userService.list().subscribe({
      next: (res: ApiResponse<User[]>) => {
        if (res.success) {
          this.dataSource.data = res.data;
        } else {
          console.error('API Error:', res.message);
        }
      },
      error: (err) => {
        console.error('HTTP Error:', err);
      },
    });
  }
}
