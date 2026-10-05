from .context import RepositoryContext
from .technology_advisor import (
    TechnologyAdvisor,
    TechnologyOption,
    TechnologyRecommendation,
)
from .technology_decision import WorkloadProfile


class RepositoryTechnologyAdvisor:

    def __init__(self):
        self.advisor = TechnologyAdvisor()

    def recommend(
        self,
        context: RepositoryContext,
        category: str,
        workload: str,
        requirements: list[str] | None = None,
        options: list[TechnologyOption] | None = None,
        workload_profile: WorkloadProfile | None = None,
    ) -> TechnologyRecommendation:

        requirements = requirements or []
        options = options or []

        repository_requirements = (
            self._derive_requirements(context)
        )

        combined_requirements = list(
            dict.fromkeys(
                requirements
                + repository_requirements
            )
        )

        if workload_profile is None:
            workload_profile = (
                self._derive_workload_profile(
                    context,
                    workload,
                )
            )

        return self.advisor.recommend(
            category=category,
            workload=workload,
            requirements=combined_requirements,
            options=options,
            workload_profile=workload_profile,
        )

    def _derive_requirements(
        self,
        context: RepositoryContext,
    ) -> list[str]:

        requirements: list[str] = []

        languages = {
            file.language.lower()
            for file in context.files
            if file.language
        }

        language_requirements = {
            "python": "python",
            "typescript": "typescript",
            "javascript": "javascript",
            "java": "java",
            "c++": "c++",
            "go": "go",
            "rust": "rust",
        }

        for language, requirement in (
            language_requirements.items()
        ):
            if language in languages:
                requirements.append(
                    requirement
                )

        dependency_targets = {
            dependency.target.lower()
            for dependency in context.dependencies
            if dependency.target
        }

        technology_keywords = {
            "postgresql": "postgresql",
            "mysql": "mysql",
            "sqlite": "sqlite",
            "redis": "redis",
            "mongodb": "mongodb",
            "fastapi": "fastapi",
            "django": "django",
            "flask": "flask",
            "react": "react",
            "next": "next.js",
        }

        for keyword, requirement in (
            technology_keywords.items()
        ):
            if any(
                keyword in target
                for target in dependency_targets
            ):
                requirements.append(
                    requirement
                )

        if context.dependencies:
            requirements.append(
                "dependency management"
            )

        if context.symbols:
            requirements.append(
                "code structure"
            )

        return list(
            dict.fromkeys(requirements)
        )

    def _derive_workload_profile(
        self,
        context: RepositoryContext,
        workload: str,
    ) -> WorkloadProfile:

        text = workload.lower()

        file_count = len(context.files)
        symbol_count = len(context.symbols)
        dependency_count = len(
            context.dependencies
        )

        return WorkloadProfile(
            cpu_intensive=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "cpu",
                        "compute",
                        "computation",
                    ]
                )
                else 0.0
            ),
            memory_intensive=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "memory",
                        "ram",
                        "in-memory",
                    ]
                )
                else 0.0
            ),
            io_intensive=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "io",
                        "disk",
                        "storage",
                        "database",
                    ]
                )
                else 0.0
            ),
            concurrency=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "concurrency",
                        "concurrent",
                        "parallel",
                        "high traffic",
                    ]
                )
                else min(
                    1.0,
                    file_count / 1000,
                )
            ),
            latency_sensitive=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "latency",
                        "low latency",
                        "real time",
                        "realtime",
                        "fast",
                    ]
                )
                else 0.0
            ),
        )


repository_technology_advisor = (
    RepositoryTechnologyAdvisor()
)