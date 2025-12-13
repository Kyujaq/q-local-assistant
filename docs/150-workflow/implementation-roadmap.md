# Assistant Implementation Roadmap – Checklist

## Legend

- **ID** – stable reference for issues / PRs
- **Depends On** – main components or other tasks
- **Status** – you tick these in GitHub as you implement

## 🟢 Tier 1 – Core Assistant MVP

Goal: voice → assistant → voice loop, with basic memory and tasks.

| ID | Category | Feature | Description | Depends On | Status |
|---|---|---|---|---|---|
| T1-01 | Core Infra | Base repo & env | Create repo, basic folder structure, Docker/venv, config management. | – | [ ] |
| T1-02 | LLM Core | Local reasoning model | Run the largest local model you can reliably use (e.g. 7B–14B) via vLLM/LM Studio/etc. | GPU, model weights | [ ] |
| T1-03 | Orchestrator | Request/response router | Single entrypoint that takes user input, calls LLM, returns response. | T1-02 | [ ] |
| T1-04 | STT | Whisper speech-to-text | Voice input → text (CLI or simple API wrapper). | Audio input path | [ ] |
| T1-05 | TTS | GLaDOS voice output | Text → speech using Piper (or similar) with GLaDOS-like voice. | Audio output path | [ ] |
| T1-06 | Turn Loop | Voice loop (STT → LLM → TTS) | End-to-end pipeline from microphone to reply in voice. | T1-03, T1-04, T1-05 | [ ] |
| T1-07 | Memory (Letta v0) | Basic episodic memory | Store/retrieve simple "episodes" (notes, preferences) via Letta. | Letta service, T1-03 | [ ] |
| T1-08 | Notes & To-Dos | Simple note/task capture | "Remember this" / "Add a todo" → saved to local DB or file. | T1-03, T1-07 | [ ] |
| T1-09 | ADHD-Friendly Prompts | Recap & clarification style | LLM prompt tuned to recap, clarify, avoid dropping context. | T1-02 | [ ] |
| T1-10 | Personality | GLaDOS-lite persona | System prompt: dry, witty, helpful, short when needed (no 10-min rants). | T1-02, T1-03 | [ ] |
| T1-11 | Local Scheduler | Basic reminders | Simple scheduler (cron/task runner) to push reminders from tasks/memory. | Local DB, T1-08 | [ ] |

## 🟡 Tier 2 – Smart Assistant

Goal: real task/project management, calendar, KB, emotions, household hooks.

| ID | Category | Feature | Description | Depends On | Status |
|---|---|---|---|---|---|
| T2-01 | Tasks & Projects | Structured task DB | Tasks table (id, title, project, status, due date, tags, priority). | T1-08 | [ ] |
| T2-02 | Projects | Goal → steps breakdown | LLM helps break big goals into steps, saves to task DB. | T2-01, T1-02 | [ ] |
| T2-03 | Project Summaries | Status & recap | "What's the status of X?" → summary from tasks + memory. | T2-01, T1-07 | [ ] |
| T2-04 | Calendar Integration | External calendar sync | Connect Google/CalDAV; read/write events. | T1-11 | [ ] |
| T2-05 | Calendar Awareness | Time-aware replies | LLM sees "today's events", free/busy, and can answer schedule questions. | T2-04, T1-03 | [ ] |
| T2-06 | Emotion Detection | Mood tags from audio or text | Small model/service that infers mood (sad, stressed, tired, excited). | T1-04 | [ ] |
| T2-07 | Emotion-Aware Style | Tone-modulated responses | Orchestrator passes mood tags to LLM → different tone (gentle, concise, etc.). | T2-06, T1-03, T1-10 | [ ] |
| T2-08 | KB Ingest | Document ingestion & parsing | Import PDFs/docs/notes; extract text and store. | File system | [ ] |
| T2-09 | KB Search (RAG) | Embeddings & retrieval | Build local vector index; allow "search my docs on X". | T2-08, embeddings model | [ ] |
| T2-10 | Work Support | Summaries & action items from docs/meetings | LLM reads docs/notes and produces summaries, risks, action items. | T2-09, T1-02 | [ ] |
| T2-11 | Household – Meals | Meal planning + inventory | Integrate Paprika/kitchen-API; suggest meals, track ingredients. | Paprika API / custom service | [ ] |
| T2-12 | Household – Maintenance | Maintenance & warranty tracking | DB of appliances & recurrent tasks; reminders via scheduler. | T1-11 | [ ] |
| T2-13 | Contacts DB | Basic CRM | Contact table (name, relation, notes, birthdays). | Local DB | [ ] |
| T2-14 | Social Support | Relationship-aware replies | Use contact info + Letta to tailor responses/recs about people. | T2-13, T1-07, T1-02 | [ ] |
| T2-15 | Proactive Alerts (Basic) | Upcoming deadlines & events prompts | Background job that surfaces "3 deadlines this week"-type alerts. | T2-01, T2-04, T1-11 | [ ] |

