export interface MemoryEntry {
  id: string
  category: "experience" | "lesson" | "strategy" | "failure"
  task: string
  outcome: "successful" | "unsuccessful" | "partial"
  summary: string
  evidence: string
  usageCount: number
  successRate: number
  created: string
  lastUsed: string
}

export const memoryEntries: MemoryEntry[] = [
  {
    id: "mem-1",
    category: "experience",
    task: "Fix authentication timeout",
    outcome: "successful",
    summary: "Connection pooling reduced latency and eliminated timeout errors under concurrent load.",
    evidence: "p95 latency dropped from 210ms to 84ms after introducing a pooled connection strategy.",
    usageCount: 12,
    successRate: 91,
    created: "2025-03-11",
    lastUsed: "2 hours ago",
  },
  {
    id: "mem-2",
    category: "strategy",
    task: "High-concurrency database access",
    outcome: "successful",
    summary: "Use pooled connections for high-concurrency database workloads instead of per-request connections.",
    evidence: "Applied successfully across 4 projects: Nexus, Warehouse Management, Finance Pilot, Procurement Assistant.",
    usageCount: 27,
    successRate: 94,
    created: "2025-01-22",
    lastUsed: "2 hours ago",
  },
  {
    id: "mem-3",
    category: "lesson",
    task: "Webhook signature verification",
    outcome: "partial",
    summary: "Retry paths must re-run the full verification pipeline, not just the initial delivery path.",
    evidence: "Incident CF-1031 exposed a bypass where retried webhooks skipped signature checks.",
    usageCount: 5,
    successRate: 80,
    created: "2025-05-02",
    lastUsed: "1 day ago",
  },
  {
    id: "mem-4",
    category: "failure",
    task: "Direct migration of legacy webhook handler",
    outcome: "unsuccessful",
    summary: "Rewriting the handler without preserving the legacy signature format broke backwards compatibility.",
    evidence: "3 of 4 signature-verification tests failed after migration; required rollback and re-plan.",
    usageCount: 1,
    successRate: 0,
    created: "2025-06-01",
    lastUsed: "1 day ago",
  },
  {
    id: "mem-5",
    category: "strategy",
    task: "Reducing cyclomatic complexity",
    outcome: "successful",
    summary: "Split large transactional functions along their validate / authorize / execute phases.",
    evidence: "Applied to payment/service.py and 3 similar functions; average complexity reduced by 40%.",
    usageCount: 9,
    successRate: 100,
    created: "2025-02-14",
    lastUsed: "6 hours ago",
  },
]
