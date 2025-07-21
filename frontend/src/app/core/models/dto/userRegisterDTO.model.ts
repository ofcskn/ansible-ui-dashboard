export interface UserRegisterDTO {
  name: string;
  email: string;
  username: string;
  password: string;
  confirmPassword?: string;
}
