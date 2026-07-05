# Frontend (React + Vite)

This folder contains an optional React + Vite scaffold to re-implement the chat UI as a modern single-page app.


Getting started (frontend only):

```bash
cd frontend
npm install
npm run dev
```

To run both backend and frontend during development (recommended):

1. Start the backend (from repository root):

```bash
"c:/Users/My PC/Desktop/rule based agent/.venv/Scripts/python.exe" -m uvicorn api.server:app --reload --port 8000
```

2. Start the frontend in a separate shell:

```bash
cd frontend
npm run dev
```

The React app proxies requests to the same host by default (`/chat`, `/history`, `/settings`). Configure a dev proxy in Vite if you need a different backend port.

Build for production:

```bash
npm run build
npm run preview
```

This scaffold is a starting point to migrate the current server-rendered `templates/index.html` into a client-side app. It implements the core chat flow and mirrors existing backend endpoints.
