export type Severity = "critical" | "high" | "medium" | "low" | "info"
export type TaskStatus = "running" | "completed" | "queued" | "failed" | "needs_review"
export type AgentName =
  | "Architect"
  | "Researcher"
  | "Developer"
  | "Tester"
  | "Debugger"
  | "Reviewer"
  | "Evaluator"
export type AgentStepStatus = "done" | "active" | "pending" | "failed"

export interface Project {
  id: string
  name: string
  repository: string
  description: string
  stack: string[]
  lastActivity: string
  codeHealth: number
  activeTasks: number
  status: "healthy" | "attention" | "critical"
}

export interface Task {
  id: string
  title: string
  repository: string
  priority: "critical" | "high" | "medium" | "low"
  agent: AgentName
  status: TaskStatus
  created: string
  updated: string
  severity?: Severity
  description?: string
}

export interface AgentPipelineStep {
  agent: AgentName
  status: AgentStepStatus
  elapsed?: string
}

export interface AgentExecution {
  id: string
  agent: AgentName
  status: "running" | "completed" | "queued" | "failed"
  currentTask: string
  elapsed: string
  toolCalls: number
  filesModified: number
  testsRun: number
  testsPassed: number
  plan: { label: string; status: AgentStepStatus }[]
  output: string[]
}

export interface CodeIssue {
  id: string
  file: string
  line: number
  column: number
  severity: Severity
  title: string
  why: string
  fix: string
}

export interface HealthMetric {
  label: string
  value: number
  trend: number
}
