import { NextRequest, NextResponse } from "next/server"
import Anthropic from "@anthropic-ai/sdk"
import { getSystemPrompt, buildUserPrompt } from "@/lib/prompts"

export async function POST(request: NextRequest) {
  try {
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

    // LLMは日本語の文字数カウントが不正確なので、内部的に25%少ない上限を渡す
    const internalLimit = Math.floor(charLimit * 0.75)

    const userPrompt = buildUserPrompt(
      profile,
      companyInfo,
      esType,
      internalLimit,
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
