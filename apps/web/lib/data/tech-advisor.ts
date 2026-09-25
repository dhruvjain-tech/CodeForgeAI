export const currentStack = [
  { name: "Python", role: "Application runtime" },
  { name: "FastAPI", role: "API framework" },
  { name: "PostgreSQL", role: "Primary datastore" },
  { name: "Redis", role: "Caching & queues" },
]

export const advisorAnalysis = {
  alternative: "Go",
  target: "Nexus — identity & authentication service",
  sections: [
    {
      label: "Workload",
      summary:
        "High-throughput, latency-sensitive token validation on the request hot path (~4,200 req/s at peak).",
    },
    {
      label: "Concurrency",
      summary:
        "Current async Python handles concurrency via the event loop; Go's goroutines show lower scheduling overhead at this connection count in benchmark data.",
    },
    {
      label: "Memory",
      summary: "Python service holds ~340MB baseline per instance vs. ~48MB observed in the Go benchmark build.",
    },
    {
      label: "Latency",
      summary: "p95 latency for token validation is 84ms in production; benchmark build measured 61ms under equivalent load.",
    },
    {
      label: "CPU",
      summary: "CPU-bound JWT signature verification benefits from Go's lower per-call overhead versus CPython.",
    },
    {
      label: "I/O",
      summary: "Both stacks are I/O-bound on PostgreSQL and Redis round-trips; driver-level performance is comparable.",
    },
    {
      label: "Infrastructure",
      summary: "Existing Kubernetes deployment and observability stack (OpenTelemetry) support both runtimes without change.",
    },
    {
      label: "Team fit",
      summary: "Two of five engineers on Nexus have production Go experience; ramp-up estimated at 2-3 sprints.",
    },
    {
      label: "Migration cost",
      summary: "Estimated 6-8 weeks to port the identity service core paths with parallel test validation.",
    },
    {
      label: "Trade-offs",
      summary: "Faster hot-path performance and lower memory footprint, at the cost of a smaller pool of readily available contributors and a temporary two-stack maintenance burden during migration.",
    },
  ],
  verdict: "Potential advantage under this workload — recommend running the controlled benchmark before committing to migration.",
}
