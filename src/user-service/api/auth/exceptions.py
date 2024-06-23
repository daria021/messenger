class TokenException(Exception):
    pass


class TokenEmptyException(TokenException):
    pass


class TokenInvalidException(TokenException):
    pass


class TokenExpiredException(TokenException):
    pass


class TokenNotFoundException(TokenException):
    pass

class UserNotFound(Exception):
    pass
