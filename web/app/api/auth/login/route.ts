import { NextResponse } from "next/server";
import { AUTH_COOKIE_NAME, DEMO_USERS, createSessionToken } from "@/lib/auth";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const email = String(body.email || "").trim().toLowerCase();
    const password = String(body.password || "").trim();

    if (!email) {
      return NextResponse.json({ error: "Email address is required." }, { status: 400 });
    }

    let user = DEMO_USERS[email];
    if (user) {
      if (user.passwordHash !== password) {
        return NextResponse.json({ error: "Invalid password for this account." }, { status: 401 });
      }
    } else {
      // Allow dynamic enterprise sign-in for any valid corporate email
      if (!password || password.length < 6) {
        return NextResponse.json(
          { error: "Password must be at least 6 characters." },
          { status: 400 },
        );
      }
      const rawName = email.split("@")[0].replace(/[._-]/g, " ");
      const formattedName = rawName
        .split(" ")
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(" ");

      user = {
        id: `usr_${Date.now()}`,
        name: formattedName || "Corporate User",
        email,
        role: "Employee",
        department: "Operations",
        avatar: (formattedName || "U").charAt(0).toUpperCase(),
        passwordHash: password,
      };
    }

    const { passwordHash: _, ...profile } = user;
    const token = createSessionToken(profile);

    const response = NextResponse.json({ user: profile, success: true });
    response.cookies.set({
      name: AUTH_COOKIE_NAME,
      value: token,
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 7 * 24 * 60 * 60,
      path: "/",
    });

    return response;
  } catch {
    return NextResponse.json({ error: "Internal server error." }, { status: 500 });
  }
}
