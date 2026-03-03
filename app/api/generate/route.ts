import { NextRequest, NextResponse } from "next/server"
import { createServerClient, type CookieOptions } from "@supabase/ssr"
import Anthropic from "@anthropic-ai/sdk"
import { getSystemPrompt, buildUserPrompt } from "@/lib/prompts"

export async function POST(request: NextRequest) {
  try {
    // 認証チェック
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          getAll() {
            return request.cookies.getAll()
          },
          setAll(_cookiesToSet: { name: string; value: string; options: CookieOptions }[]) {
            // API routeではcookieの書き込みは不要
          },
        },
      },
    )
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) {
      return NextResponse.json({ error: "認証が必要です" }, { status: 401 })
    }

    const { profile, companyInfo, esType, charLimit, customQuestion } = await request.json()

    if (!profile || !companyInfo || !esType || !charLimit) {
      return NextResponse.json(
        { error: "必須パラメータが不足しています" },
        { status: 400 },
      )
    }

    const apiKey = process.env.ANTHROPIC_API_KEY
    if (!apiKey) {
      return NextResponse.json(
        { error: "ANTHROPIC_API_KEYが設定されていません" },
        { status: 500 },
      )
    }

    const client = new Anthropic({ apiKey })

    const userPrompt = buildUserPrompt(
      profile,
      companyInfo,
      esType,
      charLimit,
      customQuestion,
    )

    const message = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 2048,
      system: getSystemPrompt(esType),
      messages: [{ role: "user", content: userPrompt }],
    })

    const text = message.content[0].type === "text" ? message.content[0].text : ""

    return NextResponse.json({ text })
  } catch (error) {
    const message = error instanceof Error ? error.message : "ES生成中にエラーが発生しました"
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
