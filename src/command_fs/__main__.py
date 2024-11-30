"""
Command-FS entry point
"""
import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import Optional
from .core import mount_fs

def get_default_config_path() -> str:
    """Get the default config file path."""
    # Check for config in current directory first
    local_config = Path(os.getcwd()) / '.config' / 'command_fs' / 'commands.yaml'
    if local_config.exists():
        return str(local_config)
    
    # Fall back to global config
    global_config = Path.home() / '.config' / 'command_fs' / 'commands.yaml'
    return str(global_config)

def initialize_config(global_config_path: Optional[Path] = None) -> bool:
    """Initialize the command-fs configuration.
    
    Args:
        global_config_path: Path to global config. If None, uses default.
    
    Returns:
        bool: True if initialization succeeded, False otherwise.
    """
    if global_config_path is None:
        global_config_path = Path.home() / '.config' / 'command_fs' / 'commands.yaml'
    
    try:
        # Create parent directories
        global_config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy default config if it doesn't exist
        if not global_config_path.exists():
            default_config = Path(__file__).parent / 'default_config' / 'commands.yaml'
            if not default_config.exists():
                print(f"Error: Default config not found at {default_config}")
                return False
            
            shutil.copy2(str(default_config), str(global_config_path))
            print(f"Created global config at: {global_config_path}")
        return True
    except Exception as e:
        print(f"Error initializing config: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Command-FS: Command Filesystem')
    parser.add_argument('mount_point', nargs='?', help='Directory to mount the filesystem')
    parser.add_argument(
        '--config',
        default=get_default_config_path(),
        help='Path to commands configuration file'
    )
    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize global config file'
    )
    
    args = parser.parse_args()
    
    # Handle initialization
    if args.init:
        if not initialize_config():
            sys.exit(1)
        if not args.mount_point:
            return
    
    # If no mount point provided, show help and exit
    if not args.mount_point:
        parser.print_help()
        sys.exit(1)

    mount_point = os.path.abspath(args.mount_point)
    config_path = os.path.abspath(args.config)

    # Create mount point if it doesn't exist
    os.makedirs(mount_point, exist_ok=True)

    print(f"Mounting Command-FS at {mount_point}")
    print(f"Using config file: {config_path}")
    print(f" {mount_point}/index - lists available commands (w/descriptions)")
    print(f" {mount_point}/exit - shows unmount instructions")

    try:
        mount_fs(mount_point, config_path)
    except KeyboardInterrupt:
        print("\nUnmounting Command-FS...")

if __name__ == '__main__':
    main()
