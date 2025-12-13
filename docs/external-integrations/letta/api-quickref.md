# Letta API Quick Reference

Common API calls you'll use frequently. See [agent-configuration.md](agent-configuration.md), [tool-development.md](tool-development.md), and [memory-system.md](memory-system.md) for detailed explanations.

## Client Setup

```python
from letta_client import Letta

# Local development
client = Letta(base_url="http://localhost:8283")

# With authentication
client = Letta(
    base_url="http://your-server:8283",
    token="your-api-token"
)
```

## Agents

### Create Agent
```python
agent = client.agents.create(
    name="agent_name",
    model="openai/gpt-4o-mini",
    embedding="openai/text-embedding-3-small",
    memory_blocks=[
        {"label": "human", "value": "User info"},
        {"label": "persona", "value": "Agent personality"}
    ],
    tool_ids=[],
    tags=["tag1", "tag2"]
)
```

### Get Agent
```python
agent = client.agents.retrieve(agent_id="agent-id")
```

### List Agents
```python
agents = client.agents.list()
for agent in agents.items:
    print(f"{agent.name}: {agent.id}")
```

### Update Agent
```python
agent = client.agents.update(
    agent_id="agent-id",
    name="new_name",
    tags=["updated"]
)
```

### Delete Agent
```python
client.agents.delete(agent_id="agent-id")
```

## Messages (Agent Interaction)

### Send Message
```python
response = client.agents.messages.create(
    agent_id="agent-id",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=False
)

# Response structure
print(response.messages)  # List of message objects
```

### Streaming Response
```python
for chunk in client.agents.messages.create(
    agent_id="agent-id",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
):
    print(chunk, end="", flush=True)
```

## Tools

### Create Tool from Function
```python
def my_function(param: str) -> str:
    """Function description."""
    return f"Result: {param}"

tool = client.tools.upsert_from_function(
    func=my_function,
    tags=["my-tag"]
)
```

### Get Tool
```python
tool = client.tools.retrieve(tool_id="tool-id")
```

### List Tools
```python
# All tools
tools = client.tools.list()

# Filter by name
tools = client.tools.list(name="my_function")

# Filter by tags
tools = client.tools.list(tags=["file-ops"])
```

### Attach Tool to Agent
```python
client.agents.attach_tool(
    agent_id="agent-id",
    tool_id="tool-id"
)
```

### Detach Tool
```python
client.agents.detach_tool(
    agent_id="agent-id",
    tool_id="tool-id"
)
```

### Delete Tool
```python
client.tools.delete(tool_id="tool-id")
```

## Memory

### View Core Memory
```python
agent = client.agents.retrieve(agent_id="agent-id")
for block in agent.memory.blocks:
    print(f"{block.label}: {block.value}")
```

### Update Core Memory Block
```python
# Get current blocks
agent = client.agents.retrieve(agent_id="agent-id")
blocks = agent.memory.blocks

# Modify a block
for block in blocks:
    if block.label == "human":
        block.value = "Updated user info"

# Update agent
client.agents.update(
    agent_id="agent-id",
    memory_blocks=[
        {"label": b.label, "value": b.value, "limit": b.limit}
        for b in blocks
    ]
)
```

### Archival Memory: Insert
```python
client.agents.passages.create(
    agent_id="agent-id",
    text="Knowledge to store",
    tags=["category"]
)
```

### Archival Memory: Search
```python
results = client.agents.passages.search(
    agent_id="agent-id",
    query="search query",
    tags=["category"],    # Optional filter
    limit=10
)

for result in results.items:
    print(f"{result.text} (score: {result.score})")
```

### Archival Memory: List
```python
passages = client.agents.passages.list(
    agent_id="agent-id",
    tags=["category"]    # Optional filter
)
```

### Archival Memory: Delete
```python
client.agents.passages.delete(
    agent_id="agent-id",
    passage_id="passage-id"
)
```

## Tags

