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
  type: TaskType;
  priority: TaskPriority;
  status?: TaskStatus;
  planned_date?: string | null;
  followup_date?: string | null;
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

export async function getStats(): Promise<Stats> {
  return asJson(await fetch(`${BASE}/stats`));
}
