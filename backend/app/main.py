from fastapi import FastAPI

app = FastAPI(title="QuestBoard API", version="0.1.0")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "QuestBoard API", "status": "ok"}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
