# Command-FS

A FUSE filesystem that executes commands and returns their output as file content. This allows you to mount a directory where files represent command outputs, making it easy to integrate command outputs into your workflows.

## Requirements

- Python 3.11 or higher
- macFUSE (for macOS)
- Poetry (for development and installation)

## Installation

### From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/mangr3n/command-fs.git
   cd command-fs
   ```

2. Build the package:
   ```bash
   poetry build
   ```

3. Install globally:
   ```bash
   pip install dist/*.whl
   ```

### Using macFUSE
1. Install macFUSE (if not already installed):
   ```bash
   brew install macfuse
   ```

2. Install Command-FS:
   ```bash
   pip install command-fs
   ```
   
   Or install from source:
   ```bash
   git clone https://github.com/mangr3n/command-fs.git
   cd command-fs
   poetry build
   pip install dist/*.whl
   ```

3. Initialize the global configuration (optional):
   ```bash
   command-fs --init
   ```
   This will create a default configuration file at `~/.config/command-fs/commands.yaml`

## Usage

### Basic Usage

1. Mount the filesystem:
   ```bash
   command-fs /path/to/mount/point
   ```

2. Access command outputs:
   ```bash
   cat /path/to/mount/point/datetime  # Shows current date/time
   cat /path/to/mount/point/uptime    # Shows system uptime
   cat /path/to/mount/point/whoami    # Shows current user
   cat /path/to/mount/point/ps        # Shows process list
   ```

3. List available commands:
   ```bash
   cat /path/to/mount/point/index
   ```

4. Unmount the filesystem:
   ```bash
   umount /path/to/mount/point
   # or
   cat /path/to/mount/point/exit
   ```

### Configuration

Command-FS uses a hierarchical configuration system:
1. Global config at `~/.config/command-fs/commands.yaml`
2. Local project config in `config/commands.yaml`

When a local config is found, its commands are automatically added to the global config,
making them available system-wide. This allows you to:
- Share useful commands across projects
- Build up a library of commonly used commands
- Override global commands with project-specific versions

The configuration is merged in this order:
1. Load global config as base
2. Merge local config on top
3. Update global config with new commands from local config

Example workflow:
```bash
# Create a project-specific config
mkdir -p config
command-fs --init --config config/commands.yaml

# Add project-specific commands to config/commands.yaml
# These will automatically be added to your global config

# Mount using combined configuration
command-fs .command-fs
```

Example configuration (commands.yaml):
```yaml
commands:
  # Special commands
  index:
    description: "Lists available commands and their descriptions"
    type: "internal"
  exit:
    description: "Unmounts the filesystem"
    type: "internal"

  # System commands
  date:
    filename: "datetime"
    description: "Current date and time"
    command: "date '+%Y-%m-%d %H:%M:%S %Z'"
    timeout: 5
  
  sys-uptime:
    filename: "uptime"
    description: "System uptime information"
    command: "uptime"
    timeout: 5
```

### Project Integration

To use Command-FS in a project:

1. Create a local config file:
   ```bash
   mkdir -p config
   command-fs --init --config config/commands.yaml
   ```

2. Customize the commands in `config/commands.yaml`

3. Mount the filesystem:
   ```bash
   command-fs .command-fs  # Mounts in a hidden directory
   ```

4. Add to your project's .gitignore:
   ```
   .command-fs/
   ```

## Development

1. Clone the repository:
   ```bash
   git clone https://github.com/mangr3n/command-fs.git
   cd command-fs
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run tests:
   ```bash
   poetry run pytest
   ```

## License

[Add your license here]
