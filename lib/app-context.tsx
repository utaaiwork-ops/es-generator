"use client"

import React, { createContext, useContext, useState, useEffect, useCallback } from "react"
import { supabase } from "./supabase"
import type { User } from "@supabase/supabase-js"

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

type Screen = "login" | "home" | "profile" | "generate" | "history"

type AppContextType = {
  screen: Screen
  setScreen: (s: Screen) => void
  user: User | null
  authLoading: boolean
  signOut: () => Promise<void>
  profile: Profile
  setProfile: (p: Profile) => void
  isProfileComplete: boolean
  profileCompletion: number
}

const AppContext = createContext<AppContextType | null>(null)

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [screen, setScreen] = useState<Screen>("home")
  const [profile, setProfile] = useState<Profile>(defaultProfile)
  const [user, setUser] = useState<User | null>(null)
  const [authLoading, setAuthLoading] = useState(true)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      if (!session?.user) setScreen("login")
      setAuthLoading(false)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      const newUser = session?.user ?? null
      setUser(newUser)
      if (!newUser) {
        setScreen("login")
        setProfile(defaultProfile)
      } else {
        setScreen((prev) => (prev === "login" ? "home" : prev))
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  const signOut = useCallback(async () => {
    await supabase.auth.signOut()
  }, [])

  const filledFields = Object.values(profile).filter((v) => v.trim() !== "").length
  const totalFields = Object.keys(profile).length
  const profileCompletion = Math.round((filledFields / totalFields) * 100)
  const isProfileComplete = filledFields >= 4

  return (
    <AppContext.Provider
      value={{
        screen,
        setScreen,
        user,
        authLoading,
        signOut,
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
