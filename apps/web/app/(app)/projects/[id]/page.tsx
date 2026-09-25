import Link from "next/link"
import { notFound } from "next/navigation"
import { ArrowLeftIcon, ListChecksIcon } from "lucide-react"

import { apiFetch } from "@/lib/api"

import {
  RepositoryActions,
  RepositoryManager,
} from "@/components/projects/repository-manager"
import { PageHeader } from "@/components/shared/page-header"
import { PriorityBadge, StatusBadge } from "@/components/shared/status-badge"
import { Badge } from "@/components/ui/badge"
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

interface ApiRepository {
  id: number
  project_id: number
  name: string
  repository_url: string
  default_branch: string
  local_path: string | null
  status: string
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

export default async function ProjectDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const projectId = Number(id)

  if (!Number.isInteger(projectId)) {
    notFound()
  }

  let project: ApiProject

  try {
    project = await apiFetch<ApiProject>(
      `/projects/${projectId}`,
    )
  } catch {
    notFound()
  }

  let repositories: ApiRepository[] = []

  try {
    repositories = await apiFetch<ApiRepository[]>(
      `/repositories/project/${projectId}`,
    )
  } catch {
    repositories = []
  }

  let projectTasks: ApiTask[] = []

  try {
    projectTasks = await apiFetch<ApiTask[]>(
      `/tasks/project/${projectId}`,
    )
  } catch {
    projectTasks = []
  }

  return (
    <div className="flex flex-col gap-6">
      <Button
        variant="ghost"
        size="sm"
        className="w-fit"
        render={<Link href="/projects" />}
        nativeButton={false}
      >
        <ArrowLeftIcon aria-hidden="true" />
        Back to Projects
      </Button>

      <PageHeader
        title={project.name}
        description={`Project #${project.id}`}
      />

      {/* Overview */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Overview</CardTitle>
          </CardHeader>

          <CardContent className="flex flex-col gap-5">
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                Description
              </p>

              <p className="mt-2 text-sm leading-6 text-foreground">
                {project.description ||
                  "No description was provided for this project."}
              </p>
            </div>

            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                Repository
              </p>

              {project.repository_url ? (
                <a
                  href={project.repository_url}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-2 block break-all font-mono text-xs text-primary hover:underline"
                >
                  {project.repository_url}
                </a>
              ) : (
                <p className="mt-2 text-sm text-muted-foreground">
                  No repository connected
                </p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4 border-t border-border pt-4 sm:grid-cols-3">
              <div className="flex flex-col gap-1">
                <span className="text-xs text-muted-foreground">
                  Project ID
                </span>

                <span className="text-xl font-semibold">
                  #{project.id}
                </span>
              </div>

              <div className="flex flex-col gap-1">
                <span className="text-xs text-muted-foreground">
                  Tasks
                </span>

                <span className="text-xl font-semibold">
                  {projectTasks.length}
                </span>
              </div>

              <div className="flex flex-col gap-1">
                <span className="text-xs text-muted-foreground">
                  Repositories
                </span>

                <span className="text-xl font-semibold">
                  {repositories.length}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Statistics */}
        <Card>
          <CardHeader>
            <CardTitle>Project Statistics</CardTitle>
          </CardHeader>

          <CardContent className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">
                Project ID
              </span>

              <span className="font-mono text-xs">
                #{project.id}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">
                Tasks
              </span>

              <span className="text-sm font-medium">
                {projectTasks.length}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">
                Repositories
              </span>

              <span className="text-sm font-medium">
                {repositories.length}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">
                Data Source
              </span>

              <span className="text-sm font-medium">
                PostgreSQL
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Repositories */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div className="flex items-center gap-3">
            <CardTitle>Repositories</CardTitle>

            <Badge variant="secondary">
              {repositories.length}{" "}
              {repositories.length === 1
                ? "Repository"
                : "Repositories"}
            </Badge>
          </div>
        <RepositoryManager projectId={projectId} />
        </CardHeader>

        <CardContent>
          {repositories.length === 0 ? (
            <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed border-border px-6 py-12 text-center">
              <p className="text-sm font-semibold">
                No repositories connected
              </p>

              <p className="text-sm text-muted-foreground">
                Add a repository to start repository-level
                engineering work.
              </p>
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              {repositories.map((repository) => (
                <div
                  key={repository.id}
                  className="flex flex-col gap-4 rounded-lg border border-border p-4"
                >
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div className="flex min-w-0 flex-col gap-1">
                      <div className="flex items-center gap-2">
                        <span className="size-2 shrink-0 rounded-full bg-primary" />

                        <span className="text-sm font-semibold text-foreground">
                          {repository.name}
                        </span>

                        <Badge
                          variant="secondary"
                          className="text-[10px]"
                        >
                          {repository.status}
                        </Badge>
                      </div>

                      <a
                        href={repository.repository_url}
                        target="_blank"
                        rel="noreferrer"
                        className="break-all font-mono text-xs text-muted-foreground hover:text-primary hover:underline"
                      >
                        {repository.repository_url}
                      </a>
                    </div>

                    <RepositoryActions
                      repository={repository}
                    />
                  </div>

                  <div className="grid grid-cols-1 gap-4 border-t border-border pt-4 sm:grid-cols-3">
                    <div className="flex flex-col gap-1">
                      <span className="text-xs text-muted-foreground">
                        Repository ID
                      </span>

                      <span className="font-mono text-xs text-foreground">
                        #{repository.id}
                      </span>
                    </div>

                    <div className="flex flex-col gap-1">
                      <span className="text-xs text-muted-foreground">
                        Default Branch
                      </span>

                      <span className="font-mono text-xs text-foreground">
                        {repository.default_branch}
                      </span>
                    </div>

                    <div className="flex flex-col gap-1">
                      <span className="text-xs text-muted-foreground">
                        Local Path
                      </span>

                      <span className="break-all font-mono text-xs text-foreground">
                        {repository.local_path ||
                          "Not configured"}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Tasks */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div className="flex items-center gap-3">
            <CardTitle>Tasks</CardTitle>

            <Badge variant="secondary">
              {projectTasks.length}{" "}
              {projectTasks.length === 1 ? "Task" : "Tasks"}
            </Badge>
          </div>
        </CardHeader>

        <CardContent>
          {projectTasks.length === 0 ? (
            <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed border-border px-6 py-12 text-center">
              <ListChecksIcon className="size-8 text-muted-foreground" />

              <div>
                <p className="text-sm font-semibold">
                  No tasks yet
                </p>

                <p className="mt-1 text-sm text-muted-foreground">
                  This project has no tasks in PostgreSQL.
                </p>
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-1">
              {projectTasks.map((task) => (
                <Link
                  key={task.id}
                  href={`/tasks/${task.id}`}
                  className="flex items-center justify-between gap-4 rounded-lg px-3 py-3 transition-colors hover:bg-muted"
                >
                  <div className="flex min-w-0 flex-col gap-1">
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
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Status */}
      <div className="flex flex-wrap gap-2">
        <Badge variant="secondary">
          PostgreSQL Connected
        </Badge>

        <Badge variant="secondary">
          {repositories.length}{" "}
          {repositories.length === 1
            ? "Repository"
            : "Repositories"}
        </Badge>

        <Badge variant="secondary">
          {projectTasks.length}{" "}
          {projectTasks.length === 1 ? "Task" : "Tasks"}
        </Badge>
      </div>
    </div>
  )
}