import { codeIssues, healthMetrics, overallHealth } from "@/lib/data/code-health"

import { HealthRing } from "@/components/shared/health-bar"
import { PageHeader } from "@/components/shared/page-header"
import { SeverityBadge } from "@/components/shared/status-badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function CodeHealthPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Code Health" description="Aggregate quality signal across all repositories, refreshed hourly." />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="flex flex-col items-center justify-center gap-2 py-8">
          <HealthRing value={overallHealth} size={140} />
          <span className="text-sm text-muted-foreground">Overall Score</span>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Metrics</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {healthMetrics.map((metric) => (
              <div key={metric.label} className="flex flex-col gap-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-medium text-foreground">{metric.label}</span>
                  <span className="flex items-center gap-1.5 text-muted-foreground">
                    <span className={metric.trend >= 0 ? "text-success" : "text-destructive"}>
                      {metric.trend >= 0 ? "+" : ""}
                      {metric.trend}
                    </span>
                    <span className="font-mono text-foreground">{metric.value}</span>
                  </span>
                </div>
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
                  <div
                    className={`h-full rounded-full ${
                      metric.value >= 80 ? "bg-success" : metric.value >= 60 ? "bg-warning" : "bg-destructive"
                    }`}
                    style={{ width: `${metric.value}%` }}
                  />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Detected Issues</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          {codeIssues.map((issue) => (
            <div key={issue.id} className="flex flex-col gap-2 rounded-lg border border-border p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <SeverityBadge severity={issue.severity} />
                  <span className="font-medium text-foreground">{issue.title}</span>
                </div>
                <span className="font-mono text-xs text-muted-foreground">
                  {issue.file}:{issue.line}:{issue.column}
                </span>
              </div>
              <p className="text-sm text-muted-foreground">
                <span className="font-medium text-foreground">Why: </span>
                {issue.why}
              </p>
              <p className="text-sm text-muted-foreground">
                <span className="font-medium text-foreground">Fix: </span>
                {issue.fix}
              </p>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
