from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.repository.context import RepositoryContext
from core.repository.service import RepositoryAnalysisService
from core.repository.technology_advisor import (
    TechnologyAdvisor,
    TechnologyOption,
    TechnologyRecommendation,
)
from core.repository.technology_decision import WorkloadProfile
from core.repository.technology_integration import (
    RepositoryTechnologyAdvisor,
)


router = APIRouter(
    prefix="/technology-advisor",
    tags=["Technology Advisor"],
)


class TechnologyOptionRequest(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)


class TechnologyRecommendationRequest(BaseModel):
    category: str = Field(..., min_length=1)
    workload: str = Field(..., min_length=1)
    requirements: list[str] = Field(default_factory=list)
    options: list[TechnologyOptionRequest] = Field(
        ...,
        min_length=1,
    )


class TechnologyExplainRequest(BaseModel):
    category: str = Field(..., min_length=1)
    recommendation: str = Field(..., min_length=1)
    alternatives: list[str] = Field(default_factory=list)
    reasoning: list[str] = Field(default_factory=list)


class TechnologyDecisionRequest(BaseModel):
    category: str = Field(..., min_length=1)
    workload: str = Field(..., min_length=1)
    requirements: list[str] = Field(default_factory=list)
    options: list[TechnologyOptionRequest] = Field(
        ...,
        min_length=1,
    )

    cpu_intensive: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    memory_intensive: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    io_intensive: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    concurrency: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    latency_sensitive: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


class RepositoryTechnologyRecommendationRequest(BaseModel):
    root_path: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    workload: str = Field(..., min_length=1)
    requirements: list[str] = Field(default_factory=list)
    options: list[TechnologyOptionRequest] = Field(
        ...,
        min_length=1,
    )


def build_options(
    options: list[TechnologyOptionRequest],
) -> list[TechnologyOption]:

    return [
        TechnologyOption(
            name=option.name,
            category=option.category,
            strengths=option.strengths,
            weaknesses=option.weaknesses,
        )
        for option in options
    ]


@router.post("/recommend")
def recommend_technology(
    request: TechnologyRecommendationRequest,
) -> dict[str, Any]:

    advisor = TechnologyAdvisor()

    recommendation = advisor.recommend(
        category=request.category,
        workload=request.workload,
        requirements=request.requirements,
        options=build_options(request.options),
    )

    return {
        "category": recommendation.category,
        "recommendation": recommendation.recommendation,
        "alternatives": recommendation.alternatives,
        "reasoning": recommendation.reasoning,
    }


@router.post("/compare")
def compare_technologies(
    request: TechnologyRecommendationRequest,
) -> dict[str, Any]:

    advisor = TechnologyAdvisor()

    results = advisor.compare(
        category=request.category,
        workload=request.workload,
        requirements=request.requirements,
        options=build_options(request.options),
    )

    if not results:
        raise HTTPException(
            status_code=400,
            detail="No technology options provided",
        )

    return {
        "category": request.category,
        "workload": request.workload,
        "results": results,
    }


@router.post("/explain")
def explain_recommendation(
    request: TechnologyExplainRequest,
) -> dict[str, Any]:

    advisor = TechnologyAdvisor()

    recommendation = TechnologyRecommendation(
        category=request.category,
        recommendation=request.recommendation,
        alternatives=request.alternatives,
        reasoning=request.reasoning,
    )

    explanation = advisor.explain(
        recommendation
    )

    return {
        "category": recommendation.category,
        "recommendation": recommendation.recommendation,
        "explanation": explanation,
    }


@router.post("/decision")
def technology_decision(
    request: TechnologyDecisionRequest,
) -> dict[str, Any]:

    advisor = TechnologyAdvisor()

    workload_profile = WorkloadProfile(
        cpu_intensive=request.cpu_intensive,
        memory_intensive=request.memory_intensive,
        io_intensive=request.io_intensive,
        concurrency=request.concurrency,
        latency_sensitive=request.latency_sensitive,
    )

    results = advisor.compare(
        category=request.category,
        workload=request.workload,
        requirements=request.requirements,
        options=build_options(request.options),
        workload_profile=workload_profile,
    )

    if not results:
        raise HTTPException(
            status_code=400,
            detail="No technology options provided",
        )

    return {
        "category": request.category,
        "workload": request.workload,
        "workload_profile": {
            "cpu_intensive": workload_profile.cpu_intensive,
            "memory_intensive": workload_profile.memory_intensive,
            "io_intensive": workload_profile.io_intensive,
            "concurrency": workload_profile.concurrency,
            "latency_sensitive": workload_profile.latency_sensitive,
        },
        "recommended": results[0],
        "rankings": results,
    }


@router.post("/repository-recommend")
def recommend_for_repository(
    request: RepositoryTechnologyRecommendationRequest,
) -> dict[str, Any]:

    analysis_service = RepositoryAnalysisService()

    try:
        analysis = analysis_service.analyze(
            request.root_path
        )
    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    context = RepositoryContext.from_analysis(
        analysis
    )

    advisor = RepositoryTechnologyAdvisor()

    recommendation = advisor.recommend(
        context=context,
        category=request.category,
        workload=request.workload,
        requirements=request.requirements,
        options=build_options(request.options),
    )

    return {
        "root_path": request.root_path,
        "category": recommendation.category,
        "recommendation": recommendation.recommendation,
        "alternatives": recommendation.alternatives,
        "reasoning": recommendation.reasoning,
        "repository": {
            "file_count": len(context.files),
            "symbol_count": len(context.symbols),
            "dependency_count": len(context.dependencies),
            "location_count": len(context.locations),
        },
    }

@router.post("/repository-decision")
def repository_technology_decision(
    request: RepositoryTechnologyRecommendationRequest,
) -> dict[str, Any]:

    analysis_service = RepositoryAnalysisService()

    try:
        analysis = analysis_service.analyze(
            request.root_path
        )
    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    context = RepositoryContext.from_analysis(
        analysis
    )

    advisor = RepositoryTechnologyAdvisor()

    recommendation = advisor.recommend(
        context=context,
        category=request.category,
        workload=request.workload,
        requirements=request.requirements,
        options=build_options(
            request.options
        ),
    )

    return {
        "root_path": request.root_path,
        "category": recommendation.category,
        "recommendation": recommendation.recommendation,
        "alternatives": recommendation.alternatives,
        "reasoning": recommendation.reasoning,
        "repository": {
            "file_count": len(context.files),
            "symbol_count": len(context.symbols),
            "dependency_count": len(context.dependencies),
            "location_count": len(context.locations),
        },
    }