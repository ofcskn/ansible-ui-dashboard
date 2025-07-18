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

  getById(id: string | number): Observable<{ data: Playbook }> {
    return this.http.get<{ data: Playbook }>(`${this.baseUrl}/get/${id}`);
  }

  create(playbook: Playbook): Observable<any> {
    return this.http.post(`${this.baseUrl}/manage`, playbook);
  }

  update(id: string | number, playbook: Playbook): Observable<any> {
    const payload = { ...playbook, id };
    return this.http.post(`${this.baseUrl}/manage`, payload);
  }

  list(): Observable<ApiResponse<Playbook[]>> {
    return this.http.get<ApiResponse<Playbook[]>>(`${this.baseUrl}/list`);
  }

  getContentById(id: string): Observable<ApiResponse<string>> {
    return this.http.get<ApiResponse<string>>(
      `${environment.API_URL}/playbooks/yaml/get/${id}`
    );
  }
  run(playbookId: number): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(`${this.baseUrl}/run`, {
      playbook_id: playbookId,
    });
  }
}
