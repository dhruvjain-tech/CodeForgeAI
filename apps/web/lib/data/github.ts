export const repositories = [
  { name: "acme/nexus-core", branch: "main", ci: "passing", stars: 42, openIssues: 8, openPRs: 3 },
  { name: "acme/procurement-assistant", branch: "main", ci: "failing", stars: 17, openIssues: 12, openPRs: 2 },
  { name: "acme/wms-platform", branch: "main", ci: "passing", stars: 29, openIssues: 5, openPRs: 1 },
  { name: "acme/finance-pilot", branch: "develop", ci: "passing", stars: 11, openIssues: 15, openPRs: 4 },
]

export const issues = [
  { id: "#482", title: "Session tokens expire mid-request under load", repo: "nexus-core", labels: ["bug", "critical"], status: "in-progress" },
  { id: "#211", title: "Add vendor payment disbursement endpoint", repo: "procurement-assistant", labels: ["feature"], status: "open" },
  { id: "#94", title: "Full table scan on high-SKU inventory lookup", repo: "wms-platform", labels: ["performance"], status: "resolved" },
  { id: "#337", title: "Reconciliation misses partial refunds", repo: "finance-pilot", labels: ["bug"], status: "open" },
]

export const pullRequests = [
  { id: "#514", title: "fix: pool token refresh with per-session lock", repo: "nexus-core", status: "review", author: "codeforge-developer", checks: "passing" },
  { id: "#233", title: "feat: idempotent payment disbursement", repo: "procurement-assistant", status: "draft", author: "codeforge-architect", checks: "pending" },
  { id: "#101", title: "perf: composite index on warehouse_sku_location", repo: "wms-platform", status: "merged", author: "codeforge-debugger", checks: "passing" },
]

export const commits = [
  { sha: "a3f9c1e", message: "fix: guard token refresh with per-session mutex", repo: "nexus-core", author: "codeforge-developer", time: "12 min ago" },
  { sha: "8b02d4a", message: "test: add coverage for reconciliation edge cases", repo: "finance-pilot", author: "codeforge-tester", time: "3 hours ago" },
  { sha: "f21e7c9", message: "perf: add composite index for SKU lookups", repo: "wms-platform", author: "codeforge-debugger", time: "35 min ago" },
]

export const approvalWorkflow = [
  "GitHub Issue",
  "Repository Analysis",
  "Branch",
  "Implementation",
  "Tests",
  "Review",
  "Human Approval",
  "Pull Request",
]
