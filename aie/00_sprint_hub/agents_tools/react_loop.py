"""
Minimal ReAct-style tool loop for interview practice.

This is intentionally lightweight and deterministic so you can focus on flow:
thought -> action -> observation -> answer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable, Dict


ToolFn = Callable[..., str]


@dataclass
class Action:
    name: str
    args: dict


def get_weather(city: str) -> str:
    weather = {"nyc": "7C cloudy", "sf": "16C sunny", "london": "5C rain"}
    return weather.get(city.lower(), f"unknown weather for {city}")


def lookup_order(order_id: str) -> str:
    orders = {"A100": "shipped", "A101": "processing", "A102": "delivered"}
    return orders.get(order_id, "order not found")


TOOLS: Dict[str, ToolFn] = {
    "get_weather": get_weather,
    "lookup_order": lookup_order,
}


def parse_action(model_output: str) -> Action | None:
    """
    Expected model output format:
    TOOL:<tool_name> ARGS:<json>
    """
    text = model_output.strip()
    if not text.startswith("TOOL:") or " ARGS:" not in text:
        return None

    tool_part, args_part = text.split(" ARGS:", 1)
    tool_name = tool_part.removeprefix("TOOL:").strip()
    if tool_name not in TOOLS:
        return None

    try:
        args = json.loads(args_part.strip())
    except json.JSONDecodeError:
        return None

    if not isinstance(args, dict):
        return None

    return Action(name=tool_name, args=args)


def mock_model(prompt: str) -> str:
    """
    Deterministic stand-in for an LLM so this file runs without API keys.
    """
    lower = prompt.lower()
    if "weather" in lower and "observation:" not in lower:
        return 'TOOL:get_weather ARGS:{"city":"NYC"}'
    if "order" in lower and "observation:" not in lower:
        return 'TOOL:lookup_order ARGS:{"order_id":"A100"}'
    return f"Final answer: {prompt.split('Observation:')[-1].strip()}"


def run_agent(user_query: str, max_steps: int = 3) -> str:
    """
    Simple agent loop with guardrails:
    - allowlisted tools only
    - strict action parsing
    - max step cap
    """
    context = user_query
    for _ in range(max_steps):
        model_output = mock_model(context)
        action = parse_action(model_output)
        if action is None:
            return model_output

        tool = TOOLS.get(action.name)
        if tool is None:
            return "Final answer: tool unavailable"

        try:
            observation = tool(**action.args)
        except Exception as exc:
            return f"Final answer: tool error: {exc}"

        context = f"{user_query}\nObservation: {observation}"

    return "Final answer: max iterations reached"


if __name__ == "__main__":
    samples = [
        "What is the weather in NYC?",
        "Can you check order A100?",
        "Say hello",
    ]
    for query in samples:
        print(f"\nQuery: {query}")
        print(run_agent(query))
