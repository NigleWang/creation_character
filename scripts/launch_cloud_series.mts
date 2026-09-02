/**
 * Launch (or follow up) a Cursor Cloud Agent that commits generated series
 * PNGs onto the same git branch — not a new cursor/... branch.
 *
 * Requires CURSOR_API_KEY (https://cursor.com/dashboard/integrations).
 * Repo must already be connected in Cursor Integrations.
 *
 * Usage (Node 22.6+ / 24, type stripping, no extra packages):
 *   node scripts/launch_cloud_series.mts launch --task-id 20260902_kai_office_series -- "全套日常姿态，锁定现有形象"
 *   node scripts/launch_cloud_series.mts follow -- "再补 04_coffee.png"
 *   node scripts/launch_cloud_series.mts status
 */

import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const API = "https://api.cursor.com/v1";
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const DEFAULT_STATE = resolve(ROOT, "outputs/drafts/cloud_agent.json");
const TERMINAL = new Set(["FINISHED", "ERROR", "CANCELLED", "EXPIRED"]);
const IMAGE_MIME: Record<string, string> = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
};

type Command = "launch" | "follow" | "status";

type Args = {
  command: Command;
  taskId: string;
  branch: string;
  repo: string;
  prUrl: string;
  agentId: string;
  model: string;
  images: string[];
  wait: boolean;
  dryRun: boolean;
  stateFile: string;
  prompt: string;
};

type CloudState = {
  agentId: string;
  runId?: string;
  repo: string;
  branch: string;
  taskId: string;
  url?: string;
  workOnCurrentBranch: true;
  autoCreatePR: false;
  updatedAt: string;
};

type GitBranch = { repoUrl?: string; branch?: string; prUrl?: string };

type ApiRun = {
  id: string;
  agentId: string;
  status: string;
  result?: string;
  durationMs?: number;
  git?: { branches?: GitBranch[] };
};

type ApiAgent = {
  id: string;
  name?: string;
  status?: string;
  url?: string;
  latestRunId?: string;
  workOnCurrentBranch?: boolean;
  autoCreatePR?: boolean;
  repos?: Array<{ url?: string; startingRef?: string; prUrl?: string }>;
};

function fail(message: string, code = 1): never {
  console.error(message);
  process.exit(code);
}

function git(args: string[]): string {
  try {
    return execFileSync("git", args, { cwd: ROOT, encoding: "utf8" }).trim();
  } catch {
    return "";
  }
}

function toHttpsRepo(raw: string): string {
  const trimmed = raw.trim().replace(/\.git$/, "");
  const ssh = trimmed.match(/^git@([^:]+):(.+)$/);
  if (ssh) return `https://${ssh[1]}/${ssh[2]}`;
  return trimmed;
}

function todayStamp(): string {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}${m}${day}`;
}

function parseArgs(argv: string[]): Args {
  const rest = argv.slice(2);
  const command = rest[0];
  if (command === "help" || command === "-h" || command === "--help" || !command) {
    printHelp();
    process.exit(0);
  }
  if (command !== "launch" && command !== "follow" && command !== "status") {
    fail(`Unknown command: ${command}\nRun with --help.`);
  }

  const dash = rest.indexOf("--");
  const flags = dash === -1 ? rest.slice(1) : rest.slice(1, dash);
  const promptParts = dash === -1 ? [] : rest.slice(dash + 1);

  const take = (name: string, fallback = ""): string => {
    const i = flags.indexOf(name);
    if (i === -1) return fallback;
    const value = flags[i + 1];
    if (!value || value.startsWith("--")) fail(`${name} needs a value`);
    return value;
  };

  const images: string[] = [];
  for (let i = 0; i < flags.length; i++) {
    if (flags[i] === "--image") {
      const value = flags[++i];
      if (!value || value.startsWith("--")) fail("--image needs a path");
      images.push(value);
    }
  }

  const detectedRepo = toHttpsRepo(
    git(["remote", "get-url", "origin"]) ||
      "https://github.com/NigleWang/creation_character",
  );
  const detectedBranch = git(["branch", "--show-current"]) || "main";

  return {
    command,
    taskId: take("--task-id", `${todayStamp()}_cloud_series`),
    branch: take("--branch", process.env.CURSOR_BRANCH || detectedBranch),
    repo: take("--repo", process.env.CURSOR_REPO_URL || detectedRepo),
    prUrl: take("--pr-url"),
    agentId: take("--agent-id"),
    model: take("--model", process.env.CURSOR_MODEL || ""),
    images,
    wait: !flags.includes("--no-wait"),
    dryRun: flags.includes("--dry-run"),
    stateFile: take("--state-file", DEFAULT_STATE),
    prompt: promptParts.join(" ").trim(),
  };
}

function printHelp(): void {
  console.log(`Cursor Cloud: generate series PNGs and push them to the SAME branch.

Commands:
  launch   Create a cloud agent on --branch (workOnCurrentBranch=true, no PR)
  follow   Send a follow-up to the saved / --agent-id agent (same workspace)
  status   Print agent + latest run + pushed branches

