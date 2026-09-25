import Link from "next/link"
import { notFound } from "next/navigation"
import {
  ArrowLeftIcon,
  GitBranchIcon,
  ListChecksIcon,
} from "lucide-react"

import { apiFetch } from "@/lib/api"

import { PageHeader } from "@/components/shared/page-header"
import {
  PriorityBadge,
  StatusBadge,
} from "@/components/shared/status-badge"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface TaskPageProps {
  params: Promise<{
    id: string
  }>
}

interface ApiTask {
  id: number
  project_id: number
  repository_id: number | null
  repository_name: string | null
  title: string
  description: string | null
  priority: string
  status: string
  assigned_agent: string | null
}

const agents = [
  "Architect",
  "Researcher",
  "Developer",
  "Tester",
  "Debugger",
  "Reviewer",
  "Evaluator",
]

export default async function TaskDetailPage({
  params,
}: TaskPageProps) {
  const { id } = await params

  const taskId = Number(id)

  if (!Number.isInteger(taskId)) {
    notFound()
  }

  let task: ApiTask

  try {
    task = await apiFetch<ApiTask>(`/tasks/${taskId}`)
  } catch {
    notFound()
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}

      <PageHeader
        title={task.title}
        description={`Task #${task.id}`}
        actions={
          <Button
            variant="outline"
            size="sm"
            nativeButton={false}
            render={<Link href="/tasks" />}
          >
            <ArrowLeftIcon aria-hidden="true" />
            Back to Tasks
          </Button>
        }
      />

      {/* Main information */}

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        {/* Task information */}

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Task Information</CardTitle>
          </CardHeader>

          <CardContent className="flex flex-col gap-6">
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                Description
              </p>

              <p className="mt-2 text-sm leading-6 text-foreground">
                {task.description ||
                  "No description was provided for this task."}
              </p>
            </div>

            <div className="border-t border-border" />

            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                Engineering Context
              </p>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                This task is stored in PostgreSQL and is ready to enter
                the CodeForge AI engineering workflow. Future execution
                will use repository analysis, planning, implementation,
                testing, debugging, review, and evaluation.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Metadata */}

        <Card>
          <CardHeader>
            <CardTitle>Task Details</CardTitle>
          </CardHeader>

          <CardContent className="flex flex-col gap-5">
            {/* Task ID */}

            <div className="flex items-center justify-between gap-4">
              <span className="text-xs text-muted-foreground">
                Task ID
              </span>

              <span className="font-mono text-xs text-foreground">
                #{task.id}
              </span>
            </div>

            {/* Project */}

            <div className="flex items-center justify-between gap-4">
              <span className="text-xs text-muted-foreground">
                Project
              </span>

              <Link
                href={`/projects/${task.project_id}`}
                className="text-xs font-medium text-primary hover:underline"
              >
                Project #{task.project_id}
              </Link>
            </div>

            {/* Repository */}

            <div className="flex items-center justify-between gap-4">
              <span className="text-xs text-muted-foreground">
                Repository
              </span>

              <span className="text-right text-xs font-medium text-foreground">
                {task.repository_name || "Not connected"}
              </span>
            </div>

            {/* Repository ID */}

            <div className="flex items-center justify-between gap-4">
              <span className="text-xs text-muted-foreground">
                Repository ID
              </span>

              <span className="font-mono text-xs text-foreground">
                {task.repository_id
                  ? `#${task.repository_id}`
                  : "—"}
              </span>
            </div>

            {/* Agent */}

            <div className="flex items-center justify-between gap-4">
              <span className="text-xs text-muted-foreground">
                Assigned Agent
              </span>

              <span className="text-xs font-medium text-foreground">
                {task.assigned_agent || "Developer"}
              </span>
            </div>

            {/* Priority */}

            <div className="flex items-center justify-between gap-4">
              <span className="text-xs text-muted-foreground">
                Priority
              </span>

              <PriorityBadge
                priority={
                  task.priority as
                    | "critical"
                    | "high"
                    | "medium"
                    | "low"
                }
              />
            </div>

            {/* Status */}

            <div className="flex items-center justify-between gap-4">
              <span className="text-xs text-muted-foreground">
                Status
              </span>

              <StatusBadge
                status={
                  task.status as
                    | "running"
                    | "completed"
                    | "queued"
                    | "failed"
                    | "needs_review"
                }
              />
            </div>

            {/* Data source */}

            <div className="flex items-center justify-between gap-4 border-t border-border pt-4">
              <span className="text-xs text-muted-foreground">
                Data Source
              </span>

              <Badge variant="secondary">
                PostgreSQL
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Engineering Pipeline */}

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between gap-4">
            <div>
              <CardTitle>Engineering Pipeline</CardTitle>

              <p className="mt-1 text-xs text-muted-foreground">
                Planned execution flow for this task.
              </p>
            </div>

            <Badge variant="outline">
              {task.status === "queued"
                ? "Ready"
                : task.status}
            </Badge>
          </div>
        </CardHeader>

        <CardContent>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {agents.map((agent, index) => (
              <div
                key={agent}
                className="rounded-lg border border-border bg-background p-4"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                    Step {index + 1}
                  </span>

                  <span className="size-2 rounded-full bg-muted-foreground/40" />
                </div>

                <p className="mt-3 text-sm font-medium text-foreground">
                  {agent}
                </p>

                <p className="mt-1 text-xs text-muted-foreground">
                  Pending
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Repository context */}

      <Card>
        <CardHeader>
          <CardTitle>Repository Context</CardTitle>
        </CardHeader>

        <CardContent>
          {task.repository_name ? (
            <div className="flex flex-wrap items-center gap-3 rounded-lg border border-border p-4">
              <div className="flex size-9 items-center justify-center rounded-lg bg-primary/10">
                <GitBranchIcon
                  className="size-4 text-primary"
                  aria-hidden="true"
                />
              </div>

              <div className="flex min-w-0 flex-col gap-1">
                <span className="text-sm font-medium text-foreground">
                  {task.repository_name}
                </span>

                <span className="text-xs text-muted-foreground">
                  Repository #{task.repository_id}
                </span>
              </div>

              <Badge
                variant="secondary"
                className="ml-auto"
              >
                Connected
              </Badge>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed border-border px-6 py-10 text-center">
              <ListChecksIcon className="size-7 text-muted-foreground" />

              <div>
                <p className="text-sm font-semibold text-foreground">
                  No repository connected
                </p>

                <p className="mt-1 text-sm text-muted-foreground">
                  Connect a repository before starting engineering
                  execution for this task.
                </p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Database status */}

      <div className="flex flex-wrap gap-2">
        <Badge variant="secondary">
          PostgreSQL Connected
        </Badge>

        <Badge variant="secondary">
          Task #{task.id}
        </Badge>

        {task.repository_name ? (
          <Badge variant="secondary">
            Repository Connected
          </Badge>
        ) : null}
      </div>
    </div>
  )
}