import { ArrowDownIcon, ArrowUpIcon } from "lucide-react"

import { benchmarkComparison, benchmarkMeta } from "@/lib/data/benchmarks"

import { BenchmarkTrendChart } from "@/components/benchmarks/trend-chart"
import { PageHeader } from "@/components/shared/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

export default function BenchmarksPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Benchmarks" description={benchmarkMeta.workload} />

      <Card>
        <CardHeader>
          <CardTitle>Run Configuration</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          <div className="flex flex-col gap-0.5">
            <span className="text-xs text-muted-foreground">Dataset</span>
            <span className="text-sm font-medium text-foreground">{benchmarkMeta.dataset}</span>
          </div>
          <div className="flex flex-col gap-0.5">
            <span className="text-xs text-muted-foreground">Environment</span>
            <span className="text-sm font-medium text-foreground">{benchmarkMeta.environment}</span>
          </div>
          <div className="flex flex-col gap-0.5">
            <span className="text-xs text-muted-foreground">Iterations</span>
            <span className="text-sm font-medium text-foreground">{benchmarkMeta.iterations}</span>
          </div>
          <div className="flex flex-col gap-0.5">
            <span className="text-xs text-muted-foreground">Timestamp</span>
            <span className="text-sm font-medium text-foreground">{benchmarkMeta.timestamp}</span>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Throughput Trend</CardTitle>
        </CardHeader>
        <CardContent>
          <BenchmarkTrendChart />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Comparison</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          {benchmarkComparison.map((row) => {
            const alternativeBetter = row.higherIsBetter
              ? row.alternative > row.current
              : row.alternative < row.current
            const delta = Math.abs(row.alternative - row.current)
            const percentDelta = row.current !== 0 ? Math.round((delta / row.current) * 100) : 0

            return (
              <div
                key={row.metric}
                className="grid grid-cols-2 items-center gap-4 rounded-lg border border-border p-4 sm:grid-cols-4"
              >
                <span className="text-sm font-medium text-foreground">{row.metric}</span>
                <span className="font-mono text-sm text-muted-foreground">
                  {row.current} {row.unit}
                </span>
                <span className="font-mono text-sm text-foreground">
                  {row.alternative} {row.unit}
                </span>
                <span
                  className={cn(
                    "flex items-center gap-1 justify-self-end text-xs font-medium",
                    alternativeBetter ? "text-success" : "text-destructive",
                  )}
                >
                  {alternativeBetter ? (
                    <ArrowUpIcon className="size-3" aria-hidden="true" />
                  ) : (
                    <ArrowDownIcon className="size-3" aria-hidden="true" />
                  )}
                  {percentDelta}%
                </span>
              </div>
            )
          })}
        </CardContent>
      </Card>
    </div>
  )
}
