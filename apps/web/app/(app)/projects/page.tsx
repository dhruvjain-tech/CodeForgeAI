import Link from "next/link"

import { apiFetch } from "@/lib/api"

import { PageHeader } from "@/components/shared/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface ApiProject {
  id: number
  name: string
  description: string | null
  repository_url: string | null
}

export default async function ProjectsPage() {
  let projects: ApiProject[] = []

  try {
    projects = await apiFetch<ApiProject[]>("/projects/")
  } catch {
    projects = []
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Projects"
        description="All repositories under active agent supervision."
      />

      {projects.length === 0 ? (
        <div className="rounded-xl border border-border bg-card p-8 text-center">
          <h2 className="text-sm font-semibold text-foreground">
            No projects found
          </h2>

          <p className="mt-2 text-sm text-muted-foreground">
            Create a project to start using CodeForge AI.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {projects.map((project) => (
            <Link
              key={project.id}
              href={`/projects/${project.id}`}
            >
              <Card className="h-full transition-colors hover:border-primary/40">
                <CardHeader>
                  <div className="flex flex-col gap-1">
                    <CardTitle>{project.name}</CardTitle>

                    <span className="text-xs text-muted-foreground">
                      Project #{project.id}
                    </span>
                  </div>
                </CardHeader>

                <CardContent className="flex flex-col gap-5">
                  {/* Description */}

                  <div>
                    <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                      Description
                    </p>

                    <p className="mt-2 text-sm leading-6 text-foreground">
                      {project.description ||
                        "No description was provided for this project."}
                    </p>
                  </div>

                  {/* Repository */}

                  <div>
                    <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                      Repository
                    </p>

                    <p className="mt-2 break-all font-mono text-xs text-muted-foreground">
                      {project.repository_url ||
                        "No repository connected"}
                    </p>
                  </div>

                  {/* Database Status */}

                  <div className="border-t border-border pt-4">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-muted-foreground">
                        Project ID
                      </span>

                      <span className="font-mono text-xs text-foreground">
                        #{project.id}
                      </span>
                    </div>

                    <div className="mt-3 flex items-center justify-between">
                      <span className="text-xs text-muted-foreground">
                        Data Source
                      </span>

                      <span className="text-xs font-medium text-foreground">
                        PostgreSQL
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}