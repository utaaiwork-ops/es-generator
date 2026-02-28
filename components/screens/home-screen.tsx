"use client"

import { User, Sparkles, FileText, ArrowRight, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useApp } from "@/lib/app-context"

const features = [
  {
    icon: User,
    title: "プロフィール設定",
    description: "一度だけ登録",
    screen: "profile" as const,
  },
  {
    icon: Sparkles,
    title: "ES生成",
    description: "URLを貼って即生成",
    screen: "generate" as const,
  },
  {
    icon: FileText,
    title: "履歴一覧",
    description: "企業別に管理",
    screen: "history" as const,
  },
]

const steps = [
  { num: "1", text: "プロフィール登録（初回のみ）" },
  { num: "2", text: "企業URLを入力" },
  { num: "3", text: "ES自動生成" },
  { num: "4", text: "コピペして提出" },
]

export function HomeScreen() {
  const { setScreen, isProfileComplete } = useApp()

  return (
    <div className="flex flex-col gap-6">
      {/* Hero Header */}
      <div className="rounded-2xl bg-gradient-to-r from-[#0D9488] to-[#0F766E] px-8 py-8">
        <h1 className="text-2xl font-bold text-[#FFFFFF]">
          プロフィールを1回登録。あとは企業URLを変えるだけ。
        </h1>
        <p className="mt-2 text-sm text-[#FFFFFF]/80">
          何十社分のES作成を、圧倒的にラクにする。
        </p>
        {isProfileComplete && (
          <Button
            onClick={() => setScreen("generate")}
            className="mt-5 h-10 rounded-[10px] bg-white/20 px-6 text-sm font-semibold text-white backdrop-blur-sm hover:bg-white/30"
          >
            ES生成へ
            <ArrowRight className="ml-1.5 size-4" />
          </Button>
        )}
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {features.map((feature) => {
          const Icon = feature.icon
          return (
            <button
              key={feature.title}
              onClick={() => setScreen(feature.screen)}
              className="group flex flex-col items-start gap-3 rounded-[14px] border border-border bg-card p-6 shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
            >
              <div className="flex size-10 items-center justify-center rounded-lg bg-[#F0FDFA]">
                <Icon className="size-5 text-primary" />
              </div>
              <div className="text-left">
                <h3 className="text-sm font-semibold text-foreground">
                  {feature.title}
                </h3>
                <p className="mt-0.5 text-xs text-muted-foreground">
                  {feature.description}
                </p>
              </div>
              <div className="flex items-center gap-1 text-xs font-medium text-primary opacity-0 transition-opacity group-hover:opacity-100">
                開く
                <ChevronRight className="size-3" />
              </div>
            </button>
          )
        })}
      </div>

      {/* Steps */}
      <div className="rounded-[14px] border border-border bg-card p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-foreground">使い方</h2>
        <div className="mt-4 flex items-center gap-3">
          {steps.map((step, i) => (
            <div key={step.num} className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <span className="flex size-6 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
                  {step.num}
                </span>
                <span className="text-sm text-foreground">{step.text}</span>
              </div>
              {i < steps.length - 1 && (
                <ArrowRight className="size-3.5 shrink-0 text-muted-foreground" />
              )}
            </div>
          ))}
        </div>
        <p className="mt-3 text-xs text-muted-foreground">
          まずはプロフィールから始めてみましょう。完璧でなくてもOKです。
        </p>
      </div>
    </div>
  )
}
