# Workflow Audit Agent

Minimal Python scaffold for a LangGraph-based workflow audit agent.

## Files

- `app.py`: Runs the sample workflow audit.
- `main.py`: CLI entry point.
- `graph.py`: LangGraph workflow definition.
- `models.py`: Typed state and result models.
- `prompts.py`: Prompt templates and system guidance.
- `sample_inputs.py`: Example workflow input payload.
- `tests/`: Basic graph test.
- `outputs/`: Reserved for generated audit artifacts.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
pytest
```

## Next Steps

- Replace the rule-based summary logic with an LLM-backed node.
- Add persistence for audit outputs under `outputs/`.
- Expand tests around severity and recommendation logic.