Required env:
  CURSOR_API_KEY     Cursor user or service-account API key

Options:
  --task-id <id>     Series folder name under outputs/approved/series/
  --branch <name>    Target branch to commit onto (default: current git branch)
  --repo <url>       GitHub HTTPS URL
  --pr-url <url>     Attach to an existing PR head instead of --branch
  --agent-id <bc-…>  Follow / status (default: last launch in outputs/drafts/)
  --image <path>     Attach a reference photo (repeatable, max 5)
  --model <id>       Optional model id
  --no-wait          Return after enqueue; do not poll
  --dry-run          Print the request body and exit
  --state-file <p>   Where to remember agentId (gitignored drafts path)
  -- <text>          Task prompt (launch / follow)

Examples:
  node scripts/launch_cloud_series.mts launch --task-id 20260902_kai_office_series -- "全套日常姿态，锁定现有形象与服装"
  node scripts/launch_cloud_series.mts follow -- "再补 04_coffee.png，同一套衣服"
  node scripts/launch_cloud_series.mts status
`);
}

function apiKey(): string {
  const key = process.env.CURSOR_API_KEY?.trim();
  if (!key) fail("Set CURSOR_API_KEY (Cursor Dashboard → Integrations / API Keys).");
  return key;
}

async function api<T>(
  method: string,
  path: string,
  body?: unknown,
): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${apiKey()}`,
      "Content-Type": "application/json",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await res.text();
  let json: unknown = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    json = { raw: text };
  }
  if (!res.ok) {
    fail(`API ${method} ${path} → ${res.status}\n${JSON.stringify(json, null, 2)}`);
  }
  return json as T;
}

function encodeImages(paths: string[]): Array<{ data: string; mimeType: string }> {
  if (paths.length > 5) fail("Cloud prompt accepts at most 5 images.");
  return paths.map((p) => {
    const abs = resolve(p);
    if (!existsSync(abs)) fail(`Image not found: ${abs}`);
    const ext = abs.slice(abs.lastIndexOf(".")).toLowerCase();
    const mimeType = IMAGE_MIME[ext];
    if (!mimeType) fail(`Unsupported image type ${ext} (${abs}). Use png/jpeg/gif/webp.`);
    return {
      data: readFileSync(abs).toString("base64"),
      mimeType,
    };
  });
}

function seriesPrompt(taskId: string, branch: string, operatorText: string): string {
  return `You are an unattended Cursor Cloud Agent for the creation_character repo (Teo 受 / Kai 攻 Xiaohongshu studio).

The operator already confirmed this task. Generate now.
Do NOT post numbered style/pose options and stop. Do NOT wait for a second turn.

## Git (hard)
- Stay on branch \`${branch}\`. Do not checkout, create, or push a cursor/… branch.
- Do not open a pull request.
- After images are written, git add them, commit, and push to origin/${branch}.
- Do not change unrelated files.

## Where to save (hard)
- Write PNGs only to \`outputs/approved/series/${taskId}/\` as \`01_<pose_id>.png\`, \`02_…\`.
- Do NOT write to \`outputs/approved/xiaohongshu_*.png\` — that path is gitignored and will not be committed.
- 3:4 vertical. One pose per image, never a collage.
- Follow AGENTS.md, .cursor/skills/pose-series/SKILL.md, character bibles. Never swap Teo/Kai.

## Task
${operatorText}`.trim();
}

function loadState(path: string): CloudState | null {
  if (!existsSync(path)) return null;
  return JSON.parse(readFileSync(path, "utf8")) as CloudState;
}

function saveState(path: string, state: CloudState): void {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(state, null, 2) + "\n");
  console.log(`Saved agent id → ${path}`);
}

function resolveAgentId(args: Args): string {
  if (args.agentId) return args.agentId;
  const state = loadState(args.stateFile);
  if (!state?.agentId) {
    fail("No --agent-id and no saved state. Run launch first.");
  }
  return state.agentId;
}

function printGit(git: ApiRun["git"], expectedBranch: string): void {
  const branches = git?.branches ?? [];
  if (branches.length === 0) {
    console.log("git.branches: (none yet)");
    return;
  }
  for (const b of branches) {
    console.log(`git.branch: ${b.branch ?? "(unknown)"}  repo=${b.repoUrl ?? ""}`);
    if (b.prUrl) console.log(`git.pr: ${b.prUrl}`);
    if (b.branch?.startsWith("cursor/")) {
      console.warn(
        `WARNING: pushed ${b.branch}, not ${expectedBranch}. workOnCurrentBranch was ignored or not set.`,
      );
    } else if (expectedBranch && b.branch && b.branch !== expectedBranch) {
      console.warn(`WARNING: pushed ${b.branch}, expected ${expectedBranch}.`);
    } else {
      console.log(`OK: commits are on ${b.branch}.`);
    }
  }
}

