import type { CodeIssue, HealthMetric } from "@/lib/types"

export const healthMetrics: HealthMetric[] = [
  { label: "Quality", value: 82, trend: 3 },
  { label: "Security", value: 76, trend: -2 },
  { label: "Performance", value: 88, trend: 5 },
  { label: "Maintainability", value: 71, trend: 1 },
  { label: "Test Coverage", value: 68, trend: 4 },
  { label: "Architecture", value: 84, trend: 0 },
  { label: "Complexity", value: 63, trend: -4 },
  { label: "Duplication", value: 91, trend: 2 },
]

export const overallHealth = 79

export const codeIssues: CodeIssue[] = [
  {
    id: "issue-1",
    file: "auth/service.py",
    line: 142,
    column: 18,
    severity: "critical",
    title: "Potential SQL Injection",
    why: "Unsafe construction of a SQL query using unescaped user input in the WHERE clause.",
    fix: "Use parameterized queries via the ORM query builder instead of string interpolation.",
  },
  {
    id: "issue-2",
    file: "payment/service.py",
    line: 88,
    column: 4,
    severity: "high",
    title: "High cyclomatic complexity",
    why: "process_payment() has a cyclomatic complexity of 18, making it difficult to test and reason about.",
    fix: "Split into smaller functions: validate_payment(), authorize_payment(), and capture_payment().",
  },
  {
    id: "issue-3",
    file: "api/routes/webhooks.ts",
    line: 54,
    column: 12,
    severity: "medium",
    title: "Missing signature verification on retry path",
    why: "Retried webhook deliveries skip HMAC verification, allowing replay of unverified payloads.",
    fix: "Verify signature before entering the retry branch, not only on first delivery.",
  },
  {
    id: "issue-4",
    file: "workers/pool.py",
    line: 211,
    column: 6,
    severity: "high",
    title: "Unbounded in-memory registry growth",
    why: "Completed jobs are never evicted from job_registry, causing steady memory growth under load.",
    fix: "Evict completed job entries after their result has been read, or use a TTL-based cache.",
  },
  {
    id: "issue-5",
    file: "lib/utils/date.ts",
    line: 27,
    column: 9,
    severity: "low",
    title: "Duplicated date formatting logic",
    why: "The same formatting logic is duplicated across 6 files instead of using a shared utility.",
    fix: "Extract formatDate() into lib/utils/date.ts and update call sites.",
  },
]
