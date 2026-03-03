"use client"

import { useState } from "react"
import { Sparkles, Loader2, Mail, Lock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { supabase } from "@/lib/supabase"

type Mode = "login" | "signup"

export function LoginScreen() {
  const [mode, setMode] = useState<Mode>("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [signupSuccess, setSignupSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      if (mode === "login") {
        const { error } = await supabase.auth.signInWithPassword({ email, password })
        if (error) throw error
      } else {
        const { error } = await supabase.auth.signUp({ email, password })
        if (error) throw error
        setSignupSuccess(true)
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "エラーが発生しました"
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-[#F0FDFA] via-white to-[#F0FDFA] px-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="mb-8 flex flex-col items-center gap-3">
          <div className="flex size-12 items-center justify-center rounded-2xl bg-gradient-to-br from-[#0D9488] to-[#0F766E] shadow-lg">
            <Sparkles className="size-6 text-white" />
          </div>
          <h1 className="text-xl font-bold text-foreground">ES Generator</h1>
          <p className="text-sm text-muted-foreground">
            {mode === "login" ? "ログインして始めましょう" : "新規アカウントを作成"}
          </p>
        </div>

        {signupSuccess ? (
          <div className="rounded-[14px] border border-[#0D9488]/20 bg-[#F0FDFA] p-6 text-center">
            <Mail className="mx-auto mb-3 size-8 text-primary" />
            <h2 className="text-sm font-semibold text-foreground">確認メールを送信しました</h2>
            <p className="mt-2 text-xs text-muted-foreground">
              {email} に届いたメールのリンクをクリックして、アカウントを有効化してください
            </p>
            <Button
              onClick={() => { setMode("login"); setSignupSuccess(false) }}
              variant="outline"
              className="mt-4 h-9 rounded-[10px] text-xs"
            >
              ログイン画面に戻る
            </Button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="rounded-[14px] border border-border bg-card p-5 shadow-sm">
              <div className="flex flex-col gap-4">
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-medium text-foreground">メールアドレス</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="you@example.com"
                      required
                      className="h-10 rounded-[10px] border-[1.5px] pl-10 text-sm"
                    />
                  </div>
                </div>
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-medium text-foreground">パスワード</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder={mode === "signup" ? "6文字以上" : "パスワード"}
                      required
                      minLength={mode === "signup" ? 6 : undefined}
                      className="h-10 rounded-[10px] border-[1.5px] pl-10 text-sm"
                    />
                  </div>
                </div>
              </div>

              {error && (
                <p className="mt-3 text-xs text-destructive">{error}</p>
              )}

              <Button
                type="submit"
                disabled={loading}
                className="mt-5 h-11 w-full rounded-[10px] bg-gradient-to-r from-[#0D9488] to-[#0F766E] text-sm font-semibold text-white hover:from-[#0F766E] hover:to-[#115E59]"
              >
                {loading ? (
                  <Loader2 className="mr-1.5 size-4 animate-spin" />
                ) : null}
                {mode === "login" ? "ログイン" : "新規登録"}
              </Button>
            </div>

            <p className="text-center text-xs text-muted-foreground">
              {mode === "login" ? (
                <>
                  アカウントをお持ちでない方は{" "}
                  <button
                    type="button"
                    onClick={() => { setMode("signup"); setError("") }}
                    className="font-medium text-primary hover:underline"
                  >
                    新規登録
                  </button>
                </>
              ) : (
                <>
                  すでにアカウントをお持ちの方は{" "}
                  <button
                    type="button"
                    onClick={() => { setMode("login"); setError("") }}
                    className="font-medium text-primary hover:underline"
                  >
                    ログイン
                  </button>
                </>
              )}
            </p>
          </form>
        )}
      </div>
    </div>
  )
}
