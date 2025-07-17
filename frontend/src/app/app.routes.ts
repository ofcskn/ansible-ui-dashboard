import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'playbooks',
    loadChildren: () =>
      import('./features/playbooks/playbooks-routing-module').then(
        (m) => m.PlaybooksRoutingModule
      ),
  },
  { path: '', redirectTo: 'playbooks', pathMatch: 'full' },
];
