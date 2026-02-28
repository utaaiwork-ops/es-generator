"use client"

import { AppProvider, useApp } from "@/lib/app-context"
import { AppSidebar } from "@/components/app-sidebar"
import { HomeScreen } from "@/components/screens/home-screen"
import { ProfileScreen } from "@/components/screens/profile-screen"
import { GenerateScreen } from "@/components/screens/generate-screen"
import { HistoryScreen } from "@/components/screens/history-screen"

function AppContent() {
  const { screen } = useApp()

  return (
    <div className="flex min-h-screen bg-background">
      <AppSidebar />
      <main className="ml-60 flex-1 px-8 py-6">
        <div className="mx-auto max-w-4xl">
          {screen === "home" && <HomeScreen />}
          {screen === "profile" && <ProfileScreen />}
          {screen === "generate" && <GenerateScreen />}
          {screen === "history" && <HistoryScreen />}
        </div>
      </main>
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
