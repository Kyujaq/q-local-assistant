# Project Philosophy

## Core Goals
- Build a personal assistant that integrates deeply into home and daily life, with reasoning, proactive behavior, memory, voice, and vision capabilities.
- Maintain a high standard of clarity and maintainability in the codebase so the system can evolve safely over years.

## Fundamental Principles

### 1. Documentation as Memory
All important decisions live in the repository.
LLMs must rely on documentation, **not** previous chat sessions.

### 2. Maintainability over Speed
For development:
- Clarity > robustness > speed > cleverness.
- No spaghetti code or shortcuts that create future complications.
- Every feature implemented with a spec, plan, and tests.

For the assistant runtime:
- Responsiveness is essential.
- The system may use "thinking acknowledgements" to stay responsive.

### 3. Local-First, Secure-by-Default
- The system runs primarily on local hardware.
- Online access is strictly controlled and allowed only for necessary integrations (email, Paprika, calendar, search).
- Sensitive or private data should not leave local systems unless explicitly required.

### 4. Clean Separation of Concerns
- Dev agents and coding models belong to the *development environment*.
- Letta agents and the orchestrator belong to the *assistant runtime*.
- They interact only through code, tests, and automation—not conversationally.

### 5. Automation as a First-Class Citizen
- Night crew and dev agents are part of the project architecture, not add-ons.
- Automated refactoring, testing, and documentation ensure consistency and reduce cognitive load.
- Automation must follow the same standards as human work.

### 6. Stable Execution Environment
- Server is the runtime heart; PC provides compute but may sleep or be busy.
- System must gracefully fall back to suitable model slots as needed.

### 7. Long-Term Sustainability
- Code, tests, and docs should be written to remain understandable months or years in the future.
- Decisions recorded in docs prevent drift, confusion, and hallucination.
- Architecture should support incremental improvements without rewriting the system.