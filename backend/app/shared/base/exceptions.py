class ResolveAIException(Exception):
    """Base exception for ResolveAI."""


class NotFoundException(ResolveAIException):
    """Raised when a record is not found."""


class AlreadyExistsException(ResolveAIException):
    """Raised when a duplicate record is found."""


class UnauthorizedException(ResolveAIException):
    """Raised when user is not authorized."""