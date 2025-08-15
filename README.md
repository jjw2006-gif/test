# LangChain Dice Agent

This repository demonstrates a simple [LangChain](https://github.com/hwchase17/langchain) agent that rolls a dice and checks whether the result is a prime number.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the agent:

```bash
python -m dice_agent.agent
```

The script uses `ChatOpenAI` by default. Set the `OPENAI_API_KEY` environment variable before running or pass your own LLM instance to `create_agent`.

## Tests

```bash
pytest
```
