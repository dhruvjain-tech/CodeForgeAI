import { cn } from "@/lib/utils"

export function HealthBar({
  label,
  value,
  trend,
  className,
}: {
  label: string
  value: number
  trend?: number
  className?: string
}) {
  const color = value >= 80 ? "bg-success" : value >= 60 ? "bg-warning" : "bg-destructive"
  return (
    <div className={cn("flex flex-col gap-1.5", className)}>
      <div className="flex items-center justify-between text-xs">
        <span className="font-medium text-foreground">{label}</span>
        <span className="flex items-center gap-1.5 text-muted-foreground">
          {trend !== undefined ? (
            <span className={trend >= 0 ? "text-success" : "text-destructive"}>
              {trend >= 0 ? "+" : ""}
              {trend}
            </span>
          ) : null}
          <span className="font-mono text-foreground">{value}</span>
        </span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
        <div className={cn("h-full rounded-full", color)} style={{ width: `${value}%` }} />
      </div>
    </div>
  )
}

export function HealthRing({ value, size = 96 }: { value: number; size?: number }) {
  const color = value >= 80 ? "var(--success)" : value >= 60 ? "var(--warning)" : "var(--destructive)"
  const radius = (size - 10) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (value / 100) * circumference
  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} strokeWidth={8} className="fill-none stroke-muted" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={8}
          strokeLinecap="round"
          style={{ stroke: color }}
          className="fill-none transition-all duration-500"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl font-semibold text-foreground">{value}</span>
        <span className="text-[10px] text-muted-foreground">/ 100</span>
      </div>
    </div>
  )
}
