import pytest
from app.core.decorators import log_execution, require_auth, validate_tenant
from app.core.exceptions import AuthError, TenantValidationError


# --- log_execution ---

def test_log_execution_returns_result():
    # define a simple decorated function inline
    # call it and assert the return value is correct
    @log_execution
    def double(num: int):
        return num * 2
    num = 6
    assert double(num) == num*2, "Decorator is affecting the function"
    


def test_log_execution_reraises_exception():
    # define a decorated function that raises
    # use pytest.raises to assert the exception propagates
    @log_execution
    def some_func():
        raise ValueError
    with pytest.raises(ValueError) as info:
        some_func()
    


# --- require_auth ---

def test_require_auth_missing_tenant_id():
    @require_auth
    def some_func(num: int, tenant_id: str):
        return num
    with pytest.raises(AuthError) as info:
        some_func(1)


def test_require_auth_none_tenant_id():
    @require_auth
    def some_func(num: int, tenant_id: str = None):
        return num  
    with pytest.raises(AuthError) as info:
        some_func(2, tenant_id=None)


def test_require_auth_valid_tenant_id():
    @require_auth
    def some_func(num: int, tenant_id: str):
        return num
    num = 3
    assert some_func(num, tenant_id="qwerty") == num, "AuthError should not be invoked"

# --- validate_tenant ---

def test_validate_tenant_missing_tenant_id():
    @validate_tenant
    def some_func(num: int, tenant_id: str):
        return num
    with pytest.raises(TenantValidationError) as info:
        some_func(1)


def test_validate_tenant_empty_string():
    @validate_tenant
    def some_func(num: int, tenant_id: str):
        return num
    with pytest.raises(TenantValidationError) as info:
        some_func(1, tenant_id="")


def test_validate_tenant_not_a_string():
    @validate_tenant
    def some_func(num: int, tenant_id: str):
        return num
    with pytest.raises(TenantValidationError) as info:
        some_func(1, tenant_id=123)


def test_validate_tenant_valid_tenant_id():
    @validate_tenant
    def some_func(num: int, tenant_id: str):
        return num
    num = 5
    assert some_func(num, tenant_id="something") == num, "TenantValidationError should not be invoked"
