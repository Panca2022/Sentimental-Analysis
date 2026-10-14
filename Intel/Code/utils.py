import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def retry(max_retries=3, backoff_factor=1.5, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    wait = backoff_factor ** attempt
                    logger.warning(
                        "Attempt %s failed for %s: %s. Retrying in %.1fs",
                        attempt + 1,
                        func.__name__,
                        e,
                        wait,
                    )
                    time.sleep(wait)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def rate_limit(seconds=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            time.sleep(seconds)
            return result
        return wrapper
    return decorator