async function waitForRun(agentId: string, runId: string, expectedBranch: string): Promise<ApiRun> {
  console.log(`Waiting for ${runId} …`);
  const started = Date.now();
  const timeoutMs = 45 * 60 * 1000;
  while (Date.now() - started < timeoutMs) {
    const run = await api<ApiRun>("GET", `/agents/${agentId}/runs/${runId}`);
    process.stdout.write(`\rstatus=${run.status}  ${Math.round((Date.now() - started) / 1000)}s   `);
    if (TERMINAL.has(run.status)) {
      console.log("");
      if (run.status !== "FINISHED") {
        fail(`Run ended ${run.status}\n${run.result ?? ""}`, 2);
      }
      if (run.result) console.log(run.result);
      printGit(run.git, expectedBranch);
      return run;
    }
    await new Promise((r) => setTimeout(r, 8000));
  }
  fail("Timed out waiting for the cloud run (45m). Use `status` later.");
}

function promptBody(args: Args, operatorText: string) {
  const images = args.images.length ? encodeImages(args.images) : undefined;
  return {
    text: seriesPrompt(args.taskId, args.branch, operatorText),
    ...(images ? { images } : {}),
  };
}

async function launch(args: Args): Promise<void> {
  if (!args.prompt) fail("launch needs a task after `--`, e.g. -- \"全套日常姿态\"");

  const repoEntry: Record<string, string> = { url: args.repo };
  if (args.prUrl) repoEntry.prUrl = args.prUrl;
  else repoEntry.startingRef = args.branch;

  const body: Record<string, unknown> = {
    name: `series ${args.taskId}`.slice(0, 100),
    prompt: promptBody(args, args.prompt),
    repos: [repoEntry],
    workOnCurrentBranch: true,
    autoCreatePR: false,
  };
  if (args.model) body.model = { id: args.model };

  if (args.dryRun) {
    const preview = structuredClone(body) as {
      prompt: { images?: Array<{ data: string }> };
    };
    if (preview.prompt.images) {
      preview.prompt.images = preview.prompt.images.map((img) => ({
        ...img,
        data: `<base64 ${img.data.length} chars>`,
      }));
    }
    console.log(JSON.stringify({ ...body, prompt: preview.prompt }, null, 2));
    return;
  }

  const created = await api<{ agent: ApiAgent; run: ApiRun }>("POST", "/agents", body);
  const agent = created.agent;
  const run = created.run;
  console.log(`agent: ${agent.id}`);
  console.log(`run:   ${run.id}`);
  if (agent.url) console.log(`url:   ${agent.url}`);
  console.log(`workOnCurrentBranch=${agent.workOnCurrentBranch} autoCreatePR=${agent.autoCreatePR}`);

  saveState(args.stateFile, {
    agentId: agent.id,
    runId: run.id,
    repo: args.repo,
    branch: args.branch,
    taskId: args.taskId,
    url: agent.url,
    workOnCurrentBranch: true,
    autoCreatePR: false,
    updatedAt: new Date().toISOString(),
  });

  if (args.wait) await waitForRun(agent.id, run.id, args.branch);
}

async function follow(args: Args): Promise<void> {
  if (!args.prompt) fail("follow needs a task after `--`");
  const agentId = resolveAgentId(args);
  const body = { prompt: promptBody(args, args.prompt) };
  if (args.dryRun) {
    console.log(JSON.stringify({ agentId, ...body }, null, 2));
    return;
  }
  const created = await api<{ run: ApiRun }>("POST", `/agents/${agentId}/runs`, body);
  console.log(`agent: ${agentId}`);
  console.log(`run:   ${created.run.id}`);
  const prev = loadState(args.stateFile);
  saveState(args.stateFile, {
    agentId,
    runId: created.run.id,
    repo: prev?.repo ?? args.repo,
    branch: prev?.branch ?? args.branch,
    taskId: prev?.taskId ?? args.taskId,
    url: prev?.url,
    workOnCurrentBranch: true,
    autoCreatePR: false,
    updatedAt: new Date().toISOString(),
  });
  if (args.wait) await waitForRun(agentId, created.run.id, args.branch);
}

async function status(args: Args): Promise<void> {
  const agentId = resolveAgentId(args);
  const agent = await api<ApiAgent>("GET", `/agents/${agentId}`);
  console.log(`agent:  ${agent.id}  (${agent.status})`);
  console.log(`name:   ${agent.name ?? ""}`);
  if (agent.url) console.log(`url:    ${agent.url}`);
  console.log(`workOnCurrentBranch=${agent.workOnCurrentBranch} autoCreatePR=${agent.autoCreatePR}`);
  const ref = agent.repos?.[0];
  if (ref) {
    console.log(`repo:   ${ref.url}  startingRef=${ref.startingRef ?? ""}  prUrl=${ref.prUrl ?? ""}`);
  }
  const runId = agent.latestRunId;
  if (!runId) {
    console.log("No runs yet.");
    return;
  }
  const run = await api<ApiRun>("GET", `/agents/${agentId}/runs/${runId}`);
  console.log(`run:    ${run.id}  status=${run.status}`);
  if (run.result) console.log(run.result);
  printGit(run.git, args.branch);
}

const args = parseArgs(process.argv);
if (args.command === "launch") await launch(args);
else if (args.command === "follow") await follow(args);
else await status(args);
