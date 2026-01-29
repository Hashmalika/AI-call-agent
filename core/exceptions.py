class ServiceError(Exception):
    pass

class TransientServiceError(ServiceError):
    pass

class PermanentServiceError(ServiceError):
    pass

class ServiceUnavailable(TransientServiceError):  # 503
    pass

class TimeoutError(TransientServiceError):
    pass

class AuthError(PermanentServiceError):
    pass

class InvalidPayloadError(PermanentServiceError):
    pass

class QuotaExceededError(PermanentServiceError):
    pass
