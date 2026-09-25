import Link from "next/link"
import {
  ActivityIcon,
  ClipboardListIcon,
  DatabaseIcon,
  FolderKanbanIcon,
} from "lucide-react"

import { apiFetch } from "@/lib/api"

import { MetricCard } from "@/components/shared/metric-card"
import { PageHeader } from "@/components/shared/page-header"
import { PriorityBadge, StatusBadge } from "@/components/shared/status-badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface ApiProject {
  id: number
  name: string
  description: string | null
  repository_url: string | null
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

interface ApiRepository {
  id: number
  project_id: number
  name: string
  repository_url: string
  default_branch: string
  local_path: string | null
  status: string
}

export default async function DashboardPage() {
  let projects: ApiProject[] = []
  let tasks: ApiTask[] = []
  let repositories: ApiRepository[] = []

  try {
    projects = await apiFetch<ApiProject[]>("/projects/")
  } catch {
    projects = []
  }

  try {
    tasks = await apiFetch<ApiTask[]>("/tasks/")
  } catch {
    tasks = []
  }

  try {
    repositories = await apiFetch<ApiRepository[]>("/repositories/")
  } catch {
    repositories = []
  }

  const activeTasks = tasks.filter(
    (task) =>
      task.status === "running" ||
      task.status === "queued",
  )

  const assignedAgents = Array.from(
    new Set(
      tasks
        .map((task) => task.assigned_agent)
        .filter(
          (agent): agent is string =>
            Boolean(agent),
        ),
    ),
  )

  const recentTasks = tasks.slice(0, 5)

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Dashboard"
        description="Overview of active work across every project and repository."
        actions={
          <Button
            render={<Link href="/tasks" />}
            nativeButton={false}
          >
            New Task
          </Button>
        }
      />

      {/* Metrics */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          label="Active Tasks"
          value={activeTasks.length}
          icon={ClipboardListIcon}
          accent="primary"
        />

        <MetricCard
          label="Projects"
          value={projects.length}
          icon={FolderKanbanIcon}
          accent="engineering"
        />

        <MetricCard
          label="Repositories"
          value={repositories.length}
          icon={DatabaseIcon}
          accent="primary"
        />

        <MetricCard
          label="Assigned Agents"
          value={assignedAgents.length}
          icon={ActivityIcon}
          accent="engineering"
        />
      </div>

      {/* Tasks + Agent Assignments */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Recent Tasks</CardTitle>

            <Button
              variant="ghost"
              size="sm"
              render={<Link href="/tasks" />}
              nativeButton={false}
            >
              View all
            </Button>
          </CardHeader>

          <CardContent className="flex flex-col gap-1">
            {recentTasks.length === 0 ? (
              <div className="rounded-lg border border-dashed border-border px-4 py-8 text-center">
                <p className="text-sm font-medium text-foreground">
                  No tasks found
                </p>

                <p className="mt-1 text-xs text-muted-foreground">
                  Create a task to start engineering work.
                </p>
              </div>
            ) : (
              recentTasks.map((task) => (
                <Link
                  key={task.id}
                  href={`/tasks/${task.id}`}
                  className="flex items-center justify-between gap-4 rounded-lg px-3 py-2.5 transition-colors hover:bg-muted"
                >
                  <div className="flex min-w-0 flex-col gap-0.5">
                    <span className="truncate text-sm font-medium text-foreground">
                      {task.title}
                    </span>

                    <span className="text-xs text-muted-foreground">
                      Task #{task.id}
                      {task.repository_name
                        ? ` · ${task.repository_name}`
                        : ""}
                    </span>
                  </div>

                  <div className="flex shrink-0 items-center gap-2">
                    <PriorityBadge
                      priority={
                        task.priority as
                          | "critical"
                          | "high"
                          | "medium"
                          | "low"
                      }
                      className="hidden sm:inline-flex"
                    />

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
                </Link>
              ))
            )}
          </CardContent>
        </Card>

        {/* Real task assignments */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Agent Assignments</CardTitle>

            <Button
              variant="ghost"
              size="sm"
              render={<Link href="/agents" />}
              nativeButton={false}
            >
              View all
            </Button>
          </CardHeader>

          <CardContent className="flex flex-col gap-4">
            {assignedAgents.length === 0 ? (
              <div className="rounded-lg border border-dashed border-border px-4 py-8 text-center">
                <p className="text-sm font-medium text-foreground">
                  No agents assigned
                </p>

                <p className="mt-1 text-xs text-muted-foreground">
                  Agents will appear here when tasks are assigned.
                </p>
              </div>
            ) : (
              assignedAgents.map((agent) => {
                const agentTasks = tasks.filter(
                  (task) => task.assigned_agent === agent,
                )

                const activeAgentTasks = agentTasks.filter(
                  (task) =>
                    task.status === "running" ||
                    task.status === "queued",
                )

                return (
                  <div
                    key={agent}
                    className="flex items-start gap-3"
                  >
                    <div className="mt-1 flex size-2 shrink-0 items-center justify-center">
                      <span className="size-2 rounded-full bg-engineering" />
                    </div>

                    <div className="flex min-w-0 flex-1 flex-col gap-0.5">
                      <span className="text-sm font-medium text-foreground">
                        {agent} Agent
                      </span>

                      <span className="text-xs text-muted-foreground">
                        {agentTasks.length}{" "}
                        {agentTasks.length === 1
                          ? "task"
                          : "tasks"}
                        {" · "}
                        {activeAgentTasks.length} active
                      </span>
                    </div>
                  </div>
                )
              })
            )}
          </CardContent>
        </Card>
      </div>

      {/* Real Projects */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Projects</CardTitle>

          <Button
            variant="ghost"
            size="sm"
            render={<Link href="/projects" />}
            nativeButton={false}
          >
            View all
          </Button>
        </CardHeader>

        <CardContent>
          {projects.length === 0 ? (
            <div className="rounded-lg border border-dashed border-border px-6 py-10 text-center">
              <p className="text-sm font-semibold text-foreground">
                No projects found
              </p>

              <p className="mt-1 text-xs text-muted-foreground">
                Create a project to start using CodeForge AI.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {projects.map((project) => {
                const projectTasks = tasks.filter(
                  (task) => task.project_id === project.id,
                )

                const projectRepositories =
                  repositories.filter(
                    (repository) =>
                      repository.project_id === project.id,
                  )

                return (
                  <Link
                    key={project.id}
                    href={`/projects/${project.id}`}
                    className="flex flex-col gap-3 rounded-xl border border-border p-4 transition-colors hover:border-primary/40 hover:bg-muted/50"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="truncate text-sm font-semibold text-foreground">
                        {project.name}
                      </span>

                      <span className="rounded-md border border-success/30 bg-success/10 px-2 py-0.5 text-[10px] font-medium text-success">
                        Connected
                      </span>
                    </div>

                    <p className="line-clamp-2 text-xs text-muted-foreground">
                      {project.description ||
                        "No project description available."}
                    </p>

                    <div className="mt-auto border-t border-border pt-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-muted-foreground">
                          Tasks
                        </span>

                        <span className="text-xs font-semibold text-foreground">
                          {projectTasks.length}
                        </span>
                      </div>

                      <div className="mt-2 flex items-center justify-between">
                        <span className="text-xs text-muted-foreground">
                          Repositories
                        </span>

                        <span className="text-xs font-semibold text-foreground">
                          {projectRepositories.length}
                        </span>
                      </div>

                      <div className="mt-2 flex items-center justify-between">
                        <span className="text-xs text-muted-foreground">
                          Project ID
                        </span>

                        <span className="font-mono text-xs text-foreground">
                          #{project.id}
                        </span>
                      </div>
                    </div>
                  </Link>
                )
              })}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Database status */}
      <div className="flex flex-wrap gap-2">
        <span className="rounded-md border border-success/30 bg-success/10 px-2.5 py-1 text-xs font-medium text-success">
          PostgreSQL Connected
        </span>

        <span className="rounded-md border border-border bg-muted px-2.5 py-1 text-xs font-medium text-muted-foreground">
          {projects.length} Projects
        </span>

        <span className="rounded-md border border-border bg-muted px-2.5 py-1 text-xs font-medium text-muted-foreground">
          {repositories.length} Repositories
        </span>

        <span className="rounded-md border border-border bg-muted px-2.5 py-1 text-xs font-medium text-muted-foreground">
          {tasks.length} Tasks
        </span>
      </div>
    </div>
  )
}