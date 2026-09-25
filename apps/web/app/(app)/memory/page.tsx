import { BrainIcon, LightbulbIcon, TargetIcon, TriangleAlertIcon } from "lucide-react"

import { memoryEntries } from "@/lib/data/memory"

import { PageHeader } from "@/components/shared/page-header"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

const categoryIcon = {
  experience: BrainIcon,
  strategy: TargetIcon,
  lesson: LightbulbIcon,
  failure: TriangleAlertIcon,
}

const categoryStyles = {
  experience: "text-engineering bg-engineering/10 border-engineering/30",
  strategy: "text-primary bg-primary/10 border-primary/30",
  lesson: "text-warning bg-warning/10 border-warning/30",
  failure: "text-destructive bg-destructive/10 border-destructive/30",
}

const outcomeStyles = {
  successful: "text-success bg-success/10 border-success/30",
  partial: "text-warning bg-warning/10 border-warning/30",
  unsuccessful: "text-destructive bg-destructive/10 border-destructive/30",
}

export default function MemoryPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Memory"
        description="Accumulated experience the agents draw on when planning and executing new tasks."
      />

      <div className="flex flex-col gap-4">
        {memoryEntries.map((entry) => {
          const Icon = categoryIcon[entry.category]
          return (
            <Card key={entry.id}>
              <CardHeader className="flex flex-row items-start justify-between gap-3">
                <div className="flex items-start gap-3">
                  <span
                    className={cn(
                      "flex size-8 shrink-0 items-center justify-center rounded-lg border",
                      categoryStyles[entry.category],
                    )}
                  >
                    <Icon className="size-4" aria-hidden="true" />
                  </span>
                  <div className="flex flex-col gap-1">
                    <CardTitle>{entry.task}</CardTitle>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="capitalize">
                        {entry.category}
                      </Badge>
                      <span
                        className={cn(
                          "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium capitalize",
                          outcomeStyles[entry.outcome],
                        )}
                      >
                        {entry.outcome}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-0.5 text-right">
                  <span className="text-xs text-muted-foreground">Success Rate</span>
                  <span className="font-mono text-sm font-medium text-foreground">{entry.successRate}%</span>
                </div>
              </CardHeader>
              <CardContent className="flex flex-col gap-3">
                <p className="text-sm text-foreground">{entry.summary}</p>
                <p className="text-sm text-muted-foreground">
                  <span className="font-medium text-foreground">Evidence: </span>
                  {entry.evidence}
                </p>
                <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
                  <span>Used {entry.usageCount} times</span>
                  <span>Created {entry.created}</span>
                  <span>Last used {entry.lastUsed}</span>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
