<script lang="ts">
  const sections = [
    'Dashboard',
    'Inbox',
    'Projects',
    'Calendar',
    'History',
    'Camp'
  ];
</script>

<svelte:head>
  <title>QuestBoard</title>
</svelte:head>

<main class="shell">
  <header class="header">
    <div>
      <p class="eyebrow">Local-first work dashboard</p>
      <h1>QuestBoard</h1>
    </div>
    <div class="actions">
      <button>+ Capture</button>
      <button>Discreet mode</button>
    </div>
  </header>

  <nav class="tabs" aria-label="Main navigation">
    {#each sections as section}
      <button class:active={section === 'Dashboard'}>{section}</button>
    {/each}
  </nav>

  <section class="grid">
    <article class="card wide">
      <h2>Today</h2>
      <p>Agenda, planned tasks, active work, waiting items and suggested next actions will appear here.</p>
    </article>

    <article class="card">
      <h2>Quick Capture</h2>
      <p>Create a task with a title first, then qualify it later.</p>
    </article>

    <article class="card">
      <h2>Camp</h2>
      <p>Company level, resources, founder and first expedition will appear here.</p>
    </article>
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family:
      Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
  }

  .eyebrow {
    margin: 0 0 4px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 12px;
  }

  h1, h2 {
    margin: 0;
  }

  .actions, .tabs {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  button {
    border: 1px solid #cbd5e1;
    background: white;
    color: inherit;
    border-radius: 10px;
    padding: 8px 12px;
    cursor: pointer;
  }

  button.active {
    border-color: #334155;
    background: #334155;
    color: white;
  }

  .tabs {
    margin: 32px 0;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }

  .card {
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    background: white;
    padding: 20px;
    min-height: 140px;
  }

  .card.wide {
    grid-column: 1 / -1;
  }
</style>
