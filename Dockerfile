FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /app

USER app

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD ["/bin/sh", "-c", "wget -qO- http://127.0.0.1:8000/health || exit 1"]

CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
