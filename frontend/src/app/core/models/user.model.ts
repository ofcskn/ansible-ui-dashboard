export interface User {
  id: number;
  name: string;
  email: string;
  username: string;
  role?: string;
  is_active?: boolean;
}
