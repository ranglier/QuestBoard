<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import {
    completeTask,
    createTask,
    getStats,
    listEvents,
    listTasks,
    updateTask,
    type CalendarEvent,
    type EventKind,
    type Stats,
    type Task,
    type TaskPriority,
    type TaskType
  } from '$lib/api';

  const EVENT_KIND_LABEL: Record<EventKind, string> = {
    event: 'Événement',
    work_slot: 'Créneau',
    meeting: 'Réunion',
    change: 'MEO'
  };
  const hhmm = (t: string | null) => (t ? t.slice(0, 5) : '');
  const AGENDA_PREF = 'qb_show_agenda';

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

  // --- date helpers (local) ---
  const toISO = (d: Date) =>
    `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const todayISO = () => toISO(new Date());
  const addDaysISO = (n: number) => {
    const d = new Date();
    d.setDate(d.getDate() + n);
    return toISO(d);
  };
  const nextMondayISO = () => {
    const d = new Date();
    const diff = (1 - d.getDay() + 7) % 7 || 7;
    d.setDate(d.getDate() + diff);
    return toISO(d);
  };

  let tasks = $state<Task[]>([]);
  let stats = $state<Stats>({ total_xp: 0, total_gold: 0, completed_tasks: 0 });
  let todayEvents = $state<CalendarEvent[]>([]);
  let showAgenda = $state(true);
  let error = $state<string | null>(null);
  let lastReward = $state<{ xp: number; gold: number } | null>(null);

  let title = $state('');
  let type = $state<TaskType>('exploitation');
  let priority = $state<TaskPriority>('normal');
  let planToday = $state(false);

  const today = todayISO();
  const isOverdue = (t: Task) => !!t.followup_date && t.followup_date <= today;

  // Répartition de chaque tâche active dans une seule section (précédence claire).
  const buckets = $derived.by(() => {
    const planned: Task[] = [];
    const inProgress: Task[] = [];
    const waiting: Task[] = [];
    const todo: Task[] = [];
    for (const t of tasks) {
      if (t.status === 'done' || t.status === 'abandoned') continue;
      if (t.status === 'in_progress') inProgress.push(t);
      else if (t.status === 'waiting') waiting.push(t);
      else if (t.status === 'planned' || t.planned_date === today) planned.push(t);
      else todo.push(t);
    }
    // à relancer en premier dans la file d'attente
    waiting.sort((a, b) => Number(isOverdue(b)) - Number(isOverdue(a)));
    return { planned, inProgress, waiting, todo };
  });

  const doneToday = $derived(
    tasks.filter((t) => t.status === 'done' && (t.completed_at ?? '').slice(0, 10) === today)
  );

  // Agenda du jour : sans-horaire d'abord, puis par heure de début.
  const agenda = $derived(
    [...todayEvents].sort((a, b) => (a.start_time ?? '').localeCompare(b.start_time ?? ''))
  );

  function toggleAgenda() {
    showAgenda = !showAgenda;
    if (browser) localStorage.setItem(AGENDA_PREF, showAgenda ? '1' : '0');
  }

  async function refresh() {
    try {
      [tasks, stats, todayEvents] = await Promise.all([
        listTasks(),
        getStats(),
        listEvents(today, today)
      ]);
      error = null;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function run(action: Promise<unknown>, reward = false) {
    try {
      const res = await action;
      if (reward && res && typeof res === 'object' && 'xp_gained' in res) {
        const r = res as { xp_gained: number; gold_gained: number };
        lastReward = { xp: r.xp_gained, gold: r.gold_gained };
      }
      await refresh();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function onCreate(event: SubmitEvent) {
    event.preventDefault();
    if (!title.trim()) return;
    await run(
      createTask({
        title: title.trim(),
        type,
        priority,
        ...(planToday ? { status: 'planned', planned_date: today } : {})
      })
    );
    title = '';
    planToday = false;
  }

  const start = (t: Task) => run(updateTask(t.id, { status: 'in_progress' }));
  const resume = (t: Task) => run(updateTask(t.id, { status: 'in_progress' }));
  const planForToday = (t: Task) => run(updateTask(t.id, { status: 'planned', planned_date: today }));
  const abandon = (t: Task) => run(updateTask(t.id, { status: 'abandoned' }));
  const complete = (t: Task) => run(completeTask(t.id), true);
  const waitUntil = (t: Task, followup: string) =>
    run(updateTask(t.id, { status: 'waiting', followup_date: followup }));

  onMount(() => {
    if (browser && localStorage.getItem(AGENDA_PREF) === '0') showAgenda = false;
    refresh();
  });
</script>

<svelte:head>
  <title>QuestBoard — Aujourd'hui</title>
</svelte:head>

{#snippet taskRow(t: Task, actions: import('svelte').Snippet<[Task]>)}
  <li>
    <div class="meta">
      <span class="badge badge-{t.priority}">{PRIORITY_LABEL[t.priority]}</span>
      <span class="badge">{TYPE_LABEL[t.type]}</span>
      {#if t.status === 'waiting' && isOverdue(t)}
        <span class="badge badge-relance">À relancer</span>
      {/if}
      <span class="title">{t.title}</span>
      {#if t.followup_date && t.status === 'waiting'}
        <span class="muted">· relance {t.followup_date}</span>
      {/if}
    </div>
    <div class="actions">{@render actions(t)}</div>
  </li>
{/snippet}

<main class="shell">
  <header class="header">
    <div>
      <p class="eyebrow">Dashboard — Aujourd'hui</p>
      <h1>QuestBoard</h1>
    </div>
    <div class="resources">
      <span class="chip">XP&nbsp;: <strong>{stats.total_xp}</strong></span>
      <span class="chip">Or&nbsp;: <strong>{stats.total_gold}</strong></span>
      <span class="chip muted">Terminées&nbsp;: {stats.completed_tasks}</span>
    </div>
  </header>

  {#if error}<p class="error">Erreur API : {error}</p>{/if}
  {#if lastReward}
    <p class="reward">Tâche terminée — +{lastReward.xp} XP, +{lastReward.gold} or.</p>
  {/if}

  <article class="card capture">
    <form onsubmit={onCreate}>
      <input bind:value={title} placeholder="Capture rapide — titre de la tâche…" required />
      <select bind:value={type}>
        {#each TYPES as t}<option value={t.value}>{t.label}</option>{/each}
      </select>
      <select bind:value={priority}>
        {#each PRIORITIES as p}<option value={p.value}>{p.label}</option>{/each}
      </select>
      <label class="check"><input type="checkbox" bind:checked={planToday} /> Aujourd'hui</label>
      <button type="submit">Créer</button>
    </form>
  </article>

  <section class="section agenda">
    <h2>
      Agenda du jour
      {#if showAgenda}<span class="count">{agenda.length}</span>{/if}
      <button class="link" onclick={toggleAgenda}>
        {showAgenda ? 'masquer' : 'afficher'}
      </button>
    </h2>
    {#if showAgenda}
      {#if agenda.length === 0}
        <p class="empty">Aucun événement aujourd'hui. <a href="/calendrier">Ouvrir le calendrier</a></p>
      {:else}
        <ul class="agenda-list">
          {#each agenda as e (e.id)}
            <li class="agenda-item kind-{e.kind}">
              <span class="ag-time">{e.start_time ? hhmm(e.start_time) + (e.end_time ? '–' + hhmm(e.end_time) : '') : 'journée'}</span>
              <span class="ag-title">{e.title}</span>
              <span class="ag-kind">{EVENT_KIND_LABEL[e.kind]}</span>
            </li>
          {/each}
        </ul>
      {/if}
    {/if}
  </section>

  <section class="section">
    <h2>Planifié aujourd'hui <span class="count">{buckets.planned.length}</span></h2>
    {#if buckets.planned.length === 0}<p class="empty">Rien de planifié pour aujourd'hui.</p>{/if}
    <ul class="tasks">
      {#each buckets.planned as t (t.id)}
        {@render taskRow(t, plannedActions)}
      {/each}
    </ul>
  </section>

  <section class="section">
    <h2>En cours <span class="count">{buckets.inProgress.length}</span></h2>
    {#if buckets.inProgress.length === 0}<p class="empty">Aucune tâche en cours.</p>{/if}
    <ul class="tasks">
      {#each buckets.inProgress as t (t.id)}
        {@render taskRow(t, inProgressActions)}
      {/each}
    </ul>
  </section>

  <section class="section">
    <h2>En attente / à relancer <span class="count">{buckets.waiting.length}</span></h2>
    {#if buckets.waiting.length === 0}<p class="empty">Rien en attente.</p>{/if}
    <ul class="tasks">
      {#each buckets.waiting as t (t.id)}
        {@render taskRow(t, waitingActions)}
      {/each}
    </ul>
  </section>

  <section class="section">
    <h2>À faire <span class="count">{buckets.todo.length}</span></h2>
    {#if buckets.todo.length === 0}<p class="empty">Boîte à faire vide.</p>{/if}
    <ul class="tasks">
      {#each buckets.todo as t (t.id)}
        {@render taskRow(t, todoActions)}
      {/each}
    </ul>
  </section>

  {#if doneToday.length > 0}
    <section class="section">
      <h2>Terminées aujourd'hui <span class="count">{doneToday.length}</span></h2>
      <ul class="tasks done">
        {#each doneToday as t (t.id)}
          <li><span class="title">{t.title}</span><span class="xp">+{t.xp_reward} XP</span></li>
        {/each}
      </ul>
    </section>
  {/if}
</main>

{#snippet todoActions(t: Task)}
  <button class="ghost" onclick={() => start(t)}>Démarrer</button>
  <button class="ghost" onclick={() => waitUntil(t, addDaysISO(2))}>En attente</button>
  <button onclick={() => complete(t)}>Terminer</button>
  <button class="ghost danger" onclick={() => abandon(t)}>Abandonner</button>
{/snippet}

{#snippet plannedActions(t: Task)}
  <button class="ghost" onclick={() => start(t)}>Démarrer</button>
  <button class="ghost" onclick={() => waitUntil(t, addDaysISO(2))}>En attente</button>
  <button onclick={() => complete(t)}>Terminer</button>
{/snippet}

{#snippet inProgressActions(t: Task)}
  <button class="ghost" onclick={() => waitUntil(t, addDaysISO(2))}>En attente</button>
  <button onclick={() => complete(t)}>Terminer</button>
  <button class="ghost danger" onclick={() => abandon(t)}>Abandonner</button>
{/snippet}

{#snippet waitingActions(t: Task)}
  <span class="relance-label">Relancer&nbsp;:</span>
  <button class="ghost" onclick={() => waitUntil(t, today)}>auj.</button>
  <button class="ghost" onclick={() => waitUntil(t, addDaysISO(2))}>+2j</button>
  <button class="ghost" onclick={() => waitUntil(t, nextMondayISO())}>lundi</button>
  <button class="ghost" onclick={() => resume(t)}>Reprendre</button>
  <button onclick={() => complete(t)}>Terminer</button>
{/snippet}

<style>
  :global(body) {
    margin: 0;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif;
    background: #f6f4ef;
    color: #1f2933;
  }
  .shell {
    max-width: 1040px;
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
  h1 {
    margin: 0;
  }
  h2 {
    margin: 0 0 10px;
    font-size: 15px;
    color: #334155;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .count {
    background: #e2e8f0;
    color: #475569;
    border-radius: 999px;
    font-size: 12px;
    padding: 1px 8px;
  }
  .link {
    border: none;
    background: none;
    color: #64748b;
    font: inherit;
    font-size: 12px;
    text-decoration: underline;
    cursor: pointer;
    padding: 0;
    margin-left: auto;
  }
  .agenda {
    background: #fbfaf7;
    border: 1px solid #e7e2d8;
    border-radius: 12px;
    padding: 12px 14px;
    margin-top: 16px;
  }
  .agenda h2 {
    margin-bottom: 0;
  }
  .agenda-list {
    list-style: none;
    padding: 0;
    margin: 10px 0 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .agenda-item {
    display: flex;
    align-items: baseline;
    gap: 12px;
    padding: 6px 10px;
    background: white;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #94a3b8;
    border-radius: 8px;
  }
  .agenda-item.kind-meeting {
    border-left-color: #6366f1;
  }
  .agenda-item.kind-change {
    border-left-color: #f97316;
  }
  .agenda-item.kind-work_slot {
    border-left-color: #0ea5e9;
  }
  .ag-time {
    font-variant-numeric: tabular-nums;
    font-weight: 600;
    color: #475569;
    min-width: 92px;
    font-size: 13px;
  }
  .ag-title {
    flex: 1;
  }
  .ag-kind {
    color: #94a3b8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
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
  .card {
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    background: white;
    padding: 14px;
  }
  .capture {
    margin: 20px 0 8px;
  }
  .capture form {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
  }
  .capture input[type='text'],
  .capture input:not([type]) {
    flex: 1;
    min-width: 220px;
  }
  input,
  select {
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 8px 10px;
    font: inherit;
  }
  .check {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #475569;
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
  .section {
    margin-top: 24px;
  }
  .tasks {
    list-style: none;
    padding: 0;
    margin: 0;
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
    background: white;
    padding: 10px 12px;
  }
  .tasks.done li {
    opacity: 0.65;
  }
  .meta {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }
  .title {
    font-weight: 500;
  }
  .muted {
    color: #94a3b8;
    font-size: 12px;
  }
  .actions {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    flex-shrink: 0;
  }
  .relance-label {
    font-size: 12px;
    color: #64748b;
    align-self: center;
  }
  .badge {
    display: inline-block;
    font-size: 11px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 2px 6px;
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
  .badge-relance {
    border-color: #fb923c;
    color: #c2410c;
    background: #fff7ed;
  }
  .xp {
    color: #166534;
    font-size: 13px;
    white-space: nowrap;
  }
  .empty {
    color: #94a3b8;
    margin: 0;
    font-size: 14px;
  }
</style>
