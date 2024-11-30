# 2. Implementation Architecture

Date: 2024-01-23

## Status

Superseded by new decision (2024-11-29)

## Context

Having selected Elixir as our implementation language (see [ADR-0001](0001-programming-language-selection.md)), we need to define the specific implementation architecture. Key considerations include:

- FUSE interface implementation
- Command execution model
- Process supervision structure
- Configuration management
- Error handling strategy

## Decision

### Updated Architecture Decision

Following our new phased approach (see [ADR-0001](0001-programming-language-selection.md)), we will implement the system as follows:

1. **Phase 1: Node.js Prototype**
   ```
   command_fs/
   ├── src/
   │   ├── fuse/              # FUSE implementation
   │   │   └── operations.js  # Core FUSE operations
   │   ├── commands/          # Command implementations
   │   │   ├── registry.js    # Command registration
   │   │   └── executors/     # Command executors
   │   ├── cache/             # Command output caching
   │   │   └── store.js       # SQLite/LowDB implementation
   │   └── index.js           # Main application
   ├── config/
   │   └── default.js         # Configuration
   ├── package.json           # Dependencies
   └── test/                  # Test files
   ```

2. **Phase 2: Production Implementation**
   ```
   command_fs/
   ├── lib/
   │   ├── command_fs/
   │   │   ├── application.ex     # OTP application
   │   │   ├── fuse/             # FUSE interface
   │   │   ├── commands/         # Command implementations
   │   │   ├── cache/           # PostgreSQL caching
   │   │   └── monitoring/      # Telemetry and logging
   │   └── command_fs.ex        # Main API module
   ├── config/
   │   └── config.exs           # Configuration
   ├── mix.exs                  # Project dependencies
   └── test/                   # Test files
   ```

### Rationale for Change

1. **Simplified Initial Implementation**
   - Node.js FUSE implementation is well-documented
   - Easier debugging and development workflow
   - Rich ecosystem for filesystem operations

2. **Clear Migration Path**
   - Start with simple, working implementation
   - Validate core concepts
   - Migrate to production stack incrementally

3. **Reduced Complexity**
   - Fewer moving parts in prototype
   - Direct filesystem integration
   - Simple data persistence

### Original Architecture (Historical)

We will implement Command-FS using a hybrid approach:

1. FUSE Interface:
   - Use `mwri/elixir-userfs` for FUSE operations (native Elixir implementation)
   - Leverage built-in callbacks for filesystem operations
   - Direct integration with Elixir's supervision tree

2. Command Execution:
   - Implement commands as individual GenServers
   - Use dynamic supervision for command processes
   - Implement command registry as a Registry process

3. System Architecture:
```
command_fs/
├── lib/
│   ├── command_fs/
│   │   ├── application.ex           # OTP application
│   │   ├── filesystem.ex            # FUSE implementation
│   │   ├── command.ex               # Command behavior
│   │   ├── command_registry.ex      # Command registration
│   │   ├── command_supervisor.ex    # Dynamic command supervision
│   │   └── commands/                # Individual command implementations
│   │       ├── datetime.ex
│   │       ├── sys/
│   │       │   ├── cpu.ex
│   │       │   └── memory.ex
│   │       └── net/
│   │           ├── connections.ex
│   │           └── ports.ex
│   └── command_fs.ex               # Main API module
├── config/
│   └── config.exs                  # Configuration
├── mix.exs                         # Project dependencies
└── test/                          # Test files
```

4. Process Structure:
```
Application Supervisor
├── FUSE Server
├── Command Registry
└── Command Supervisor
    ├── DateTime Command
    ├── CPU Command
    └── Memory Command
```

## Rationale

1. FUSE Integration:
   - Using `mwri/elixir-userfs` provides a native Elixir FUSE implementation
   - Built-in supervision and OTP integration
   - Idiomatic Elixir callbacks and patterns
   - Maintains compatibility with underlying erlang-fuse implementation

2. Command Model:
   - GenServers provide natural isolation for commands
   - Dynamic supervision enables runtime command loading
   - Registry enables easy command discovery and management

3. Directory Structure:
   - Follows standard Mix project layout
   - Separates concerns clearly
   - Enables easy testing and maintenance

4. Process Structure:
   - Provides fault isolation
   - Enables independent command lifecycle management
   - Facilitates runtime updates

## Consequences

### Positive
- Clean separation of concerns
- Strong fault isolation
- Runtime command management
- Leverages OTP patterns
- Easy testing and maintenance

### Negative
- Additional complexity from FUSE interface
- Learning curve for OTP concepts
- Need to manage process lifecycle

### Neutral
- Need to establish command implementation patterns
- Configuration management strategy required
- Testing strategy needs to cover both Elixir and FUSE components

## Implementation Notes

1. Initial Setup:
   ```bash
   mix new command_fs --sup
   cd command_fs
   # Add dependencies to mix.exs
   ```

2. Key Dependencies:
   ```elixir
   # mix.exs
   defp deps do
     [
       {:userfs, git: "https://github.com/mwri/elixir-userfs.git"}, # Elixir FUSE implementation
       {:jason, "~> 1.4"},       # JSON parsing
       {:yaml_elixir, "~> 2.9"}, # YAML config
       {:telemetry, "~> 1.2"}    # Metrics
     ]
   end
   ```

3. FUSE Implementation:
   ```elixir
   # lib/command_fs/filesystem.ex
   defmodule CommandFS.Filesystem do
     use UserFS
     
     @impl UserFS
     def init(args) do
       {:ok, args}
     end
     
     @impl UserFS
     def readdir(_path, _offset, state) do
       # List available commands
       commands = [".", "..", "datetime", "sys", "net"]
       {:ok, commands, state}
     end
     
     @impl UserFS
     def getattr(path, state) do
       case path do
         "/" ->
           {:ok, %{access: 0o755, kind: :directory}, state}
         "/datetime" ->
           {:ok, %{access: 0o444, kind: :regular}, state}
         _ ->
           {:error, :enoent}
       end
     end
     
     @impl UserFS
     def read("/datetime", _offset, _size, state) do
       content = DateTime.utc_now() |> DateTime.to_string()
       {:ok, content, state}
     end
     def read(_path, _offset, _size, _state) do
       {:error, :enoent}
     end
   end
   ```

4. Command Behavior:
   ```elixir
   # lib/command_fs/command.ex
   defmodule CommandFS.Command do
     @callback init() :: {:ok, state :: term()} | {:error, term()}
     @callback read(path :: String.t(), state :: term()) :: 
       {:ok, content :: binary(), new_state :: term()} | 
       {:error, term()}
   end
   ```

5. Application Integration:
   ```elixir
   # lib/command_fs/application.ex
   defmodule CommandFS.Application do
     use Application
     
     def start(_type, _args) do
       children = [
         {Registry, keys: :unique, name: CommandFS.Registry},
         {DynamicSupervisor, strategy: :one_for_one, name: CommandFS.CommandSupervisor},
         {CommandFS.Filesystem, mountpoint: "/tmp/command_fs"}
       ]
       
       opts = [strategy: :one_for_one, name: CommandFS.Supervisor]
       Supervisor.start_link(children, opts)
     end
   end
   ```

## Related Decisions

- Need to define command implementation pattern
- Need to establish configuration format
- Need to define testing strategy
- Need to establish deployment process

## References

- [mwri/elixir-userfs](https://github.com/mwri/elixir-userfs)
- [Elixir GenServer](https://hexdocs.pm/elixir/GenServer.html)
- [OTP Supervisor](https://hexdocs.pm/elixir/Supervisor.html)
