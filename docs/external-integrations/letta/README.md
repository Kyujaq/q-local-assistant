# Letta Integration Documentation

**Version Tracking**: (To be determined - check `letta --version`)  
**Official Docs**: https://docs.letta.com/  
**GitHub**: https://github.com/letta-ai/letta

## What is Letta?

Letta (formerly MemGPT) is a platform for building stateful AI agents with advanced memory systems. Key features:
- **Persistent Memory**: Core memory (in-context), Recall memory (conversation history), Archival memory (long-term storage)
- **Tool Calling**: Agents can use custom Python tools/functions
- **Stateful Execution**: Agents maintain state across sessions
- **Self-Editing Memory**: Agents can modify their own memory blocks

## Quick Links

- [Agent Configuration](agent-configuration.md) - How to create and configure Letta agents
- [Tool Development](tool-development.md) - Building custom tools for agents
- [Memory System](memory-system.md) - Understanding Letta's memory architecture
- [API Quick Reference](api-quickref.md) - Common API calls we use
- [Code Examples](code-examples/) - Working examples for common patterns

## Our Use Case

We use Letta for two separate systems:

1. **Dev Agents (PC)**: Orchestrator, Coder, Tester, Doc Specialist, Reviewer
2. **Prod Agents (glad0s)**: The assistant itself - user-facing runtime agents

Both use Letta's agent + tool framework, but serve different purposes.

## Installation

```bash
pip install letta
```

## Version Compatibility

**Current Target**: (TBD - document after first installation)  
**Breaking Changes**: Track here when upgrading

## Key Concepts for Our Project

- **Agent**: A Letta instance with memory, tools, and a system prompt
- **Tool**: A Python function the agent can call
- **Memory Block**: A labeled section of in-context memory (e.g., "human", "persona")
- **System Prompt**: Instructions that define agent behavior
- **Agent State**: The persistent state of an agent (ID, name, memory, tools, config)

## Next Steps

1. Read [agent-configuration.md](agent-configuration.md) to understand agent setup
2. Review [tool-development.md](tool-development.md) for tool patterns
3. Check [code-examples/](code-examples/) for copy-paste-ready code
