export type UserProfile = {
  id: string;
  name: string;
  email: string;
  role: string;
  department: string;
  avatar: string;
};

export const DEMO_USERS: Record<string, UserProfile & { passwordHash: string }> = {
  "simran@xyz.example": {
    id: "usr_simran_1",
    name: "Simran Dangol",
    email: "simran@xyz.example",
    role: "Employee",
    department: "Engineering",
    avatar: "S",
    passwordHash: "password123",
  },
  "alex@xyz.example": {
    id: "usr_alex_2",
    name: "Alex Chen",
    email: "alex@xyz.example",
    role: "Staff Engineer",
    department: "Platform Infrastructure",
    avatar: "A",
    passwordHash: "password123",
  },
  "admin@xyz.example": {
    id: "usr_admin_3",
    name: "Jordan Lee",
    email: "admin@xyz.example",
    role: "IT Administrator",
    department: "Corporate IT & Security",
    avatar: "J",
    passwordHash: "admin123",
  },
};

export const AUTH_COOKIE_NAME = "xyz_copilot_session";

export function createSessionToken(user: UserProfile): string {
  const payload = {
    ...user,
    iat: Date.now(),
    exp: Date.now() + 7 * 24 * 60 * 60 * 1000, // 7 days
  };
  return Buffer.from(JSON.stringify(payload)).toString("base64url");
}

export function parseSessionToken(token: string): UserProfile | null {
  try {
    const raw = Buffer.from(token, "base64url").toString("utf-8");
    const data = JSON.parse(raw);
    if (!data || !data.email || !data.name || (data.exp && Date.now() > data.exp)) {
      return null;
    }
    return {
      id: data.id || "usr_default",
      name: data.name,
      email: data.email,
      role: data.role || "Employee",
      department: data.department || "General",
      avatar: data.avatar || data.name.charAt(0).toUpperCase(),
    };
  } catch {
    return null;
  }
}
