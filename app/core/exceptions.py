# 1. Base exception for everything in DevRelay
class DevRelayError(Exception):
    ...


# 2. Base for auth-related errors
class AuthError(DevRelayError):
    ...

#I want it under DevRelayError. There are instances where Tenant validation does not relate the authentication.
class TenantValidationError(DevRelayError):
    ...

