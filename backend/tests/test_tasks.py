"""Tests de la boucle V0 : créer → terminer → calculer XP/or."""


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_defaults_difficulty_from_type(client):
    res = client.post("/tasks", json={"title": "Rédiger note", "type": "documentation"})
    assert res.status_code == 201
    task = res.json()
    # documentation -> difficulté "normal" (cf. scoring)
    assert task["difficulty"] == "normal"
    assert task["priority"] == "normal"
    assert task["status"] == "todo"
    assert task["xp_reward"] == 0


def test_create_with_explicit_difficulty(client):
    res = client.post(
        "/tasks",
        json={"title": "Gros projet", "type": "documentation", "difficulty": "complex"},
    )
    assert res.json()["difficulty"] == "complex"


def test_complete_computes_xp_and_gold(client):
    tid = client.post(
        "/tasks", json={"title": "Incident", "type": "incident", "priority": "critical"}
    ).json()["id"]

    res = client.post(f"/tasks/{tid}/complete")
    assert res.status_code == 200
    body = res.json()
    # incident -> difficulté "hard" -> 50 XP ; priorité "critical" -> 35 or
    assert body["xp_gained"] == 50
    assert body["gold_gained"] == 35
    assert body["task"]["status"] == "done"
    assert body["task"]["xp_reward"] == 50
    assert body["task"]["completed_at"] is not None


def test_complete_twice_returns_conflict(client):
    tid = client.post("/tasks", json={"title": "Une fois"}).json()["id"]
    assert client.post(f"/tasks/{tid}/complete").status_code == 200
    assert client.post(f"/tasks/{tid}/complete").status_code == 409


def test_complete_unknown_returns_404(client):
    assert client.post("/tasks/9999/complete").status_code == 404


def test_stats_aggregate_completed_tasks(client):
    a = client.post(
        "/tasks", json={"title": "A", "type": "documentation", "priority": "high"}
    ).json()["id"]
    client.post("/tasks", json={"title": "B", "type": "script", "priority": "low"})  # non terminée
    client.post(f"/tasks/{a}/complete")

    stats = client.get("/stats").json()
    # seule A est terminée : doc -> 25 XP, high -> 15 or
    assert stats == {"total_xp": 25, "total_gold": 15, "completed_tasks": 1}
