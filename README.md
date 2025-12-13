# q-local-assistant

## Development Workflow

### Branching Strategy
- **Main Branch**: `main` (protected, default branch)
- **Feature Branches**: All changes must go through `feature/<name>` branches
- Create a new feature branch for each change: `git checkout -b feature/your-feature-name`
- Submit a pull request to merge into `main`

## Project Structure

```
├── docs/
│   ├── dev-100-architecture/    # Dev team architecture
│   ├── dev-150-workflow/        # Dev team workflow guides
│   ├── dev-200-features/        # Dev system feature specs
│   ├── dev-300-agents/          # Dev team agent playbooks
│   ├── dev-daily-logs/          # Development activity logs
│   ├── prod-100-architecture/   # Assistant runtime architecture
│   ├── prod-200-components/     # Runtime services & modules
│   ├── prod-300-agents/         # Assistant runtime agents (Letta)
│   ├── prod-400-integrations/   # External system integrations
│   ├── prod-500-behaviors/      # User-facing behaviors
│   └── coding-standards.md      # Coding standards for all work
├── src/
│   ├── agents/                  # Agent implementations
│   ├── services/                # Service layer
│   └── tools/                   # Utility tools
├── tests/
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── tools/                       # Development tools
├── scripts/                     # Build and deployment scripts
└── README.md
```

### Documentation Structure

The docs folder is organized into two major categories:

**`dev-*` folders** - Development Team System
- Documentation about how we build the assistant
- Dev team agents (Orchestrator, Architect, Coder, etc.)
- Development workflows and standards
- Feature specs for dev system improvements

**`prod-*` folders** - Assistant Runtime System (The Product)
- Documentation about what we're building
- Runtime agents that will run on the assistant (Letta agents)
- System architecture and services
- User-facing behaviors and integrations