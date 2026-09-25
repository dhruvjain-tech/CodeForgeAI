"use client"

import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts"

import { successTrend } from "@/lib/data/evaluations"
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart"

const chartConfig: ChartConfig = {
  success: { label: "Success Rate", color: "var(--chart-1)" },
  regression: { label: "Regression Rate", color: "var(--chart-4)" },
}

export function SuccessTrendChart() {
  return (
    <ChartContainer config={chartConfig} className="h-64 w-full">
      <AreaChart data={successTrend} margin={{ left: 8, right: 8, top: 8, bottom: 0 }}>
        <defs>
          <linearGradient id="fillSuccess" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="var(--color-success)" stopOpacity={0.3} />
            <stop offset="95%" stopColor="var(--color-success)" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="week" tickLine={false} axisLine={false} tickMargin={8} />
        <YAxis tickLine={false} axisLine={false} tickMargin={8} width={32} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Area
          dataKey="success"
          type="monotone"
          stroke="var(--color-success)"
          fill="url(#fillSuccess)"
          strokeWidth={2}
        />
        <Area
          dataKey="regression"
          type="monotone"
          stroke="var(--color-regression)"
          fill="transparent"
          strokeWidth={2}
        />
      </AreaChart>
    </ChartContainer>
  )
}
