import logging
import functools
import time


def auto_log(logger_name):
    logger = logging.getLogger(logger_name)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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
