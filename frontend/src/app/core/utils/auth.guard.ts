import { Injectable } from '@angular/core';
import {
  CanActivate,
  Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
} from '@angular/router';
import { AuthService } from '../services/auth.service';
import { jwtDecode } from 'jwt-decode';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private _authService: AuthService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    const token = this._authService.getToken() || '';
    if (token == null || this._authService.isTokenValid(token) == false) {
      this.router.navigate(['/auth/login'], {
        queryParams: { returnUrl: state.url },
      });
      return false;
    }

    const expectedRoles = route.data['roles'];
    if (expectedRoles && !this._authService.userHasRole(expectedRoles)) {
      this.router.navigate(['/unauthorized']);
      return false;
    }

    return true;
  }
}
