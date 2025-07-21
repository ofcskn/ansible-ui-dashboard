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
    if (token == null || this.isTokenValid(token) == false) {
      this.router.navigate(['/users/login'], {
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

  private isTokenValid(token: string): boolean {
    try {
      const decoded: any = jwtDecode(token);
      if (!decoded.exp) return false; // no expiry claim

      const now = Date.now().valueOf() / 1000; // seconds since epoch
      return decoded.exp > now; // token expiration check
    } catch (error) {
      return false; // invalid token format
    }
  }
}
