/**
 * Client API minimal pour la V0 technique.
 *
 * L'URL de base provient de PUBLIC_API_BASE_URL (cf. .env.example / compose),
 * avec repli sur http://localhost:8000 pour un lancement hors Docker.
 */
import { env } from '$env/dynamic/public';

const BASE = env.PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

export type TaskType =
  | 'incident'
  | 'interruption'
  | 'exploitation'
  | 'project'
  | 'audit'
  | 'documentation'
  | 'script'
  | 'communication'
  | 'meeting'
  | 'analysis'
  | 'followup'
  | 'watch'
  | 'improvement'
  | 'change'
  | 'user_ticket';

export type TaskPriority = 'low' | 'normal' | 'high' | 'critical';
export type TaskDifficulty = 'trivial' | 'easy' | 'normal' | 'hard' | 'complex' | 'major';
export type TaskStatus =
  | 'inbox'
  | 'todo'
  | 'in_progress'
  | 'waiting'
  | 'planned'
  | 'done'
  | 'abandoned';

export interface Task {
  id: number;
  title: string;
  description: string;
  notes: string;
  type: TaskType;
  priority: TaskPriority;
  difficulty: TaskDifficulty;
  status: TaskStatus;
  planned_date: string | null;
  due_date: string | null;
  followup_date: string | null;
  xp_reward: number;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface NewTask {
  title: string;
  type?: TaskType;
  priority?: TaskPriority;
  status?: TaskStatus;
  planned_date?: string | null;
  followup_date?: string | null;
  project_id?: number | null;
}

export type TaskUpdate = Partial<{
  title: string;
  description: string;
  notes: string;
  type: TaskType;
  priority: TaskPriority;
  difficulty: TaskDifficulty;
  status: TaskStatus;
  planned_date: string | null;
  due_date: string | null;
  followup_date: string | null;
  project_id: number | null;
}>;

export type ProjectStatus = 'active' | 'archived';

export interface Project {
  id: number;
  name: string;
  domain: string;
  description: string;
  status: ProjectStatus;
  created_at: string;
  updated_at: string;
}

export interface ProjectDetail extends Project {
  tasks: Task[];
}

export interface NewProject {
  name: string;
  domain?: string;
  description?: string;
}

export type ProjectUpdate = Partial<{
  name: string;
  domain: string;
  description: string;
  status: ProjectStatus;
}>;

export type EventKind = 'event' | 'work_slot' | 'meeting' | 'change';

export interface CalendarEvent {
  id: number;
  title: string;
  event_date: string;
  start_time: string | null;
  end_time: string | null;
  kind: EventKind;
  task_id: number | null;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface NewEvent {
  title: string;
  event_date: string;
  start_time?: string | null;
  end_time?: string | null;
  kind?: EventKind;
  task_id?: number | null;
  notes?: string;
}

export type EventUpdate = Partial<{
  title: string;
  event_date: string;
  start_time: string | null;
  end_time: string | null;
  kind: EventKind;
  task_id: number | null;
  notes: string;
}>;

export interface CompletionResult {
  task: Task;
  xp_gained: number;
  gold_gained: number;
}

export interface Stats {
  total_xp: number;
  total_gold: number;
  completed_tasks: number;
}

async function asJson<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`${res.status} ${res.statusText} — ${detail}`);
  }
  return res.json() as Promise<T>;
}

export async function listTasks(): Promise<Task[]> {
  return asJson(await fetch(`${BASE}/tasks`));
}

export async function createTask(payload: NewTask): Promise<Task> {
  return asJson(
    await fetch(`${BASE}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
  );
}

export async function updateTask(id: number, patch: TaskUpdate): Promise<Task> {
  return asJson(
    await fetch(`${BASE}/tasks/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(patch)
    })
  );
}

export async function completeTask(id: number): Promise<CompletionResult> {
  return asJson(await fetch(`${BASE}/tasks/${id}/complete`, { method: 'POST' }));
}

export async function deleteTask(id: number): Promise<void> {
  const res = await fetch(`${BASE}/tasks/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
}

export async function getStats(): Promise<Stats> {
  return asJson(await fetch(`${BASE}/stats`));
}

export async function listProjects(includeArchived = false): Promise<Project[]> {
  return asJson(await fetch(`${BASE}/projects?include_archived=${includeArchived}`));
}

export async function getProject(id: number): Promise<ProjectDetail> {
  return asJson(await fetch(`${BASE}/projects/${id}`));
}

export async function createProject(payload: NewProject): Promise<Project> {
  return asJson(
    await fetch(`${BASE}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
  );
}

export async function updateProject(id: number, patch: ProjectUpdate): Promise<Project> {
  return asJson(
    await fetch(`${BASE}/projects/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(patch)
    })
  );
}

export async function listEvents(start: string, end: string): Promise<CalendarEvent[]> {
  return asJson(await fetch(`${BASE}/events?start=${start}&end=${end}`));
}

export async function createEvent(payload: NewEvent): Promise<CalendarEvent> {
  return asJson(
    await fetch(`${BASE}/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
  );
}

export async function updateEvent(id: number, patch: EventUpdate): Promise<CalendarEvent> {
  return asJson(
    await fetch(`${BASE}/events/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(patch)
    })
  );
}

export async function deleteEvent(id: number): Promise<void> {
  const res = await fetch(`${BASE}/events/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
}
