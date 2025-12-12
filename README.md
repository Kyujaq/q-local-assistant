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
│   ├── 100-architecture/    # Architecture documentation
│   ├── 150-workflow/         # Workflow guides
│   ├── 200-features/         # Feature documentation
│   ├── 300-agents/           # Agent-specific docs
│   └── daily-logs/           # Development logs
├── src/
│   ├── agents/               # Agent implementations
│   ├── services/             # Service layer
│   └── tools/                # Utility tools
├── tests/
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── tools/                    # Development tools
├── scripts/                  # Build and deployment scripts
└── README.md
```