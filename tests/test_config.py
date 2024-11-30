"""Test the configuration loading system."""
import os
from pathlib import Path
import pytest
import yaml
from command_fs.config import Config

def setup_test_configs():
    """Set up test configuration files."""
    # Create global config
    global_config_dir = Path.home() / '.config' / 'command_fs'
    global_config_dir.mkdir(parents=True, exist_ok=True)
    global_config = {
        'commands': {
            'date': {
                'description': 'Show current date',
                'command': 'date'
            },
            'uptime': {
                'description': 'Show system uptime',
                'command': 'uptime'
            }
        }
    }
    with open(global_config_dir / 'commands.yaml', 'w') as f:
        yaml.safe_dump(global_config, f)

    # Create local config
    local_config_dir = Path.cwd() / '.config' / 'command_fs'
    local_config_dir.mkdir(parents=True, exist_ok=True)
    local_config = {
        'commands': {
            'date': {
                'description': 'Custom date format',
                'command': 'date "+%Y-%m-%d"'
            },
            'ps': {
                'description': 'Process list',
                'command': 'ps aux'
            }
        }
    }
    with open(local_config_dir / 'commands.yaml', 'w') as f:
        yaml.safe_dump(local_config, f)

def cleanup_test_configs():
    """Clean up test configuration files."""
    # Remove global config
    global_config_file = Path.home() / '.config' / 'command_fs' / 'commands.yaml'
    if global_config_file.exists():
        global_config_file.unlink()
    
    # Remove local config
    local_config_file = Path.cwd() / '.config' / 'command_fs' / 'commands.yaml'
    if local_config_file.exists():
        local_config_file.unlink()

def test_config_loading():
    """Test that configs are loaded correctly and local overrides work."""
    try:
        # Set up test configs
        setup_test_configs()

        # Load configs
        config = Config()

        # Check that all commands are present
        assert 'date' in config.commands['commands']
        assert 'uptime' in config.commands['commands']
        assert 'ps' in config.commands['commands']

        # Check that local config overrides global config
        assert config.commands['commands']['date']['command'] == 'date "+%Y-%m-%d"'
        
        # Check that global-only commands are preserved
        assert config.commands['commands']['uptime']['command'] == 'uptime'
        
        # Check that local-only commands are added
        assert config.commands['commands']['ps']['command'] == 'ps aux'

        print("\nTest Results:")
        print("=============")
        print("Commands loaded:", list(config.commands['commands'].keys()))
        print("\nCommand Details:")
        for name, cmd in config.commands['commands'].items():
            print(f"\n{name}:")
            print(f"  Description: {cmd['description']}")
            print(f"  Command: {cmd['command']}")

    finally:
        # Clean up test configs
        cleanup_test_configs()

if __name__ == '__main__':
    test_config_loading()
