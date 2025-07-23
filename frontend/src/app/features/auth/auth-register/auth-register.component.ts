import { ChangeDetectorRef, Component, NgZone } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { UserRegisterDTO } from '../../../core/models/dto/userRegisterDTO.model';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-auth-register',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
  ],
  templateUrl: './auth-register.component.html',
  styleUrl: './auth-register.component.scss',
})
export class AuthRegisterComponent {
  registerForm!: FormGroup;
  errorMessage?: string | null;

  constructor(
    private fb: FormBuilder,
    private _authService: AuthService,
    private router: Router,
    private _ctr: ChangeDetectorRef,
    private _ngZone: NgZone
  ) {}

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      name: ['', Validators.required],
      username: ['', [Validators.required, Validators.max(12)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required],
      rememberMe: [false],
    });
  }

  onSubmit() {
    if (this.registerForm.valid) {
      const formValue = this.registerForm.value;
      const newUser: UserRegisterDTO = {
        name: formValue.name,
        email: formValue.email,
        username: formValue.username,
        password: formValue.password,
        confirmPassword: formValue.confirmPassword,
      };
      this._authService.register(newUser).subscribe({
        next: (response) => {
          this.router.navigate(['/auth/login']);
        },
        error: (error) => {
          const backendMessage =
            error.error?.message || 'Registration failed due to unknown error.';
          this._ngZone.run(() => {
            this.errorMessage = backendMessage;
            this._ctr.markForCheck();
          });
        },
      });
    }
  }
}
