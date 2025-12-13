#!/usr/bin/env python3
"""
Agent with custom tools example.

Creates an agent with file reading and git tools.
"""

from letta_client import Letta
from typing import List
import subprocess


# Define custom tools
def read_file(file_path: str, start_line: int = None, end_line: int = None) -> str:
    """
    Read contents of a file.
    
    Args:
        file_path: Absolute path to the file
        start_line: Optional starting line (1-indexed)
        end_line: Optional ending line (inclusive)
        
    Returns:
        File contents as string
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if start_line is not None and end_line is not None:
            lines = content.splitlines()
            return "\n".join(lines[start_line-1:end_line])
        return content
    except FileNotFoundError:
        return f"Error: File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {e}"


def list_files(directory: str) -> List[str]:
    """
    List files in a directory.
    
    Args:
        directory: Path to directory
        
    Returns:
        List of filenames
    """
    import os
    try:
        return os.listdir(directory)
    except Exception as e:
        return [f"Error: {e}"]


def git_status() -> str:
    """
    Get git status.
    
    Returns:
        Git status output
    """
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout if result.stdout else "No changes"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except FileNotFoundError:
        return "Error: git not found"


def main():
    client = Letta(base_url="http://localhost:8283")
    
    print("Creating tools...")
    # Create tools from functions
    tool_read = client.tools.upsert_from_function(
        func=read_file,
        tags=["file", "dev"]
    )
    tool_list = client.tools.upsert_from_function(
        func=list_files,
        tags=["file", "dev"]
    )
    tool_git = client.tools.upsert_from_function(
        func=git_status,
        tags=["git", "dev"]
    )
    
    print(f"Created tools: {tool_read.name}, {tool_list.name}, {tool_git.name}")
    
    # Create agent with tools
    print("Creating agent...")
    agent = client.agents.create(
        name="dev_assistant",
        model="openai/gpt-4o-mini",
        embedding="openai/text-embedding-3-small",
        memory_blocks=[
            {
                "label": "role",
                "value": "You are a development assistant. You can read files and check git status."
            },
            {
                "label": "human",
                "value": "The developer is working on a Python project."
            }
        ],
        tool_ids=[tool_read.id, tool_list.id, tool_git.id],
        tags=["dev", "example"]
    )
    
    print(f"Created agent: {agent.id}\n")
    
    # Conversation with tool usage
    prompts = [
        "What tools do you have available?",
        "Can you check the git status?",
        "List files in the current directory.",
    ]
    
    for prompt in prompts:
        print(f"User: {prompt}")
        
        response = client.agents.messages.create(
            agent_id=agent.id,
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        
        # Print all messages (including tool calls)
        for msg in response.messages:
            if msg.role == "assistant":
                print(f"Agent: {msg.content}")
            elif msg.role == "tool":
                print(f"Tool result: {msg.content[:100]}...")
        print()
    
    # Cleanup
    print("Cleaning up...")
    client.agents.delete(agent_id=agent.id)
    client.tools.delete(tool_id=tool_read.id)
    client.tools.delete(tool_id=tool_list.id)
    client.tools.delete(tool_id=tool_git.id)
    print("Done!")


if __name__ == "__main__":
    main()
