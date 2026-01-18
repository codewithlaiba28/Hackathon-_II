import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function GET(req: NextRequest) {
    const cookieStore = await cookies();
    const token = cookieStore.get("better-auth.session_token") ||
        cookieStore.get("__Secure-better-auth.session_token") ||
        cookieStore.get("session_token");

    if (!token) {
        console.error("Token route failed: No session token cookie found. Available cookies:",
            cookieStore.getAll().map(c => c.name).join(", "));
        return NextResponse.json({ error: "No session token found" }, { status: 401 });
    }

    return NextResponse.json({ token: token.value });
}
