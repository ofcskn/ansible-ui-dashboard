export interface User {
  id: number;
  name: string;
  email: string;
  username: string;
  role?: string;
  is_active?: boolean;
}

export interface UserRegister {
  name: string;
  email: string;
  username: string;
  password: string;
  confirmPassword?: string;
}
