# GitHub Copilot Instructions for q-local-assistant

## Project Overview

This is a local-first home assistant with reasoning, memory, voice/vision, and Home Assistant integration. The codebase is **documentation-driven**: all decisions live in `docs/`, not chat history.

**Critical Distinction:**
- **Dev system** (`docs/dev-*`): Development agents, workflows, and how we build the assistant
- **Runtime system** (`docs/prod-*`): The assistant itself—Letta agents, orchestrator, behaviors, integrations

## Documentation Architecture

The `docs/` folder is the single source of truth:

```
docs/
├── dev-100-architecture/     # Dev team system design
├── dev-150-workflow/         # Branching, context management, project philosophy
├── dev-200-features/         # Feature specs with decision logs
├── dev-300-agents/           # Dev agent playbooks (Orchestrator, Architect, Coder, etc.)
├── dev-daily-logs/           # Development activity logs
├── prod-100-architecture/    # Assistant runtime architecture
├── prod-200-components/      # Runtime services & modules
├── prod-300-agents/          # Letta runtime agents
├── prod-400-integrations/    # External system integrations (Home Assistant, Paprika)
├── prod-500-behaviors/       # User-facing behaviors
└── coding-standards.md       # Code style, formatting, testing requirements
```

**Before implementing anything:** Read the relevant feature spec in [docs/dev-200-features](docs/dev-200-features) and check its decision log table.

## Coding Standards

**Python-only project** with strict requirements:

- **Type hints everywhere**: All functions, methods, classes, and significant variables
- **Docstrings required**: Every module, class, and public function
- **Code quality tools**: Ruff (linting) → Black (formatting) before merging
- **Function size**: <80 lines preferred unless justified
- **Module size**: <500 lines preferred unless domain requires more
- **Clarity principle**: Clarity > robustness > speed > cleverness

**Commit message format:**
```
feat(module): summary
fix(module): summary
refactor(module): summary
```

See [docs/coding-standards.md](docs/coding-standards.md) for complete standards.

## Development Workflow

**Branching:**
- `main`: Protected, stable
- `feature/<name>`: All development work
- `nightly/YYYY-MM-DD`: Night crew branches (may contain failing tests)

**Process:**
1. Start with or create feature spec in `docs/dev-200-features/`
2. Log all decisions in the spec's decision log table immediately:
   ```markdown
   | Date | Decision | Rationale | Impact |
   ```
3. Implement in small increments with tests alongside code
4. Update docs in lockstep with code changes
5. Commit only when tests + docs are complete

**Tests:**
- Unit tests: `tests/unit/` (required for all features)
- Integration tests: `tests/integration/` (required for orchestrator/agent interactions or external systems)

See [docs/dev-150-workflow](docs/dev-150-workflow) for complete workflow rules.

## Context Management

**Prevent context overflow** by working in bite-sized increments:

1. **Load only what you need**: Don't read entire docs—target specific sections
2. **Log decisions immediately**: Update the feature spec decision log as you make choices
3. **Session boundary ritual**: At handoffs, document status, decisions, next actions, and blockers
4. **Tests + docs in lockstep**: Don't defer either to "later"

Each feature spec increment specifies required memory blocks (which docs/sections are needed). Stick to your assigned increment.

See [docs/dev-150-workflow/context-management.md](docs/dev-150-workflow/context-management.md) for the complete ritual.

## Project Philosophy

**Core principles** (read [docs/dev-150-workflow/project-philosophy.md](docs/dev-150-workflow/project-philosophy.md)):

1. **Documentation as Memory**: LLMs rely on repo docs, not previous chats
2. **Maintainability over Speed**: No shortcuts, no spaghetti code
3. **Local-First, Secure-by-Default**: Runs on local hardware, online access strictly controlled
4. **Clean Separation**: Dev agents vs. runtime agents—they don't "talk" except via code/tests
5. **Automation First-Class**: Night crew and agents follow same standards as humans
6. **Long-Term Sustainability**: Code must remain understandable months/years later

