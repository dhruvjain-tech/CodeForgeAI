export const benchmarkMeta = {
  workload: "Token validation hot path",
  dataset: "Synthetic session load, 500k active tokens",
  environment: "4 vCPU / 8GB, isolated benchmark cluster",
  iterations: 10,
  timestamp: "2025-06-02 14:12 UTC",
}

export const benchmarkComparison = [
  { metric: "Throughput", unit: "req/s", current: 8420, alternative: 11210, higherIsBetter: true },
  { metric: "Average latency", unit: "ms", current: 52, alternative: 38, higherIsBetter: false },
  { metric: "p95 latency", unit: "ms", current: 84, alternative: 61, higherIsBetter: false },
  { metric: "p99 latency", unit: "ms", current: 141, alternative: 97, higherIsBetter: false },
  { metric: "CPU utilization", unit: "%", current: 71, alternative: 54, higherIsBetter: false },
  { metric: "Memory", unit: "MB", current: 340, alternative: 48, higherIsBetter: false },
  { metric: "Startup time", unit: "ms", current: 890, alternative: 120, higherIsBetter: false },
  { metric: "DB query time", unit: "ms", current: 12, alternative: 11, higherIsBetter: false },
]

export const benchmarkTrend = [
  { run: "Run 1", current: 8110, alternative: 10800 },
  { run: "Run 2", current: 8290, alternative: 10950 },
  { run: "Run 3", current: 8340, alternative: 11040 },
  { run: "Run 4", current: 8420, alternative: 11120 },
  { run: "Run 5", current: 8380, alternative: 11180 },
  { run: "Run 6", current: 8460, alternative: 11210 },
]
