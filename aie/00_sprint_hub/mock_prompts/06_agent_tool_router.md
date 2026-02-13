# Agent Tool Router

Pattern: agents_tools
Difficulty: medium

Implement a tiny agent loop that can call tools from model output:

- Input: user question
- Model output format: `TOOL:<tool_name> ARGS:<json>`
- Available tools: `get_weather(city)`, `lookup_order(order_id)`

Requirements:

- Parse model action safely.
- Route to tool function.
- Feed observation back into the loop.
- Stop after max 3 iterations.

Interview follow-up:

- How do you prevent infinite loops and runaway cost?
- How would you evaluate tool-call accuracy?
