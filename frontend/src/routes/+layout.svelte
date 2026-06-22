<script lang="ts">
  import { page } from '$app/state';

  let { children } = $props();

  const tabs = [
    { href: '/', label: "Aujourd'hui" },
    { href: '/inbox', label: 'Inbox' },
    { href: '/projets', label: 'Projets' },
    { href: '/calendrier', label: 'Calendrier' }
  ];

  const isActive = (href: string) =>
    href === '/' ? page.url.pathname === '/' : page.url.pathname.startsWith(href);
</script>

<nav class="topnav">
  <span class="brand">QuestBoard</span>
  <div class="links">
    {#each tabs as tab}
      <a href={tab.href} class:active={isActive(tab.href)}>{tab.label}</a>
    {/each}
  </div>
</nav>

{@render children()}

<style>
  :global(body) {
    margin: 0;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif;
    background: #f6f4ef;
    color: #1f2933;
  }
  .topnav {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 12px 32px;
    background: #1f2933;
    color: white;
  }
  .brand {
    font-weight: 700;
    letter-spacing: 0.02em;
  }
  .links {
    display: flex;
    gap: 6px;
  }
  .links a {
    color: #cbd5e1;
    text-decoration: none;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 14px;
  }
  .links a.active {
    background: #334155;
    color: white;
  }
  .links a:hover {
    color: white;
  }
</style>
