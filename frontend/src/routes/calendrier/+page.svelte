<script lang="ts">
  import {
    createEvent,
    deleteEvent,
    listEvents,
    listTasks,
    updateTask,
    type CalendarEvent,
    type EventKind,
    type Task
  } from '$lib/api';

  const KINDS: { value: EventKind; label: string }[] = [
    { value: 'event', label: 'Événement' },
    { value: 'work_slot', label: 'Créneau' },
    { value: 'meeting', label: 'Réunion' },
    { value: 'change', label: 'MEO' }
  ];
  const KIND_LABEL = Object.fromEntries(KINDS.map((k) => [k.value, k.label]));
  const DAY_NAMES = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];

  const toISO = (d: Date) =>
    `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const mondayOf = (base: Date) => {
    const d = new Date(base);
    const offset = (d.getDay() + 6) % 7; // jours depuis lundi
    d.setDate(d.getDate() - offset);
    d.setHours(0, 0, 0, 0);
    return d;
  };
  const hhmm = (t: string | null) => (t ? t.slice(0, 5) : '');

  let weekOffset = $state(0);
  let events = $state<CalendarEvent[]>([]);
  let tasks = $state<Task[]>([]);
  let error = $state<string | null>(null);

  const weekStart = $derived.by(() => {
    const m = mondayOf(new Date());
    m.setDate(m.getDate() + weekOffset * 7);
    return m;
  });
  const days = $derived(
    Array.from({ length: 7 }, (_, i) => {
      const d = new Date(weekStart);
      d.setDate(d.getDate() + i);
      return d;
    })
  );
  const weekLabel = $derived(
    `${days[0]?.toLocaleDateString('fr-FR')} – ${days[6]?.toLocaleDateString('fr-FR')}`
  );

  // formulaire
  let fTitle = $state('');
  let fDate = $state(toISO(new Date()));
  let fStart = $state('09:00');
  let fEnd = $state('09:30');
  let fKind = $state<EventKind>('event');
  let fTask = $state<number | ''>('');

  const eventsOf = (iso: string) => events.filter((e) => e.event_date === iso);
  const plannedOf = (iso: string) =>
    tasks.filter(
      (t) => t.planned_date === iso && t.status !== 'done' && t.status !== 'abandoned'
    );
  const openTasks = $derived(
    tasks.filter((t) => t.status !== 'done' && t.status !== 'abandoned' && t.status !== 'inbox')
  );

  async function refresh() {
    try {
      const start = toISO(days[0]);
      const end = toISO(days[6]);
      [events, tasks] = await Promise.all([listEvents(start, end), listTasks()]);
      error = null;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function onCreate(event: SubmitEvent) {
    event.preventDefault();
    if (!fTitle.trim()) return;
    try {
      await createEvent({
        title: fTitle.trim(),
        event_date: fDate,
        start_time: fStart || null,
        end_time: fEnd || null,
        kind: fKind,
        task_id: fTask === '' ? null : fTask
      });
      // bloc créé depuis une tâche -> la planifier ce jour-là
      if (fTask !== '') await updateTask(fTask, { planned_date: fDate, status: 'planned' });
      fTitle = '';
      fTask = '';
      await refresh();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function remove(id: number) {
    try {
      await deleteEvent(id);
      await refresh();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  $effect(() => {
    weekOffset; // re-fetch quand la semaine change
    refresh();
  });
</script>

<svelte:head><title>QuestBoard — Calendrier</title></svelte:head>

<main class="shell">
  <header class="head">
    <div>
      <p class="eyebrow">Calendrier local — vue semaine</p>
      <h1>Calendrier</h1>
    </div>
    <div class="nav">
      <button class="ghost" onclick={() => (weekOffset -= 1)}>‹ semaine</button>
      <button class="ghost" onclick={() => (weekOffset = 0)}>Aujourd'hui</button>
      <button class="ghost" onclick={() => (weekOffset += 1)}>semaine ›</button>
      <span class="weeklabel">{weekLabel}</span>
    </div>
  </header>

  {#if error}<p class="error">Erreur API : {error}</p>{/if}

  <form class="card" onsubmit={onCreate}>
    <input bind:value={fTitle} placeholder="Titre de l'événement…" required />
    <input type="date" bind:value={fDate} required />
    <input type="time" bind:value={fStart} />
    <input type="time" bind:value={fEnd} />
    <select bind:value={fKind}>
      {#each KINDS as k}<option value={k.value}>{k.label}</option>{/each}
    </select>
    <select bind:value={fTask}>
      <option value="">— lier une tâche (option) —</option>
      {#each openTasks as t}<option value={t.id}>{t.title}</option>{/each}
    </select>
    <button type="submit">Ajouter</button>
  </form>

  <div class="week">
    {#each days as d, i}
      {@const iso = toISO(d)}
      {@const isToday = iso === toISO(new Date())}
      <div class="day" class:today={isToday}>
        <div class="dayhead">
          <span class="dname">{DAY_NAMES[i]}</span>
          <span class="dnum">{d.getDate()}/{d.getMonth() + 1}</span>
        </div>
        {#each eventsOf(iso) as e (e.id)}
          <div class="ev kind-{e.kind}">
            <div class="evtop">
              {#if e.start_time}<span class="time">{hhmm(e.start_time)}{e.end_time ? '–' + hhmm(e.end_time) : ''}</span>{/if}
              <button class="x" title="Supprimer" onclick={() => remove(e.id)}>×</button>
            </div>
            <span class="evtitle">{e.title}</span>
            <span class="kindtag">{KIND_LABEL[e.kind]}</span>
          </div>
        {/each}
        {#each plannedOf(iso) as t (t.id)}
          <div class="ev planned"><span class="evtitle">{t.title}</span><span class="kindtag">tâche</span></div>
        {/each}
        {#if eventsOf(iso).length === 0 && plannedOf(iso).length === 0}
          <p class="empty">—</p>
        {/if}
      </div>
    {/each}
  </div>
</main>

<style>
  .shell {
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px;
  }
  .head {
    display: flex;
    align-items: flex-end;
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
  .nav {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .weeklabel {
    color: #475569;
    font-size: 13px;
    margin-left: 6px;
  }
  .card {
    display: flex;
    gap: 8px;
    margin: 18px 0;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 12px;
    flex-wrap: wrap;
    align-items: center;
  }
  .card input[type='text'],
  .card input:not([type]) {
    flex: 1;
    min-width: 180px;
  }
  input,
  select {
    border: 1px solid #cbd5e1;
    border-radius: 9px;
    padding: 7px 9px;
    font: inherit;
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
  .week {
    display: grid;
    grid-template-columns: repeat(7, minmax(120px, 1fr));
    gap: 8px;
    overflow-x: auto;
  }
  .day {
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    background: white;
    padding: 8px;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .day.today {
    border-color: #334155;
    box-shadow: inset 0 2px 0 #334155;
  }
  .dayhead {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 4px;
  }
  .dname {
    font-weight: 600;
    font-size: 13px;
  }
  .dnum {
    color: #94a3b8;
    font-size: 12px;
  }
  .ev {
    border: 1px solid #e2e8f0;
    border-left: 3px solid #94a3b8;
    border-radius: 6px;
    padding: 5px 7px;
    font-size: 12px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    background: #f8fafc;
  }
  .ev.kind-meeting {
    border-left-color: #6366f1;
  }
  .ev.kind-change {
    border-left-color: #f97316;
  }
  .ev.kind-work_slot {
    border-left-color: #0ea5e9;
  }
  .ev.planned {
    border-left-color: #22c55e;
    border-style: dashed;
  }
  .evtop {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .time {
    color: #475569;
    font-weight: 600;
  }
  .evtitle {
    color: #1f2933;
  }
  .kindtag {
    color: #94a3b8;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .x {
    border: none;
    background: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 15px;
    line-height: 1;
    padding: 0 2px;
  }
  .x:hover {
    color: #b91c1c;
  }
  .error {
    background: #fee2e2;
    border: 1px solid #fca5a5;
    color: #991b1b;
    padding: 10px 14px;
    border-radius: 10px;
  }
  .empty {
    color: #cbd5e1;
    text-align: center;
    margin: auto 0;
  }
</style>
