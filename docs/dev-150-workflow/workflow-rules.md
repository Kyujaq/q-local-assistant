# Workflow Rules

## Branching Strategy
- **main**: stable branch; merges require passing tests and updated documentation.
- **feature/<name>**: each feature or fix has its own branch and its own spec.
- **nightly/YYYY-MM-DD**: branches used by night crew for automated work; may contain failing tests.

## Documentation Discipline
- Every feature starts with a spec in `docs/dev-200-features/`.
- All decisions and architectural choices must be written immediately into the feature spec.
- Daily logs should extract or summarize key decisions; relevant items get merged back into feature specs.
- Architecture documents updated only for significant system-wide changes.

## Development Cycle
1. Write or update feature spec.
2. Architect agent refines plan.
3. Implement feature in small, testable increments.
4. Write tests (unit first, integration when needed).
5. Commit using conventional commit messages.
6. Merge only when docs + tests are updated.

## Testing Requirements
- **Unit tests**: Required for all features.
- **Integration tests**: Required when features affect orchestrator/agent interactions or external systems.
- **Night crew**: Runs both unit and integration tests where applicable.

## Night Crew Behavior
- Operates only on nightly branches.
- Allowed to push code even if tests fail, but never to main.
- Must produce:
  - code changes (committed to nightly branch)
  - test results
  - nightly summary written into `docs/dev-daily-logs/`
- Server controls night jobs; PC provides compute via coding models.

## Dev Agents
- Architect: plans features.
- Orchestrator: receives plan from Architect and makes sure the team apply it correctly to get thee expected output
- Coder: generates/refactors code.
- Tester: creates & runs tests.
- Documentation Specialist: updates feature specs & logs.
- Reviewer: validates consistency between agents and plans.