import { CheckIcon, CircleIcon, LoaderIcon, XIcon } from "lucide-react"

import { agentExecutions, agentPipeline } from "@/lib/data/agents"
import type { AgentStepStatus } from "@/lib/types"

import { MetricCard } from "@/components/shared/metric-card"
import { PageHeader } from "@/components/shared/page-header"
import { StatusBadge } from "@/components/shared/status-badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { ActivityIcon, CheckCircle2Icon, ClockIcon, WrenchIcon } from "lucide-react"

const stepIcon: Record<AgentStepStatus, typeof CircleIcon> = {
  done: CheckIcon,
  active: LoaderIcon,
  pending: CircleIcon,
  failed: XIcon,
}

const stepStyles: Record<AgentStepStatus, string> = {
  done: "bg-success text-success-foreground border-success",
  active: "bg-engineering text-white border-engineering",
  pending: "bg-muted text-muted-foreground border-border",
  failed: "bg-destructive text-destructive-foreground border-destructive",
}

export default function AgentsPage() {
  const running = agentExecutions.filter((e) => e.status === "running").length
  const queued = agentExecutions.filter((e) => e.status === "queued").length
  const completed = agentExecutions.filter((e) => e.status === "completed").length
  const failed = agentExecutions.filter((e) => e.status === "failed").length

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Agents"
        description="Live execution state across the seven-agent pipeline: Architect, Researcher, Developer, Tester, Debugger, Reviewer, Evaluator."
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard label="Running" value={running} icon={ActivityIcon} accent="engineering" />
        <MetricCard label="Queued" value={queued} icon={ClockIcon} />
        <MetricCard label="Completed" value={completed} icon={CheckCircle2Icon} accent="success" />
        <MetricCard label="Failed" value={failed} icon={WrenchIcon} accent="destructive" />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Pipeline</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap items-center gap-2">
            {agentPipeline.map((agent, index) => (
              <div key={agent} className="flex items-center gap-2">
                <span className="rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium text-foreground">
                  {agent}
                </span>
                {index < agentPipeline.length - 1 ? (
                  <span className="text-muted-foreground">&rarr;</span>
                ) : null}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="flex flex-col gap-4">
        {agentExecutions.map((exec) => (
          <Card key={exec.id}>
            <CardHeader className="flex flex-row items-center justify-between gap-3">
              <div className="flex flex-col gap-1">
                <CardTitle>{exec.agent} Agent</CardTitle>
                <span className="text-sm text-muted-foreground">{exec.currentTask}</span>
              </div>
              <StatusBadge status={exec.status} />
            </CardHeader>
            <CardContent className="flex flex-col gap-5">
              <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                <div className="flex flex-col gap-0.5">
                  <span className="text-xs text-muted-foreground">Elapsed</span>
                  <span className="font-mono text-sm text-foreground">{exec.elapsed}</span>
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-xs text-muted-foreground">Tool Calls</span>
                  <span className="font-mono text-sm text-foreground">{exec.toolCalls}</span>
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-xs text-muted-foreground">Files Modified</span>
                  <span className="font-mono text-sm text-foreground">{exec.filesModified}</span>
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-xs text-muted-foreground">Tests</span>
                  <span className="font-mono text-sm text-foreground">
                    {exec.testsPassed}/{exec.testsRun}
                  </span>
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <span className="text-xs font-medium text-muted-foreground">Plan</span>
                <div className="flex flex-wrap gap-2">
                  {exec.plan.map((step) => {
                    const Icon = stepIcon[step.status]
                    return (
                      <span
                        key={step.label}
                        className={cn(
                          "flex items-center gap-1.5 rounded-md border px-2 py-1 text-xs font-medium",
                          stepStyles[step.status],
                        )}
                      >
                        <Icon className={cn("size-3", step.status === "active" && "animate-spin")} aria-hidden="true" />
                        {step.label}
                      </span>
                    )
                  })}
                </div>
              </div>

              {exec.output.length > 0 ? (
                <div className="flex flex-col gap-2">
                  <span className="text-xs font-medium text-muted-foreground">Output</span>
                  <div className="flex flex-col gap-1 rounded-lg bg-muted/60 p-3 font-mono text-xs text-muted-foreground">
                    {exec.output.map((line, i) => (
                      <span key={i}>
                        <span className="text-primary">$</span> {line}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
