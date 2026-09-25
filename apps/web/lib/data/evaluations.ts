export const evaluationSummary = [
  { label: "Task success rate", value: 87, trend: 3, suffix: "%" },
  { label: "Regression rate", value: 4, trend: -1, suffix: "%" },
  { label: "Test pass rate", value: 96, trend: 2, suffix: "%" },
  { label: "Agent success", value: 91, trend: 1, suffix: "%" },
  { label: "Avg task duration", value: 6.4, trend: -0.8, suffix: "m" },
  { label: "Learning effectiveness", value: 78, trend: 5, suffix: "%" },
]

export const successTrend = [
  { week: "W1", success: 74, regression: 9 },
  { week: "W2", success: 78, regression: 8 },
  { week: "W3", success: 81, regression: 6 },
  { week: "W4", success: 83, regression: 6 },
  { week: "W5", success: 85, regression: 5 },
  { week: "W6", success: 87, regression: 4 },
]

export const benchmarkImprovements = [
  { area: "Token validation throughput", improvement: "+33%", basis: "Go migration benchmark" },
  { area: "Warehouse query latency", improvement: "+58%", basis: "Index restructuring" },
  { area: "Test suite runtime", improvement: "-21%", basis: "Parallelized test execution" },
  { area: "Memory footprint (worker pool)", improvement: "-64%", basis: "Job registry eviction fix" },
]
