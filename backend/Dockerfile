FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Autorités racine locales (proxy d'entreprise qui intercepte TLS). Le dossier
# certs/ existe toujours (.gitkeep) ; les .crt sont fournis par machine et NON
# versionnés. S'ils sont absents, cette étape est neutre (PyPI public direct).
COPY certs/ /certs/

COPY pyproject.toml ./
COPY app ./app
RUN if ls /certs/*.crt >/dev/null 2>&1; then \
        cat /certs/*.crt >> /etc/ssl/certs/ca-certificates.crt && \
        export PIP_CERT=/etc/ssl/certs/ca-certificates.crt; \
    fi; \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
