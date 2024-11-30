"""
Command execution and management for Command-FS.
"""
from typing import Any, Dict, NamedTuple
import subprocess
import json
import time


class CommandResult(NamedTuple):
    """Result of a command execution."""
    output: str
    execution_time: float
    timestamp: float
    success: bool
    error: str | None


def execute_command(config: Dict[str, Any]) -> CommandResult:
    """Execute a command and return its result."""
    start_time = time.time()
    error = None
    output = ""
    success = True

    try:
        # Get command configuration
        command = config.get('command', '')
        timeout = config.get('timeout', 30)  # default 30 seconds
        format_output = config.get('format_output', True)

        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        # Process output
        output = result.stdout if result.returncode == 0 else result.stderr
        success = result.returncode == 0
        if not success:
            error = f"Command failed with exit code {result.returncode}"

        # Format output if requested
        if format_output and success:
            try:
                output_dict = {
                    "output": output.strip(),
                    "timestamp": time.time(),
                    "execution_time": time.time() - start_time
                }
                output = json.dumps(output_dict, indent=2)
            except Exception as e:
                error = f"Failed to format output: {str(e)}"
                success = False

    except subprocess.TimeoutExpired:
        error = f"Command timed out after {timeout} seconds"
        success = False
    except Exception as e:
        error = f"Command execution failed: {str(e)}"
        success = False

    return CommandResult(
        output=output,
        execution_time=time.time() - start_time,
        timestamp=time.time(),
        success=success,
        error=error
    )
