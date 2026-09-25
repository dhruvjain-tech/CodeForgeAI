import {
  CheckIcon,
  CircleIcon,
  GitBranchIcon,
  GitCommitHorizontalIcon,
  GitPullRequestIcon,
  StarIcon,
} from "lucide-react"

import { apiFetch } from "@/lib/api"

import {
  approvalWorkflow,
  commits,
  issues,
  pullRequests,
} from "@/lib/data/github"

import { PageHeader } from "@/components/shared/page-header"
import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface ApiRepository {
  id: number
  project_id: number
  name: string
  repository_url: string
  default_branch: string
  local_path: string | null
  status: string
}

export default async function GithubPage() {
  let repositories: ApiRepository[] = []

  try {
    repositories = await apiFetch<ApiRepository[]>(
      "/repositories/",
    )
  } catch {
    repositories = []
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="GitHub Integration"
        description="Repository activity and the human-in-the-loop approval workflow agents follow before merging."
      />

      {/* Approval Workflow */}
      <Card>
        <CardHeader>
          <CardTitle>Approval Workflow</CardTitle>
        </CardHeader>

        <CardContent>
          <div className="flex flex-wrap items-center gap-2">
            {approvalWorkflow.map((step, index) => (
              <div
                key={step}
                className="flex items-center gap-2"
              >
                <span className="rounded-md border border-border bg-muted px-2.5 py-1 text-xs font-medium text-foreground">
                  {step}
                </span>

                {index < approvalWorkflow.length - 1 ? (
                  <span
                    className="text-muted-foreground"
                    aria-hidden="true"
                  >
                    →
                  </span>
                ) : null}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Real Repositories */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between gap-4">
            <CardTitle>Repositories</CardTitle>

            <Badge variant="secondary">
              {repositories.length}{" "}
              {repositories.length === 1
                ? "Repository"
                : "Repositories"}
            </Badge>
          </div>
        </CardHeader>

        <CardContent className="flex flex-col gap-3">
          {repositories.length === 0 ? (
            <div className="rounded-lg border border-dashed border-border px-6 py-10 text-center">
              <GitBranchIcon className="mx-auto size-8 text-muted-foreground" />

              <p className="mt-3 text-sm font-semibold text-foreground">
                No repositories connected
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                Connect a repository to start autonomous engineering
                workflows.
              </p>
            </div>
          ) : (
            repositories.map((repo) => (
              <div
                key={repo.id}
                className="rounded-lg border border-border p-4"
              >
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div className="flex min-w-0 items-start gap-3">
                    <span
                      className={cn(
                        "mt-1.5 flex size-2 shrink-0 rounded-full",
                        repo.status === "active"
                          ? "bg-success"
                          : "bg-muted-foreground",
                      )}
                      aria-hidden="true"
                    />

                    <div className="flex min-w-0 flex-col gap-1">
                      <span className="font-mono text-sm font-medium text-foreground">
                        {repo.name}
                      </span>

                      <a
                        href={repo.repository_url}
                        target="_blank"
                        rel="noreferrer"
                        className="break-all font-mono text-xs text-muted-foreground hover:text-primary hover:underline"
                      >
                        {repo.repository_url}
                      </a>
                    </div>
                  </div>

                  <Badge
                    variant={
                      repo.status === "active"
                        ? "secondary"
                        : "outline"
                    }
                    className="capitalize"
                  >
                    {repo.status}
                  </Badge>
                </div>

                <div className="mt-4 grid grid-cols-1 gap-3 border-t border-border pt-4 sm:grid-cols-3">
                  <div className="flex flex-col gap-1">
                    <span className="text-xs text-muted-foreground">
                      Repository ID
                    </span>

                    <span className="font-mono text-xs text-foreground">
                      #{repo.id}
                    </span>
                  </div>

                  <div className="flex flex-col gap-1">
                    <span className="text-xs text-muted-foreground">
                      Default Branch
                    </span>

                    <span className="flex items-center gap-1.5 text-xs font-medium text-foreground">
                      <GitBranchIcon className="size-3" />
                      {repo.default_branch}
                    </span>
                  </div>

                  <div className="flex min-w-0 flex-col gap-1">
                    <span className="text-xs text-muted-foreground">
                      Local Path
                    </span>

                    <span className="break-all font-mono text-xs text-foreground">
                      {repo.local_path || "Not configured"}
                    </span>
                  </div>
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>

      {/* Open Issues + Pull Requests */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Open Issues</CardTitle>
          </CardHeader>

          <CardContent className="flex flex-col gap-3">
            {issues.map((issue) => (
              <div
                key={issue.id}
                className="flex flex-col gap-1.5 rounded-lg border border-border p-3"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-xs text-muted-foreground">
                    {issue.id}
                  </span>

                  <Badge
                    variant="outline"
                    className="capitalize"
                  >
                    {issue.status.replace("-", " ")}
                  </Badge>
                </div>

                <span className="text-sm font-medium text-foreground">
                  {issue.title}
                </span>

                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="text-xs text-muted-foreground">
                    {issue.repo}
                  </span>

                  {issue.labels.map((label) => (
                    <Badge
                      key={label}
                      variant="secondary"
                      className="text-[10px]"
                    >
                      {label}
                    </Badge>
                  ))}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Pull Requests</CardTitle>
          </CardHeader>

          <CardContent className="flex flex-col gap-3">
            {pullRequests.map((pr) => (
              <div
                key={pr.id}
                className="flex flex-col gap-1.5 rounded-lg border border-border p-3"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="flex items-center gap-1.5 font-mono text-xs text-muted-foreground">
                    <GitPullRequestIcon
                      className="size-3"
                      aria-hidden="true"
                    />
                    {pr.id}
                  </span>

                  <Badge
                    variant="outline"
                    className="capitalize"
                  >
                    {pr.status}
                  </Badge>
                </div>

                <span className="text-sm font-medium text-foreground">
                  {pr.title}
                </span>

                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>
                    {pr.repo} · {pr.author}
                  </span>

                  <span
                    className={cn(
                      "flex items-center gap-1",
                      pr.checks === "passing"
                        ? "text-success"
                        : "text-warning",
                    )}
                  >
                    {pr.checks === "passing" ? (
                      <CheckIcon
                        className="size-3"
                        aria-hidden="true"
                      />
                    ) : (
                      <CircleIcon
                        className="size-3"
                        aria-hidden="true"
                      />
                    )}

                    {pr.checks}
                  </span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Recent Commits */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Commits</CardTitle>
        </CardHeader>

        <CardContent className="flex flex-col gap-3">
          {commits.map((commit) => (
            <div
              key={commit.sha}
              className="flex items-center justify-between gap-3 rounded-lg border border-border p-3"
            >
              <div className="flex min-w-0 items-center gap-3">
                <GitCommitHorizontalIcon
                  className="size-4 shrink-0 text-muted-foreground"
                  aria-hidden="true"
                />

                <div className="flex min-w-0 flex-col gap-0.5">
                  <span className="truncate text-sm text-foreground">
                    {commit.message}
                  </span>

                  <span className="text-xs text-muted-foreground">
                    {commit.repo} · {commit.author}
                  </span>
                </div>
              </div>

              <div className="flex shrink-0 flex-col items-end gap-0.5 text-right">
                <span className="font-mono text-xs text-muted-foreground">
                  {commit.sha}
                </span>

                <span className="text-xs text-muted-foreground">
                  {commit.time}
                </span>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Database Status */}
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
          GitHub Integration
        </Badge>
      </div>
    </div>
  )
}