import type { ReactNode } from "react"

export function PageHeader({
  title,
  description,
  children,
}: {
  title: string
  description: string
  children?: ReactNode
}) {
  return (
    <div className="rounded-2xl bg-gradient-to-r from-[#0D9488] to-[#0F766E] px-5 py-5 md:px-8 md:py-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-[#FFFFFF] md:text-xl">{title}</h1>
          <p className="mt-1 text-sm text-[#FFFFFF]/80">{description}</p>
        </div>
        {children}
      </div>
    </div>
  )
}
