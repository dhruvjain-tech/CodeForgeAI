from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    project_id: int
    repository_id: int | None = None
    title: str
    description: str | None = None
    priority: str = "medium"
    assigned_agent: str | None = None


class TaskResponse(BaseModel):
    id: int
    project_id: int
    repository_id: int | None = None
    repository_name: str | None = None
    title: str
    description: str | None = None
    priority: str
    status: str
    assigned_agent: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    status: str | None = None
    assigned_agent: str | None = None
    repository_id: int | None = None