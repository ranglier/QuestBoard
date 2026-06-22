<script lang="ts">
  import { onMount } from 'svelte';
  import {
    createProject,
    createTask,
    deleteTask,
    listTasks,
    updateTask,
    type Task
  } from '$lib/api';

  let entries = $state<Task[]>([]);
  let error = $state<string | null>(null);
  let title = $state('');

  async function refresh() {
    try {
      entries = (await listTasks()).filter((t) => t.status === 'inbox');
      error = null;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function run(action: Promise<unknown>) {
    try {
      await action;
      await refresh();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function onCapture(event: SubmitEvent) {
    event.preventDefault();
    if (!title.trim()) return;
    await run(createTask({ title: title.trim(), status: 'inbox' }));
    title = '';
  }

  const toTask = (t: Task) => run(updateTask(t.id, { status: 'todo' }));
  const discard = (t: Task) => run(deleteTask(t.id));
  const toProject = (t: Task) =>
    run(createProject({ name: t.title }).then(() => deleteTask(t.id)));
</script>

<svelte:head><title>QuestBoard — Inbox</title></svelte:head>

<main class="shell">
  <header>
    <p class="eyebrow">Capturer sans réfléchir, qualifier plus tard</p>
    <h1>Inbox</h1>
  </header>

  {#if error}<p class="error">Erreur API : {error}</p>{/if}

  <form class="card" onsubmit={onCapture}>
    <input bind:value={title} placeholder="Note libre, sujet, idée…" required />
    <button type="submit">Capturer</button>
  </form>

  <section class="section">
    <h2>Entrées <span class="count">{entries.length}</span></h2>
    {#if entries.length === 0}<p class="empty">Inbox vide. 🎉</p>{/if}
    <ul class="list">
      {#each entries as t (t.id)}
        <li>
          <span class="title">{t.title}</span>
          <div class="actions">
            <button onclick={() => toTask(t)}>→ Tâche</button>
            <button class="ghost" onclick={() => toProject(t)}>→ Projet</button>
            <button class="ghost danger" onclick={() => discard(t)}>Supprimer</button>
          </div>
        </li>
      {/each}
    </ul>
  </section>
</main>

<style>
  .shell {
    max-width: 820px;
    margin: 0 auto;
    padding: 32px;
  }
  .eyebrow {
    margin: 0 0 4px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 12px;
  }
  h1 {
    margin: 0;
  }
  h2 {
    font-size: 15px;
    color: #334155;
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .count {
    background: #e2e8f0;
    color: #475569;
    border-radius: 999px;
    font-size: 12px;
    padding: 1px 8px;
  }
  .card {
    display: flex;
    gap: 8px;
    margin: 20px 0;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 14px;
  }
  input {
    flex: 1;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 8px 10px;
    font: inherit;
  }
  .section {
    margin-top: 16px;
  }
  .list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .list li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 12px;
  }
  .title {
    font-weight: 500;
  }
  .actions {
    display: flex;
    gap: 6px;
    flex-shrink: 0;
  }
  button {
    border: 1px solid #334155;
    background: #334155;
    color: white;
    border-radius: 9px;
    padding: 7px 12px;
    cursor: pointer;
    font: inherit;
    font-size: 13px;
  }
  button.ghost {
    background: white;
    color: #334155;
    border-color: #cbd5e1;
  }
  button.danger {
    color: #b91c1c;
    border-color: #fca5a5;
  }
  .error {
    background: #fee2e2;
    border: 1px solid #fca5a5;
    color: #991b1b;
    padding: 10px 14px;
    border-radius: 10px;
  }
  .empty {
    color: #94a3b8;
  }
</style>
