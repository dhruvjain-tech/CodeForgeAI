"use client"

import { useEffect, useState } from "react"
import Link from "next/link"

import { AlertCircle, Loader2, Plus, RefreshCw } from "lucide-react"

import { apiFetch } from "@/lib/api"

import { PageHeader } from "@/components/shared/page-header"

import {
  PriorityBadge,
  StatusBadge,
} from "@/components/shared/status-badge"

import { Button } from "@/components/ui/button"

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

// -----------------------------------------------------------------------------
// Types
// -----------------------------------------------------------------------------

type Priority =
  | "critical"
  | "high"
  | "medium"
  | "low"

type Agent =
  | "Architect"
  | "Researcher"
  | "Developer"
  | "Tester"
  | "Debugger"
  | "Reviewer"
  | "Evaluator"

type TaskStatus =
  | "running"
  | "completed"
  | "queued"
  | "failed"
  | "needs_review"

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

interface TaskRow {
  id: string
  title: string
  repository: string
  priority: Priority
  agent: Agent
  status: TaskStatus
  created: string
  updated: string
  description: string
}

// -----------------------------------------------------------------------------
// Constants
// -----------------------------------------------------------------------------

const agents: Agent[] = [
  "Architect",
  "Researcher",
  "Developer",
  "Tester",
  "Debugger",
  "Reviewer",
  "Evaluator",
]

const priorities: Priority[] = [
  "critical",
  "high",
  "medium",
  "low",
]

// -----------------------------------------------------------------------------
// Page
// -----------------------------------------------------------------------------

