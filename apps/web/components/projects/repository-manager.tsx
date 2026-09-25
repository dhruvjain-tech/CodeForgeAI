"use client"

import { FormEvent, useState } from "react"
import { PencilIcon, PlusIcon, Trash2Icon } from "lucide-react"
import { useRouter } from "next/navigation"

import { apiFetch } from "@/lib/api"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface RepositoryManagerProps {
  projectId: number
}

interface RepositoryData {
  id: number
  project_id: number
  name: string
  repository_url: string
  default_branch: string
  local_path: string | null
  status: string
}

interface RepositoryManagerEditProps {
  repository: RepositoryData
  onUpdated: () => void
  onDeleted: () => void
}

function EditRepositoryDialog({
  repository,
  onUpdated,
}: RepositoryManagerEditProps) {
  const [open, setOpen] = useState(false)
  const [name, setName] = useState(repository.name)
  const [repositoryUrl, setRepositoryUrl] = useState(
    repository.repository_url,
  )
  const [defaultBranch, setDefaultBranch] = useState(
    repository.default_branch,
  )
  const [localPath, setLocalPath] = useState(repository.local_path ?? "")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!name.trim()) {
      setError("Repository name is required.")
      return
    }

    if (!repositoryUrl.trim()) {
      setError("Repository URL is required.")
      return
    }

    setLoading(true)
    setError("")

    try {
      await apiFetch(`/repositories/${repository.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          name: name.trim(),
          repository_url: repositoryUrl.trim(),
          default_branch: defaultBranch.trim() || "main",
          local_path: localPath.trim() || null,
        }),
      })

      setOpen(false)
      onUpdated()
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to update repository.",
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger
        render={
          <Button
            variant="outline"
            size="sm"
            type="button"
          >
            <PencilIcon aria-hidden="true" />
            Edit
          </Button>
        }
      />

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Repository</DialogTitle>
          <DialogDescription>
            Update the repository configuration for this project.
          </DialogDescription>
        </DialogHeader>

        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-5"
        >
          <div className="flex flex-col gap-2">
            <Label htmlFor={`edit-repository-name-${repository.id}`}>
              Repository Name
            </Label>

            <Input
              id={`edit-repository-name-${repository.id}`}
              value={name}
              onChange={(event) => setName(event.target.value)}
              disabled={loading}
            />
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor={`edit-repository-url-${repository.id}`}>
              Repository URL
            </Label>

            <Input
              id={`edit-repository-url-${repository.id}`}
              value={repositoryUrl}
              onChange={(event) =>
                setRepositoryUrl(event.target.value)
              }
              disabled={loading}
            />
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor={`edit-default-branch-${repository.id}`}>
              Default Branch
            </Label>

            <Input
              id={`edit-default-branch-${repository.id}`}
              value={defaultBranch}
              onChange={(event) =>
                setDefaultBranch(event.target.value)
              }
              disabled={loading}
            />
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor={`edit-local-path-${repository.id}`}>
              Local Path
            </Label>

            <Input
              id={`edit-local-path-${repository.id}`}
              value={localPath}
              onChange={(event) =>
                setLocalPath(event.target.value)
              }
              disabled={loading}
            />
          </div>

          {error ? (
            <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
              {error}
            </div>
          ) : null}

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              disabled={loading}
            >
              Cancel
            </Button>

            <Button type="submit" disabled={loading}>
              {loading ? "Saving..." : "Save Changes"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

function DeleteRepositoryButton({
  repository,
  onDeleted,
}: {
  repository: RepositoryData
  onDeleted: () => void
}) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleDelete() {
    const confirmed = window.confirm(
      `Delete repository "${repository.name}"? This action cannot be undone.`,
    )

    if (!confirmed) {
      return
    }

    setLoading(true)
    setError("")

    try {
      await apiFetch(`/repositories/${repository.id}`, {
        method: "DELETE",
      })

      onDeleted()
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to delete repository.",
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-end gap-2">
      <Button
        variant="destructive"
        size="sm"
        type="button"
        onClick={handleDelete}
        disabled={loading}
      >
        <Trash2Icon aria-hidden="true" />
        {loading ? "Deleting..." : "Delete"}
      </Button>

      {error ? (
        <span className="max-w-xs text-right text-xs text-destructive">
          {error}
        </span>
      ) : null}
    </div>
  )
}

export function RepositoryManager({
  projectId,
}: RepositoryManagerProps) {
  const router = useRouter()

  const [open, setOpen] = useState(false)
  const [name, setName] = useState("")
  const [repositoryUrl, setRepositoryUrl] = useState("")
  const [defaultBranch, setDefaultBranch] = useState("main")
  const [localPath, setLocalPath] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!name.trim()) {
      setError("Repository name is required.")
      return
    }

    if (!repositoryUrl.trim()) {
      setError("Repository URL is required.")
      return
    }

    setLoading(true)
    setError("")

    try {
      await apiFetch("/repositories/", {
        method: "POST",
        body: JSON.stringify({
          project_id: projectId,
          name: name.trim(),
          repository_url: repositoryUrl.trim(),
          default_branch: defaultBranch.trim() || "main",
          local_path: localPath.trim() || null,
        }),
      })

      setName("")
      setRepositoryUrl("")
      setDefaultBranch("main")
      setLocalPath("")
      setOpen(false)

      router.refresh()
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to create repository.",
      )
    } finally {
      setLoading(false)
    }
  }

  function refreshRepositories() {
    router.refresh()
  }

  return (
    <div className="flex items-center gap-2">
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger
          render={
            <Button type="button">
              <PlusIcon aria-hidden="true" />
              Add Repository
            </Button>
          }
        />

        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Repository</DialogTitle>

            <DialogDescription>
              Connect a repository to this CodeForge AI project.
            </DialogDescription>
          </DialogHeader>

          <form
            onSubmit={handleSubmit}
            className="flex flex-col gap-5"
          >
            <div className="flex flex-col gap-2">
              <Label htmlFor="repository-name">
                Repository Name
              </Label>

              <Input
                id="repository-name"
                placeholder="CodeForgeAI"
                value={name}
                onChange={(event) => setName(event.target.value)}
                disabled={loading}
              />
            </div>

            <div className="flex flex-col gap-2">
              <Label htmlFor="repository-url">
                Repository URL
              </Label>

              <Input
                id="repository-url"
                placeholder="https://github.com/username/repository"
                value={repositoryUrl}
                onChange={(event) =>
                  setRepositoryUrl(event.target.value)
                }
                disabled={loading}
              />
            </div>

            <div className="flex flex-col gap-2">
              <Label htmlFor="default-branch">
                Default Branch
              </Label>

              <Input
                id="default-branch"
                placeholder="main"
                value={defaultBranch}
                onChange={(event) =>
                  setDefaultBranch(event.target.value)
                }
                disabled={loading}
              />
            </div>

            <div className="flex flex-col gap-2">
              <Label htmlFor="local-path">
                Local Path
              </Label>

              <Input
                id="local-path"
                placeholder="D:\CodeForgeAI"
                value={localPath}
                onChange={(event) =>
                  setLocalPath(event.target.value)
                }
                disabled={loading}
              />
            </div>

            {error ? (
              <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
                {error}
              </div>
            ) : null}

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setOpen(false)}
                disabled={loading}
              >
                Cancel
              </Button>

              <Button type="submit" disabled={loading}>
                {loading ? "Adding..." : "Add Repository"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export function RepositoryActions({
  repository,
}: {
  repository: RepositoryData
}) {
  const router = useRouter()

  function refresh() {
    router.refresh()
  }

  return (
    <div className="flex flex-wrap items-start justify-end gap-2">
      <EditRepositoryDialog
        repository={repository}
        onUpdated={refresh}
        onDeleted={refresh}
      />

     <DeleteRepositoryButton
  repository={repository}
  onDeleted={refresh}
/>
    </div>
  )
}