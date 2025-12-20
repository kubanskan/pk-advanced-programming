from fastapi import status


class ValidationError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DuplicateNameError(ValidationError):
    status_code = status.HTTP_409_CONFLICT


class InvalidFormatError(ValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class PriceOutOfRangeError(ValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class ForbiddenWordError(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
