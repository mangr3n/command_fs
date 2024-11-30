"""
Configuration management for Command-FS.
"""
from typing import Dict, Any, Optional
import os
from pathlib import Path
import yaml


class Config:
    """Configuration manager for Command-FS."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self.global_config_path = Path.home() / '.config' / 'command_fs' / 'commands.yaml'
        self.local_config_path = Path(os.getcwd()) / '.config' / 'command_fs' / 'commands.yaml'
        self.commands: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML files, merging global and local configs."""
        self.commands = {'commands': {}}
        
        # Load global config if it exists
        if self.global_config_path.exists():
            with open(self.global_config_path, 'r') as f:
                global_config = yaml.safe_load(f)
                if global_config and 'commands' in global_config:
                    self.commands['commands'].update(global_config['commands'])
        
        # Load and merge local config if it exists
        if self.local_config_path.exists():
            with open(self.local_config_path, 'r') as f:
                local_config = yaml.safe_load(f)
                if local_config and 'commands' in local_config:
                    # Local config overrides global config in memory only
                    self.commands['commands'].update(local_config['commands'])
        
        if not self.commands['commands']:
            raise ValueError("No valid configuration found")
    
    def get_command(self, name: str) -> Optional[Dict[str, Any]]:
        """Get command configuration by name."""
        return self.commands['commands'].get(name)
    
    def list_commands(self) -> Dict[str, str]:
        """List all available commands with their descriptions."""
        return {
            name: cmd.get('description', 'No description available')
            for name, cmd in self.commands['commands'].items()
        }
    
    @property
    def command_files(self) -> Dict[str, None]:
        """Get dictionary of command files for FUSE filesystem."""
        return {f"/{name}": None for name in self.commands['commands'].keys()}
