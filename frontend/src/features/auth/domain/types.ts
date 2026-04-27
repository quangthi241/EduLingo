export type Role = "learner" | "admin";

export interface AuthUser {
  userId: string;
  email: string;
  role: Role;
  displayName?: string | null;
}

export interface AuthResponse {
  userId: string;
  email: string;
  role: Role;
}

export interface RegisterPayload {
  email: string;
  password: string;
  displayName?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}
