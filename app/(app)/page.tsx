import Link from "next/link"
import { ActivityIcon, ClipboardListIcon, GitPullRequestIcon, ShieldCheckIcon } from "lucide-react"

import { agentExecutions } from "@/lib/data/agents"
import { projects } from "@/lib/data/projects"
import { tasks } from "@/lib/data/tasks"

import { MetricCard } from "@/components/shared/metric-card"
import { PageHeader } from "@/components/shared/page-header"
import { PriorityBadge, StatusBadge } from "@/components/shared/status-badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { HealthBar } from "@/components/shared/health-bar"

export default function DashboardPage() {
  const runningAgents = agentExecutions.filter((a) => a.status === "running")
  const activeTasks = tasks.filter((t) => t.status === "running" || t.status === "queued")
  const recentTasks = tasks.slice(0, 5)
  const openPRs = 3

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Dashboard"
        description="Overview of active work across every project and agent."
        actions={
          <Button asChild>
            <Link href="/tasks">New Task</Link>
          </Button>
        }
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard label="Active Tasks" value={activeTasks.length} icon={ClipboardListIcon} accent="primary" trend={12} />
        <MetricCard label="Agents Running" value={runningAgents.length} icon={ActivityIcon} accent="engineering" trend={4} />
        <MetricCard label="Avg Code Health" value={78} suffix="/100" icon={ShieldCheckIcon} trend={3} />
        <MetricCard label="Open Pull Requests" value={openPRs} icon={GitPullRequestIcon} trend={-1} />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Recent Tasks</CardTitle>
            <Button variant="ghost" size="sm" asChild>
              <Link href="/tasks">View all</Link>
            </Button>
          </CardHeader>
          <CardContent className="flex flex-col gap-1">
            {recentTasks.map((task) => (
              <Link
                key={task.id}
                href={`/tasks/${task.id}`}
                className="flex items-center justify-between gap-4 rounded-lg px-3 py-2.5 transition-colors hover:bg-muted"
              >
                <div className="flex flex-col gap-0.5">
                  <span className="text-sm font-medium text-foreground">{task.title}</span>
                  <span className="text-xs text-muted-foreground">
                    {task.id} · {task.repository}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <PriorityBadge priority={task.priority} className="hidden sm:inline-flex" />
                  <StatusBadge status={task.status} />
                </div>
              </Link>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Agent Activity</CardTitle>
            <Button variant="ghost" size="sm" asChild>
              <Link href="/agents">View all</Link>
            </Button>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            {agentExecutions.slice(0, 4).map((exec) => (
              <div key={exec.id} className="flex items-start gap-3">
                <div className="mt-1 flex size-2 shrink-0 items-center justify-center">
                  <span
                    className={
                      exec.status === "running"
                        ? "size-2 animate-pulse rounded-full bg-engineering"
                        : exec.status === "failed"
                          ? "size-2 rounded-full bg-destructive"
                          : exec.status === "completed"
                            ? "size-2 rounded-full bg-success"
                            : "size-2 rounded-full bg-muted-foreground"
                    }
                  />
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-sm font-medium text-foreground">{exec.agent} Agent</span>
                  <span className="text-xs text-muted-foreground">{exec.currentTask}</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Projects</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {projects.map((project) => (
            <Link
              key={project.id}
              href={`/projects/${project.id}`}
              className="flex flex-col gap-3 rounded-xl border border-border p-4 transition-colors hover:border-primary/40 hover:bg-muted/50"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-foreground">{project.name}</span>
                <StatusBadge status={project.status} />
              </div>
              <HealthBar label="Code Health" value={project.codeHealth} />
              <span className="text-xs text-muted-foreground">{project.activeTasks} active tasks</span>
            </Link>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
