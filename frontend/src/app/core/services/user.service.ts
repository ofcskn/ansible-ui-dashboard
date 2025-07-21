import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from '../models/user.model';
import { ApiResponse } from '../models/api-response.model';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class UserService {
  private baseUrl = `${environment.API_URL}/users`;

  constructor(private http: HttpClient) {}

  getById(id: string | number): Observable<{ data: User }> {
    return this.http.get<{ data: User }>(`${this.baseUrl}/get/${id}`);
  }

  update(id: string | number, user: User): Observable<any> {
    const payload = { ...user, id };
    return this.http.post(`${this.baseUrl}/manage`, payload);
  }

  list(): Observable<ApiResponse<User[]>> {
    return this.http.get<ApiResponse<User[]>>(`${this.baseUrl}/list`);
  }

  delete(userId: number): Observable<ApiResponse<any>> {
    return this.http.delete<ApiResponse<any>>(`${this.baseUrl}/delete`, {
      body: { id: userId },
    });
  }
}
