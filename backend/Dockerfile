# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app

# Build-time only : si un secret CA "proxy_ca" est fourni (proxy d'entreprise qui
# intercepte TLS), pip l'utilise pour valider PyPI. Le secret n'est PAS persiste
# dans l'image. Sans secret (cas par defaut), build PyPI public normal.
# Activation locale : voir compose.override.example.yaml.
RUN --mount=type=secret,id=proxy_ca \
    if [ -s /run/secrets/proxy_ca ]; then export PIP_CERT=/run/secrets/proxy_ca; fi; \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
