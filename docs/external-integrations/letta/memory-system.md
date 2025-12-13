# Letta Memory System

Letta agents have three types of memory. Understanding these is critical for building effective agents.

## Memory Types Overview

```
┌─────────────────────────────────────────────────────────┐
│ CORE MEMORY (In-Context)                                │
│ - Always visible to agent                               │
│ - Limited size (~2000 chars per block)                  │
│ - Agent can edit with tools                             │
│ - Blocks: human, persona, custom                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ RECALL MEMORY (Conversation History)                    │
│ - Recent messages in context                            │
│ - Older messages searchable via tool                    │
│ - Automatic management                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ARCHIVAL MEMORY (Long-Term Storage)                     │
│ - Infinite size                                         │
│ - Semantic search via tool                              │
│ - Agent writes/searches explicitly                      │
│ - Tagged for organization                               │
└─────────────────────────────────────────────────────────┘
```

## Core Memory

Core memory is always in-context. Agents see it in every interaction.

### Viewing Core Memory

```python
agent = client.agents.retrieve(agent_id="agent-123")

for block in agent.memory.blocks:
    print(f"{block.label}: {block.value}")
```

### Memory Blocks Structure

```python
{
    "label": "human",          # Block identifier
    "value": "Name: Alex...",  # Actual content
    "limit": 2000              # Character limit
}
```

### Common Block Labels

| Label | Purpose | Example |
|-------|---------|---------|
| `human` | Info about the user | "Name: Alex, Role: Developer, Prefers Python" |
| `persona` | Agent's personality/role | "I am a code review assistant. I focus on security and clarity." |
| `instructions` | Task-specific guidance | "Review PRs for bugs. Suggest improvements. Be concise." |
| `context` | Current task state | "Working on feature X. Completed: A, B. Next: C" |

### Agent Self-Editing Core Memory

Agents use tools to modify their own memory:

**`core_memory_append`** - Add to a block:
```python
# Agent calls (internally):
core_memory_append(label="human", content="\nFavorite language: Rust")
```

**`core_memory_replace`** - Replace content:
```python
# Agent calls:
core_memory_replace(
    label="persona",
    old_content="I am helpful",
    new_content="I am a security-focused assistant"
)
```

### Best Practices

- **Keep blocks focused**: One topic per block
- **Use clear labels**: Descriptive, lowercase, underscore-separated
- **Monitor size**: Agents should summarize if approaching limits
- **Read-only blocks**: Mark blocks as read-only if agents shouldn't edit them

```python
# Example for dev agents
memory_blocks=[
    {
        "label": "role",
        "value": "You are the Coder agent. Write clean, tested code."
    },
    {
        "label": "current_task",
        "value": "Implement feature X in module Y."
    }
]
```

## Recall Memory (Conversation Search)

Recall memory is the conversation history. Recent messages are in-context; older ones are searchable.

### Searching Conversation History

Agent uses `conversation_search` tool:

```python
# Agent calls this:
conversation_search(
    query="decisions about API design",
    limit=5,
    roles=["user", "assistant"]  # Optional filter
)
```

Returns recent messages matching the query.

### Usage Pattern

Agents automatically use this when they need to recall:
- Previous decisions
- User preferences mentioned earlier
- Past errors or solutions

**You don't manage this manually** - Letta handles it.

## Archival Memory (Long-Term Storage)

Archival memory is for facts, documents, knowledge the agent explicitly stores.

### Inserting into Archival Memory

Agent uses `archival_memory_insert` tool:

```python
# Agent stores a finding:
archival_memory_insert(
    content="Bug found in auth.py line 42: missing null check on token.",
    tags=["bugs", "auth"]
)
```

### Searching Archival Memory

Agent uses `archival_memory_search` tool:

```python
# Agent searches its long-term memory:
archival_memory_search(
    query="authentication bugs",
    tags=["bugs"],        # Filter by tags
    top_k=5               # Limit results
)
```

