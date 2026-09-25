from pydantic import BaseModel, ConfigDict


class RepositoryCreate(BaseModel):
    project_id: int
    name: str
    repository_url: str
    default_branch: str = "main"
    local_path: str | None = None


class RepositoryResponse(BaseModel):
    id: int
    project_id: int
    name: str
    repository_url: str
    default_branch: str
    local_path: str | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class RepositoryUpdate(BaseModel):
    name: str | None = None
    repository_url: str | None = None
    default_branch: str | None = None
    local_path: str | None = None
    status: str | None = None