from dataclasses import dataclass


@dataclass
class LLMCost:
    input_cost: float = 0.0
    output_cost: float = 0.0
    total_cost: float = 0.0


def estimate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    input_price_per_million: float = 0.0,
    output_price_per_million: float = 0.0,
) -> LLMCost:

    input_cost = (
        prompt_tokens / 1_000_000
    ) * input_price_per_million

    output_cost = (
        completion_tokens / 1_000_000
    ) * output_price_per_million

    return LLMCost(
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=input_cost + output_cost,
    )