### Via API (For Pre-Loading)

You can pre-load archival memory:

```python
# Insert knowledge before agent runs
client.agents.passages.create(
    agent_id=agent.id,
    text="Project uses Python 3.11, pytest for testing, ruff for linting.",
    tags=["project-info"]
)
```

### Tagging Strategy

**For Dev Agents**:
- `["project-docs"]` - Project standards, conventions
- `["decisions"]` - Architectural decisions
- `["bugs"]` - Known issues
- `["solutions"]` - Past solutions to problems

**For Prod Agents**:
- `["user-prefs"]` - User preferences
- `["recipes"]` - Paprika recipes
- `["home-layout"]` - Room/device information
- `["schedules"]` - Recurring events

### Listing/Deleting Archival Memories

```python
# List memories
passages = client.agents.passages.list(agent_id=agent.id)

# Delete a memory
client.agents.passages.delete(
    agent_id=agent.id,
    passage_id="passage-123"
)
```

## Memory in Action: Example Flow

### Dev Agent (Coder)

1. **Core Memory**: Holds current task, coding standards
2. **Recall Memory**: Searches for similar past implementations
3. **Archival Memory**: Looks up project conventions ("How do we name test files?")

### Prod Agent (Home Assistant)

1. **Core Memory**: User preferences, current state
2. **Recall Memory**: "What did user say about lights yesterday?"
3. **Archival Memory**: Room layouts, device capabilities

## Memory Limits

| Type | Size | Notes |
|------|------|-------|
| Core Memory | ~2000 chars/block | Agent sees all the time |
| Recall Memory | Last N messages in context | Older searchable |
| Archival Memory | Unlimited | Search required |

**Context Window**: Total tokens available to LLM. Core memory + recent messages must fit.

## Memory Management Tools

Agents have access to:
- `core_memory_append(label, content)` - Add to core block
- `core_memory_replace(label, old, new)` - Replace in core block
- `conversation_search(query)` - Search past messages
- `archival_memory_insert(content, tags)` - Store long-term
- `archival_memory_search(query, tags)` - Retrieve long-term

## Monitoring Memory Usage

```python
# Check memory stats
agent = client.agents.retrieve(agent_id=agent.id)

print(f"Core memory blocks: {len(agent.memory.blocks)}")
for block in agent.memory.blocks:
    print(f"  {block.label}: {len(block.value)}/{block.limit} chars")

# Archival memory size
passages = client.agents.passages.list(agent_id=agent.id)
print(f"Archival passages: {len(passages.items)}")
```

## Best Practices

### Core Memory
✅ Keep essential, frequently-used info  
✅ Update as situation changes  
✅ Use clear, consistent formatting  
❌ Don't store logs or verbose data  

### Recall Memory
✅ Let Letta manage automatically  
✅ Trust the search function  
❌ Don't try to manipulate directly  

### Archival Memory
✅ Store facts, documents, knowledge  
✅ Use tags consistently  
✅ Write clear, searchable content  
❌ Don't store temporary state  

## Example: Dev Agent Memory Setup

```python
agent = client.agents.create(
    name="coder",
    memory_blocks=[
        {
            "label": "role",
            "value": "You are the Coder agent. Write Python code following PEP 8."
        },
        {
            "label": "task",
            "value": "Current task: None"
        }
    ],
    # ...
)

# Pre-load project knowledge
client.agents.passages.create(
    agent_id=agent.id,
    text="Project uses pytest for testing. Test files: tests/unit/*.py",
    tags=["project-standards"]
)

client.agents.passages.create(
    agent_id=agent.id,
    text="Code style: Black formatter, Ruff linter, type hints required.",
    tags=["project-standards", "code-style"]
)
```

## Links

- [Official Memory Docs](https://docs.letta.com/concepts/memory)
- [agent-configuration.md](agent-configuration.md) - Setting up memory blocks
- [api-quickref.md](api-quickref.md) - Memory API calls
