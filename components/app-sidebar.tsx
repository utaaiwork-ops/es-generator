"use client"

import { Home, User, Sparkles, FileText, LogOut } from "lucide-react"
import { useApp } from "@/lib/app-context"
import { cn } from "@/lib/utils"

const navItems = [
  { id: "home" as const, label: "ホーム", icon: Home },
  { id: "profile" as const, label: "プロフィール", icon: User },
  { id: "generate" as const, label: "ES生成", icon: Sparkles },
  { id: "history" as const, label: "履歴", icon: FileText },
]

export function AppSidebar() {
  const { screen, setScreen, user, signOut } = useApp()

  return (
    <aside className="fixed left-0 top-0 z-40 hidden h-screen w-60 flex-col border-r border-border bg-card md:flex">
      <div className="flex items-center gap-2 px-5 py-5">
        <div className="flex size-8 items-center justify-center rounded-lg bg-primary">
          <Sparkles className="size-4 text-primary-foreground" />
        </div>
        <span className="text-lg font-bold text-foreground">ES Generator</span>
      </div>
      <nav className="flex flex-1 flex-col gap-1 px-3 pt-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = screen === item.id
          return (
            <button
              key={item.id}
              onClick={() => setScreen(item.id)}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                isActive
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-muted-foreground hover:bg-secondary hover:text-foreground"
              )}
            >
              <Icon className="size-[18px]" />
              {item.label}
            </button>
          )
        })}
      </nav>
      <div className="border-t border-border px-4 py-4">
        <p className="truncate text-xs text-muted-foreground">{user?.email ?? ""}</p>
        <button
          className="mt-2 flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground"
          onClick={() => signOut()}
        >
          <LogOut className="size-3.5" />
          ログアウト
        </button>
      </div>
    </aside>
  )
}
