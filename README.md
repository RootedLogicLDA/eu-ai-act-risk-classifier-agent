# EU AI Act Classifier Demo

A LangGraph + FastAPI classifier that categorizes software products under the EU AI Act, with Promptfoo shim integration for automated evaluation.

## Architecture

```
FastAPI endpoint (/classify)
       │
       ▼
LangGraph StateGraph
  START → classify (LLM call) → conditional routing → handler → END
                                   │
                            prohibited / high_risk / limited_risk / minimal_risk

Promptfoo shim (promptfoo_shim.py)
  call_api(prompt) → graph.invoke() → {"output": json_result}
```

## Setup

```bash
uv sync
echo "OPENAI_API_KEY=sk-..." > .env
```

## Run the API

```bash
uv run uvicorn app:app --port 8000
```

Test it:
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"product_name": "MailGuard", "description": "AI spam filter"}'
```

## Run Promptfoo Evaluation

```bash
export $(cat .env | xargs)
npx promptfoo@latest eval
npx promptfoo view  # open browser results UI
```

## EU AI Act Risk Categories

| Category | Examples |
|----------|---------|
| `prohibited` | Social scoring, real-time biometric surveillance, subliminal manipulation |
| `high_risk` | CV screening, medical diagnosis, law enforcement tools, credit scoring |
| `limited_risk` | Chatbots, deepfake generators, emotion recognition |
| `minimal_risk` | Spam filters, game AI, recommendation systems |
