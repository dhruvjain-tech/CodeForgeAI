
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api/v1"

export async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    },
  )

  if (!response.ok) {
    const errorText = await response.text()

    throw new Error(
      errorText || `API request failed: ${response.status}`,
    )
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

export interface Task {
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

export interface CreateTaskInput {
  project_id: number
  repository_id?: number | null
  title: string
  description?: string | null
  priority?: string
  assigned_agent?: string | null
}

export async function getTasks(): Promise<Task[]> {
  return apiFetch<Task[]>("/tasks/")
}

export async function getTask(
  taskId: number,
): Promise<Task> {
  return apiFetch<Task>(`/tasks/${taskId}`)
}

export async function createTask(
  task: CreateTaskInput,
): Promise<Task> {
  return apiFetch<Task>("/tasks/", {
    method: "POST",
    body: JSON.stringify(task),
  })
}

export async function updateTask(
  taskId: number,
  updates: Partial<CreateTaskInput> & {
    status?: string
  },
): Promise<Task> {
  return apiFetch<Task>(`/tasks/${taskId}`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  })
}

export async function deleteTask(
  taskId: number,
): Promise<void> {
  return apiFetch<void>(`/tasks/${taskId}`, {
    method: "DELETE",
  })
}

export interface Repository {
  id: number
  project_id: number
  name: string
  repository_url: string
  default_branch: string
  local_path: string | null
  status: string
}

export async function getRepositories(): Promise<Repository[]> {
  return apiFetch<Repository[]>("/repositories/")
}

export interface Project {
  id: number
  name: string
  description: string | null
  repository_url: string | null
}

export async function getProjects(): Promise<Project[]> {
  return apiFetch<Project[]>("/projects/")
}