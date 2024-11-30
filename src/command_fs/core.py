"""
Core FUSE implementation for Command-FS.
"""
import os
import errno
import yaml
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import subprocess
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

logger = logging.getLogger(__name__)

class CommandFS(LoggingMixIn, Operations):
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        # Build filename to command mapping
        self.files = {}
        for cmd_name, cmd_info in self.config['commands'].items():
            if cmd_info.get('type') == 'internal':
                # Special handling for internal commands
                self.files[f"/{cmd_name}"] = cmd_info
            else:
                # Regular commands
                filename = cmd_info.get('filename', cmd_name)
                self.files[f"/{filename}"] = cmd_info

    def _load_config(self, config_path: str) -> dict:
        """Load command configuration from YAML file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _execute_command(self, command: str, timeout: int = 5) -> bytes:
        """Execute a shell command and return its output."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout.encode()
        except subprocess.TimeoutExpired:
            return b"Command timed out"
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return str(e).encode()

    def _handle_internal_command(self, cmd_name: str) -> bytes:
        """Handle special internal commands."""
        if cmd_name == 'index':
            # Generate list of commands and descriptions
            output = ["Available Commands:", ""]
            for name, info in self.config['commands'].items():
                if info.get('type') != 'internal':
                    filename = info.get('filename', name)
                    desc = info.get('description', 'No description')
                    output.append(f"{filename}: {desc}")
            return '\n'.join(output).encode()
        elif cmd_name == 'exit':
            # Handle unmounting - implementation depends on your needs
            return b"Use 'umount' command to unmount the filesystem"
        return b"Unknown internal command"

    def getattr(self, path: str, fh: Optional[int] = None) -> Dict[str, Any]:
        if path == '/':
            st = dict(
                st_mode=(0o755 | 0o040000),  # directory
                st_nlink=2,
                st_size=0,
                st_ctime=0,
                st_mtime=0,
                st_atime=0,
                st_uid=os.getuid(),
                st_gid=os.getgid()
            )
        elif path in self.files:
            st = dict(
                st_mode=(0o444 | 0o100000),  # read-only file
                st_nlink=1,
                st_size=1024,  # approximate size
                st_ctime=0,
                st_mtime=0,
                st_atime=0,
                st_uid=os.getuid(),
                st_gid=os.getgid()
            )
        else:
            raise FuseOSError(errno.ENOENT)
        return st

    def read(self, path: str, size: int, offset: int, fh: int) -> bytes:
        if path not in self.files:
            raise FuseOSError(errno.ENOENT)
        
        cmd_info = self.files[path]
        
        # Handle internal commands
        if cmd_info.get('type') == 'internal':
            output = self._handle_internal_command(path[1:])  # remove leading /
        else:
            # Execute the command
            command = cmd_info['command']
            timeout = cmd_info.get('timeout', 5)
            output = self._execute_command(command, timeout)
        
        return output[offset:offset + size]

    def readdir(self, path: str, fh: int) -> list[str]:
        dirents = ['.', '..']
        if path == '/':
            dirents.extend(name[1:] for name in self.files.keys())
        return dirents


def mount_fs(mount_point: str, config_path: str) -> None:
    """Mount the Command-FS filesystem."""
    FUSE(CommandFS(config_path), mount_point, nothreads=True, foreground=True)
