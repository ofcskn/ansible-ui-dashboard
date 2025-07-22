import { Component, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { AuthService } from './core/services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    CommonModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('frontend');

  constructor(private _router: Router, private _authService: AuthService) {}

  isLoggedIn(): boolean {
    return this._authService.isLoggedIn();
  }

  goTo(href: string) {
    this._router.navigate([href]);
  }

  logout() {
    this._authService.logout();
    this._router.navigate(['/auth/login']).then((success) => {});
  }
}
