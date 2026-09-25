import type { LucideIcon } from "lucide-react"
import { ArrowDownIcon, ArrowUpIcon } from "lucide-react"
import { cn } from "@/lib/utils"
import { Card } from "@/components/ui/card"

export function MetricCard({
  label,
  value,
  suffix,
  trend,
  icon: Icon,
  accent = "default",
}: {
  label: string
  value: string | number
  suffix?: string
  trend?: number
  icon?: LucideIcon
  accent?: "default" | "primary" | "engineering"
}) {
  const trendPositive = (trend ?? 0) >= 0
  return (
    <Card className="gap-2 rounded-xl border-border bg-card p-5">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-muted-foreground">{label}</span>
        {Icon ? (
          <Icon
            className={cn(
              "size-4",
              accent === "primary" && "text-primary",
              accent === "engineering" && "text-engineering",
              accent === "default" && "text-muted-foreground",
            )}
            aria-hidden="true"
          />
        ) : null}
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-semibold tracking-tight text-foreground">
          {value}
          {suffix ? <span className="text-base font-medium text-muted-foreground">{suffix}</span> : null}
        </span>
        {trend !== undefined ? (
          <span
            className={cn(
              "flex items-center gap-0.5 text-xs font-medium",
              trendPositive ? "text-success" : "text-destructive",
            )}
          >
            {trendPositive ? (
              <ArrowUpIcon className="size-3" aria-hidden="true" />
            ) : (
              <ArrowDownIcon className="size-3" aria-hidden="true" />
            )}
            {Math.abs(trend)}
            {typeof trend === "number" && Number.isInteger(trend) ? "%" : ""}
          </span>
        ) : null}
      </div>
    </Card>
  )
}
