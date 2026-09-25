from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "codeforge-ai-api",
        "version": "0.1.0",
    }