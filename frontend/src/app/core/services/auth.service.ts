import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { UserLoginDTO } from '../models/dto/userLoginDTO.model';
import { UserRegisterDTO } from '../models/dto/userRegisterDTO.model';
import { jwtDecode } from 'jwt-decode';
import { ApiResponse } from '../models/api-response.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private tokenKey = 'auth_token';
  private baseUrl = `${environment.API_URL}/users`;

  constructor(private http: HttpClient) {}

  getToken(): string | null {
    if (typeof window !== 'undefined' && window.localStorage) {
      return localStorage.getItem(this.tokenKey);
    }
    return null;
  }

  setToken(token: string): void {
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem(this.tokenKey, token);
    }
  }

  removeToken(): void {
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.removeItem(this.tokenKey);
    }
  }

  login(loginDTO: UserLoginDTO): Observable<any> {
    const payload = { ...loginDTO };
    return this.http
      .post<ApiResponse<{ token: string }>>(`${this.baseUrl}/login`, payload)
      .pipe(
        tap((response) => {
          this.setToken(response.data.token);
        })
      );
  }

  userHasRole(expectedRoles: string[]): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const decoded: any = jwtDecode(token);
      const userRole = decoded.role;

      if (Array.isArray(userRole)) {
        return expectedRoles.some((role) => userRole.includes(role));
      } else {
        return expectedRoles.includes(userRole);
      }
    } catch {
      return false;
    }
  }

  register(user: UserRegisterDTO): Observable<any> {
    const payload = { ...user };
    return this.http.post(`${this.baseUrl}/register`, payload);
  }

  logout() {
    this.removeToken();
  }
}
