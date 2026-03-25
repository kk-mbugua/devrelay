import logging
import functools
import time
from typing import Callable

from app.core.exceptions import AuthError, TenantValidationError

logger = logging.getLogger(__name__)


def log_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            time_taken = time.perf_counter() - start
            logger.info(f"The function {func.__name__} took {time_taken} to execute")
            return result
        except Exception:
            time_taken = time.perf_counter() - start
            logger.exception(f"There was an error running {func.__name__} after {time_taken}")
            raise
    return wrapper


def require_auth(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "tenant_id" not in kwargs or kwargs["tenant_id"] is None:
            raise AuthError("tenant_id is required")
        return func(*args, **kwargs)
    return wrapper



def validate_tenant(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "tenant_id" not in kwargs:
                raise TenantValidationError("tenant_id must be a non-empty string")
        if not isinstance(kwargs["tenant_id"], str) or not kwargs["tenant_id"]:
            raise TenantValidationError("tenant_id must be a non-empty string")
        return func(*args, **kwargs)
    return wrapper