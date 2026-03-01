"use client"

import { useEffect, useRef } from "react"
import { AppProvider, useApp } from "@/lib/app-context"
import { AppSidebar } from "@/components/app-sidebar"
import { MobileBottomNav } from "@/components/mobile-bottom-nav"
import { ScreenTransition } from "@/components/screen-transition"
import { HomeScreen } from "@/components/screens/home-screen"
import { ProfileScreen } from "@/components/screens/profile-screen"
import { GenerateScreen } from "@/components/screens/generate-screen"
import { HistoryScreen } from "@/components/screens/history-screen"

function AppContent() {
  const { screen } = useApp()
  const prevScreen = useRef(screen)

  useEffect(() => {
    if (prevScreen.current !== screen) {
      window.scrollTo({ top: 0 })
      prevScreen.current = screen
    }
  }, [screen])

  return (
    <div className="flex min-h-screen bg-background">
      <AppSidebar />
      <main className="safe-top flex-1 px-4 pb-20 pt-6 md:ml-60 md:px-8 md:py-6 md:pb-6">
        <div className="mx-auto max-w-4xl">
          <ScreenTransition screenKey={screen}>
            {screen === "home" && <HomeScreen />}
            {screen === "profile" && <ProfileScreen />}
            {screen === "generate" && <GenerateScreen />}
            {screen === "history" && <HistoryScreen />}
          </ScreenTransition>
        </div>
      </main>
      <MobileBottomNav />
    </div>
  )
}

export default function Page() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  )
}
