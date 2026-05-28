"""
Logger Factory — Demo_QA
==========================
Creates configured loggers with consistent ISO 8601 formatting.
Outputs to both console and a session-specific log file.

Usage:
    from framework.utils.logger_factory import get_logger

    log = get_logger(__name__)
    log.info("Test started")
    log.error("Element not found: %s", locator)
"""

import logging
import os
from datetime import datetime
from pathlib import Path

from framework.utils.constants import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT, LOGS_DIR


# Module-level state for session log file
_session_log_file: str = None
_file_handler: logging.FileHandler = None
_initialized: bool = False


def _get_project_root() -> str:
    """Resolve project root from this file's location."""
    # framework/utils/logger_factory.py -> framework/utils -> framework -> Demo_QA
    return str(Path(__file__).resolve().parents[2])


def _ensure_logs_dir() -> str:
    """Create logs directory if it doesn't exist. Returns absolute path."""
    logs_path = os.path.join(_get_project_root(), LOGS_DIR)
    os.makedirs(logs_path, exist_ok=True)
    return logs_path


def _get_session_log_path() -> str:
    """Generate a unique log file path for this session."""
    global _session_log_file
    if _session_log_file is None:
        logs_dir = _ensure_logs_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        _session_log_file = os.path.join(logs_dir, f"session_{timestamp}.log")
    return _session_log_file


def _resolve_log_level(level: str = None) -> int:
    """Convert log level string to logging constant.

    Args:
        level: Log level string (DEBUG, INFO, WARNING, ERROR).
               Defaults to constants.LOG_LEVEL or INFO.

    Returns:
        Logging level integer constant.
    """
    level_str = (level or LOG_LEVEL or "INFO").upper()
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    resolved = level_map.get(level_str)
    if resolved is None:
        # Invalid level — default to INFO and warn
        logging.getLogger("logger_factory").warning(
            "Invalid log level '%s', defaulting to INFO", level_str
        )
        return logging.INFO
    return resolved


def _get_file_handler() -> logging.FileHandler:
    """Get or create the shared file handler for this session."""
    global _file_handler
    if _file_handler is None:
        log_path = _get_session_log_path()
        _file_handler = logging.FileHandler(log_path, encoding="utf-8")
        _file_handler.setLevel(logging.DEBUG)  # File captures everything
        formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        _file_handler.setFormatter(formatter)
    return _file_handler


def get_logger(name: str, level: str = None) -> logging.Logger:
    """Create or retrieve a named logger with ISO 8601 formatting.

    Loggers output to both console (at configured level) and a session-specific
    log file (at DEBUG level for full traceability).

    Format: {ISO_timestamp}.{ms} {LEVEL} {filename}:{lineno} {message}

    Args:
        name: Logger name. Typically __name__ or a class name.
        level: Override log level for this logger.
               Defaults to DEMO_QA_LOG_LEVEL env var or constants.LOG_LEVEL.

    Returns:
        Configured logging.Logger instance.

    Example:
        log = get_logger(__name__)
        log.info("Starting test execution")
        log.debug("Element found: %s", element)
        log.error("Timeout waiting for: %s", locator)
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    resolved_level = _resolve_log_level(level)
    logger.setLevel(logging.DEBUG)  # Logger captures all; handlers filter

    # Console handler — respects configured level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(resolved_level)
    console_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler — captures DEBUG and above for full session trace
    try:
        file_handler = _get_file_handler()
        logger.addHandler(file_handler)
    except (IOError, OSError) as e:
        # If we can't write to log file, continue with console only
        console_handler.setLevel(logging.DEBUG)
        logger.warning("Cannot create log file: %s. Using console only.", e)

    # Prevent propagation to root logger (avoids duplicate output)
    logger.propagate = False

    return logger


def reset():
    """Reset logger factory state. Used in testing."""
    global _session_log_file, _file_handler, _initialized
    _session_log_file = None
    if _file_handler:
        _file_handler.close()
    _file_handler = None
    _initialized = False
