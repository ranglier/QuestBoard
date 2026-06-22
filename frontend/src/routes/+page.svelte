<script lang="ts">
  import { onMount } from 'svelte';
  import {
    completeTask,
    createTask,
    getStats,
    listTasks,
    type Stats,
    type Task,
    type TaskPriority,
    type TaskType
  } from '$lib/api';

  const TYPES: { value: TaskType; label: string }[] = [
    { value: 'exploitation', label: 'Exploitation' },
    { value: 'incident', label: 'Incident' },
    { value: 'interruption', label: 'Interruption / imprévu' },
    { value: 'project', label: 'Projet' },
    { value: 'audit', label: 'Audit' },
    { value: 'documentation', label: 'Documentation' },
    { value: 'script', label: 'Script / automatisation' },
    { value: 'communication', label: 'Communication' },
    { value: 'meeting', label: 'Réunion' },
    { value: 'analysis', label: 'Analyse' },
    { value: 'followup', label: 'Suivi / relance' },
    { value: 'watch', label: 'Veille' },
    { value: 'improvement', label: 'Amélioration continue' },
    { value: 'change', label: 'MEO / changement' },
    { value: 'user_ticket', label: 'Ticket utilisateur' }
  ];

  const PRIORITIES: { value: TaskPriority; label: string }[] = [
    { value: 'low', label: 'Basse' },
    { value: 'normal', label: 'Normale' },
    { value: 'high', label: 'Haute' },
    { value: 'critical', label: 'Critique' }
  ];

  const PRIORITY_LABEL = Object.fromEntries(PRIORITIES.map((p) => [p.value, p.label]));
  const TYPE_LABEL = Object.fromEntries(TYPES.map((t) => [t.value, t.label]));

  let tasks = $state<Task[]>([]);
  let stats = $state<Stats>({ total_xp: 0, total_gold: 0, completed_tasks: 0 });
  let error = $state<string | null>(null);
  let lastReward = $state<{ xp: number; gold: number } | null>(null);

  let title = $state('');
  let type = $state<TaskType>('exploitation');
  let priority = $state<TaskPriority>('normal');

  const openTasks = $derived(tasks.filter((t) => t.status !== 'done'));
  const doneTasks = $derived(tasks.filter((t) => t.status === 'done'));

  async function refresh() {
    try {
      [tasks, stats] = await Promise.all([listTasks(), getStats()]);
      error = null;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function onCreate(event: SubmitEvent) {
    event.preventDefault();
    if (!title.trim()) return;
    try {
      await createTask({ title: title.trim(), type, priority });
      title = '';
      await refresh();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function onComplete(id: number) {
    try {
      const result = await completeTask(id);
      lastReward = { xp: result.xp_gained, gold: result.gold_gained };
      await refresh();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  onMount(refresh);
</script>

<svelte:head>
  <title>QuestBoard — V0</title>
</svelte:head>

<main class="shell">
  <header class="header">
    <div>
      <p class="eyebrow">Outil de travail local-first</p>
      <h1>QuestBoard</h1>
    </div>
    <div class="resources">
      <span class="chip">XP&nbsp;: <strong>{stats.total_xp}</strong></span>
      <span class="chip">Or&nbsp;: <strong>{stats.total_gold}</strong></span>
      <span class="chip muted">Terminées&nbsp;: {stats.completed_tasks}</span>
    </div>
  </header>

  {#if error}
    <p class="error">Erreur API : {error}</p>
  {/if}

  {#if lastReward}
    <p class="reward">
      Tâche terminée — +{lastReward.xp} XP, +{lastReward.gold} or.
    </p>
  {/if}

  <section class="grid">
    <article class="card">
      <h2>Capture rapide</h2>
      <form onsubmit={onCreate}>
        <label>
          Titre
          <input bind:value={title} placeholder="Ex. Relancer NOC port 2701" required />
        </label>
        <div class="row">
          <label>
            Type
            <select bind:value={type}>
              {#each TYPES as t}
                <option value={t.value}>{t.label}</option>
              {/each}
            </select>
          </label>
          <label>
            Priorité
            <select bind:value={priority}>
              {#each PRIORITIES as p}
                <option value={p.value}>{p.label}</option>
              {/each}
            </select>
          </label>
        </div>
        <button type="submit">Créer la tâche</button>
        <p class="hint">La difficulté (donc l'XP) est déduite du type, modifiable plus tard.</p>
      </form>
    </article>

    <article class="card wide">
      <h2>À faire ({openTasks.length})</h2>
      {#if openTasks.length === 0}
        <p class="empty">Aucune tâche en cours. Capture ta première tâche.</p>
      {:else}
        <ul class="tasks">
          {#each openTasks as task (task.id)}
            <li>
              <div>
                <span class="badge badge-{task.priority}">{PRIORITY_LABEL[task.priority]}</span>
                <span class="badge">{TYPE_LABEL[task.type]}</span>
                <span class="title">{task.title}</span>
              </div>
              <button class="ghost" onclick={() => onComplete(task.id)}>Terminer</button>
            </li>
          {/each}
        </ul>
      {/if}

      {#if doneTasks.length > 0}
        <h3>Terminées</h3>
        <ul class="tasks done">
          {#each doneTasks as task (task.id)}
            <li>
              <div>
                <span class="title">{task.title}</span>
              </div>
              <span class="xp">+{task.xp_reward} XP</span>
            </li>
          {/each}
        </ul>
      {/if}
    </article>
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif;
    background: #f6f4ef;
    color: #1f2933;
  }

  .shell {
    max-width: 1120px;
    margin: 0 auto;
    padding: 32px;
  }

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
  }

  .eyebrow {
    margin: 0 0 4px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 12px;
  }

  h1,
  h2,
  h3 {
    margin: 0;
  }

  .resources {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .chip {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 999px;
    padding: 6px 14px;
    font-size: 14px;
  }

  .chip.muted {
    color: #64748b;
  }

  .error {
    background: #fee2e2;
    border: 1px solid #fca5a5;
    color: #991b1b;
    padding: 10px 14px;
    border-radius: 10px;
  }

  .reward {
    background: #dcfce7;
    border: 1px solid #86efac;
    color: #166534;
    padding: 10px 14px;
    border-radius: 10px;
  }

  .grid {
    display: grid;
    grid-template-columns: minmax(280px, 1fr) 2fr;
    gap: 16px;
    margin-top: 24px;
    align-items: start;
  }

  .card {
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    background: white;
    padding: 20px;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 12px;
  }

  label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 13px;
    color: #475569;
  }

  .row {
    display: flex;
    gap: 12px;
  }

  .row label {
    flex: 1;
  }

  input,
  select {
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 8px 10px;
    font: inherit;
  }

  button {
    border: 1px solid #334155;
    background: #334155;
    color: white;
    border-radius: 10px;
    padding: 9px 14px;
    cursor: pointer;
    font: inherit;
  }

  button.ghost {
    background: white;
    color: #334155;
  }

  .hint {
    margin: 0;
    font-size: 12px;
    color: #94a3b8;
  }

  .tasks {
    list-style: none;
    padding: 0;
    margin: 12px 0 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .tasks li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 12px;
  }

  .tasks.done li {
    opacity: 0.7;
  }

  .title {
    font-weight: 500;
  }

  .badge {
    display: inline-block;
    font-size: 11px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 2px 6px;
    margin-right: 6px;
    color: #475569;
  }

  .badge-high {
    border-color: #fbbf24;
    color: #92400e;
  }

  .badge-critical {
    border-color: #f87171;
    color: #991b1b;
  }

  .xp {
    color: #166534;
    font-size: 13px;
    white-space: nowrap;
  }

  .empty {
    color: #94a3b8;
  }

  h3 {
    margin-top: 20px;
    font-size: 14px;
    color: #64748b;
  }
</style>
