import { Routes } from '@angular/router';
import { AuthGuard } from './core/utils/auth.guard';

export const routes: Routes = [
  {
    path: 'playbooks',
    loadChildren: () =>
      import('./features/playbooks/playbooks-routing-module').then(
        (m) => m.PlaybooksRoutingModule
      ),
    data: { roles: ['user', 'admin'] },
    canActivate: [AuthGuard],
  },
  {
    path: 'users',
    loadChildren: () =>
      import('./features/users/users-routing-module').then(
        (m) => m.UsersRoutingModule
      ),
  },
  { path: '', redirectTo: 'playbooks', pathMatch: 'full' },
];
