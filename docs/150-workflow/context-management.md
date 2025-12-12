# Context Management

## Purpose
Prevent context overflow and maintain clarity during long development sessions by managing what information agents load and when.

## Core Practices

### 1. Bite-Sized Increments
- Break work into small, self-contained increments.
- Each increment should include:
  - Clear goal
  - Explicit dependencies
  - Tests that validate the work
  - Clean handoff to the next agent or increment

### 2. Decision & Rationale Logging
- Every feature spec must include a **Decision Log** table.
- Format:
  ```markdown
  | Date | Decision | Rationale | Impact |
  |------|----------|-----------|--------|
  | YYYY-MM-DD | What was decided | Why this choice | What it affects |
  ```
- Log decisions immediately during development.
- Decisions live in feature specs, not just chat history.

### 3. Structured Memory Bundles
- **Orchestrator** is responsible for attaching relevant memory blocks to each task.
- Memory blocks are focused document sections or spec excerpts.
- Agents receive only what they need for their current increment.
- Prevents agents from loading entire docs unnecessarily.

### 4. Session Boundary Ritual
At the end of each work session or handoff:
1. **Status**: What was accomplished?
2. **Decisions**: What choices were made and why?
3. **Next Actions**: What's the immediate next step?
4. **Blockers**: Any obstacles that need resolution?

Document this in the relevant feature spec or daily log.

### 5. Incremental Tests + Docs in Lockstep
- Write tests as features are implemented, not after.
- Update documentation alongside code changes.
- Both tests and docs are acceptance criteria for merging.

### 6. Inter-Agent Q&A
- Agents should **ask the Documentation Specialist** for specific information.
- Avoid loading entire documentation sets.
- Doc Specialist retrieves and summarizes only what's needed.

## Memory Assignment Process
1. **Orchestrator** reviews the current task and feature spec.
2. Identifies relevant doc sections, dependencies, and context.
3. Bundles these into a focused memory package.
4. Assigns memory package + task to the appropriate agent.
5. Agent works within that focused context.

## Anti-Patterns to Avoid
- Loading all docs at once "just in case."
- Making architectural decisions without logging them.
- Completing work without handoff notes.
- Skipping tests or docs "for now" with intent to add later.
- Long sessions without status checkpoints.
