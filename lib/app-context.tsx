"use client"

import React, { createContext, useContext, useState } from "react"

export type ESItem = {
  id: number
  companyId: number
  companyName: string
  esType: string
  question: string | null
  content: string
  charLimit: number
  isEdited: boolean
  createdAt: string
}

export type Profile = {
  name: string
  university: string
  industry: string
  hobby: string
  seminar: string
  gakuchika: string
  selfPR: string
  partTimeJob: string
  strength: string
  weakness: string
  values: string
  vision: string
  other: string
}

export const defaultProfile: Profile = {
  name: "",
  university: "",
  industry: "",
  hobby: "",
  seminar: "",
  gakuchika: "",
  selfPR: "",
  partTimeJob: "",
  strength: "",
  weakness: "",
  values: "",
  vision: "",
  other: "",
}

type Screen = "home" | "profile" | "generate" | "history"

type AppContextType = {
  screen: Screen
  setScreen: (s: Screen) => void
  isLoggedIn: boolean
  profile: Profile
  setProfile: (p: Profile) => void
  isProfileComplete: boolean
  profileCompletion: number
}

const AppContext = createContext<AppContextType | null>(null)

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [screen, setScreen] = useState<Screen>("home")
  const [profile, setProfile] = useState<Profile>(defaultProfile)

  // 認証は後のフェーズで実装。現在はデフォルトでログイン済み
  const isLoggedIn = true

  const filledFields = Object.values(profile).filter((v) => v.trim() !== "").length
  const totalFields = Object.keys(profile).length
  const profileCompletion = Math.round((filledFields / totalFields) * 100)
  const isProfileComplete = filledFields >= 4

  return (
    <AppContext.Provider
      value={{
        screen,
        setScreen,
        isLoggedIn,
        profile,
        setProfile,
        isProfileComplete,
        profileCompletion,
      }}
    >
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error("useApp must be used within AppProvider")
  return ctx
}
