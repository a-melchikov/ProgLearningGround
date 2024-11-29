import pytest
from logging import Logger, StreamHandler
from app.core.logger_setup import LogConfig, LoggerSetup, LogLevel, get_logger


def test_default_logger_config() -> None:
    """
    Test that the default logger is created with default settings.
    """
    logger = get_logger("test_logger")
    assert isinstance(logger, Logger)
    assert logger.level == LogLevel.INFO.value


def test_logger_with_custom_config() -> None:
    """
    Test creating a logger with custom configuration.
    """
    custom_config = LogConfig(
        level=LogLevel.DEBUG,
        filename=None,  # Console output only
        max_bytes=1_000_000,
        backup_count=2,
        console_level=LogLevel.INFO,
        file_level=LogLevel.WARNING,
    )
    logger_setup = LoggerSetup(log_config=custom_config, logger_name="custom_logger")
    logger = logger_setup.get_logger()

    # Check that the logging level matches the custom configuration
    assert logger.level == LogLevel.DEBUG.value

    # Check that the logger has the appropriate handlers
    assert len(logger.handlers) == 1
    console_handler = logger.handlers[0]
    assert isinstance(console_handler, StreamHandler)
    assert console_handler.level == LogLevel.INFO.value


def test_file_handler_creation(tmp_path) -> None:
    """
    Test creating a logger with a file handler and verifying log file creation.
    """
    log_file = tmp_path / "test.log"
    config = LogConfig(
        level=LogLevel.DEBUG,
        filename=str(log_file),
        max_bytes=500_000,
        backup_count=1,
        console_level=LogLevel.INFO,
        file_level=LogLevel.DEBUG,
    )
    logger_setup = LoggerSetup(log_config=config, logger_name="file_logger")
    logger = logger_setup.get_logger()

    # Write a log message and ensure the log file is created
    logger.debug("This is a debug message")
    logger.handlers[0].flush()

    assert log_file.exists()


def test_logger_restart() -> None:
    """
    Test restarting a logger with a new configuration.
    """
    initial_config = LogConfig(
        level=LogLevel.INFO,
        filename=None,
        console_level=LogLevel.INFO,
        file_level=LogLevel.WARNING,
    )
    logger_setup = LoggerSetup(log_config=initial_config, logger_name="restart_logger")
    logger = logger_setup.get_logger()

    # Verify the initial logging level
    assert logger.level == LogLevel.INFO.value

    # Restart the logger with a new configuration
    new_config = LogConfig(
        level=LogLevel.DEBUG,
        filename=None,
        console_level=LogLevel.DEBUG,
        file_level=LogLevel.ERROR,
    )
    logger_setup.restart_logger(new_config=new_config)

    # Verify that the logging level has been updated
    assert logger.level == LogLevel.DEBUG.value


def test_invalid_log_config():
    """
    Test that invalid configuration raises appropriate exceptions.
    """
    with pytest.raises(ValueError, match="max_bytes must be greater than 0"):
        LogConfig(max_bytes=0)

    with pytest.raises(ValueError, match="backup_count cannot be negative"):
        LogConfig(backup_count=-1)
