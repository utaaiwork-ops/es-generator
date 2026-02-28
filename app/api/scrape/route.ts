import { NextRequest, NextResponse } from "next/server"
import * as cheerio from "cheerio"

/** ES作成に有用なページを見つけるためのキーワード */
const RELEVANT_KEYWORDS = [
  // 事業・サービス
  "事業", "サービス", "service", "business", "product", "solution",
  // 企業情報
  "会社概要", "企業情報", "about", "company", "corporate", "理念", "ミッション",
  "ビジョン", "mission", "vision", "philosophy", "value",
  // 採用
  "採用", "recruit", "career", "新卒", "キャリア", "働く", "仕事",
  "job", "entry", "intern",
  // 社員
  "社員", "メンバー", "member", "people", "interview", "インタビュー",
  "voice", "先輩", "座談会", "team",
  // 文化・環境
  "文化", "culture", "環境", "welfare", "制度",
]

const USER_AGENT =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

function isRelevantLink(href: string, text: string): boolean {
  const target = (href + " " + text).toLowerCase()
  return RELEVANT_KEYWORDS.some((kw) => target.includes(kw.toLowerCase()))
}

function extractText($: cheerio.CheerioAPI, maxChars: number = 4000): string {
  // script/style/nav等を除去
  $("script, style, nav, footer, header, iframe, noscript").remove()

  const text = $.root().text()
  const lines = text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
  let result = lines.join("\n")

  if (result.length > maxChars) {
    result = result.slice(0, maxChars)
  }
  return result
}

async function fetchPage(url: string, timeout: number = 15000): Promise<cheerio.CheerioAPI | null> {
  try {
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), timeout)
    const resp = await fetch(url, {
      headers: { "User-Agent": USER_AGENT },
      signal: controller.signal,
    })
    clearTimeout(timer)
    if (!resp.ok) return null
    const html = await resp.text()
    return cheerio.load(html)
  } catch {
    return null
  }
}

function findRelevantLinks(
  $: cheerio.CheerioAPI,
  baseUrl: string,
  maxLinks: number = 8,
): { url: string; label: string }[] {
  const baseDomain = new URL(baseUrl).hostname
  const found: Map<string, string> = new Map()

  $("a[href]").each((_, el) => {
    if (found.size >= maxLinks) return false

    const href = $(el).attr("href")?.trim()
    const text = $(el).text().trim()
    if (!href) return

    // 相対URLを絶対URLに変換
    let fullUrl: string
    try {
      fullUrl = new URL(href, baseUrl).toString()
    } catch {
      return
    }

    // 同一ドメインのみ
    try {
      if (new URL(fullUrl).hostname !== baseDomain) return
    } catch {
      return
    }

    // ファイルリンク除外
    if (/\.(pdf|jpg|png|gif|zip|doc|xlsx)$/i.test(fullUrl)) return

    // 関連性チェック
    if (isRelevantLink(href, text) && !found.has(fullUrl)) {
      const label = text.length > 0 ? text.slice(0, 50) : href
      found.set(fullUrl, label)
    }
  })

  return Array.from(found.entries()).map(([url, label]) => ({ url, label }))
}

export async function POST(request: NextRequest) {
  try {
    const { url } = await request.json()
    if (!url || typeof url !== "string") {
      return NextResponse.json({ error: "URLが指定されていません" }, { status: 400 })
    }

    // 1. トップページを取得
    const $ = await fetchPage(url)
    if (!$) {
      return NextResponse.json(
        { error: `ページの取得に失敗しました: ${url}` },
        { status: 502 },
      )
    }

    const sections: string[] = []
    const topText = extractText(cheerio.load($.html()!), 3000)
    sections.push(`【トップページ】\n${topText}`)

    // 2. 関連ページのリンクを発見
    const links = findRelevantLinks($, url)

    // 3. 関連ページを巡回して情報取得
    for (const link of links) {
      const sub$ = await fetchPage(link.url)
      if (!sub$) continue

      const subText = extractText(sub$, 2000)
      if (subText.length > 100) {
        sections.push(`【${link.label}】\n${subText}`)
      }
    }

    let result = sections.join("\n\n")

    // 全体の上限（Claude APIのコンテキスト節約）
    const maxTotal = 12000
    if (result.length > maxTotal) {
      result = result.slice(0, maxTotal) + "\n...(以下省略)"
    }

    return NextResponse.json({ text: result })
  } catch (error) {
    const message = error instanceof Error ? error.message : "スクレイピング中にエラーが発生しました"
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
