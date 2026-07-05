# Project Structure

```text
rulebot-ai/
|-- .github/
|   `-- workflows/
|       `-- python.yml
|-- api/
|   |-- __init__.py
|   |-- routes.py
|   |-- schemas.py
|   `-- server.py
|-- chatbot/
|   |-- data/
|   |-- knowledge/
|   |-- logs/
|   |-- bot.py
|   |-- commands.py
|   |-- config.py
|   |-- formatter.py
|   |-- history.py
|   |-- knowledge_loader.py
|   |-- logger.py
|   |-- matcher.py
|   |-- session.py
|   |-- statistics.py
|   `-- utils.py
|-- core/
|   |-- __init__.py
|   |-- logging.py
|   `-- settings.py
|-- docs/
|   |-- architecture.md
|   `-- project_structure.md
|-- llm/
|   |-- base.py
|   |-- gemini_client.py
|   |-- groq_client.py
|   |-- openrouter_client.py
|   `-- router.py
|-- services/
|   `-- chat_service.py
|-- static/
|   |-- css/
|   |   `-- style.css
|   `-- js/
|       |-- app.js
|       `-- theme.js
|-- templates/
|   `-- index.html
|-- tests/
|-- .env.example
|-- Dockerfile
|-- README.md
|-- render.yaml
|-- railway.json
`-- requirements.txt
```
