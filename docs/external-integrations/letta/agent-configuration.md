# Letta Agent Configuration

## Creating an Agent (Python Client)

```python
from letta_client import Letta

# Connect to Letta server
client = Letta(base_url="http://localhost:8283")

# Create an agent
agent = client.agents.create(
    name="my_agent",
    model="openai/gpt-4o-mini",  # Format: provider/model-name
    embedding="openai/text-embedding-3-small",  # For memory search
    memory_blocks=[
        {
            "label": "human",
            "value": "User's name is Alex. Prefers Python."
        },
        {
            "label": "persona",
            "value": "I am a helpful coding assistant."
        }
    ],
    tool_ids=[],  # List of tool IDs to attach
    tags=["dev", "agent"],  # For filtering/organization
)

print(f"Created agent: {agent.id}")
```

## Agent Configuration Fields

### Required
- `model`: LLM model (format: `provider/model-name`)
- `embedding`: Embedding model for memory search

### Optional but Recommended
- `name`: Human-readable name
- `memory_blocks`: List of initial memory blocks
- `tool_ids`: Tools the agent can use
- `system`: Custom system prompt (default provided)
- `agent_type`: `"letta_v1_agent"` (default), `"memgpt_v2_agent"`, etc.

### Advanced
- `include_base_tools`: `True` to include core memory tools (default: `True`)
- `tags`: For filtering agents
- `timezone`: Agent's timezone (IANA format, e.g., "America/Los_Angeles")
- `llm_config`: Detailed LLM configuration (use `model` field instead)
- `embedding_config`: Detailed embedding config (use `embedding` field instead)

## Agent Types

| Type | Description | Use Case |
|------|-------------|----------|
| `letta_v1_agent` | Default, optimized for conversations | Most agents |
| `memgpt_v2_agent` | Legacy MemGPT v2 behavior | Compatibility |
| `react_agent` | ReAct reasoning pattern | Complex reasoning tasks |

**Recommendation**: Use `letta_v1_agent` (default) unless you have specific needs.

## Memory Blocks

Memory blocks are always in-context and visible to the agent. Common patterns:

```python
memory_blocks=[
    {
        "label": "human",      # About the user
        "value": "Name: Alex, Role: Developer"
    },
    {
        "label": "persona",    # Agent's personality
        "value": "I am a helpful assistant specializing in Python."
    },
    {
        "label": "instructions",  # Task-specific guidance
        "value": "Review code for bugs, suggest improvements."
    }
]
```

**Limits**: Each block has a character limit (default ~2000 chars). Agents can edit blocks using `core_memory_append` and `core_memory_replace` tools.

## Attaching Tools

```python
# Create a tool first (see tool-development.md)
tool = client.tools.upsert_from_function(func=my_function)

# Option 1: At agent creation
agent = client.agents.create(
    name="agent_with_tools",
    tool_ids=[tool.id],
    # ...
)

# Option 2: Attach later
client.agents.tools.attach(agent_id=agent.id, tool_id=tool.id)
```

## System Prompt

The system prompt defines agent behavior. Letta provides defaults, but you can customize:

```python
custom_system = """
You are a specialized code review agent.
Your role is to:
1. Analyze code for bugs and security issues
2. Suggest improvements
3. Explain your reasoning clearly

Use your tools to search memory and write findings.
"""

agent = client.agents.create(
    name="code_reviewer",
    system=custom_system,
    # ...
)
```

## Updating Agents

```python
# Update agent configuration
updated_agent = client.agents.update(
    agent_id=agent.id,
    name="new_name",
    # Other fields...
)
```

## Deleting Agents

```python
client.agents.delete(agent_id=agent.id)
```

## Listing Agents

```python
# List all agents
agents = client.agents.list()
for agent in agents.items:
    print(f"{agent.name}: {agent.id}")

# Filter by tags
dev_agents = client.agents.list(tags=["dev"])
```

## Agent State

When you create or retrieve an agent, you get an `AgentState` object:

```python
agent = client.agents.retrieve(agent_id="agent-123")

# Access properties
print(agent.id)
print(agent.name)
print(agent.memory.blocks)  # Memory blocks
print(agent.tools)          # Attached tools
print(agent.model)          # LLM model
```

## Best Practices for Our Project

### Dev Agents
- **Name**: Clear role (e.g., "orchestrator", "coder-primary")
- **Memory**: Role-specific instructions in "persona" block
- **Tools**: Only tools needed for that role (git, file ops, test runner)
- **Tags**: `["dev", "role_name"]`

### Prod Agents
- **Name**: User-facing or task-specific (e.g., "home-assistant", "conversation")
- **Memory**: User preferences in "human", agent personality in "persona"
- **Tools**: Home Assistant, Paprika, web search, etc.
- **Tags**: `["prod", "capability"]`

## Troubleshooting

**"Agent not found"**: Check agent ID matches exactly (includes prefix like `agent-`)

**"Tool not found"**: Ensure tool is created before attaching to agent

**"Memory block too large"**: Split content across multiple blocks or use archival memory

## Links

- [Official Agent API Docs](https://docs.letta.com/api-reference/agents)
- [tool-development.md](tool-development.md) - Creating tools
- [memory-system.md](memory-system.md) - Understanding memory
