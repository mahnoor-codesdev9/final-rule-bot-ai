# RuleBot AI

RuleBot AI is a modern, production-quality, rule-first chatbot with optional AI
provider fallbacks. This repository demonstrates a clean FastAPI backend,
a modern web frontend, and pluggable AI providers (Gemini, Groq, OpenRouter).

**Highlights**

- Deterministic rule-based responses backed by JSON knowledge files
- Optional AI providers with safe fallbacks and non-blocking integration
- Rich frontend with markdown, code blocks, voice input/output, and exports
- FastAPI backend with structured error handling and centralized logging
- CI/CD: GitHub Actions for linting, testing, security auditing, and automated deployments
- Docker + docker-compose for local development
- Comprehensive test suite for backend APIs and chatbot logic

## Features

- Rule-first chat engine
- Intelligent AI fallback mechanism for robust responses
- AI `auto/ai/rule` modes and provider selection
- Conversation history persistence and export (TXT/JSON/PDF)
- Browser TTS/STT and voice controls
- Analytics endpoints for usage metrics

## Project Structure

```
rulebot-ai/
├── api/                 # FastAPI routes, schemas, and app setup
├── chatbot/             # Rule engine, CLI bot, sessions, stats, knowledge
├── core/                # Settings and logging helpers
├── docs/                # Architecture and structure notes
├── llm/                 # Optional AI provider clients and router
├── scripts/             # Utility scripts for knowledge base generation
├── services/            # Application service layer
├── static/              # Frontend CSS and JavaScript
├── templates/           # FastAPI Jinja templates
├── tests/               # Unit and API tests
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/   # CI pipeline
├── .env.example         # Example environment variables
└── requirements.txt
```

## Quickstart (development)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. Run the app locally:

```powershell
uvicorn api.server:app --reload
```

3. Open `http://localhost:8000` in your browser.

## Docker

Build and run the Docker image:

```powershell
docker build -t rulebot-ai .
docker run --env-file .env -p 8000:8000 rulebot-ai
```

For development with live-reload, use `docker-compose up`.

## API

- `GET /health` — health and version
- `GET /settings` — frontend-safe runtime settings
- `GET /history` — saved chat history
- `DELETE /history` — clear history
- `GET /stats` — session statistics
- `POST /chat` — send a chat message (request validated via Pydantic)

Example `POST /chat` request body:

```json
{
  "message": "Hello",
  "mode": "auto",
  "provider": null,
  "voice_output": false
}
```

Response:

```json
{
  "response": "...",
  "mode": "rule",
  "provider": null,
  "fallback": false
}
```

## Extending AI Providers

Environment variables control provider credentials. See `.env.example` for names:
- `GEMINI_API_KEY`
- `AI_REQUEST_TIMEOUT`
- `AI_RETRY_LIMIT`

If `GEMINI_API_KEY` is configured, RuleBot uses Google Gemini as the primary
AI provider when a rule-based answer is not available.

If no AI key is configured, the app will gracefully fall back to rule-based
responses and return a fallback message explaining that AI is unavailable.

## Tests & Linting

Run tests:

```powershell
pytest -q
```

Run lint/format checks:

```powershell
black --check .
flake8 . --exclude .venv
```

## Deployment

- CI is configured via `.github/workflows/ci.yml` to run tests, linters and
  `pip-audit`.
- The app can be deployed to Render, Railway, or any container platform.

## Roadmap

- UI/UX polish: premium glassmorphism, micro-interactions, accessibility
  improvements
- Async LLM clients (httpx) and streaming responses
- Server-side TTS and STT providers
- Role-based access and multi-user sessions

## License

This project is MIT-licensed. See the `LICENSE` file.
