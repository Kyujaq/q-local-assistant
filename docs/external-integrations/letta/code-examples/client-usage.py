#!/usr/bin/env python3
"""
Letta client usage examples.

Demonstrates common operations: creating/retrieving/updating/deleting agents,
managing tools, and working with memory.
"""

from letta_client import Letta


def demo_agent_lifecycle(client: Letta):
    """Demo: Create, retrieve, update, delete agent."""
    print("=== Agent Lifecycle ===\n")
    
    # Create
    print("Creating agent...")
    agent = client.agents.create(
        name="lifecycle_demo",
        model="openai/gpt-4o-mini",
        embedding="openai/text-embedding-3-small",
        memory_blocks=[
            {"label": "human", "value": "User is a developer"}
        ],
        tags=["demo"]
    )
    print(f"Created: {agent.id}\n")
    
    # Retrieve
    print("Retrieving agent...")
    retrieved = client.agents.retrieve(agent_id=agent.id)
    print(f"Name: {retrieved.name}")
    print(f"Tags: {retrieved.tags}\n")
    
    # Update
    print("Updating agent...")
    updated = client.agents.update(
        agent_id=agent.id,
        name="updated_demo",
        tags=["demo", "updated"]
    )
    print(f"New name: {updated.name}")
    print(f"New tags: {updated.tags}\n")
    
    # Delete
    print("Deleting agent...")
    client.agents.delete(agent_id=agent.id)
    print("Deleted!\n")


def demo_tool_management(client: Letta):
    """Demo: Create, list, attach tools."""
    print("=== Tool Management ===\n")
    
    def example_tool(param: str) -> str:
        """Example tool function."""
        return f"Received: {param}"
    
    # Create tool
    print("Creating tool...")
    tool = client.tools.upsert_from_function(
        func=example_tool,
        tags=["demo"]
    )
    print(f"Created: {tool.name} ({tool.id})\n")
    
    # List tools with filter
    print("Listing tools with tag 'demo'...")
    tools = client.tools.list(tags=["demo"])
    for t in tools.items:
        print(f"  - {t.name}")
    print()
    
    # Create agent and attach tool
    print("Creating agent with tool...")
    agent = client.agents.create(
        name="tool_demo",
        model="openai/gpt-4o-mini",
        embedding="openai/text-embedding-3-small",
        tool_ids=[tool.id],
        memory_blocks=[{"label": "human", "value": "Demo user"}],
        tags=["demo"]
    )
    print(f"Agent {agent.name} has {len(agent.tool_ids)} tool(s)\n")
    
    # Cleanup
    client.agents.delete(agent_id=agent.id)
    client.tools.delete(tool_id=tool.id)
    print("Cleaned up!\n")


def demo_memory_operations(client: Letta):
    """Demo: Core memory and archival memory."""
    print("=== Memory Operations ===\n")
    
    # Create agent
    agent = client.agents.create(
        name="memory_demo",
        model="openai/gpt-4o-mini",
        embedding="openai/text-embedding-3-small",
        memory_blocks=[
            {"label": "human", "value": "User: Alex"},
            {"label": "persona", "value": "I am helpful"}
        ],
        tags=["demo"]
    )
    
    # View core memory
    print("Core memory blocks:")
    for block in agent.memory.blocks:
        print(f"  {block.label}: {block.value}")
    print()
    
    # Insert archival memories
    print("Inserting archival memories...")
    client.agents.passages.create(
        agent_id=agent.id,
        text="Alex prefers Python over JavaScript",
        tags=["preferences"]
    )
    client.agents.passages.create(
        agent_id=agent.id,
        text="Alex uses pytest for testing",
        tags=["preferences", "testing"]
    )
    print("Inserted 2 passages\n")
    
    # Search archival memory
    print("Searching archival memory for 'Python'...")
    results = client.agents.passages.search(
        agent_id=agent.id,
        query="Python",
        limit=5
    )
    for result in results.items:
        print(f"  - {result.text}")
    print()
    
    # List all passages
    print("All archival passages:")
    passages = client.agents.passages.list(agent_id=agent.id)
    for p in passages.items:
        print(f"  - {p.text} (tags: {p.tags})")
    print()
    
    # Update core memory
    print("Updating core memory...")
    blocks = agent.memory.blocks
    for block in blocks:
        if block.label == "human":
            block.value = "User: Alex (updated)"
    
    updated_agent = client.agents.update(
        agent_id=agent.id,
        memory_blocks=[
            {"label": b.label, "value": b.value, "limit": b.limit}
            for b in blocks
        ]
    )
    
    print("Updated core memory:")
    for block in updated_agent.memory.blocks:
        print(f"  {block.label}: {block.value}")
    print()
    
    # Cleanup
    client.agents.delete(agent_id=agent.id)
    print("Cleaned up!\n")


def demo_conversation(client: Letta):
    """Demo: Basic conversation with an agent."""
    print("=== Conversation ===\n")
    
    agent = client.agents.create(
        name="chat_demo",
        model="openai/gpt-4o-mini",
        embedding="openai/text-embedding-3-small",
        memory_blocks=[
            {"label": "human", "value": "User is learning Letta"},
            {"label": "persona", "value": "I am a patient teacher"}
        ],
        tags=["demo"]
    )
    
    messages = [
        "Hello!",
        "What is Letta?",
        "Thanks!"
    ]
    
    for msg in messages:
        print(f"User: {msg}")
        
        response = client.agents.messages.create(
            agent_id=agent.id,
            messages=[{"role": "user", "content": msg}],
            stream=False
        )
        
        for resp_msg in response.messages:
            if resp_msg.role == "assistant":
                print(f"Agent: {resp_msg.content}")
        print()
    
    # Cleanup
    client.agents.delete(agent_id=agent.id)
    print("Cleaned up!\n")


def main():
    """Run all demos."""
    print("Letta Client Usage Examples")
    print("=" * 40)
    print()
    
    # Connect to Letta server
    client = Letta(base_url="http://localhost:8283")
    
    # Run demos
    demo_agent_lifecycle(client)
    demo_tool_management(client)
    demo_memory_operations(client)
    demo_conversation(client)
    
    print("All demos complete!")


if __name__ == "__main__":
    main()
