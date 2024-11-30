# Command Interaction Protocol

## Overview

The Command-FS protocol defines two types of command files:
1. **Read-Only Commands**: Execute on read, return raw output
2. **Writable Commands**: Require write for execution, cache results with context

## Read-Only Commands

### Read Operation
- Executes command immediately
- Returns raw output directly
- No caching or metadata

### Example
```bash
# Simple read executes and returns output
cat /cmd/uptime
# Returns: 12:23  up 5 days, 2 users, load averages: 1.20 1.35 1.40

cat /cmd/date
# Returns: Mon Jan 29 12:23:45 PST 2024
```

## Writable Commands

### Write Operation
```json
{
  "command": "command_name",
  "args": ["arg1", "arg2", ...],
  "options": {
    "timeout": number,
    "format": "string|json|raw"
  }
}
```

### Read Operation
Returns the cached result of the last execution:
```json
{
  "command": "command_name",
  "args": ["arg1", "arg2", ...],
  "status": "complete|error",
  "output": "command_output",
  "error": "error_message",
  "timestamp": "ISO8601_timestamp"
}
```

## Implementation

### File Handle Types

1. **Read-Only Files**
   - Pre-configured commands
   - No arguments needed
   - Raw output only
   - Execute on every read
   - Examples: `uptime`, `date`, `who`

2. **Writable Files**
   - Configurable commands
   - Arguments required
   - Structured output with context
   - Cache last execution
   - Examples: `curl`, `convert`, `ffmpeg`

### Example Flow

#### Read-Only Command
```bash
# Each read executes command
cat /cmd/uptime
# Returns raw output: 12:23  up 5 days...

# Next read executes again
cat /cmd/uptime
# Returns fresh output: 12:24  up 5 days...
```

#### Writable Command
```bash
# Write command
echo '{"command": "curl", "args": ["https://api.example.com"]}' > /cmd/curl

# Read result (cached)
cat /cmd/curl
# Returns:
{
  "command": "curl",
  "args": ["https://api.example.com"],
  "status": "complete",
  "output": "{\\"status\\": \\"ok\\"}",
  "timestamp": "2024-01-29T12:34:56Z"
}
```

### Error Handling

#### Read-Only Commands
```bash
cat /cmd/invalid
# Returns error message directly:
Command not found: invalid
```

#### Writable Commands
```json
{
  "command": "invalid_cmd",
  "args": [],
  "status": "error",
  "error": "command not found",
  "output": null,
  "timestamp": "2024-01-29T12:34:56Z"
}
```

## Implementation Notes

1. **Command Configuration**
   - Read-only commands defined at mount time
   - No runtime configuration needed
   - Simple command mapping

2. **Performance**
   - Read-only commands: fresh execution
   - Writable commands: cached results
   - Optimized for common use cases

3. **Security**
   - Read-only commands: fixed set
   - Writable commands: validation on write
   - Resource limits per type
