"use client"

import { Home, User, Sparkles, FileText } from "lucide-react"
import { useApp } from "@/lib/app-context"
import { cn } from "@/lib/utils"

const navItems = [
  { id: "home" as const, label: "ホーム", icon: Home },
  { id: "profile" as const, label: "プロフィール", icon: User },
  { id: "generate" as const, label: "ES生成", icon: Sparkles },
  { id: "history" as const, label: "履歴", icon: FileText },
]

export function MobileBottomNav() {
  const { screen, setScreen } = useApp()

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 flex h-16 items-center justify-around border-t border-border bg-card/80 backdrop-blur-lg pb-[env(safe-area-inset-bottom)]">
      {navItems.map((item) => {
        const Icon = item.icon
        const isActive = screen === item.id
        return (
          <button
            key={item.id}
            onClick={() => {
              setScreen(item.id)
              window.scrollTo({ top: 0 })
            }}
            className={cn(
              "flex min-h-[44px] min-w-[44px] flex-col items-center justify-center gap-0.5 rounded-lg px-3 py-1 transition-colors active:scale-95",
              isActive
                ? "text-primary"
                : "text-muted-foreground"
            )}
          >
            <Icon className="size-5" />
            <span className="text-[10px] font-medium">{item.label}</span>
          </button>
        )
      })}
    </nav>
  )
}
