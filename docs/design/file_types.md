# Command-FS File Types

## Overview

Command-FS implements four fundamental types of file handles, each serving a distinct purpose in the filesystem:

1. OS Command Files
2. REST Endpoint Files
3. Index Files
4. Native Command Files

## 1. OS Command Files

### Purpose
Executes operating system commands and presents their output as file content.

### Behavior
- **Read Operations**: Execute the command and return its output
- **Write Operations**: Provide input or arguments to the command
- **Permissions**: Configurable based on command security requirements

### Features
- Command output formatting
- Argument templating
- Error capture and reporting
- Output caching (optional)
- Resource usage limits

## 2. REST Endpoint Files

### Purpose
Maps REST endpoints to file operations, transforming HTTP methods into filesystem operations.

### Behavior
- **Read Operations**: Execute GET requests
- **Write Operations**: Execute POST/PUT requests
- **Delete Operations**: Execute DELETE requests (where supported)

### Features
- Authentication support
- Response formatting
- Error handling and retry logic
- Request caching
- Rate limiting
- Timeout management

## 3. Index Files

### Purpose
Provides human-readable listing and documentation of available commands.

### Behavior
- **Read Operations**: Generate formatted command listings
- **Write Operations**: Not supported
- **Refresh**: Auto-updates when command registry changes

### Features
- Command categorization
- Detailed command documentation
- Usage examples
- Permission information
- Command status and health

## 4. Native Command Files

### Purpose
Base implementation for commands implemented directly in the filesystem.

### Behavior
- **Read Operations**: Execute custom logic and return results
- **Write Operations**: Process input through custom handlers
- **Special Operations**: Support for custom filesystem operations

### Features
- Custom data processing
- Direct system integration
- Specialized output formatting
- Performance optimization
- Resource management

## Common Characteristics

### Error Handling
- Standard error codes
- Detailed error messages
- Operation logging
- Retry mechanisms (where appropriate)

### Caching
- Output caching
- Cache invalidation rules
- Memory management
- Cache persistence options

### Security
- Permission management
- Resource limits
- Input validation
- Execution isolation

### Configuration
- Command definitions
- Runtime parameters
- Resource limits
- Logging settings
