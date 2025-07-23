import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, NgZone, OnInit } from '@angular/core';
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
import { ActivatedRoute, Router } from '@angular/router';

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
export class AuthLoginComponent implements OnInit {
  loginForm!: FormGroup;
  errorMessage?: string | null;

  constructor(
    private fb: FormBuilder,
    private _authService: AuthService,
    private _router: Router,
    private _route: ActivatedRoute,
    private _ctr: ChangeDetectorRef,
    private _ngZone: NgZone
  ) {
    this.loginForm = this.fb.group({
      handle: ['', [Validators.required]],
      password: ['', Validators.required],
    });
  }

  redirectAfterLogin() {
    const returnUrl =
      this._route.snapshot.queryParamMap.get('returnUrl') || '/';
    this._router.navigate([returnUrl]);
  }

  async ngOnInit(): Promise<void> {
    const isValidToken = await this._authService.isTokenValid();
    if (isValidToken) {
      this._router.navigate(['']);
    }
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const credentials = this.loginForm.value;
      const loginDTO: UserLoginDTO = {
        handle: credentials.handle,
        password: credentials.password,
      };
      this._authService.login(loginDTO).subscribe({
        next: (response) => {
          this.redirectAfterLogin();
        },
        error: (error) => {
          const backendMessage =
            error.error?.message || 'Login failed due to unknown error.';
          this._ngZone.run(() => {
            this.errorMessage = backendMessage;
            this._ctr.markForCheck();
          });
        },
      });
    }
  }
}
