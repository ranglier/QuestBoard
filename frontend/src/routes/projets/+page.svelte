<script lang="ts">
  import {
    createProject,
    listProjects,
    listTasks,
    updateProject,
    type Project,
    type Task
  } from '$lib/api';

  const STATUS_LABEL: Record<string, string> = {
    inbox: 'Inbox',
    todo: 'À faire',
    in_progress: 'En cours',
    waiting: 'En attente',
    planned: 'Planifié',
    done: 'Terminé',
    abandoned: 'Abandonné'
  };

  let projects = $state<Project[]>([]);
  let tasks = $state<Task[]>([]);
  let error = $state<string | null>(null);
  let includeArchived = $state(false);
  let domainFilter = $state('');
  let expanded = $state<number | null>(null);

  let name = $state('');
  let domain = $state('');

  const domains = $derived([...new Set(projects.map((p) => p.domain).filter(Boolean))].sort());
  const visible = $derived(
    domainFilter ? projects.filter((p) => p.domain === domainFilter) : projects
  );
  const tasksOf = (pid: number) => tasks.filter((t) => t.project_id === pid);
  const openCount = (pid: number) =>
    tasksOf(pid).filter((t) => t.status !== 'done' && t.status !== 'abandoned').length;

  async function refresh() {
    try {
      [projects, tasks] = await Promise.all([listProjects(includeArchived), listTasks()]);
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

  async function onCreate(event: SubmitEvent) {
    event.preventDefault();
    if (!name.trim()) return;
    await run(createProject({ name: name.trim(), domain: domain.trim() }));
    name = '';
    domain = '';
  }

  const archive = (p: Project) => run(updateProject(p.id, { status: 'archived' }));
  const reactivate = (p: Project) => run(updateProject(p.id, { status: 'active' }));
  const toggle = (id: number) => (expanded = expanded === id ? null : id);

  $effect(() => {
    includeArchived;
    refresh();
  });
</script>

<svelte:head><title>QuestBoard — Projets</title></svelte:head>

<main class="shell">
  <header>
    <p class="eyebrow">Regroupements de travail par domaine</p>
    <h1>Projets</h1>
  </header>

  {#if error}<p class="error">Erreur API : {error}</p>{/if}

  <form class="card" onsubmit={onCreate}>
    <input bind:value={name} placeholder="Nom du projet…" required />
    <input bind:value={domain} placeholder="Domaine (optionnel)" list="domains" />
    <datalist id="domains">
      {#each domains as d}<option value={d}></option>{/each}
    </datalist>
    <button type="submit">Créer</button>
  </form>

  <div class="filters">
    <label>
      Domaine :
      <select bind:value={domainFilter}>
        <option value="">Tous</option>
        {#each domains as d}<option value={d}>{d}</option>{/each}
      </select>
    </label>
    <label class="check">
      <input type="checkbox" bind:checked={includeArchived} /> Inclure archivés
    </label>
  </div>

  <section class="section">
    {#if visible.length === 0}<p class="empty">Aucun projet.</p>{/if}
    <ul class="list">
      {#each visible as p (p.id)}
        <li class:archived={p.status === 'archived'}>
          <div class="row">
            <button class="name" onclick={() => toggle(p.id)}>
              {expanded === p.id ? '▾' : '▸'} {p.name}
            </button>
            <div class="meta">
              {#if p.domain}<span class="badge">{p.domain}</span>{/if}
              <span class="muted">{openCount(p.id)} ouverte(s) / {tasksOf(p.id).length}</span>
              {#if p.status === 'archived'}
                <button class="ghost" onclick={() => reactivate(p)}>Réactiver</button>
              {:else}
                <button class="ghost" onclick={() => archive(p)}>Archiver</button>
              {/if}
            </div>
          </div>
          {#if expanded === p.id}
            <ul class="tasks">
              {#each tasksOf(p.id) as t (t.id)}
                <li><span class="st">{STATUS_LABEL[t.status]}</span> {t.title}</li>
              {:else}
                <li class="empty">Aucune tâche liée.</li>
              {/each}
            </ul>
          {/if}
        </li>
      {/each}
    </ul>
  </section>
</main>

<style>
  .shell {
    max-width: 900px;
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
  .card {
    display: flex;
    gap: 8px;
    margin: 20px 0 12px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 14px;
    flex-wrap: wrap;
  }
  input {
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 8px 10px;
    font: inherit;
  }
  .card input:first-of-type {
    flex: 1;
    min-width: 200px;
  }
  .filters {
    display: flex;
    gap: 16px;
    align-items: center;
    margin-bottom: 12px;
    font-size: 13px;
    color: #475569;
  }
  select {
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 6px 8px;
    font: inherit;
  }
  .check {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .list > li {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 12px;
  }
  .list > li.archived {
    opacity: 0.6;
  }
  .row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
  .name {
    border: none;
    background: none;
    font: inherit;
    font-weight: 600;
    cursor: pointer;
    padding: 0;
    color: #1f2933;
  }
  .meta {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .muted {
    color: #94a3b8;
    font-size: 12px;
  }
  .badge {
    font-size: 11px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 2px 6px;
    color: #475569;
  }
  .tasks {
    list-style: none;
    margin: 10px 0 0;
    padding: 8px 0 0;
    border-top: 1px dashed #e2e8f0;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 14px;
  }
  .tasks .st {
    display: inline-block;
    min-width: 84px;
    color: #64748b;
    font-size: 12px;
  }
  button:not(.name) {
    border: 1px solid #cbd5e1;
    background: white;
    color: #334155;
    border-radius: 9px;
    padding: 6px 11px;
    cursor: pointer;
    font: inherit;
    font-size: 13px;
  }
  form button {
    background: #334155;
    color: white;
    border-color: #334155;
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
