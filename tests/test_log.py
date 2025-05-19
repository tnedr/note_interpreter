import os
import re
import tempfile
import logging
import sys
import io
import pytest
from note_interpreter.log import Log, log

@pytest.fixture(autouse=True)
def reset_log_singleton():
    # Reset singleton for each test
    log.reset()
    yield
    log.reset()

def test_pytest_runs():
    assert True

def test_log_print_and_levels(capsys):
    l = Log(level="basic", use_color=False)
    l.print("plain print")
    l.info("info message")
    l.debug("debug message")
    l.warning("warning message")
    l.error("error message")
    out, err = capsys.readouterr()
    assert "plain print" in out
    assert "info message" in out
    assert "warning message" in out
    assert "error message" in out
    # debug should not appear at INFO level
    assert "debug message" not in out

def test_log_debug_level_includes_debug(capsys):
    l = Log(level="debug", use_color=False)
    l.debug("debug message visible")
    out, err = capsys.readouterr()
    assert "debug message visible" in out

def test_log_coloring_in_terminal(capsys):
    l = Log(level="debug", use_color=True)
    l.info("colored info")
    l.warning("colored warning")
    l.error("colored error")
    l.debug("colored debug")
    out, err = capsys.readouterr()
    # Check for ANSI color codes
    assert "\033[32m" in out  # INFO (green)
    assert "\033[33m" in out  # WARNING (yellow)
    assert "\033[31m" in out  # ERROR (red)
    assert "\033[36m" in out  # DEBUG (cyan)

def test_log_file_output(tmp_path):
    log_file = tmp_path / "test_log.log"
    l = Log(level="debug", log_file=str(log_file), use_color=False)
    l.info("file info")
    l.error("file error")
    l.debug("file debug")
    l.warning("file warning")
    # Flush handlers
    for handler in l.logger.handlers:
        handler.flush()
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
    assert "file info" in content
    assert "file error" in content
    assert "file debug" in content
    assert "file warning" in content
    # No color codes in file
    assert "\033[" not in content

def test_log_level_filtering(capsys):
    l = Log(level="basic", use_color=False)
    l.info("info ok")
    l.debug("debug not shown")
    out, err = capsys.readouterr()
    assert "info ok" in out
    assert "debug not shown" not in out

def test_log_color_demo():
    """Demonstrate all log levels and their colors for visual inspection."""
    log.debug("This is a DEBUG message (should be cyan)")
    log.info("This is an INFO message (should be green)")
    log.warning("This is a WARNING message (should be yellow)")
    log.error("This is an ERROR message (should be red)")
    log.print("This is a PRINT message (should be default terminal color)") 