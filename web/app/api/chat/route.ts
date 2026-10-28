import { NextResponse } from "next/server";

export const runtime = "nodejs";

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { detail: "Request body must be valid JSON." },
      { status: 400 },
    );
  }

  if (
    typeof body !== "object" ||
    body === null ||
    !("message" in body) ||
    typeof body.message !== "string" ||
    !body.message.trim()
  ) {
    return NextResponse.json(
      { detail: "A non-empty message is required." },
      { status: 422 },
    );
  }

  const apiUrl = (process.env.API_URL ?? "http://127.0.0.1:8000").replace(
    /\/+$/,
    "",
  );

  try {
    const response = await fetch(`${apiUrl}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: body.message }),
      cache: "no-store",
      signal: AbortSignal.timeout(130_000),
    });
    const responseBody: unknown = await response.json();

    return NextResponse.json(responseBody, { status: response.status });
  } catch (error) {
    const detail =
      error instanceof Error && error.name === "TimeoutError"
        ? "The API request timed out. Please try again."
        : `Could not reach the FastAPI backend at ${apiUrl}. Make sure it is running.`;

    return NextResponse.json({ detail }, { status: 503 });
  }
}