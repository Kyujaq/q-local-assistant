# Letta Tool Development

Tools are Python functions that Letta agents can call. Think of them as the agent's "hands" - they let agents interact with systems, read files, run tests, etc.

## Creating a Tool from a Function

```python
from letta_client import Letta

client = Letta(base_url="http://localhost:8283")

# Define your function
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
    with open(file_path, 'r') as f:
        content = f.read()
    
    if start_line and end_line:
        lines = content.splitlines()
        return "\n".join(lines[start_line-1:end_line])
    return content

# Create tool from function
tool = client.tools.upsert_from_function(
    func=read_file,
    tags=["file", "dev"],  # Optional: for organization
)

print(f"Tool created: {tool.id} - {tool.name}")
```

## Tool Function Requirements

### Type Hints
**Required**: All parameters and return type must have type hints.

```python
# ✅ Good
def good_function(name: str, count: int) -> str:
    return f"{name}: {count}"

# ❌ Bad - no type hints
def bad_function(name, count):
    return f"{name}: {count}"
```

### Docstrings
**Required**: Function docstring with Args and Returns sections.

```python
def example_tool(param1: str, param2: int = 10) -> dict:
    """
    One-line summary of what the tool does.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
        
    Returns:
        Description of what is returned
    """
    return {"result": param1, "count": param2}
```

### Supported Types
- **Primitives**: `str`, `int`, `float`, `bool`
- **Collections**: `List[T]`, `Dict[str, T]`, `Optional[T]`
- **Pydantic Models**: For complex structures

```python
from typing import List, Optional
from pydantic import BaseModel

class TestResult(BaseModel):
    test_name: str
    passed: bool
    message: str

def run_tests(test_file: str, verbose: bool = False) -> List[TestResult]:
    """
    Run tests and return results.
    
    Args:
        test_file: Path to test file
        verbose: Include detailed output
        
    Returns:
        List of test results
    """
    # Implementation...
    return [TestResult(test_name="test_1", passed=True, message="OK")]
```

## Tool Patterns for Dev Agents

### File Operations
```python
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        file_path: Absolute path to file
        content: Content to write
        
    Returns:
        Success message
    """
    with open(file_path, 'w') as f:
        f.write(content)
    return f"Wrote {len(content)} characters to {file_path}"
```

### Git Operations
```python
def git_commit(message: str, files: List[str] = None) -> str:
    """
    Commit changes to git.
    
    Args:
        message: Commit message
        files: Optional list of files to commit (all if None)
        
    Returns:
        Commit hash
    """
    import subprocess
    
    if files:
        subprocess.run(["git", "add"] + files, check=True)
    else:
        subprocess.run(["git", "add", "-A"], check=True)
    
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True, text=True, check=True
    )
    
    # Extract commit hash from output
    return result.stdout.strip().split()[1]
```

### Test Runner
```python
def run_pytest(test_path: str, verbose: bool = False) -> dict:
    """
    Run pytest on specified tests.
    
    Args:
        test_path: Path to test file or directory
        verbose: Include verbose output
        
    Returns:
        Test results summary
    """
    import subprocess
    
    cmd = ["pytest", test_path, "--tb=short"]
    if verbose:
        cmd.append("-v")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "passed": result.returncode == 0
    }
```

## Tool Patterns for Prod Agents

### Home Assistant
```python
async def turn_on_light(entity_id: str, brightness: int = None) -> str:
    """
    Turn on a light via Home Assistant.
    
    Args:
        entity_id: Light entity (e.g., 'light.living_room')
        brightness: Brightness 0-255 (optional)
        
    Returns:
        Success message
    """
    import aiohttp
    
    url = "http://homeassistant.local:8123/api/services/light/turn_on"
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    
    data = {"entity_id": entity_id}
    if brightness is not None:
        data["brightness"] = brightness
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as resp:
            return f"Light {entity_id} turned on"
```

## Managing Tools

### List Tools
```python
# All tools
all_tools = client.tools.list()

# Filter by tag
file_tools = client.tools.list(tags=["file"])

# Search by name
tool = client.tools.list(name="read_file").items[0]
```

### Update Tools
```python
# Update an existing tool
tool = client.tools.update(
    tool_id=tool.id,
    description="New description",
    tags=["updated_tag"]
)
```

### Delete Tools
```python
client.tools.delete(tool_id=tool.id)
```

## Testing Tools Locally

Before attaching to an agent, test your tool function:

```python
# Test the function directly
result = read_file("/path/to/file.txt", start_line=1, end_line=10)
print(result)

# Then create the tool
tool = client.tools.upsert_from_function(func=read_file)
```

## Tool Return Values

Tools should return **strings or JSON-serializable data**:

```python
# ✅ Good returns
return "Operation completed successfully"
return {"status": "ok", "files": ["a.py", "b.py"]}
return ["item1", "item2", "item3"]

# ❌ Avoid
return MyCustomClass()  # Not JSON-serializable
return open("file.txt")  # File object
```

## Error Handling

Raise clear exceptions:

```python
def delete_file(file_path: str) -> str:
    """
    Delete a file.
    
    Args:
        file_path: Path to file to delete
        
    Returns:
        Success message
        
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If lacking permissions
    """
    import os
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        os.remove(file_path)
        return f"Deleted {file_path}"
    except PermissionError as e:
        raise PermissionError(f"Cannot delete {file_path}: {e}")
```

## Tool Naming Conventions

For our project:

### Dev Tools
- `dev_` prefix: `dev_read_file`, `dev_git_commit`
- Clear action: `write_file`, not `file_writer`
- Specific: `run_unit_tests`, not `run_tests`

### Prod Tools
- `prod_` prefix or domain: `ha_turn_on_light`, `paprika_get_recipe`
- User-facing names: `search_recipes`, `control_lights`

## Advanced: Async Tools

Tools can be async:

```python
async def fetch_url(url: str) -> str:
    """
    Fetch content from a URL.
    
    Args:
        url: URL to fetch
        
    Returns:
        Response content
    """
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

# Letta handles async tools automatically
tool = client.tools.upsert_from_function(func=fetch_url)
```

## Tool Sandboxing

Letta can run tools in sandboxed environments (Modal, E2B). For local dev:

```python
# Tools run in the same process by default
# For production, configure sandboxing in Letta server
```

## Common Pitfalls

❌ **No type hints**: Tool creation will fail  
❌ **Missing docstring**: Schema generation fails  
❌ **Returning non-serializable objects**: Agent can't process result  
❌ **Too much output**: Keep returns <10KB if possible (agents have context limits)  

## Links

- [Official Tools API](https://docs.letta.com/api-reference/tools)
- [agent-configuration.md](agent-configuration.md) - Attaching tools to agents
- [code-examples/](code-examples/) - Complete tool examples
