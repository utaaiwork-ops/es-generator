"use client"

import { useEffect, useState, type ReactNode } from "react"

export function ScreenTransition({
  screenKey,
  children,
}: {
  screenKey: string
  children: ReactNode
}) {
  const [visible, setVisible] = useState(false)
  const [currentKey, setCurrentKey] = useState(screenKey)
  const [currentChildren, setCurrentChildren] = useState(children)

  useEffect(() => {
    if (screenKey !== currentKey) {
      setVisible(false)
      const timeout = setTimeout(() => {
        setCurrentKey(screenKey)
        setCurrentChildren(children)
        setVisible(true)
      }, 100)
      return () => clearTimeout(timeout)
    }
  }, [screenKey, children, currentKey])

  useEffect(() => {
    const timeout = setTimeout(() => setVisible(true), 10)
    return () => clearTimeout(timeout)
  }, [])

  return (
    <div
      className="transition-all duration-200 ease-out"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(8px)",
      }}
    >
      {currentChildren}
    </div>
  )
}
