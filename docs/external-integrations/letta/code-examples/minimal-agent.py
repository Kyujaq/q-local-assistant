#!/usr/bin/env python3
"""
Minimal Letta agent example.

Creates a simple agent with basic memory and has a conversation.
"""

from letta_client import Letta


def main():
    # Connect to local Letta server
    client = Letta(base_url="http://localhost:8283")
    
    # Create agent with minimal configuration
    agent = client.agents.create(
        name="minimal_agent",
        model="openai/gpt-4o-mini",
        embedding="openai/text-embedding-3-small",
        memory_blocks=[
            {
                "label": "human",
                "value": "The user's name is Alex."
            },
            {
                "label": "persona",
                "value": "I am a helpful assistant."
            }
        ],
        tags=["example", "minimal"]
    )
    
    print(f"Created agent: {agent.id}")
    print(f"Name: {agent.name}")
    print(f"Model: {agent.model}")
    print()
    
    # Have a conversation
    messages = [
        "Hello! What's my name?",
        "What can you help me with?",
        "Thank you!"
    ]
    
    for user_msg in messages:
        print(f"User: {user_msg}")
        
        response = client.agents.messages.create(
            agent_id=agent.id,
            messages=[{"role": "user", "content": user_msg}],
            stream=False
        )
        
        # Print assistant responses
        for msg in response.messages:
            if msg.role == "assistant":
                print(f"Agent: {msg.content}")
        print()
    
    # Cleanup
    print(f"Deleting agent {agent.id}...")
    client.agents.delete(agent_id=agent.id)
    print("Done!")


if __name__ == "__main__":
    main()
