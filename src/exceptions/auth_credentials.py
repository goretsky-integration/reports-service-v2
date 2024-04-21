from exceptions.core import ApplicationError

__all__ = (
    'AuthCredentialsError',
    'AuthCredentialsValidationError',
    'AuthCredentialsRetrieveAttemptsExceededError',
)


class AuthCredentialsError(ApplicationError):
    """Base class for auth credentials exceptions."""
    code: str = 'AUTH_CREDENTIALS_ERROR'
    message: str = 'Auth credentials error'

    def __init__(self, account_name: str):
        self.account_name = account_name


class AuthCredentialsValidationError(AuthCredentialsError):
    """Raised when an error occurs while decoding JSON auth credentials data."""
    code: str = 'AUTH_CREDENTIALS_VALIDATION'
    message: str = 'Auth credentials validation error'


class AuthCredentialsRetrieveAttemptsExceededError(AuthCredentialsError):
    """
    Raised when the number of attempts to retrieve auth credentials is exceeded.
    """
    code: str = 'AUTH_CREDENTIALS_RETRIEVE_ATTEMPTS_EXCEEDED'
    message: str = (
        'The number of attempts to retrieve auth credentials is exceeded'
    )
