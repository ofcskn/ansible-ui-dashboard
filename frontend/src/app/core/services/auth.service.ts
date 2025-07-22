import { jwtDecode } from 'jwt-decode';
import { TokenStorageService } from './token-storage.service';
import { environment } from '../../../environments/environment';
import { computed, Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserLoginDTO } from '../models/dto/userLoginDTO.model';
import { BehaviorSubject, Observable, switchMap, tap } from 'rxjs';
import { ApiResponse } from '../models/api-response.model';
import { UserRegisterDTO } from '../models/dto/userRegisterDTO.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseUrl = `${environment.API_URL}/users`;
  private isLoggedInSubject = new BehaviorSubject<boolean>(false);
  public isLoggedIn$ = this.isLoggedInSubject.asObservable();

  constructor(
    private _http: HttpClient,
    private _tokenStorage: TokenStorageService
  ) {
    this.checkTokenValidity();
  }

  async checkTokenValidity() {
    const isValid = await this.isTokenValid();
    this.isLoggedInSubject.next(isValid);
  }

  async isTokenValid(): Promise<boolean> {
    try {
      const token = await this._tokenStorage.getToken();
      if (token) {
        const decoded: any = jwtDecode(token);
        if (!decoded.exp) return false;
        const now = Date.now().valueOf() / 1000;
        return decoded.exp > now;
      }
      return false;
    } catch {
      return false;
    }
  }

  async userHasRole(expectedRoles: string[]): Promise<boolean> {
    const token = await this._tokenStorage.getToken();
    if (!token) return false;

    try {
      const decoded: any = jwtDecode(token);
      const userRole = decoded.role;
      if (Array.isArray(userRole)) {
        return expectedRoles.some((r) => userRole.includes(r));
      } else {
        return expectedRoles.includes(userRole);
      }
    } catch {
      return false;
    }
  }

  login(loginDTO: UserLoginDTO): Observable<any> {
    return this._http
      .post<ApiResponse<{ token: string }>>(`${this.baseUrl}/login`, loginDTO)
      .pipe(
        switchMap(async (response) => {
          await this._tokenStorage.setToken(response.data.token);
          await this.checkTokenValidity();
          return response;
        })
      );
  }

  register(user: UserRegisterDTO): Observable<any> {
    return this._http.post(`${this.baseUrl}/register`, user);
  }

  logout(): void {
    this._tokenStorage.removeToken();
    this.isLoggedInSubject.next(false);
  }
}