export default function TasksPage() {
  // ---------------------------------------------------------------------------
  // Database data
  // ---------------------------------------------------------------------------

  const [taskList, setTaskList] = useState<TaskRow[]>([])

  const [repositories, setRepositories] =
    useState<ApiRepository[]>([])

  const [loading, setLoading] =
    useState(true)

  const [taskError, setTaskError] =
    useState<string | null>(null)

  const [loadingRepositories, setLoadingRepositories] =
    useState(true)

  const [creating, setCreating] =
    useState(false)

  // ---------------------------------------------------------------------------
  // Dialog
  // ---------------------------------------------------------------------------

  const [open, setOpen] =
    useState(false)

  // ---------------------------------------------------------------------------
  // Form
  // ---------------------------------------------------------------------------

  const [taskTitle, setTaskTitle] =
    useState("")

  const [taskDescription, setTaskDescription] =
    useState("")

  const [taskRepository, setTaskRepository] =
    useState("")

  const [taskPriority, setTaskPriority] =
    useState<Priority>("medium")

  const [taskAgent, setTaskAgent] =
    useState<Agent>("Developer")

  // ---------------------------------------------------------------------------
  // Load repositories
  // ---------------------------------------------------------------------------

  const loadRepositories = async () => {
    try {
      setLoadingRepositories(true)

      const apiRepositories =
        await apiFetch<ApiRepository[]>(
          "/repositories/"
        )

      const normalizedRepositories =
        apiRepositories.filter(
          (repository) =>
            repository.id !== null &&
            repository.name &&
            repository.name.trim().length > 0
        )

      setRepositories(normalizedRepositories)

      // Automatically select the first repository
      // when nothing has been selected yet.
      if (
        normalizedRepositories.length > 0 &&
        !taskRepository
      ) {
        setTaskRepository(
          String(
            normalizedRepositories[0].id
          )
        )
      }
    } catch (error) {
      console.error(
        "Failed to load repositories:",
        error
      )
    } finally {
      setLoadingRepositories(false)
    }
  }

  // ---------------------------------------------------------------------------
  // Load tasks
  // ---------------------------------------------------------------------------

  const loadTasks = async () => {
    try {
      setLoading(true)
      setTaskError(null)

      const apiTasks =
        await apiFetch<ApiTask[]>(
          "/tasks/"
        )

      const formattedTasks: TaskRow[] =
        apiTasks.map((task) => ({
          id: String(task.id),

          title: task.title,

          // Repository name comes directly from FastAPI.
          repository:
            task.repository_name ??
            "CodeForgeAI",

          priority:
            task.priority as Priority,

          agent:
            (task.assigned_agent ??
              "Developer") as Agent,

          status:
            task.status as TaskStatus,

          created:
            "from database",

          updated:
            "from database",

          description:
            task.description ?? "",
        }))

      setTaskList(formattedTasks)
    } catch (error) {
      console.error(
        "Failed to load tasks:",
        error
      )

      setTaskError(
        "Unable to load tasks. Make sure the CodeForge AI backend is running."
      )
    } finally {
      setLoading(false)
    }
  }

  // ---------------------------------------------------------------------------
  // Initial loading
  // ---------------------------------------------------------------------------

  useEffect(() => {
    loadRepositories()
    loadTasks()
  }, [])

  // ---------------------------------------------------------------------------
  // Reset form
  // ---------------------------------------------------------------------------

  const resetForm = () => {
    setTaskTitle("")
    setTaskDescription("")
    setTaskPriority("medium")
    setTaskAgent("Developer")

    // Keep the repository selected.
    // This makes creating multiple tasks faster.
  }

  // ---------------------------------------------------------------------------
  // Create task
  // ---------------------------------------------------------------------------

  const handleCreateTask = async () => {
    if (!taskTitle.trim()) {
      return
    }

    if (!taskRepository) {
      return
    }

    try {
      setCreating(true)

      /*
       * For now CodeForgeAI is Project ID 1.
       *
       * Repository ID comes directly from
       * the selected repository.
       */

      await apiFetch<ApiTask>(
        "/tasks/",
        {
          method: "POST",

          body: JSON.stringify({
            project_id: 1,

            repository_id:
              Number(taskRepository),

            title:
              taskTitle.trim(),

            description:
              taskDescription.trim() ||
              null,

            priority:
              taskPriority,

            assigned_agent:
              taskAgent,
          }),
        }
      )

      // Reset form
      resetForm()

      // Close dialog
      setOpen(false)

      // Reload tasks directly from PostgreSQL
      // so the UI always reflects database state.
      await loadTasks()
    } catch (error) {
      console.error(
        "Failed to create task:",
        error
      )
    } finally {
      setCreating(false)
    }
  }

  // ---------------------------------------------------------------------------
  // UI
  // ---------------------------------------------------------------------------

  return (
    <div className="flex flex-col gap-6">

      {/* ------------------------------------------------------------------- */}
      {/* Header */}
      {/* ------------------------------------------------------------------- */}

      <PageHeader
        title="Tasks"
        description="Every task assigned to an agent across all projects."
        actions={
          <Dialog
            open={open}
            onOpenChange={setOpen}
          >
            <DialogTrigger
              render={
                <Button>
                  <Plus
                    className="mr-2 size-4"
                    aria-hidden="true"
                  />
                  New Task
                </Button>
              }
            />

            <DialogContent className="sm:max-w-2xl">

              <DialogHeader>

                <DialogTitle>
                  Create New Task
                </DialogTitle>

                <DialogDescription>
                  Create a new engineering task for
                  CodeForge AI.
                </DialogDescription>

              </DialogHeader>

              {/* ----------------------------------------------------------- */}
              {/* Form */}
              {/* ----------------------------------------------------------- */}

              <div className="flex flex-col gap-5">

                {/* Task title */}

                <div className="flex flex-col gap-2">

                  <Label htmlFor="task-title">
                    Task title
                  </Label>

                  <Input
                    id="task-title"
                    placeholder="e.g. Fix authentication timeout"
                    value={taskTitle}
                    onChange={(event) =>
                      setTaskTitle(
                        event.target.value
                      )
                    }
                  />

                </div>

                {/* Description */}

                <div className="flex flex-col gap-2">

                  <Label htmlFor="task-description">
                    Description
                  </Label>

                  <textarea
                    id="task-description"
                    placeholder="Describe what needs to be done..."
                    value={taskDescription}
                    onChange={(event) =>
                      setTaskDescription(
                        event.target.value
                      )
                    }
                    className="min-h-32 w-full resize-y rounded-lg border border-input bg-background px-4 py-3 text-sm text-foreground outline-none transition-colors placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
                  />

                </div>

                {/* Repository */}

                <div className="flex flex-col gap-2">

                  <Label htmlFor="task-repository">
                    Repository
                  </Label>

                  <select
                    id="task-repository"
                    value={taskRepository}
                    onChange={(event) =>
                      setTaskRepository(
                        event.target.value
                      )
                    }
                    disabled={
                      loadingRepositories ||
                      repositories.length === 0
                    }
                    className="h-10 w-full rounded-lg border border-input bg-background px-3 text-sm text-foreground outline-none transition-colors focus:border-ring focus:ring-3 focus:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                  >

                    {loadingRepositories ? (

                      <option value="">
                        Loading repositories...
                      </option>

                    ) : repositories.length === 0 ? (

                      <option value="">
                        No repositories available
                      </option>

                    ) : (

                      <>
                        <option
                          value=""
                          disabled
                        >
                          Select repository
                        </option>

                        {repositories.map(
                          (repository) => (
                            <option
                              key={repository.id}
                              value={String(
                                repository.id
                              )}
                            >
                              {repository.name}
                            </option>
                          )
                        )}
                      </>
                    )}

                  </select>

                </div>

                {/* Priority */}

                <div className="flex flex-col gap-2">

                  <Label htmlFor="task-priority">
                    Priority
                  </Label>

                  <select
                    id="task-priority"
                    value={taskPriority}
                    onChange={(event) =>
                      setTaskPriority(
                        event.target
                          .value as Priority
                      )
                    }
                    className="h-10 w-full rounded-lg border border-input bg-background px-3 text-sm text-foreground outline-none transition-colors focus:border-ring focus:ring-3 focus:ring-ring/50"
                  >

                    {priorities.map(
                      (priority) => (
                        <option
                          key={priority}
                          value={priority}
                        >
                          {priority}
                        </option>
                      )
                    )}

                  </select>

                </div>

                {/* Agent */}

                <div className="flex flex-col gap-2">

                  <Label htmlFor="task-agent">
                    Assigned Agent
                  </Label>

                  <select
                    id="task-agent"
                    value={taskAgent}
                    onChange={(event) =>
                      setTaskAgent(
                        event.target
                          .value as Agent
                      )
                    }
                    className="h-10 w-full rounded-lg border border-input bg-background px-3 text-sm text-foreground outline-none transition-colors focus:border-ring focus:ring-3 focus:ring-ring/50"
                  >

                    {agents.map(
                      (agent) => (
                        <option
                          key={agent}
                          value={agent}
                        >
                          {agent}
                        </option>
                      )
                    )}

                  </select>

                </div>

                {/* Buttons */}

                <div className="flex justify-end gap-2 pt-2">

                  <Button
                    variant="outline"
                    onClick={() => {
                      setOpen(false)
                      resetForm()
                    }}
                    disabled={creating}
                  >
                    Cancel
                  </Button>

                  <Button
                    onClick={
                      handleCreateTask
                    }
                    disabled={
                      creating ||
                      !taskTitle.trim() ||
                      !taskRepository
                    }
                  >

                    {creating ? (
                      <>
                        <Loader2
                          className="mr-2 size-4 animate-spin"
                          aria-hidden="true"
                        />
                        Creating...
                      </>
                    ) : (
                      "Create Task"
                    )}

                  </Button>

                </div>

              </div>

            </DialogContent>

          </Dialog>
        }
      />

      {/* ------------------------------------------------------------------- */}
      {/* Task table */}
      {/* ------------------------------------------------------------------- */}

      <div className="overflow-hidden rounded-xl border border-border">

        {/* Table header */}

        <div className="grid grid-cols-[2fr_1.5fr_1fr_1fr_1fr_1fr] gap-4 border-b border-border px-4 py-3 text-sm font-medium text-muted-foreground">

          <div>
            Task
          </div>

          <div>
            Repository
          </div>

          <div>
            Agent
          </div>

          <div>
            Priority
          </div>

          <div>
            Status
          </div>

          <div className="text-right">
            Updated
          </div>

        </div>

        {/* Loading */}

        {loading ? (

          <div className="flex items-center justify-center py-16 text-sm text-muted-foreground">

            <Loader2
              className="mr-2 size-4 animate-spin"
              aria-hidden="true"
            />

            Loading tasks...

          </div>

        ) : taskError ? (

          /* ---------------------------------------------------------------- */
          /* Error state */
          /* ---------------------------------------------------------------- */

          <div className="flex flex-col items-center justify-center gap-4 py-16 text-center">

            <div className="flex size-10 items-center justify-center rounded-full bg-red-500/10 text-red-400">

              <AlertCircle
                className="size-5"
                aria-hidden="true"
              />

            </div>

            <div>

              <div className="text-sm font-medium text-foreground">
                Unable to load tasks
              </div>

              <div className="mt-1 max-w-md text-sm text-muted-foreground">
                {taskError}
              </div>

            </div>

            <Button
              variant="outline"
              onClick={loadTasks}
            >
              <RefreshCw
                className="mr-2 size-4"
                aria-hidden="true"
              />
              Retry
            </Button>

          </div>

        ) : taskList.length === 0 ? (

          /* ---------------------------------------------------------------- */
          /* Empty state */
          /* ---------------------------------------------------------------- */

          <div className="flex flex-col items-center justify-center gap-2 py-16 text-center">

            <div className="text-sm font-medium">
              No tasks yet
            </div>

            <div className="text-sm text-muted-foreground">
              Create your first engineering task.
            </div>

          </div>

        ) : (

          /* ---------------------------------------------------------------- */
          /* Tasks */
          /* ---------------------------------------------------------------- */

          taskList.map((task) => (

            <Link
              key={task.id}
              href={`/tasks/${task.id}`}
              className="grid grid-cols-[2fr_1.5fr_1fr_1fr_1fr_1fr] gap-4 border-b border-border px-4 py-4 transition-colors last:border-b-0 hover:bg-muted/40"
            >

              {/* Task */}

              <div className="min-w-0">

                <div className="truncate font-medium">
                  {task.title}
                </div>

                <div className="mt-1 text-xs text-muted-foreground">
                  #{task.id}
                </div>

              </div>

              {/* Repository */}

              <div className="flex items-center text-sm text-muted-foreground">
                {task.repository}
              </div>

              {/* Agent */}

              <div className="flex items-center text-sm text-muted-foreground">
                {task.agent}
              </div>

              {/* Priority */}

              <div className="flex items-center">

                <PriorityBadge
                  priority={task.priority}
                />

              </div>

              {/* Status */}

              <div className="flex items-center">

                <StatusBadge
                  status={task.status}
                />

              </div>

              {/* Updated */}

              <div className="flex items-center justify-end text-sm text-muted-foreground">
                {task.updated}
              </div>

            </Link>

          ))

        )}

      </div>

    </div>
  )
}