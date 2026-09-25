"use client"

import { useEffect } from "react"
import { AlertTriangleIcon, RefreshCwIcon } from "lucide-react"

import { Button } from "@/components/ui/button"

interface ErrorPageProps {
  error: Error & { digest?: string }
  reset: () => void
}

export default function ErrorPage({
  error,
  reset,
}: ErrorPageProps) {
  useEffect(() => {
    console.error("CodeForge AI application error:", error)
  }, [error])

  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <div className="flex w-full max-w-md flex-col items-center gap-5 rounded-xl border border-border bg-card p-8 text-center">
        <div className="flex size-12 items-center justify-center rounded-xl border border-destructive/30 bg-destructive/10">
          <AlertTriangleIcon
            className="size-6 text-destructive"
            aria-hidden="true"
          />
        </div>

        <div>
          <h1 className="text-lg font-semibold text-foreground">
            Something went wrong
          </h1>

          <p className="mt-2 text-sm leading-6 text-muted-foreground">
            CodeForge AI could not load this workspace correctly.
            You can retry the operation without leaving the application.
          </p>
        </div>

        <Button onClick={() => reset()}>
          <RefreshCwIcon aria-hidden="true" />
          Try Again
        </Button>

        {error.digest ? (
          <p className="font-mono text-[11px] text-muted-foreground">
            Error ID: {error.digest}
          </p>
        ) : null}
      </div>
    </div>
  )
}