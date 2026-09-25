from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    repository_url: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    repository_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    repository_url: str | None = None