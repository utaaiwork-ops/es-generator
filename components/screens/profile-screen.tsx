"use client"

import { useState, useEffect } from "react"
import { Save, Lightbulb, CheckCircle2, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { PageHeader } from "@/components/page-header"
import { useApp, defaultProfile } from "@/lib/app-context"
import type { Profile } from "@/lib/app-context"
import { getProfile, upsertProfile } from "@/lib/db"

function getProgressMessage(percent: number) {
  if (percent === 0) return "まずは名前と大学だけでもOK"
  if (percent < 30) return "少しずつ埋めていきましょう"
  if (percent < 80) return "エピソード欄を埋めるとES生成の質がグッと上がります"
  if (percent < 100) return "あと少しで完成！"
  return "全項目入力済み！ESを生成してみましょう"
}

function getProgressColor(percent: number) {
  if (percent < 30) return "bg-[#F97316]"
  if (percent < 80) return "bg-[#0D9488]"
  return "bg-[#059669]"
}

export function ProfileScreen() {
  const { profile, setProfile, profileCompletion, setScreen } = useApp()
  const [form, setForm] = useState<Profile>(profile)
  const [saved, setSaved] = useState(false)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  // DBからプロフィールを読み込み
  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const data = await getProfile()
        if (!cancelled) {
          const merged = { ...defaultProfile, ...data }
          setForm(merged)
          setProfile(merged)
        }
      } catch (err) {
        console.error("プロフィール読み込みエラー:", err)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [setProfile])

  const handleChange = (field: keyof Profile, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const keys = Object.keys(form) as (keyof Profile)[]
      await Promise.all(keys.map((key) => upsertProfile(key, form[key])))
      setProfile(form)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (err) {
      console.error("プロフィール保存エラー:", err)
      alert("保存に失敗しました。もう一度お試しください。")
    } finally {
      setSaving(false)
    }
  }

  const filledFields = Object.values(form).filter((v) => v.trim() !== "").length
  const totalFields = Object.keys(form).length
  const localCompletion = Math.round((filledFields / totalFields) * 100)

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 py-20">
        <Loader2 className="size-8 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">プロフィールを読み込み中...</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="プロフィール設定"
        description="ここで登録した情報をもとに、全企業のESを生成します"
      />

      {/* Progress */}
      <div className="rounded-[14px] border border-border bg-card p-5 shadow-sm">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-foreground">
            一度登録すれば、何社分でもESが作れます
          </p>
          <span className="text-sm font-semibold text-primary">
            {localCompletion}%
          </span>
        </div>
        <div className="relative mt-3 h-2 w-full overflow-hidden rounded-full bg-secondary">
          <div
            className={`h-full rounded-full transition-all duration-500 ${getProgressColor(localCompletion)}`}
            style={{ width: `${localCompletion}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-muted-foreground">
          {getProgressMessage(localCompletion)}
        </p>
      </div>

      {/* Basic Info */}
      <section className="rounded-[14px] border border-border bg-card p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-foreground">基本情報</h2>
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
          <FieldInput label="氏名" value={form.name} onChange={(v) => handleChange("name", v)} placeholder="山田 太郎" />
          <FieldInput label="大学" value={form.university} onChange={(v) => handleChange("university", v)} placeholder="東京大学 工学部" />
          <FieldInput label="志望業界" value={form.industry} onChange={(v) => handleChange("industry", v)} placeholder="IT、コンサル、メーカーなど" />
          <FieldInput label="趣味" value={form.hobby} onChange={(v) => handleChange("hobby", v)} placeholder="読書、サッカーなど" />
        </div>
      </section>

      {/* Episodes */}
      <section className="rounded-[14px] border border-border bg-card p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-foreground">あなたのエピソード</h2>
        <div className="mt-4 flex flex-col gap-4">
          <FieldTextarea label="ゼミ・研究内容" value={form.seminar} onChange={(v) => handleChange("seminar", v)} placeholder="ゼミや研究の内容を具体的に書いてください" />
          <FieldTextarea label="ガクチカ（学生時代に力を入れたこと）" value={form.gakuchika} onChange={(v) => handleChange("gakuchika", v)} placeholder="取り組んだこと、工夫した点、結果を書いてください" />
          <FieldTextarea label="自己PR" value={form.selfPR} onChange={(v) => handleChange("selfPR", v)} placeholder="自分の強みが発揮されたエピソードを書いてください" />
          <FieldTextarea label="アルバイト経験" value={form.partTimeJob} onChange={(v) => handleChange("partTimeJob", v)} placeholder="バイト先、役割、学んだことなど" />
        </div>
      </section>

      {/* Values */}
      <section className="rounded-[14px] border border-border bg-card p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-foreground">あなたの軸</h2>
        <div className="mt-4 flex flex-col gap-4">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <FieldInput label="強み" value={form.strength} onChange={(v) => handleChange("strength", v)} placeholder="リーダーシップ、分析力など" />
            <FieldInput label="弱み" value={form.weakness} onChange={(v) => handleChange("weakness", v)} placeholder="心配性、こだわりが強いなど" />
          </div>
          <FieldTextarea label="価値観" value={form.values} onChange={(v) => handleChange("values", v)} placeholder="仕事で大切にしたいこと" />
          <FieldTextarea label="将来のビジョン" value={form.vision} onChange={(v) => handleChange("vision", v)} placeholder="5〜10年後にどうなっていたいか" />
          <FieldTextarea label="その他（自由記述）" value={form.other} onChange={(v) => handleChange("other", v)} placeholder="補足情報があれば記入してください" />
        </div>
      </section>

      {/* Hint */}
      <div className="flex items-start gap-3 rounded-[14px] border border-[#0D9488]/20 bg-[#F0FDFA] p-4">
        <Lightbulb className="mt-0.5 size-4 shrink-0 text-primary" />
        <p className="text-xs leading-relaxed text-foreground/80">
          数字や固有名詞を入れると、AIがより具体的なESを生成できます
        </p>
      </div>

      {/* Save */}
      <Button
        onClick={handleSave}
        disabled={saving}
        className="h-11 w-full rounded-[10px] bg-gradient-to-r from-[#0D9488] to-[#0F766E] text-sm font-semibold text-[#FFFFFF] hover:from-[#0F766E] hover:to-[#115E59]"
      >
        {saving ? (
          <>
            <Loader2 className="mr-1.5 size-4 animate-spin" />
            保存中...
          </>
        ) : saved ? (
          <>
            <CheckCircle2 className="mr-1.5 size-4" />
            保存しました
          </>
        ) : (
          <>
            <Save className="mr-1.5 size-4" />
            保存する
          </>
        )}
      </Button>

      {profileCompletion === 100 && (
        <Button
          onClick={() => setScreen("generate")}
          variant="outline"
          className="h-10 w-full rounded-[10px] border-primary text-sm font-medium text-primary hover:bg-[#F0FDFA] hover:text-primary"
        >
          ES生成画面へ進む
        </Button>
      )}
    </div>
  )
}

function FieldInput({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string
  value: string
  onChange: (v: string) => void
  placeholder: string
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-foreground">{label}</label>
      <Input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="h-10 rounded-[10px] border-[1.5px] text-sm"
      />
    </div>
  )
}

function FieldTextarea({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string
  value: string
  onChange: (v: string) => void
  placeholder: string
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-foreground">{label}</label>
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="min-h-[100px] rounded-[10px] border-[1.5px] text-sm"
        rows={4}
      />
    </div>
  )
}
