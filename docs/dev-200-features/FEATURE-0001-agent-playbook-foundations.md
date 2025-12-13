# FEATURE-0001: Agent Playbook Foundations

**Status:** In Progress  
**Created:** 2025-12-12  
**Owner:** System Architecture

## Overview & Goals
Establish the foundational playbooks, context management strategy, tooling requirements, and operational processes for the dev agent team. This feature sets up the framework for all subsequent development work.

### Primary Goals
1. Define and document playbooks for each dev agent role.
2. Document context-management ritual and memory-assignment process.
3. Specify tooling needs and identify any blockers.
4. Create daily log template and establish status ritual.

## Scope

### In Scope
- **Agent Playbooks**: Finalize playbooks for:
  - Architect
  - Orchestrator
  - Coder
  - Tester
  - Documentation Specialist
  - Reviewer
- **Context Management**: Document the context-management ritual and memory-assignment process (see `docs/dev-150-workflow/context-management.md`).
- **Tooling Specifications**: 
  - Define requirements for `repo_write_file`, `git_runner`, `test_runner`.
  - Document any blockers or implementation challenges.
- **Daily Log Template**: Create standardized template for daily logs.
- **Status Ritual**: Define when and how status updates are logged.

### Out of Scope
- Actual implementation of custom tools (deferred pending API resolution).
- Integration with Letta server (separate feature).
- Home Assistant integration specifics.

## Agent Roles Summary

| Role | Primary Responsibility | Key Outputs |
|------|----------------------|-------------|
| Architect | Feature planning & system design | Architecture docs, feature specs |
| Orchestrator | Task coordination & memory management | Task assignments, memory bundles |
| Coder | Code implementation | Source code, commit messages |
| Tester | Test creation & validation | Test files, test reports |
| Documentation Specialist | Docs & decision logging | Updated specs, daily logs |
| Reviewer | Quality assurance & consistency | Review reports, merge approval |

## Tooling Requirements

### Required Tools
1. **repo_write_file**: Write/modify files in the repository.
   - **Blocker**: Letta tool creation API has token/positional argument errors.
   - **Workaround**: Manual file operations during bootstrap phase.

2. **git_runner**: Execute git commands (commit, branch, merge).
   - **Status**: Can use shell commands as temporary solution.

3. **test_runner**: Execute unit and integration tests.
   - **Status**: Can use shell commands as temporary solution.

### Nice-to-Have Tools
- **code_search**: Semantic search across codebase.
- **doc_retrieval**: Fetch specific doc sections by query.

## Acceptance Criteria
- [ ] All six agent playbooks committed to `docs/300-agents/`.
- [ ] Context management doc published at `docs/150-workflow/context-management.md`.
- [ ] Tooling specifications logged with status and blockers.
- [ ] Daily log template created at `docs/daily-logs/TEMPLATE.md`.
- [ ] First daily log completed for project bootstrap phase.

## Decision Log

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| 2025-12-12 | Created numbered documentation folders (100-architecture, 150-workflow, etc.) | Provides clear ordering and logical grouping | Easier navigation and documentation discovery |
| 2025-12-12 | Agent playbooks go in docs/dev-300-agents/ | Separates agent-specific guidance from general workflows | Clear separation of concerns |
| 2025-12-12 | Defer custom tool implementation | Letta API blockers prevent immediate implementation | Focus on doc foundation, revisit tools later |

## Next Actions
1. Create individual agent playbook files in `docs/dev-300-agents/`.
2. Finalize daily log template.
3. Create first daily log summarizing bootstrap work.
4. Review and refine context-management process.

## Blockers
- Letta tool creation API errors (token/positional arguments).
- Need to validate agent playbook structure with actual usage.
