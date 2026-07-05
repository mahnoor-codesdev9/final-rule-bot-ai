# RuleBot AI Architecture

## Runtime Components

- `api.server` creates the FastAPI app, mounts static assets, configures CORS,
  and registers error handlers.
- `api.routes` exposes stable API endpoints for chat, history, analytics,
  settings, and health checks.
- `api.schemas` contains validated request and response models.
- `services.chat_service` coordinates rule matching, optional AI calls,
  persistent history, and statistics.
- `chatbot.matcher` performs deterministic rule matching with exact, synonym,
  intent, partial, and conservative fuzzy matching.
- `chatbot.knowledge_loader` validates and caches JSON knowledge files.
- `chatbot.session` manages persistent web history and terminal counters.
- `chatbot.statistics` tracks web analytics and terminal stats.
- `llm.router` selects Gemini, Groq, or OpenRouter when configured.
- `templates` and `static` provide the SaaS-style browser experience.

## Web Request Flow

```text
Browser
  -> FastAPI route
  -> ChatService
  -> Rule matcher or optional LLM router
  -> SessionManager
  -> Statistics
  -> JSON response
```

## Fallback Strategy

RuleBot always keeps the rule-based engine available. AI mode is optional:

1. If mode is `rule`, the matcher responds deterministically.
2. If mode is `auto`, RuleBot uses AI only when a provider is configured.
3. If mode is `ai` and the provider is unavailable or fails, RuleBot logs the
   issue and returns a rule response.

## Security Notes

- API keys are read from environment variables and never returned to clients.
- Validation errors return clean messages.
- Unexpected server errors are logged and hidden from API responses.
- Frontend markdown rendering escapes user content before formatting.
