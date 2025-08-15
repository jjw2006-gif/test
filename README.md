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

### Streamlit UI

An interactive web interface is available using [Streamlit](https://streamlit.io/):

```bash
streamlit run src/dice_agent/streamlit_app.py
```

Click the button to roll a dice and the app will report whether the number is
prime.

## Deployment on Google Cloud VM

A helper script is included to spin up a small Compute Engine instance and
run the Streamlit application automatically.  Ensure the gcloud CLI is
installed and authenticated, then execute:

```bash
bash deploy/gcp_deploy.sh
```

Edit `deploy/gcp_deploy.sh` and `deploy/startup.sh` to supply your project ID,
preferred zone and the Git repository URL.  Once the VM starts the interface
will be accessible at `http://<EXTERNAL_IP>:8501`.

## Tests

```bash
pytest
```
