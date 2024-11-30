"""Test the command-fs CLI interface."""
import subprocess
import pytest
import yaml
from pathlib import Path
from command_fs.__main__ import initialize_config

def test_help_command(capsys):
    """Test that --help shows the correct usage information."""
    result = subprocess.run(
        ["poetry", "run", "command-fs", "--help"],
        capture_output=True,
        text=True
    )
    
    # Check return code
    assert result.returncode == 0
    
    # Check help text contains expected information
    help_text = result.stdout
    assert "Command-FS: Command Filesystem" in help_text
    assert "mount_point" in help_text
    assert "--config" in help_text
    assert "--init" in help_text
    
    # Print help text for manual verification
    print("\nHelp text output:")
    print("================")
    print(help_text)   

def test_missing_mount_point():
    """Test that running without mount_point shows help text."""
    result = subprocess.run(
        ["poetry", "run", "command-fs"],
        capture_output=True,
        text=True
    )
    
    # Should show help text
    assert "Command-FS: Command Filesystem" in result.stdout
    assert "mount_point" in result.stdout

def test_config_initialization():
    """Test that initialization creates and populates the global config."""
    # Clean up any existing config
    global_config = Path.home() / '.config' / 'command_fs' / 'commands.yaml'
    if global_config.exists():
        global_config.unlink()
    
    try:
        # Test initialization
        assert initialize_config(global_config), "Initialization should succeed"
        assert global_config.exists(), "Global config should be created"
        
        # Verify config contents
        with open(global_config) as f:
            config = yaml.safe_load(f)
        assert 'commands' in config, "Config should have commands section"
        assert len(config['commands']) > 0, "Config should have some commands defined"
        
        # Check a specific command
        assert 'date' in config['commands'], "Config should have 'date' command"
        assert 'description' in config['commands']['date'], "Command should have description"
        assert 'command' in config['commands']['date'], "Command should have command definition"
    
    finally:
        # Clean up
        if global_config.exists():
            global_config.unlink()

if __name__ == '__main__':
    print("\nRunning CLI Tests")
    print("================")
    exit_code = pytest.main([__file__, '-v', '-s'])
    print("\nTest Summary")
    print("============")
    print(f"Total tests: {len([item for item in globals().items() if item[0].startswith('test_')])}")
    print(f"Exit code: {exit_code}")