Tags help organize agents, tools, and memories.

### Filtering by Tags
```python
# Get all dev agents
dev_agents = client.agents.list(tags=["dev"])

# Get file operation tools
file_tools = client.tools.list(tags=["file"])

# Get project knowledge
docs = client.agents.passages.list(
    agent_id="agent-id",
    tags=["project-docs"]
)
```

## Models

### List Available Models
```python
models = client.models.list()
for model in models:
    print(f"{model.name}: {model.context_window} tokens")
```

## Common Patterns

### Initialize Agent with Tools
```python
# 1. Create tools
tool1 = client.tools.upsert_from_function(func=func1)
tool2 = client.tools.upsert_from_function(func=func2)

# 2. Create agent with tool IDs
agent = client.agents.create(
    name="my_agent",
    model="openai/gpt-4o-mini",
    embedding="openai/text-embedding-3-small",
    tool_ids=[tool1.id, tool2.id],
    memory_blocks=[...]
)
```

### Agent Conversation Loop
```python
agent_id = "agent-id"

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    
    response = client.agents.messages.create(
        agent_id=agent_id,
        messages=[{"role": "user", "content": user_input}],
        stream=False
    )
    
    for msg in response.messages:
        if msg.role == "assistant":
            print(f"Agent: {msg.content}")
```

### Pre-Load Agent Knowledge
```python
agent = client.agents.create(...)

# Insert project docs
docs = [
    ("Coding standards: PEP 8, type hints required", ["standards"]),
    ("Test framework: pytest in tests/ directory", ["standards"]),
    ("Branch: feature/* for new work", ["workflow"])
]

for text, tags in docs:
    client.agents.passages.create(
        agent_id=agent.id,
        text=text,
        tags=tags
    )
```

## Error Handling

```python
from letta_client.errors import LettaError

try:
    agent = client.agents.create(...)
except LettaError as e:
    print(f"Error: {e}")
```

## Response Structures

### Agent Object
```python
{
    "id": "agent-123",
    "name": "my_agent",
    "model": "openai/gpt-4o-mini",
    "embedding": "openai/text-embedding-3-small",
    "memory": {
        "blocks": [
            {
                "label": "human",
                "value": "...",
                "limit": 2000
            }
        ]
    },
    "tool_ids": ["tool-1", "tool-2"],
    "tags": ["dev"]
}
```

### Message Object
```python
{
    "role": "assistant",         # or "user", "tool"
    "content": "Response text",
    "tool_calls": [...],        # If agent called tools
    "tool_call_id": "...",      # If this is a tool response
}
```

### Tool Object
```python
{
    "id": "tool-123",
    "name": "function_name",
    "description": "Function description from docstring",
    "tags": ["file-ops"],
    "schema": {...}  # JSON schema of function parameters
}
```

## Environment Variables

```bash
# Set Letta server URL
export LETTA_BASE_URL="http://localhost:8283"

# Set API token (if using auth)
export LETTA_API_TOKEN="your-token"
```

## Useful Snippets

### Check if Tool Exists
```python
tools = client.tools.list(name="my_function")
if tools.items:
    tool = tools.items[0]
    print(f"Tool exists: {tool.id}")
else:
    print("Tool not found, creating...")
    tool = client.tools.upsert_from_function(func=my_function)
```

### Get Agent's Tools
```python
agent = client.agents.retrieve(agent_id="agent-id")
for tool_id in agent.tool_ids:
    tool = client.tools.retrieve(tool_id=tool_id)
    print(f"- {tool.name}")
```

### Count Agent Messages
```python
# Messages are in recall memory
# Use conversation_search via agent or check logs
```

## Links

- [Official API Reference](https://docs.letta.com/api-reference)
- [agent-configuration.md](agent-configuration.md) - Detailed agent setup
- [tool-development.md](tool-development.md) - Creating custom tools
- [memory-system.md](memory-system.md) - Memory management
