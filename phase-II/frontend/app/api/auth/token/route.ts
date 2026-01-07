import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function GET(req: NextRequest) {
    const cookieStore = await cookies();
    const token = cookieStore.get("better-auth.session_token") || cookieStore.get("session_token");

    if (!token) {
        return NextResponse.json({ error: "No session token found" }, { status: 401 });
    }

    return NextResponse.json({ token: token.value });
}
