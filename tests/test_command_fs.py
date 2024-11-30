"""
Tests for Command-FS.
"""
import pytest
from command_fs.commands import execute_command, CommandResult
from command_fs.cache import Cache


def test_execute_command_success():
    """Test successful command execution."""
    config = {
        'command': 'echo "test"',
        'timeout': 5,
        'format_output': True
    }
    
    result = execute_command(config)
    assert isinstance(result, CommandResult)
    assert result.success
    assert result.error is None
    assert '"test"' in result.output


def test_execute_command_failure():
    """Test failed command execution."""
    config = {
        'command': 'nonexistent_command',
        'timeout': 5,
        'format_output': True
    }
    
    result = execute_command(config)
    assert isinstance(result, CommandResult)
    assert not result.success
    assert result.error is not None


def test_cache_basic_operations():
    """Test basic cache operations."""
    cache = Cache(default_ttl=1)
    
    # Test set and get
    cache.set('test_key', 'test_value')
    assert cache.get('test_key') == 'test_value'
    
    # Test delete
    cache.delete('test_key')
    assert cache.get('test_key') is None
    
    # Test clear
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.clear()
    assert cache.get('key1') is None
    assert cache.get('key2') is None


def test_cache_expiration():
    """Test cache entry expiration."""
    import time
    
    cache = Cache(default_ttl=1)
    cache.set('test_key', 'test_value')
    
    # Value should be available immediately
    assert cache.get('test_key') == 'test_value'
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Value should be expired
    assert cache.get('test_key') is None
