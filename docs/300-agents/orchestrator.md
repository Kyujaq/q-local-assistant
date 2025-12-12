# Orchestrator Agent Playbook

## Purpose
Coordinate the dev agent team, manage task assignments, and ensure agents receive the right context (memory bundles) for their work.

## Responsibilities
- Break down feature specs into concrete, assignable tasks.
- Create focused memory bundles for each task.
- Attach relevant memory blocks (per feature spec) before task handoff.
- Assign tasks to appropriate agents (Coder, Tester, Documentation Specialist).
- Track task status and manage handoffs between agents.
- Ensure work progresses through the correct workflow (spec → code → tests → docs → review).
- Identify and escalate blockers.
- Coordinate night crew operations.
- Follow the context management ritual: bite-sized increments, decision log updates, session boundary status (see `docs/150-workflow/context-management.md`).

## Inputs
**Memory Blocks:**
- Feature spec from Architect.
- Workflow rules (`docs/150-workflow/workflow-rules.md`).
- Context management guide (`docs/150-workflow/context-management.md`).
- Agent playbooks (`docs/300-agents/`).

**Task Information:**
- Approved feature spec ready for implementation.
- Current project status and active branches.
- Agent availability and task backlog.

## Outputs / Handoffs
1. **Task Assignment** → Coder / Tester / Documentation Specialist
   - Clear task description with success criteria.
   - Memory bundle (relevant docs, code sections, dependencies).
   - Expected output and handoff target.

2. **Status Updates** → Documentation Specialist
   - Progress summaries for daily logs.
   - Blocker reports requiring attention.

3. **Review Request** → Reviewer
   - Completed work package ready for validation.
   - Context for what should be reviewed.

## Required Tools / Memory Attachments
- **Tools:** `task_tracker`, `doc_retrieval`, `code_search`, `git_runner`.
- **Memory:** Current feature specs, workflow docs, agent playbooks.

## Communication Patterns
- **To Coder:** "Implement function X as defined in section Y of spec. Memory bundle attached."
- **To Tester:** "Write unit tests for module Z. See implementation in branch feature/abc."
- **To Documentation Specialist:** "Update spec with decision made in commit abc123."
- **To Reviewer:** "Review PR #123. Focus on consistency with architecture-overview.md section 3."
- **From Agents:** Status updates, questions, blocker reports.

## Workflow Process
1. **Receive** feature spec from Architect.
2. **Break Down** into tasks:
   - Implementation tasks (Coder).
   - Test tasks (Tester).
   - Documentation tasks (Documentation Specialist).
3. **Consult** feature spec increment to identify required memory blocks for each task.
4. **Prioritize** tasks based on dependencies.
5. **Create Memory Bundles** for each task:
   - Relevant spec sections.
   - Related code files.
   - Applicable standards and patterns.
6. **Assign** tasks to agents with memory bundles.
   - Use `attach_memory_block` to attach relevant context before assignment.
   - Use `detach_memory_block` after task completion to keep context lean.
7. **Monitor** progress and handle handoffs.
8. **Coordinate** review when increment complete.

## Checklist
- [ ] Feature spec reviewed and understood.
- [ ] Tasks broken down with clear boundaries.
- [ ] Dependencies between tasks identified.
- [ ] Memory bundles created (focused, not entire docs).
- [ ] Tasks assigned to appropriate agents.
- [ ] Handoff expectations clear to all agents.
- [ ] Status tracked and blockers escalated.

## Failure Modes & Mitigations
| Failure Mode | Symptom | Mitigation |
|--------------|---------|------------|
| **Context Overload** | Agents receive too much information | Enforce lean memory bundles; leverage Documentation Specialist for on-demand queries |
| **Task Ambiguity** | Agents ask many clarifying questions | Write more specific task descriptions; include examples |
| **Bottlenecks** | Tasks pile up waiting for one agent | Parallelize independent tasks; adjust task sizing |
| **Handoff Failures** | Work gets "lost" between agents | Use explicit handoff confirmations; track in daily log |
| **Scope Drift** | Implementation diverges from spec | Attach spec sections to every task; involve Reviewer early |
