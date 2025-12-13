# Letta Code Examples

Copy-paste ready examples for common Letta operations.

## Running the Examples

Make sure Letta server is running:
```bash
letta server start
```

Then run an example:
```bash
python minimal-agent.py
```

## Examples

### [minimal-agent.py](minimal-agent.py)
**Simplest possible agent**: Create agent, have a conversation, delete agent.

**Use when**: You want to understand the absolute basics.

```bash
python minimal-agent.py
```

### [agent-with-tools.py](agent-with-tools.py)
**Agent with custom tools**: File operations and git status tools.

**Use when**: You need to give agents custom capabilities.

```bash
python agent-with-tools.py
```

### [client-usage.py](client-usage.py)
**Comprehensive API demo**: Shows all common operations.

**Use when**: You need examples of specific API calls.

```bash
python client-usage.py
```

## Quick Start Template

```python
from letta_client import Letta

client = Letta(base_url="http://localhost:8283")

# 1. Create tools (if needed)
tool = client.tools.upsert_from_function(func=your_function)

# 2. Create agent
agent = client.agents.create(
    name="agent_name",
    model="openai/gpt-4o-mini",
    embedding="openai/text-embedding-3-small",
    memory_blocks=[
        {"label": "human", "value": "User info"},
        {"label": "persona", "value": "Agent role"}
    ],
    tool_ids=[tool.id],
    tags=["your-tag"]
)

# 3. Send message
response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "Hello!"}],
    stream=False
)

# 4. Process response
for msg in response.messages:
    if msg.role == "assistant":
        print(msg.content)

# 5. Cleanup
client.agents.delete(agent_id=agent.id)
client.tools.delete(tool_id=tool.id)
```

## Testing Your Setup

Run `minimal-agent.py` to verify:
- ✅ Letta server is running
- ✅ Python client works
- ✅ Models are configured
- ✅ Basic agent operations work

```bash
python minimal-agent.py
```

Expected output:
```
Created agent: agent-123
Name: minimal_agent
Model: openai/gpt-4o-mini

User: Hello! What's my name?
Agent: Hi Alex! How can I help you today?

...

Deleting agent agent-123...
Done!
```

## Common Issues

### "Connection refused"
- Letta server not running: `letta server start`
- Wrong URL: Check `base_url` parameter

### "Model not found"
- Model not configured in Letta server
- Check available models: `client.models.list()`

### "Tool function missing type hints"
- All parameters and return type need type hints
- See [tool-development.md](../tool-development.md)

## Next Steps

- Modify examples for your use case
- Read [agent-configuration.md](../agent-configuration.md) for agent setup details
- Read [tool-development.md](../tool-development.md) for custom tools
- Read [memory-system.md](../memory-system.md) for memory management