## 🔴 Tier 3 – Next-Gen Personal Assistant

Goal: proactive, identity-aware, schedule-shuffling, "bigger than its size" assistant.

| ID | Category | Feature | Description | Depends On | Status |
|---|---|---|---|---|---|
| T3-01 | Identity Model | Long-term Q profile | Aggregated model of your values, habits, preferences, goals (read-only profile used to condition responses). | T1-07, T2-01, T2-13 | [ ] |
| T3-02 | Advanced Proactivity | Daily "What matters today?" brief | Background agent checks tasks, calendar, KB, and crafts a brief prioritized daily summary. | T2-01, T2-04, T2-09, T3-01, T1-02 | [ ] |
| T3-03 | Proactive Schedule Management | Reschedule & shuffle intelligently | Detect overload/conflicts, propose or auto-shuffle events/tasks based on priorities, energy, constraints. | T2-01, T2-04, T3-01, T2-06 | [ ] |
| T3-04 | Energy & Mood-Aware Planning | Adjust tasks by energy level | Use mood + time-of-day patterns to suggest "light" vs "heavy" tasks; adjust schedule accordingly. | T2-06, T2-01, T3-01 | [ ] |
| T3-05 | Information Triage | Automatic info filing | Ingest new info (links, notes, emails) and auto-tag/place into KB, with occasional confirmations. | T2-08, T2-09 | [ ] |
| T3-06 | Subscription Management | Subscriptions DB & nudges | Track recurring subscriptions; proactively flag unused or price-changed ones. | Financial/ subscription DB, T2-15 | [ ] |
| T3-07 | Advanced CRM | Rich person profiles | Interaction history, preferences, topics to revisit; helps prep for calls/meetings. | T2-13, T1-07, T2-09 | [ ] |
| T3-08 | Mode System | Work / Chill / Parent / Show GLaDOS modes | Switch persona & priorities depending on context or explicit command. | T1-10, T3-01, T1-03 | [ ] |
| T3-09 | Multi-Modal Reasoning | Vision-in-the-loop | Use cameras/screenshots (YOLO/VL model) as extra input for context ("what's on my screen?", "what's on table?"). | Vision models, T1-03, T1-02 | [ ] |
| T3-10 | Ownership & Discretion | Safe autonomous execution | Clear policies for which tasks the assistant can handle fully vs must confirm; implemented as rules in orchestrator. | T2-01, T2-04, T3-01 | [ ] |
| T3-11 | Deep Continuity | Cross-month narrative tracking | Letta + identity model work together so projects and life arcs keep continuity across months. | T3-01, T1-07 | [ ] |

## Bonus: Simple "Modules" Table (Optional for README)

You can also add this as a quick reference section for the repo:

## Core Modules Overview

| Module          | Role                                              |
|-----------------|---------------------------------------------------|
| orchestrator    | Routes input → tools → LLM → output.              |
| llm-core        | Local main reasoning model (vLLM/LM Studio/etc.). |
| stt-service     | Whisper-based speech-to-text.                     |
| tts-service     | Piper / GLaDOS voice.                             |
| memory-letta    | Episodic & long-term personalized memory.         |
| task-service    | Tasks & projects DB API.                          |
| calendar-bridge | Calendar integration (Google/CalDAV).            |
| kb-service      | Document ingest, embeddings, retrieval.           |
| emotion-service | Mood estimation from audio/text.                  |
| proactive-agent | Background jobs for alerts & schedule proposals.  |
| household-api   | Paprika, home automation, inventory links.        |
| contacts-api    | Simple CRM/contacts database.                     |
