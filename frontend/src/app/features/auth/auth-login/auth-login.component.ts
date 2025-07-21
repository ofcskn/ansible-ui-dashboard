import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { UserLoginDTO } from '../../../core/models/dto/userLoginDTO.model';
import { AuthService } from '../../../core/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'auth-user-login',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
  ],
  templateUrl: './auth-login.component.html',
  styleUrl: './auth-login.component.scss',
})
export class AuthLoginComponent {
  loginForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private _authService: AuthService,
    private _router: Router
  ) {}

  ngOnInit(): void {
    const token = this._authService.getToken() || '';
    const isValidToken = this._authService.isTokenValid(token);
    if (isValidToken) {
      this._router.navigate(['']);
    }

    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      rememberMe: [false],
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const credentials = this.loginForm.value;
      const loginDTO: UserLoginDTO = {
        handle: credentials.email,
        password: credentials.password,
      };
      this._authService.login(loginDTO).subscribe({
        next: (response) => {
          this._router.navigate(['/playbooks']);
        },
        error: (error) => {
          console.log(error);
        },
      });
    }
  }
}
