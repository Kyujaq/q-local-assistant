"""Coder agent configuration - implements features following specifications."""

from typing import Dict, List

from src.common.letta_client import get_letta_client


def create_coder_agent(
    name: str = "coder",
    model: str = "openai/gpt-4o-mini",
    embedding: str = "openai/text-embedding-3-small",
    tool_ids: List[str] = None,
) -> Dict:
    """
    Create a Coder agent following the playbook in docs/dev-300-agents/coder.md.

    Args:
        name: Agent name (default: "coder")
        model: LLM model to use
        embedding: Embedding model for memory search
        tool_ids: List of tool IDs to attach (file_operations, git_runner, code_search)

    Returns:
        Agent configuration dict with id, name, memory_blocks, etc.

    Raises:
        ConnectionError: If cannot connect to Letta server
    """
    client = get_letta_client()

    if tool_ids is None:
        tool_ids = []

    # Memory blocks based on coder.md playbook
    memory_blocks = [
        {
            "label": "role",
            "value": (
                "You are the Coder agent. Write clean, maintainable code following "
                "project coding standards.\n\n"
                "Responsibilities:\n"
                "- Implement features as specified in feature specs\n"
                "- Follow coding standards: clarity > robustness > speed > cleverness\n"
                "- Write conventional commit messages (feat/fix/refactor)\n"
                "- Request context via Documentation Specialist when needed\n"
                "- Coordinate with Tester for testability\n"
                "- Work in bite-sized increments\n"
                "- Update decision logs immediately"
            ),
        },
        {
            "label": "current_task",
            "value": "No task assigned. Awaiting assignment from Orchestrator.",
        },
        {
            "label": "coding_standards",
            "value": (
                "Python-only project:\n"
                "- Type hints everywhere (functions, methods, classes, significant variables)\n"
                "- Docstrings required (every module, class, public function)\n"
                "- Functions <80 lines, modules <500 lines (unless justified)\n"
                "- Clarity principle: clarity > robustness > speed > cleverness\n"
                "- Ruff (linting) → Black (formatting) before commit\n"
                "- Conventional commits: feat(module), fix(module), refactor(module)"
            ),
        },
    ]

    agent = client.agents.create(
        name=name,
        model=model,
        embedding=embedding,
        memory_blocks=memory_blocks,
        tool_ids=tool_ids,
        tags=["dev", "coder"],
    )

    return {
        "id": agent.id,
        "name": agent.name,
        "model": agent.model,
        "memory_blocks": agent.memory.blocks,
        "tool_ids": agent.tool_ids,
        "tags": agent.tags,
    }


def update_coder_task(agent_id: str, task_description: str) -> None:
    """
    Update the Coder agent's current_task memory block.

    Args:
        agent_id: Agent ID
        task_description: New task description from Orchestrator
    """
    client = get_letta_client()
    agent = client.agents.retrieve(agent_id=agent_id)

    # Update current_task memory block
    memory_blocks = agent.memory.blocks
    for block in memory_blocks:
        if block.label == "current_task":
            block.value = task_description
            break

    client.agents.update(
        agent_id=agent_id,
        memory_blocks=[
            {"label": b.label, "value": b.value, "limit": b.limit} for b in memory_blocks
        ],
    )
