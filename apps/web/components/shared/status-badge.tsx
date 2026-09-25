import { cn } from "@/lib/utils"
import {
  CheckCircle2Icon,
  CircleDashedIcon,
  CircleIcon,
  ClockIcon,
  EyeIcon,
  LoaderIcon,
  XCircleIcon,
} from "lucide-react"

type Status =
  | "running"
  | "completed"
  | "queued"
  | "failed"
  | "needs_review"
  | "healthy"
  | "attention"
  | "critical"
  | "passing"
  | "merged"
  | "open"
  | "draft"
  | "review"
  | "resolved"
  | "in-progress"

const statusConfig: Record<
  Status,
  { label: string; icon: typeof CircleIcon; className: string }
> = {
  running: { label: "Running", icon: LoaderIcon, className: "text-engineering bg-engineering/10 border-engineering/30" },
  completed: { label: "Completed", icon: CheckCircle2Icon, className: "text-success bg-success/10 border-success/30" },
  queued: { label: "Queued", icon: ClockIcon, className: "text-muted-foreground bg-muted border-border" },
  failed: { label: "Failed", icon: XCircleIcon, className: "text-destructive bg-destructive/10 border-destructive/30" },
  needs_review: { label: "Needs Review", icon: EyeIcon, className: "text-warning bg-warning/10 border-warning/30" },
  healthy: { label: "Healthy", icon: CheckCircle2Icon, className: "text-success bg-success/10 border-success/30" },
  attention: { label: "Needs Attention", icon: ClockIcon, className: "text-warning bg-warning/10 border-warning/30" },
  critical: { label: "Critical", icon: XCircleIcon, className: "text-destructive bg-destructive/10 border-destructive/30" },
  passing: { label: "Passing", icon: CheckCircle2Icon, className: "text-success bg-success/10 border-success/30" },
  merged: { label: "Merged", icon: CheckCircle2Icon, className: "text-primary bg-primary/10 border-primary/30" },
  open: { label: "Open", icon: CircleDashedIcon, className: "text-engineering bg-engineering/10 border-engineering/30" },
  draft: { label: "Draft", icon: CircleDashedIcon, className: "text-muted-foreground bg-muted border-border" },
  review: { label: "In Review", icon: EyeIcon, className: "text-warning bg-warning/10 border-warning/30" },
  resolved: { label: "Resolved", icon: CheckCircle2Icon, className: "text-success bg-success/10 border-success/30" },
  "in-progress": { label: "In Progress", icon: LoaderIcon, className: "text-engineering bg-engineering/10 border-engineering/30" },
}

export function StatusBadge({
  status,
  className,
}: {
  status: Status
  className?: string
}) {
  const config = statusConfig[status]
  const Icon = config.icon
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 text-xs font-medium",
        config.className,
        className,
      )}
    >
      <Icon className={cn("size-3", status === "running" && "animate-spin")} aria-hidden="true" />
      {config.label}
    </span>
  )
}

const severityConfig = {
  critical: "text-destructive bg-destructive/10 border-destructive/30",
  high: "text-warning bg-warning/10 border-warning/30",
  medium: "text-engineering bg-engineering/10 border-engineering/30",
  low: "text-muted-foreground bg-muted border-border",
  info: "text-muted-foreground bg-muted border-border",
}

export function SeverityBadge({
  severity,
  className,
}: {
  severity: keyof typeof severityConfig
  className?: string
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium uppercase tracking-wide",
        severityConfig[severity],
        className,
      )}
    >
      {severity}
    </span>
  )
}

const priorityConfig = {
  critical: "text-destructive bg-destructive/10 border-destructive/30",
  high: "text-warning bg-warning/10 border-warning/30",
  medium: "text-engineering bg-engineering/10 border-engineering/30",
  low: "text-muted-foreground bg-muted border-border",
}

export function PriorityBadge({
  priority,
  className,
}: {
  priority: keyof typeof priorityConfig
  className?: string
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium capitalize",
        priorityConfig[priority],
        className,
      )}
    >
      {priority}
    </span>
  )
}
