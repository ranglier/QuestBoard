<script lang="ts">
  import {
    createEvent,
    deleteEvent,
    listEvents,
    listTasks,
    updateEvent,
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
  const DAY_NAMES = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];

  const DAY_START = 7; // première heure affichée
  const DAY_END = 21; // dernière heure (exclue)
  const HOUR_H = 44; // px par heure
  const hours = Array.from({ length: DAY_END - DAY_START }, (_, i) => DAY_START + i);

  const toISO = (d: Date) =>
    `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const mondayOf = (base: Date) => {
    const d = new Date(base);
    d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
    d.setHours(0, 0, 0, 0);
    return d;
  };
  const hhmm = (t: string | null) => (t ? t.slice(0, 5) : '');
  const mins = (t: string | null) => {
    if (!t) return 0;
    const [h, m] = t.split(':');
    return Number(h) * 60 + Number(m);
  };
  const pad = (n: number) => String(n).padStart(2, '0');

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
    `${days[0]?.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })} – ${days[6]?.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })}`
  );

  const openTasks = $derived(
    tasks.filter((t) => t.status !== 'done' && t.status !== 'abandoned' && t.status !== 'inbox')
  );
  const timedOf = (iso: string) => events.filter((e) => e.event_date === iso && e.start_time);
  const alldayOf = (iso: string) => events.filter((e) => e.event_date === iso && !e.start_time);
  const plannedOf = (iso: string) =>
    tasks.filter(
      (t) => t.planned_date === iso && t.status !== 'done' && t.status !== 'abandoned'
    );

  function evStyle(e: CalendarEvent) {
    const top = ((mins(e.start_time) - DAY_START * 60) / 60) * HOUR_H;
    const dur = e.end_time ? Math.max(mins(e.end_time) - mins(e.start_time), 20) : 30;
    const height = Math.max((dur / 60) * HOUR_H, 18);
    return `top:${Math.max(top, 0)}px;height:${height}px;`;
  }

  // --- modal create/edit ---
  let modalOpen = $state(false);
  let editingId = $state<number | null>(null);
  let mTitle = $state('');
  let mDate = $state('');
  let mStart = $state('09:00');
  let mEnd = $state('10:00');
  let mKind = $state<EventKind>('event');
  let mTask = $state<number | ''>('');
  let mAllDay = $state(false);

  function openCreate(dayISO: string, hour: number) {
    editingId = null;
    mTitle = '';
    mDate = dayISO;
    mStart = `${pad(hour)}:00`;
    mEnd = `${pad(Math.min(hour + 1, 23))}:00`;
    mKind = 'event';
    mTask = '';
    mAllDay = false;
    modalOpen = true;
  }

  function openEdit(e: CalendarEvent) {
    editingId = e.id;
    mTitle = e.title;
    mDate = e.event_date;
    mAllDay = !e.start_time;
    mStart = e.start_time ? hhmm(e.start_time) : '09:00';
    mEnd = e.end_time ? hhmm(e.end_time) : '10:00';
    mKind = e.kind;
    mTask = e.task_id ?? '';
    modalOpen = true;
  }

  function dayClick(event: MouseEvent, dayISO: string) {
    const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
    const y = event.clientY - rect.top;
    const hour = Math.min(DAY_END - 1, DAY_START + Math.floor(y / HOUR_H));
    openCreate(dayISO, hour);
  }

  async function save(event: SubmitEvent) {
    event.preventDefault();
    if (!mTitle.trim()) return;
    const payload = {
      title: mTitle.trim(),
      event_date: mDate,
      start_time: mAllDay ? null : mStart,
      end_time: mAllDay ? null : mEnd,
      kind: mKind,
      task_id: mTask === '' ? null : mTask
    };
    try {
      if (editingId === null) {
        await createEvent(payload);
        if (mTask !== '') await updateTask(mTask, { planned_date: mDate, status: 'planned' });
      } else {
        await updateEvent(editingId, payload);
      }
      modalOpen = false;
      await refresh();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function removeEvent() {
    if (editingId === null) return;
    try {
      await deleteEvent(editingId);
      modalOpen = false;
      await refresh();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  async function refresh() {
    try {
      [events, tasks] = await Promise.all([
        listEvents(toISO(days[0]), toISO(days[6])),
        listTasks()
      ]);
      error = null;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  $effect(() => {
    weekOffset;
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
      <button class="ghost" onclick={() => (weekOffset -= 1)}>‹</button>
      <button class="ghost" onclick={() => (weekOffset = 0)}>Aujourd'hui</button>
      <button class="ghost" onclick={() => (weekOffset += 1)}>›</button>
      <span class="weeklabel">{weekLabel}</span>
    </div>
  </header>

  {#if error}<p class="error">Erreur API : {error}</p>{/if}
  <p class="hint">Clique un créneau pour ajouter un événement · clique un événement pour le modifier.</p>

  <div class="cal">
    <!-- en-têtes jours -->
    <div class="corner"></div>
    {#each days as d, i}
      {@const iso = toISO(d)}
      <div class="dayhead" class:today={iso === toISO(new Date())}>
        <span class="dn">{DAY_NAMES[i]}</span>
        <span class="dd">{d.getDate()}/{d.getMonth() + 1}</span>
      </div>
    {/each}

    <!-- bande journée -->
    <div class="allday-label">jour</div>
    {#each days as d}
      {@const iso = toISO(d)}
      <div class="allday">
        {#each alldayOf(iso) as e (e.id)}
          <button class="chip kind-{e.kind}" onclick={() => openEdit(e)}>{e.title}</button>
        {/each}
        {#each plannedOf(iso) as t (t.id)}
          <span class="chip planned" title="Tâche planifiée">{t.title}</span>
        {/each}
      </div>
    {/each}

    <!-- grille horaire -->
    <div class="times">
      {#each hours as h}
        <div class="hourlabel" style="height:{HOUR_H}px">{pad(h)}:00</div>
      {/each}
    </div>
    {#each days as d}
      {@const iso = toISO(d)}
      <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_noninteractive_tabindex -->
      <div
        class="daycol"
        style="height:{hours.length * HOUR_H}px; background-size: 100% {HOUR_H}px;"
        role="button"
        tabindex="-1"
        onclick={(ev) => dayClick(ev, iso)}
      >
        {#each timedOf(iso) as e (e.id)}
          <button
            class="ev kind-{e.kind}"
            style={evStyle(e)}
            onclick={(ev) => {
              ev.stopPropagation();
              openEdit(e);
            }}
          >
            <span class="evt">{hhmm(e.start_time)} {e.title}</span>
          </button>
        {/each}
      </div>
    {/each}
  </div>
</main>

{#if modalOpen}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="backdrop"
    role="presentation"
    onclick={() => (modalOpen = false)}
  >
    <form
      class="modal"
      role="presentation"
      onclick={(e) => e.stopPropagation()}
      onsubmit={save}
    >
      <h2>{editingId === null ? 'Nouvel événement' : 'Modifier l’événement'}</h2>
      <label>Titre<input bind:value={mTitle} required /></label>
      <div class="grid2">
        <label>Date<input type="date" bind:value={mDate} required /></label>
        <label class="check"><input type="checkbox" bind:checked={mAllDay} /> Journée</label>
      </div>
      {#if !mAllDay}
        <div class="grid2">
          <label>Début<input type="time" bind:value={mStart} /></label>
          <label>Fin<input type="time" bind:value={mEnd} /></label>
        </div>
      {/if}
      <div class="grid2">
        <label>Type
          <select bind:value={mKind}>
            {#each KINDS as k}<option value={k.value}>{k.label}</option>{/each}
          </select>
        </label>
        <label>Tâche liée
          <select bind:value={mTask}>
            <option value="">—</option>
            {#each openTasks as t}<option value={t.id}>{t.title}</option>{/each}
          </select>
        </label>
      </div>
      <div class="modalactions">
        {#if editingId !== null}
          <button type="button" class="danger" onclick={removeEvent}>Supprimer</button>
        {/if}
        <span class="spacer"></span>
        <button type="button" class="ghost" onclick={() => (modalOpen = false)}>Annuler</button>
        <button type="submit">Enregistrer</button>
      </div>
    </form>
  </div>
{/if}

<style>
  .shell {
    max-width: 1100px;
    margin: 0 auto;
    padding: 24px 32px 40px;
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
    gap: 6px;
  }
  .weeklabel {
    color: #475569;
    font-size: 13px;
    margin-left: 8px;
  }
  .hint {
    color: #94a3b8;
    font-size: 12px;
    margin: 10px 0;
  }
  .error {
    background: #fee2e2;
    border: 1px solid #fca5a5;
    color: #991b1b;
    padding: 10px 14px;
    border-radius: 10px;
  }

  .cal {
    display: grid;
    grid-template-columns: 52px repeat(7, 1fr);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    background: white;
  }
  .corner {
    border-bottom: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
  }
  .dayhead {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #e2e8f0;
    border-right: 1px solid #f1f5f9;
  }
  .dayhead.today {
    background: #eef2ff;
  }
  .dn {
    font-weight: 600;
    font-size: 13px;
  }
  .dd {
    color: #94a3b8;
    font-size: 11px;
  }
  .allday-label {
    font-size: 10px;
    color: #94a3b8;
    text-align: right;
    padding: 4px 6px;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
  }
  .allday {
    min-height: 24px;
    border-right: 1px solid #f1f5f9;
    border-bottom: 1px solid #e2e8f0;
    padding: 3px;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  .times {
    border-right: 1px solid #e2e8f0;
  }
  .hourlabel {
    font-size: 11px;
    color: #94a3b8;
    text-align: right;
    padding-right: 6px;
    box-sizing: border-box;
    transform: translateY(-7px);
  }
  .daycol {
    position: relative;
    border-right: 1px solid #f1f5f9;
    background-image: linear-gradient(to bottom, #eef2f7 1px, transparent 1px);
    cursor: copy;
  }
  .ev {
    position: absolute;
    left: 3px;
    right: 3px;
    border: none;
    border-left: 3px solid #64748b;
    border-radius: 5px;
    background: #eef2ff;
    color: #1f2933;
    text-align: left;
    padding: 2px 5px;
    font-size: 11px;
    overflow: hidden;
    cursor: pointer;
  }
  .ev .evt {
    display: block;
    line-height: 1.25;
  }
  .chip {
    border: 1px solid #cbd5e1;
    border-left: 3px solid #64748b;
    border-radius: 5px;
    background: #f8fafc;
    font-size: 11px;
    padding: 2px 6px;
    text-align: left;
    cursor: pointer;
    color: #1f2933;
  }
  .chip.planned {
    border-left-color: #22c55e;
    border-style: dashed;
    cursor: default;
  }
  .kind-meeting {
    border-left-color: #6366f1;
  }
  .kind-change {
    border-left-color: #f97316;
  }
  .kind-work_slot {
    border-left-color: #0ea5e9;
  }
  .kind-event {
    border-left-color: #64748b;
  }

  button {
    font: inherit;
  }
  .ghost {
    border: 1px solid #cbd5e1;
    background: white;
    color: #334155;
    border-radius: 9px;
    padding: 6px 11px;
    cursor: pointer;
    font-size: 13px;
  }

  /* modal */
  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    z-index: 10;
  }
  .modal {
    background: white;
    border-radius: 14px;
    padding: 20px;
    width: 100%;
    max-width: 420px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
  }
  .modal h2 {
    margin: 0;
    font-size: 17px;
  }
  .modal label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 13px;
    color: #475569;
  }
  .modal input,
  .modal select {
    border: 1px solid #cbd5e1;
    border-radius: 9px;
    padding: 8px 10px;
    font: inherit;
  }
  .grid2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    align-items: end;
  }
  .check {
    flex-direction: row !important;
    align-items: center;
    gap: 6px;
  }
  .modalactions {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 4px;
  }
  .spacer {
    flex: 1;
  }
  .modal button[type='submit'] {
    border: 1px solid #334155;
    background: #334155;
    color: white;
    border-radius: 9px;
    padding: 8px 14px;
    cursor: pointer;
  }
  .danger {
    border: 1px solid #fca5a5;
    background: white;
    color: #b91c1c;
    border-radius: 9px;
    padding: 8px 12px;
    cursor: pointer;
  }
</style>
