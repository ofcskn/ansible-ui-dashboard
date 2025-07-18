import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SocketService {
  constructor(private socket: Socket) {}

  getPlaybookLogs(): Observable<string> {
    return new Observable((observer) => {
      this.socket.on('playbook_log', (data: any) => {
        observer.next(data.log); // emits the log line
      });

      return () => {
        this.socket.off('playbook_log'); // unsubscribe on destroy
      };
    });
  }
}
