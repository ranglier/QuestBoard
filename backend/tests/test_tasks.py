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


def test_create_with_dates_and_status(client):
    res = client.post(
        "/tasks",
        json={
            "title": "Relancer NOC",
            "type": "followup",
            "status": "waiting",
            "followup_date": "2026-06-25",
            "planned_date": "2026-06-23",
        },
    )
    assert res.status_code == 201
    task = res.json()
    assert task["status"] == "waiting"
    assert task["followup_date"] == "2026-06-25"
    assert task["planned_date"] == "2026-06-23"


def test_patch_transitions_status_and_followup(client):
    tid = client.post("/tasks", json={"title": "Sujet"}).json()["id"]
    res = client.patch(
        f"/tasks/{tid}", json={"status": "waiting", "followup_date": "2026-06-30"}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "waiting"
    assert body["followup_date"] == "2026-06-30"


def test_patch_cannot_set_done(client):
    tid = client.post("/tasks", json={"title": "X"}).json()["id"]
    assert client.patch(f"/tasks/{tid}", json={"status": "done"}).status_code == 422


def test_patch_unknown_returns_404(client):
    assert client.patch("/tasks/9999", json={"status": "waiting"}).status_code == 404


def test_delete_task(client):
    tid = client.post("/tasks", json={"title": "À jeter", "status": "inbox"}).json()["id"]
    assert client.delete(f"/tasks/{tid}").status_code == 204
    assert client.delete(f"/tasks/{tid}").status_code == 404


def test_project_crud_and_detail(client):
    # création
    pid = client.post(
        "/projects", json={"name": "Audit mail", "domain": "Messagerie"}
    ).json()["id"]
    # liste (actifs)
    assert any(p["id"] == pid for p in client.get("/projects").json())
    # tâche liée au projet
    tid = client.post(
        "/tasks", json={"title": "Analyser flux", "project_id": pid}
    ).json()["id"]
    detail = client.get(f"/projects/{pid}").json()
    assert detail["name"] == "Audit mail"
    assert [t["id"] for t in detail["tasks"]] == [tid]
    # archivage -> disparaît de la liste active, visible avec include_archived
    client.patch(f"/projects/{pid}", json={"status": "archived"})
    assert all(p["id"] != pid for p in client.get("/projects").json())
    assert any(
        p["id"] == pid for p in client.get("/projects?include_archived=true").json()
    )


def test_transform_inbox_entry_to_task(client):
    # une entrée inbox = tâche au statut inbox ; la qualifier = PATCH
    tid = client.post("/tasks", json={"title": "Idée vrac", "status": "inbox"}).json()["id"]
    res = client.patch(f"/tasks/{tid}", json={"status": "todo", "priority": "high"})
    assert res.status_code == 200
    assert res.json()["status"] == "todo"
    assert res.json()["priority"] == "high"
