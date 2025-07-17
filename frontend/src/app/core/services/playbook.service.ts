import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Playbook } from '../models/playbook.model';
import { ApiResponse } from '../models/api-response.model';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class PlaybookService {
  private baseUrl = `${environment.API_URL}/playbooks`;

  constructor(private http: HttpClient) {}

  list(): Observable<ApiResponse<Playbook[]>> {
    return this.http.get<ApiResponse<Playbook[]>>(`${this.baseUrl}/list`);
  }

  run(playbookId: string): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(`${this.baseUrl}/run`, {
      playbook: playbookId,
    });
  }
}
