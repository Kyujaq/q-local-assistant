# GitHub Copilot Instructions for q-local-assistant

## Project Overview

This is a local-first home assistant with reasoning, memory, voice/vision, and Home Assistant integration. The codebase is **documentation-driven**: all decisions live in `docs/`, not chat history.

**Three-Phase Architecture:**

1. **Bootstrap Phase (GitHub Copilot - NOW)**: You help create the infrastructure for self-hosted development—Letta agent configs, dev tools, framework setup
2. **Self-Hosted Dev (Letta on PC)**: Dev agents (Orchestrator, Coder, Tester, etc.) build the assistant following Architect's plans
3. **Production Assistant (Letta on glad0s)**: The final product—runtime agents that interact with users and home systems

**Critical Distinction:**
- **Dev system** (`docs/dev-*`, `src/dev_agents/`, `src/dev_tools/`): Self-hosted development team that builds the assistant
- **Runtime system** (`docs/prod-*`, `src/prod_agents/`, `src/prod_tools/`): The assistant itself—user-facing Letta agents

## Your Role: Bootstrapping Self-Hosted Development

**Goal**: Minimize reliance on paid services by creating self-hosted dev infrastructure.

Your job is to help build the foundation so Letta dev agents can take over:
- Create Letta agent configurations based on `docs/dev-300-agents/` playbooks
- Build tools that dev agents will use (git operations, file I/O, test runner)
- Set up the framework for both Letta instances (dev on PC, prod on glad0s)
- Document everything so the system is self-sustaining

**End State**: Letta dev agents on PC build the assistant autonomously, with only the Architect potentially remaining external (for now).

## Documentation Architecture

The `docs/` folder is the single source of truth:

```
docs/
├── dev-100-architecture/     # Dev team system design
├── dev-150-workflow/         # Branching, context management, project philosophy
├── dev-200-features/         # Feature specs with decision logs
├── dev-300-agents/           # Dev agent playbooks → translate to src/dev_agents/
├── dev-daily-logs/           # Development activity logs
├── prod-100-architecture/    # Assistant runtime architecture
├── prod-200-components/      # Runtime services & modules
├── prod-300-agents/          # Runtime agent specs → translate to src/prod_agents/
├── prod-400-integrations/    # External system integrations (Home Assistant, Paprika)
├── prod-500-behaviors/       # User-facing behaviors
└── coding-standards.md       # Code style, formatting, testing requirements

src/
├── dev_agents/               # Letta agent configs for dev team (PC)
├── dev_tools/                # Tools for dev agents (git, file ops, testing)
├── prod_agents/              # Letta agent configs for assistant (glad0s)
├── prod_tools/               # Tools for assistant (Home Assistant, Paprika, etc.)
├── common/                   # Shared infrastructure (Letta client, config, logging)
└── services/                 # Supporting services for runtime
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

**Three-Phase Progression:**

```
┌─────────────────────────────────────────────────────────┐
│ PHASE 1: Bootstrap (GitHub Copilot)                     │
│ Creates: Agent configs, dev tools, framework            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ PHASE 2: Self-Hosted Dev (Letta on PC)                 │
│ - Orchestrator, Coder, Tester, Doc Specialist, Reviewer │
│ - Builds prod_agents/ and prod_tools/                   │
│ - Night crew runs heavy dev tasks                       │
│ - Architect: External (biggest model) or local later    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ PHASE 3: Production Assistant (Letta on glad0s)        │
│ - Runtime agents for user interactions                  │
│ - Home Assistant, Paprika, voice, vision integrations  │
│ - Proactive behaviors, memory, reasoning                │
└─────────────────────────────────────────────────────────┘
```

**Hardware:**
- **PC**: High-performance (RTX 4070 Ti Super), hosts Letta dev instance, runs coding models; may be busy/asleep
- **Server (glad0s)**: Always-on (GTX 1070 + K80), hosts Letta prod instance (the assistant), Home Assistant integrations, night crew executor

**Model Slots:**
- Slot S (~7B): Fast reactions, routing, lightweight tasks
- Slot M (~14–30B): Core reasoning (preferred from PC when idle)
- Slot L (Large): Deep reasoning, planning, Architect role (PC or external)

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

**Code Structure Example**:
```python
# src/dev_tools/file_operations.py
"""File operations tool for Letta dev agents."""

from typing import Dict, List, Optional
from pathlib import Path

def read_file(
    file_path: str,
    start_line: Optional[int] = None,
    end_line: Optional[int] = None
) -> str:
    """Read file contents for dev agent.
    
    Args:
        file_path: Absolute path to file
        start_line: Optional starting line (1-indexed)
        end_line: Optional ending line (inclusive)
        
    Returns:
        File contents as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    content = path.read_text()
    if start_line is not None and end_line is not None:
        lines = content.splitlines()
        return "\n".join(lines[start_line-1:end_line])
    return content
```

```python
# src/prod_tools/home_assistant.py
"""Home Assistant integration tool for production assistant."""

from typing import Dict, Any
import aiohttp

async def turn_on_light(
    entity_id: str,
    brightness: Optional[int] = None
) -> Dict[str, Any]:
    """Turn on a light via Home Assistant API.
    
    Args:
        entity_id: Home Assistant entity (e.g., 'light.living_room')
        brightness: Optional brightness 0-255
        
    Returns:
        API response with new state
    """
    # Implementation for production assistant
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

## Bootstrap Phase Tasks (Your Current Mission)

As GitHub Copilot, you're helping build the foundation for self-hosted development:

**Priority 1: Dev Agent Infrastructure**
- [ ] Create base classes for Letta agent configuration
- [ ] Translate `docs/dev-300-agents/*.md` playbooks into `src/dev_agents/*.py` configs
- [ ] Build core dev tools: file operations, git operations, test runner
- [ ] Set up Letta client wrapper in `src/common/letta_client.py`

**Priority 2: Framework & Testing**
- [ ] Establish Python environment (pyproject.toml, requirements.txt)
- [ ] Create test infrastructure (conftest.py, fixtures)
- [ ] Build first end-to-end test: Can Letta dev agent read a file?

**Priority 3: Night Crew Automation**
- [ ] Script to trigger Letta dev agents on nightly/* branches
- [ ] Result collection and commit automation
- [ ] Daily log generation

**When Bootstrap Complete**: Letta dev agents take over, building `src/prod_agents/` and `src/prod_tools/` autonomously.

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
