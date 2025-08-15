import re
from unittest.mock import patch

from langchain_community.llms import FakeListLLM

from dice_agent.agent import create_agent, is_prime


def test_is_prime_basic():
    assert is_prime.invoke("2")
    assert is_prime.invoke("3")
    assert not is_prime.invoke("4")
    assert not is_prime.invoke("1")


def test_agent_rolls_and_checks_prime():
    responses = [
        "Thought: I should roll the dice\nAction: roll_dice\nAction Input: \"\"",
        "Thought: I should check if the number is prime\nAction: is_prime\nAction Input: 3",
        "Thought: I now know the answer\nFinal Answer: The dice shows 3 and it is prime.",
    ]

    llm = FakeListLLM(responses=responses)
    with patch("dice_agent.agent.random.randint", return_value=3):
        agent = create_agent(llm)
        result = agent.run("Roll a dice and tell me if it's prime.")

    assert "3" in result
    assert re.search(r"prime", result, re.I)
