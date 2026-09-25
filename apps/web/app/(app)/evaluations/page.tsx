import { ActivityIcon, GaugeIcon, ShieldCheckIcon, TimerIcon, TrendingUpIcon, CheckCheckIcon } from "lucide-react"

import { benchmarkImprovements, evaluationSummary } from "@/lib/data/evaluations"

import { SuccessTrendChart } from "@/components/evaluations/success-trend-chart"
import { MetricCard } from "@/components/shared/metric-card"
import { PageHeader } from "@/components/shared/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const icons = [CheckCheckIcon, ShieldCheckIcon, GaugeIcon, ActivityIcon, TimerIcon, TrendingUpIcon]

export default function EvaluationsPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Evaluations"
        description="Continuous scoring of agent output quality, regressions, and learning effectiveness."
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {evaluationSummary.map((metric, i) => (
          <MetricCard
            key={metric.label}
            label={metric.label}
            value={metric.value}
            suffix={metric.suffix}
            trend={metric.trend}
            icon={icons[i % icons.length]}
            accent="primary"
          />
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Success vs. Regression Rate</CardTitle>
        </CardHeader>
        <CardContent>
          <SuccessTrendChart />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Benchmark Improvements</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          {benchmarkImprovements.map((item) => (
            <div
              key={item.area}
              className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-border p-4"
            >
              <div className="flex flex-col gap-0.5">
                <span className="text-sm font-medium text-foreground">{item.area}</span>
                <span className="text-xs text-muted-foreground">{item.basis}</span>
              </div>
              <span
                className={`font-mono text-sm font-semibold ${
                  item.improvement.startsWith("+") ? "text-success" : "text-success"
                }`}
              >
                {item.improvement}
              </span>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
