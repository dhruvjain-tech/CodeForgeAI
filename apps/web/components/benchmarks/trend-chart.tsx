"use client"

import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts"

import { benchmarkTrend } from "@/lib/data/benchmarks"
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart"

const chartConfig: ChartConfig = {
  current: { label: "Python (current)", color: "var(--chart-1)" },
  alternative: { label: "Go (benchmark)", color: "var(--chart-2)" },
}

export function BenchmarkTrendChart() {
  return (
    <ChartContainer config={chartConfig} className="h-64 w-full">
      <LineChart data={benchmarkTrend} margin={{ left: 8, right: 8, top: 8, bottom: 0 }}>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="run" tickLine={false} axisLine={false} tickMargin={8} />
        <YAxis tickLine={false} axisLine={false} tickMargin={8} width={40} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Line
          dataKey="current"
          type="monotone"
          stroke="var(--color-current)"
          strokeWidth={2}
          dot={false}
        />
        <Line
          dataKey="alternative"
          type="monotone"
          stroke="var(--color-alternative)"
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </ChartContainer>
  )
}
