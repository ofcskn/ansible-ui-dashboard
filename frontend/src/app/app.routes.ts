import { Routes } from '@angular/router';
import { AuthGuard } from './core/utils/auth.guard';
import { UnauthorizedComponent } from './features/shared/unauthorized/unauthorized.component';
import { NotFoundComponent } from './features/shared/not-found/not-found.component';

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
    data: { roles: ['admin'] },
    canActivate: [AuthGuard],
  },
  {
    path: 'auth',
    loadChildren: () =>
      import('./features/auth/auth-routing-module').then(
        (m) => m.AuthRoutingModule
      ),
  },
  { path: '', redirectTo: 'playbooks', pathMatch: 'full' },
  { path: 'unauthorized', component: UnauthorizedComponent },
  { path: '**', component: NotFoundComponent },
];
