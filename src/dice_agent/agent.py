"""Agent that rolls a dice and checks if the number is prime.

This module exposes two LangChain :class:`~langchain.tools.Tool` objects:

``roll_dice``
    Simulates a six‑sided dice roll.

``is_prime``
    Performs a very small primality test.

The :func:`create_agent` helper wires those tools into a minimal
zero‑shot agent that can be driven from the command line or other
interfaces.
"""

from __future__ import annotations

import random
from typing import Any

from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool

try:  # pragma: no cover - optional dependency
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover - optional dependency
    ChatOpenAI = None


def _roll(_: str) -> int:
    """Return a random number between 1 and 6.

    The tool callback signature expects a single string argument.  The value
    passed by LangChain is ignored so we accept it as ``_`` and simply return
    a random integer.
    """

    # ``randint`` includes both end points, giving us numbers 1 through 6.
    return random.randint(1, 6)


roll_dice = Tool(
    name="roll_dice",
    func=_roll,
    description="Roll a six-sided dice and return the result.",
)


def _is_prime(n: str) -> bool:
    """Return ``True`` if ``n`` is a prime number.

    The implementation uses a basic trial-division algorithm which is more
    than adequate for the very small numbers produced by a dice roll.
    """

    num = int(n)
    if num < 2:
        return False

    # Try dividing ``num`` by every integer up to its square root.  If any
    # division is exact, the number is not prime.
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


is_prime = Tool(
    name="is_prime",
    func=_is_prime,
    description="Return True if a number is prime.",
)


def create_agent(llm: Any | None = None):
    """Create a LangChain agent that can roll a dice and check primality.

    Parameters
    ----------
    llm
        Optional language model instance.  If omitted, the function tries to
        construct a :class:`ChatOpenAI` model.  The optional import above keeps
        this module usable in environments where ``langchain-openai`` is not
        installed.
    """

    if llm is None:
        if ChatOpenAI is None:  # pragma: no cover - handled in tests
            raise RuntimeError(
                "ChatOpenAI is not available. Install langchain-openai or provide an LLM."
            )
        llm = ChatOpenAI(temperature=0)

    tools = [roll_dice, is_prime]
    return initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )


def main() -> None:  # pragma: no cover - simple CLI
    """Run a demo interaction on the command line."""

    agent = create_agent()
    result = agent.run("Roll a dice and tell me if it's prime.")
    print(result)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
