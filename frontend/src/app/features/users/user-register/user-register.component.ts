import { Component, NgZone } from '@angular/core';
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
import { UserService } from '../../../core/services/user.service';
import { UserRegister } from '../../../core/models/user.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-register',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
  ],
  templateUrl: './user-register.component.html',
  styleUrl: './user-register.component.scss',
})
export class UserRegisterComponent {
  registerForm!: FormGroup;
  errorMessage?: string | null;

  constructor(
    private fb: FormBuilder,
    private _userService: UserService,
    private router: Router,
    private ngZone: NgZone
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
      const newUser: UserRegister = {
        name: formValue.name,
        email: formValue.email,
        username: formValue.username,
        password: formValue.password,
        confirmPassword: formValue.confirmPassword,
      };
      this._userService.register(newUser).subscribe({
        next: (response) => {
          this.router.navigate(['/users/login']);
        },
        error: (error) => {
          const backendMessage =
            error.error?.message || 'Registration failed due to unknown error.';
          this.ngZone.run(() => {
            this.errorMessage = backendMessage;
          });
          console.log(this.errorMessage);
        },
      });
    }
  }
}
