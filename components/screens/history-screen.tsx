"use client"

import { useState, useEffect, useCallback } from "react"
import {
  Building2,
  FileText,
  Copy,
  Trash2,
  Save,
  ChevronDown,
  ChevronUp,
  Search,
  CheckCircle2,
  Sparkles,
  Loader2,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { PageHeader } from "@/components/page-header"
import { useApp } from "@/lib/app-context"
import type { ESItem } from "@/lib/app-context"
import { listEs, updateEs, deleteEs } from "@/lib/db"

/** 改行・空白除去後の文字数カウント */
function countChars(text: string): number {
  return text.replace(/[\s\n\r]/g, "").length
}

export function HistoryScreen() {
  const { setScreen } = useApp()
  const [history, setHistory] = useState<ESItem[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState<number | null>(null)
  const [companyFilter, setCompanyFilter] = useState("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [copiedId, setCopiedId] = useState<number | null>(null)
  const [savedId, setSavedId] = useState<number | null>(null)
  const [editContents, setEditContents] = useState<Record<number, string>>({})

  // DBからES一覧を取得
  const loadHistory = useCallback(async () => {
    try {
      const data = await listEs()
      const items: ESItem[] = data.map((row) => ({
        id: row.id,
        companyId: row.company_id,
        companyName: row.companies?.name ?? "不明",
        esType: row.es_type,
        question: row.question,
        content: row.content,
        charLimit: row.char_limit,
        isEdited: row.is_edited ?? false,
        createdAt: new Date(row.created_at).toLocaleDateString("ja-JP"),
      }))
      setHistory(items)
    } catch (err) {
      console.error("履歴読み込みエラー:", err)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  const uniqueCompanies = Array.from(new Set(history.map((h) => h.companyName)))

  const filtered = history.filter((item) => {
    const matchCompany =
      companyFilter === "all" || item.companyName === companyFilter
    const matchSearch =
      searchQuery === "" ||
      item.content.includes(searchQuery) ||
      item.companyName.includes(searchQuery) ||
      item.esType.includes(searchQuery)
    return matchCompany && matchSearch
  })

  const totalCompanies = uniqueCompanies.length
  const totalES = history.length

  const handleCopy = (id: number, content: string) => {
    navigator.clipboard.writeText(content)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const handleUpdate = async (id: number) => {
    const newContent = editContents[id]
    if (newContent === undefined) return
    try {
      await updateEs(id, newContent)
      setHistory((prev) =>
        prev.map((item) =>
          item.id === id ? { ...item, content: newContent, isEdited: true } : item,
        ),
      )
      setSavedId(id)
      setTimeout(() => setSavedId(null), 2000)
    } catch (err) {
      console.error("更新エラー:", err)
      alert("更新に失敗しました")
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm("このESを削除しますか？")) return
    try {
      await deleteEs(id)
      setHistory((prev) => prev.filter((item) => item.id !== id))
    } catch (err) {
      console.error("削除エラー:", err)
      alert("削除に失敗しました")
    }
  }

  const getEditContent = (item: ESItem) => {
    return editContents[item.id] ?? item.content
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 py-20">
        <Loader2 className="size-8 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">履歴を読み込み中...</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-5">
      <PageHeader title="履歴一覧" description="企業ごとに生成したESを管理" />

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-[14px] border border-border bg-card p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-lg bg-[#F0FDFA]">
              <Building2 className="size-4 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold text-foreground">{totalCompanies}</p>
              <p className="text-xs text-muted-foreground">登録企業数</p>
            </div>
          </div>
        </div>
        <div className="rounded-[14px] border border-border bg-card p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-lg bg-[#F0FDFA]">
              <FileText className="size-4 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold text-foreground">{totalES}</p>
              <p className="text-xs text-muted-foreground">生成ES数</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-3 md:flex-row md:items-center">
        <Select value={companyFilter} onValueChange={setCompanyFilter}>
          <SelectTrigger className="h-9 w-full rounded-[10px] border-[1.5px] text-xs md:w-48">
            <SelectValue placeholder="会社フィルタ" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">すべての企業</SelectItem>
            {uniqueCompanies.map((c) => (
              <SelectItem key={c} value={c}>
                {c}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 size-3.5 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="キーワード検索"
            className="h-9 rounded-[10px] border-[1.5px] pl-9 text-xs"
          />
        </div>
      </div>

      {/* List */}
      {filtered.length === 0 ? (
        <div className="flex flex-col items-center gap-3 rounded-[14px] border border-border bg-card py-16 shadow-sm">
          <div className="flex size-14 items-center justify-center rounded-full bg-secondary">
            <FileText className="size-6 text-muted-foreground" />
          </div>
          <p className="text-sm font-medium text-foreground">
            {history.length === 0
              ? "まだ保存されたESはありません"
              : "該当するESが見つかりません"}
          </p>
          <p className="text-xs text-muted-foreground">
            {history.length === 0
              ? "ES生成画面で作成して保存すると、ここに表示されます"
              : "フィルタ条件を変更してください"}
          </p>
          {history.length === 0 && (
            <Button
              onClick={() => setScreen("generate")}
              className="mt-2 h-9 rounded-[10px] bg-gradient-to-r from-[#0D9488] to-[#0F766E] px-5 text-xs font-semibold text-[#FFFFFF] hover:from-[#0F766E] hover:to-[#115E59]"
            >
              <Sparkles className="mr-1.5 size-3.5" />
              ES生成画面へ
            </Button>
          )}
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map((item) => {
            const isExpanded = expandedId === item.id
            const currentContent = getEditContent(item)
            const charCount = countChars(currentContent)
            return (
              <div
                key={item.id}
                className="rounded-[14px] border border-border bg-card shadow-sm transition-all hover:shadow-md"
              >
                {/* Header */}
                <div className="flex flex-col gap-2 px-4 py-4 md:flex-row md:items-center md:justify-between md:px-5">
                  <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-3">
                    <button
                      onClick={() =>
                        setExpandedId(isExpanded ? null : item.id)
                      }
                      className="flex items-center gap-3"
                      aria-label={isExpanded ? "折りたたむ" : "展開する"}
                    >
                      {isExpanded ? (
                        <ChevronUp className="size-4 text-muted-foreground" />
                      ) : (
                        <ChevronDown className="size-4 text-muted-foreground" />
                      )}
                      <span className="text-sm font-semibold text-foreground">
                        {item.companyName}
                      </span>
                    </button>
                    <div className="flex items-center gap-2 pl-7 md:pl-0">
                      <Badge
                        variant="secondary"
                        className="rounded-full text-[10px]"
                      >
                        {item.esType}
                      </Badge>
                      <span className="text-xs text-muted-foreground">
                        {item.createdAt}
                      </span>
                    </div>
                  </div>
                  <Button
                    onClick={() => handleCopy(item.id, currentContent)}
                    variant="ghost"
                    size="sm"
                    className="h-8 gap-1.5 rounded-lg px-3 text-xs"
                  >
                    {copiedId === item.id ? (
                      <>
                        <CheckCircle2 className="size-3.5 text-[#059669]" />
                        <span className="text-[#059669]">コピー済</span>
                      </>
                    ) : (
                      <>
                        <Copy className="size-3.5" />
                        コピー
                      </>
                    )}
                  </Button>
                </div>

                {/* Expanded content */}
                {isExpanded && (
                  <div className="border-t border-border px-4 pb-5 pt-4 md:px-5">
                    <Textarea
                      value={currentContent}
                      onChange={(e) =>
                        setEditContents((prev) => ({
                          ...prev,
                          [item.id]: e.target.value,
                        }))
                      }
                      className="min-h-[160px] rounded-[10px] border-[1.5px] text-sm leading-relaxed"
                      rows={8}
                    />
                    <div className="mt-2 flex items-center justify-between">
                      <span className="text-xs text-muted-foreground">
                        編集して内容を調整できます
                      </span>
                      <span
                        className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                          charCount <= item.charLimit
                            ? "bg-[#059669]/10 text-[#059669]"
                            : "bg-destructive/10 text-destructive"
                        }`}
                      >
                        {charCount} / {item.charLimit}字
                      </span>
                    </div>
                    <div className="mt-4 flex gap-2">
                      <Button
                        onClick={() => handleUpdate(item.id)}
                        className="h-9 rounded-[10px] bg-gradient-to-r from-[#0D9488] to-[#0F766E] px-4 text-xs font-semibold text-[#FFFFFF] hover:from-[#0F766E] hover:to-[#115E59]"
                      >
                        {savedId === item.id ? (
                          <>
                            <CheckCircle2 className="mr-1 size-3.5" />
                            更新済
                          </>
                        ) : (
                          <>
                            <Save className="mr-1 size-3.5" />
                            更新
                          </>
                        )}
                      </Button>
                      <Button
                        onClick={() => handleCopy(item.id, currentContent)}
                        variant="outline"
                        className="h-9 rounded-[10px] px-4 text-xs"
                      >
                        <Copy className="mr-1 size-3.5" />
                        コピー
                      </Button>
                      <Button
                        onClick={() => handleDelete(item.id)}
                        variant="outline"
                        className="h-9 rounded-[10px] border-destructive/30 px-4 text-xs text-destructive hover:bg-destructive/5 hover:text-destructive"
                      >
                        <Trash2 className="mr-1 size-3.5" />
                        削除
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