## Architecture Quick Reference

**Hardware:**
- **Server (glad0s)**: Always-on (GTX 1070 + K80), runs core orchestrator, Letta agents, Home Assistant integrations, night crew executor
- **PC**: High-performance (RTX 4070 Ti Super), runs coding models, dev agents, heavy offline tasks; may be busy/asleep

**Model Slots:**
- Slot S (~7B): Fast reactions, routing, lightweight tasks
- Slot M (~14–30B): Core reasoning (preferred from PC when idle)
- Slot L (Large): Deep reasoning, planning, night jobs (PC only)

See [docs/dev-100-architecture/architecture-overview.md](docs/dev-100-architecture/architecture-overview.md) for complete architecture.

## Key Patterns & Examples

**Decision Logging** (mandatory for all non-trivial choices):
```markdown
| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| 2025-12-13 | Use Pydantic for config validation | Type safety + clear errors | All config modules |
```

**Feature Spec Increments** (from [docs/dev-300-agents/architect.md](docs/dev-300-agents/architect.md)):
Each increment includes:
- Goal: Clear, specific objective
- Dependencies: What must be completed first
- Tests: Expected test cases
- Handoffs: Who's next and what they need
- Decision Log Entry: Key design decisions
- Memory Blocks: Required docs/sections (e.g., "auth-design.md sections 2-3")

**Code Structure Example** (hypothetical—`src/` is currently empty):
```python
"""Module docstring explaining purpose."""

from typing import Dict, List, Optional

def process_user_input(
    text: str,
    context: Optional[Dict[str, str]] = None
) -> List[str]:
    """Process user input and return action list.
    
    Args:
        text: Raw user input string
        context: Optional context dictionary with previous state
        
    Returns:
        List of action strings to execute
    """
    # Clear intent comment for non-obvious logic
    ...
```

## Common Anti-Patterns to Avoid

- Loading entire docs "just in case" → Load targeted sections only
- Making architectural decisions without logging them → Update decision log immediately
- Completing work without handoff notes → Follow session boundary ritual
- Skipping tests/docs "for now" → Tests and docs are acceptance criteria
- Implementing beyond assigned increment → Stick to scope, propose extras separately
- Clever, compact code → Prioritize clarity and maintainability

## Integration Points

**External Systems:**
- Home Assistant (sensor/event/control layer)
- Paprika (recipes, pantry, groceries)
- Cameras / screen-watch services
- Tailscale (secure access to satellites/mobile)

See [docs/prod-400-integrations](docs/prod-400-integrations) for integration details.

## Quick Start Checklist

When starting work on this codebase:

- [ ] Read [docs/dev-150-workflow/project-philosophy.md](docs/dev-150-workflow/project-philosophy.md)
- [ ] Review [docs/coding-standards.md](docs/coding-standards.md)
- [ ] Check relevant feature spec in [docs/dev-200-features](docs/dev-200-features)
- [ ] Consult the feature spec's decision log for context
- [ ] Identify your assigned increment and required memory blocks
- [ ] Set up Ruff and Black in your environment
- [ ] Create feature branch: `git checkout -b feature/<name>`
- [ ] Write tests alongside code (never defer)
- [ ] Update decision log immediately when making choices
- [ ] Follow session boundary ritual at handoffs

## Need More Context?

- Architecture overview: [docs/dev-100-architecture/architecture-overview.md](docs/dev-100-architecture/architecture-overview.md)
- Agent playbooks: [docs/dev-300-agents](docs/dev-300-agents) (Orchestrator, Architect, Coder, Tester, Reviewer, Documentation Specialist)
- Workflow rules: [docs/dev-150-workflow/workflow-rules.md](docs/dev-150-workflow/workflow-rules.md)
- Context management: [docs/dev-150-workflow/context-management.md](docs/dev-150-workflow/context-management.md)
- Active features: [docs/dev-200-features](docs/dev-200-features)
- Daily logs: [docs/dev-daily-logs](docs/dev-daily-logs)
