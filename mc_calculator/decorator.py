import logging
import functools
import time
from typing import Callable, Any


def auto_log(logger_name: str) -> Callable:
    """
    A decorator factory that creates a logging decorator.

    Args:
        logger_name (str): The name of the logger to be used.

    Returns:
        Callable: A decorator that wraps a function to add entry and exit logging.
    """
    logger = logging.getLogger(logger_name)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            logger.info(f"Entering {func.__name__}")

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                logger.info(
                    f"Exiting {func.__name__}, Execution time: {end_time - start_time:.2f} seconds"
                )

        return wrapper

    return decorator
