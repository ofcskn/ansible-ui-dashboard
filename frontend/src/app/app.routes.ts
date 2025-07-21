import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'playbooks',
    loadChildren: () =>
      import('./features/playbooks/playbooks-routing-module').then(
        (m) => m.PlaybooksRoutingModule
      ),
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
