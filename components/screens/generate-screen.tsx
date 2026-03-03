"use client"

import { useState, useRef, useEffect } from "react"
import {
  Sparkles,
  Copy,
  Save,
  ArrowRight,
  Lightbulb,
  CheckCircle2,
  Loader2,
  Globe,
  PenLine,
  AlertTriangle,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Slider } from "@/components/ui/slider"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { PageHeader } from "@/components/page-header"
import { useApp, defaultProfile } from "@/lib/app-context"
import { getProfile } from "@/lib/db"
import { createCompany, saveEs } from "@/lib/db"
import { profileKeyToDbField } from "@/lib/field-map"
import type { Profile } from "@/lib/app-context"

const esTypes = [
  "志望動機",
  "ガクチカ",
  "自己PR",
  "強み・弱み",
  "将来やりたいこと",
  "その他",
]

/** 改行・空白除去後の文字数カウント（Python版と同じ） */
function countChars(text: string): number {
  return text.replace(/[\s\n\r]/g, "").length
}

export function GenerateScreen() {
  const { profile, setProfile, isProfileComplete, setScreen, user } = useApp()

  const [companyName, setCompanyName] = useState("")
  const [companyUrl, setCompanyUrl] = useState("")
  const [manualInfo, setManualInfo] = useState("")
  const [esType, setEsType] = useState("")
  const [customQuestion, setCustomQuestion] = useState("")
  const [charLimit, setCharLimit] = useState([400])
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedText, setGeneratedText] = useState("")
  const [copied, setCopied] = useState(false)
  const [savedMsg, setSavedMsg] = useState(false)
  const [fetchingUrl, setFetchingUrl] = useState(false)
  const [scrapedInfo, setScrapedInfo] = useState("")
  const [profileLoaded, setProfileLoaded] = useState(false)
  const resultRef = useRef<HTMLDivElement>(null)

  // プロフィールをDBから読み込み
  useEffect(() => {
    async function load() {
      try {
        const data = await getProfile()
        const merged = { ...defaultProfile, ...data }
        setProfile(merged)
      } catch (err) {
        console.error("プロフィール読み込みエラー:", err)
      } finally {
        setProfileLoaded(true)
      }
    }
    load()
  }, [setProfile])

  const canGenerate = companyName.trim() !== "" && esType !== ""

  const handleFetchUrl = async () => {
    if (!companyUrl.trim()) return
    setFetchingUrl(true)
    try {
      const resp = await fetch("/api/scrape", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: companyUrl }),
      })
      const data = await resp.json()
      if (data.error) {
        alert(`スクレイピングエラー: ${data.error}`)
      } else {
        setScrapedInfo(data.text)
        setManualInfo((prev) =>
          prev
            ? prev + "\n\n" + data.text
            : data.text,
        )
      }
    } catch (err) {
      console.error("スクレイピングエラー:", err)
      alert("企業情報の取得に失敗しました")
    } finally {
      setFetchingUrl(false)
    }
  }

  const handleGenerate = async () => {
    if (!canGenerate) return
    setIsGenerating(true)
    setGeneratedText("")
    try {
      // プロフィールをDB形式で送信（プロンプト側がkey: valueで使うため）
      const profileForApi: Record<string, string> = {}
      for (const [key, value] of Object.entries(profile)) {
        if (value) {
          profileForApi[profileKeyToDbField(key as keyof Profile)] = value
        }
      }

      const companyInfo = manualInfo || scrapedInfo || `会社名: ${companyName}`

      const resp = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          profile: profileForApi,
          companyInfo,
          esType: esType === "その他" ? "その他" : esType,
          charLimit: charLimit[0],
          customQuestion: esType === "その他" ? customQuestion || null : null,
        }),
      })
      const data = await resp.json()
      if (data.error) {
        alert(`ES生成エラー: ${data.error}`)
      } else {
        setGeneratedText(data.text)
        setTimeout(() => {
          resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
        }, 100)
      }
    } catch (err) {
      console.error("ES生成エラー:", err)
      alert("ES生成に失敗しました")
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedText)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleSave = async () => {
    try {
      const companyId = await createCompany(
        user!.id,
        companyName,
        companyUrl || null,
        scrapedInfo || null,
        manualInfo || null,
      )
      await saveEs(
        user!.id,
        companyId,
        esType,
        esType === "その他" ? customQuestion || null : null,
        charLimit[0],
        generatedText,
      )
      setSavedMsg(true)
      setTimeout(() => setSavedMsg(false), 2000)
    } catch (err) {
      console.error("保存エラー:", err)
      alert("保存に失敗しました")
    }
  }

  const handleNext = () => {
    setCompanyName("")
    setCompanyUrl("")
    setManualInfo("")
    setScrapedInfo("")
    setEsType("")
    setCustomQuestion("")
    setCharLimit([400])
    setGeneratedText("")
    setCopied(false)
    setSavedMsg(false)
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  const charCount = countChars(generatedText)
  const charStatus =
    charCount === 0
      ? "neutral"
      : charCount <= charLimit[0] * 0.9
        ? "ok"
        : charCount <= charLimit[0]
          ? "warn"
          : "over"

  return (
    <div className="flex flex-col gap-5">
      <PageHeader title="ES生成" description="企業URLを入力して、AIが自動生成" />

      {/* プロフィール未登録警告 */}
      {profileLoaded && !isProfileComplete && (
        <div className="flex items-start gap-3 rounded-[14px] border border-[#F97316]/30 bg-[#FFF7ED] p-4">
          <AlertTriangle className="mt-0.5 size-4 shrink-0 text-[#F97316]" />
          <div>
            <p className="text-sm font-medium text-foreground">
              プロフィールが未登録です
            </p>
            <p className="mt-0.5 text-xs text-muted-foreground">
              先にプロフィールを登録すると、より質の高いESが生成できます
            </p>
            <Button
              onClick={() => setScreen("profile")}
              variant="outline"
              className="mt-2 h-8 rounded-lg border-[#F97316]/30 px-3 text-xs text-[#F97316] hover:bg-[#FFF7ED]"
            >
              プロフィール設定へ
            </Button>
          </div>
        </div>
      )}

      {/* Step 1 */}
      <section className="rounded-[14px] border border-border bg-card p-4 shadow-sm md:p-6">
        <div className="flex items-center gap-2.5">
          <span className="flex size-6 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
            1
          </span>
          <h2 className="text-sm font-semibold text-foreground">会社情報を入力</h2>
        </div>
        <div className="mt-4 flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-foreground">会社名</label>
            <Input
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder="株式会社〇〇"
              className="h-10 rounded-[10px] border-[1.5px] text-sm"
            />
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {/* URL auto-fetch */}
            <div className="flex flex-col gap-1.5">
              <label className="flex items-center gap-1.5 text-xs font-medium text-foreground">
                <Globe className="size-3.5 text-muted-foreground" />
                URLから自動取得
              </label>
              <div className="flex gap-2">
                <Input
                  value={companyUrl}
                  onChange={(e) => setCompanyUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="h-10 rounded-[10px] border-[1.5px] text-sm"
                />
                <Button
                  onClick={handleFetchUrl}
                  disabled={fetchingUrl || !companyUrl.trim()}
                  variant="outline"
                  className="h-10 shrink-0 rounded-[10px] px-4 text-xs font-medium"
                >
                  {fetchingUrl ? (
                    <Loader2 className="size-4 animate-spin" />
                  ) : (
                    "取得"
                  )}
                </Button>
              </div>
            </div>

            {/* Manual input */}
            <div className="flex flex-col gap-1.5">
              <label className="flex items-center gap-1.5 text-xs font-medium text-foreground">
                <PenLine className="size-3.5 text-muted-foreground" />
                手動で入力
              </label>
              <Textarea
                value={manualInfo}
                onChange={(e) => setManualInfo(e.target.value)}
                placeholder="企業理念、事業内容など"
                className="min-h-[80px] rounded-[10px] border-[1.5px] text-sm"
                rows={3}
              />
            </div>
          </div>

          <div className="flex items-start gap-2.5 rounded-lg border border-[#0D9488]/20 bg-[#F0FDFA] px-3 py-2.5">
            <Lightbulb className="mt-0.5 size-3.5 shrink-0 text-primary" />
            <p className="text-xs leading-relaxed text-foreground/70">
              URLと手動入力は併用できます。説明会で聞いた情報を追加すると精度UP
            </p>
          </div>
        </div>
      </section>

      {/* Step 2 */}
      <section className="rounded-[14px] border border-border bg-card p-4 shadow-sm md:p-6">
        <div className="flex items-center gap-2.5">
          <span className="flex size-6 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
            2
          </span>
          <h2 className="text-sm font-semibold text-foreground">ES項目を選択</h2>
        </div>
        <div className="mt-4 flex flex-col gap-3">
          <Select value={esType} onValueChange={setEsType}>
            <SelectTrigger className="h-10 w-full rounded-[10px] border-[1.5px] text-sm">
              <SelectValue placeholder="ES項目を選んでください" />
            </SelectTrigger>
            <SelectContent>
              {esTypes.map((type) => (
                <SelectItem key={type} value={type}>
                  {type}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {esType === "その他" && (
            <Input
              value={customQuestion}
              onChange={(e) => setCustomQuestion(e.target.value)}
              placeholder="質問内容を入力してください（例: あなたの挫折経験を教えてください）"
              className="h-10 rounded-[10px] border-[1.5px] text-sm"
            />
          )}
        </div>
      </section>

      {/* Step 3 */}
      <section className="rounded-[14px] border border-border bg-card p-4 shadow-sm md:p-6">
        <div className="flex items-center gap-2.5">
          <span className="flex size-6 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
            3
          </span>
          <h2 className="text-sm font-semibold text-foreground">文字数を指定</h2>
        </div>
        <div className="mt-4 flex flex-col gap-3">
          <Slider
            value={charLimit}
            onValueChange={setCharLimit}
            min={100}
            max={800}
            step={50}
            className="w-full"
          />
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">100字</span>
            <span className="rounded-full bg-primary/10 px-3 py-0.5 text-sm font-semibold text-primary">
              {charLimit[0]}字
            </span>
            <span className="text-xs text-muted-foreground">800字</span>
          </div>
        </div>
      </section>

      {/* Step 4 - Generate */}
      <section className="rounded-[14px] border border-border bg-card p-4 shadow-sm md:p-6">
        <div className="flex items-center gap-2.5">
          <span className="flex size-6 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
            4
          </span>
          <h2 className="text-sm font-semibold text-foreground">生成</h2>
        </div>
        <div className="mt-4">
          <Button
            onClick={handleGenerate}
            disabled={!canGenerate || isGenerating}
            className="h-12 w-full rounded-[10px] bg-gradient-to-r from-[#0D9488] to-[#0F766E] text-base font-semibold text-[#FFFFFF] hover:from-[#0F766E] hover:to-[#115E59] disabled:opacity-50"
          >
            {isGenerating ? (
              <>
                <Loader2 className="mr-2 size-5 animate-spin" />
                生成中...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 size-5" />
                ESを生成する
              </>
            )}
          </Button>
          <p className="mt-2 text-center text-xs text-muted-foreground">
            あとから編集もできます
          </p>
        </div>
      </section>

      {/* Result */}
      {generatedText && (
        <div ref={resultRef} className="flex flex-col gap-4">
          {/* Success banner */}
          <div className="flex items-center gap-2 rounded-[10px] bg-[#059669]/10 px-4 py-3">
            <CheckCircle2 className="size-4 text-[#059669]" />
            <span className="text-sm font-medium text-[#059669]">生成完了</span>
          </div>

          <section className="rounded-[14px] border border-border bg-card p-4 shadow-sm md:p-6">
            <Textarea
              value={generatedText}
              onChange={(e) => setGeneratedText(e.target.value)}
              className="min-h-[200px] rounded-[10px] border-[1.5px] text-sm leading-relaxed"
              rows={10}
            />

            {/* Char counter */}
            <div className="mt-3 flex items-center justify-between">
              <p className="text-xs text-muted-foreground">
                {charStatus === "ok" && "このまま提出できるレベルです"}
                {charStatus === "warn" &&
                  `あと${charLimit[0] - charCount}字の余裕があります`}
                {charStatus === "over" &&
                  `${charCount - charLimit[0]}字オーバーしています`}
              </p>
              <span
                className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                  charStatus === "ok"
                    ? "bg-[#059669]/10 text-[#059669]"
                    : charStatus === "warn"
                      ? "bg-[#F59E0B]/10 text-[#D97706]"
                      : charStatus === "over"
                        ? "bg-destructive/10 text-destructive"
                        : "bg-secondary text-muted-foreground"
                }`}
              >
                {charCount} / {charLimit[0]}字
              </span>
            </div>

            {/* Action buttons */}
            <div className="mt-5 flex flex-col gap-2 sm:flex-row">
              <Button
                onClick={handleCopy}
                className="h-11 flex-1 rounded-[10px] bg-accent text-sm font-semibold text-accent-foreground hover:bg-[#EA680C]"
              >
                {copied ? (
                  <>
                    <CheckCircle2 className="mr-1.5 size-4" />
                    コピーしました
                  </>
                ) : (
                  <>
                    <Copy className="mr-1.5 size-4" />
                    コピー
                  </>
                )}
              </Button>
              <Button
                onClick={handleSave}
                variant="outline"
                className="h-11 flex-1 rounded-[10px] border-[1.5px] text-sm font-medium"
              >
                {savedMsg ? (
                  <>
                    <CheckCircle2 className="mr-1.5 size-4 text-[#059669]" />
                    保存しました
                  </>
                ) : (
                  <>
                    <Save className="mr-1.5 size-4" />
                    保存する
                  </>
                )}
              </Button>
              <Button
                onClick={handleNext}
                variant="outline"
                className="h-11 flex-1 rounded-[10px] border-[1.5px] border-primary text-sm font-medium text-primary hover:bg-[#F0FDFA] hover:text-primary"
              >
                次の企業のESを作る
                <ArrowRight className="ml-1.5 size-4" />
              </Button>
            </div>
          </section>
        </div>
      )}
    </div>
  )
}
