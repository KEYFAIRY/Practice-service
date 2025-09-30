class PracticeServiceException(Exception):
    """Base exception for the practice service"""
    def __init__(self, message: str, code: int = 500, error_code: str = "SERVICE_ERROR", details: dict | None = None):
        self.message = message
        self.code = int(code)
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)

    def __str__(self):
        return f"[{self.code}] {self.error_code}: {self.message} | Details: {self.details}"


class PracticeNotFoundException(PracticeServiceException):
    """Practice not found"""
    def __init__(self, practice_id: str):
        super().__init__(
            message=f"Practice with id {practice_id} not found",
            code=404,
            error_code="PRACTICE_NOT_FOUND",
            details={"practice_id": practice_id}
        )
        

class ReportNotFoundException(PracticeServiceException):
    """Report not found"""
    def __init__(self, practice_id: str):
        super().__init__(
            message=f"Report for practice {practice_id} not found",
            code=404,
            error_code="REPORT_NOT_FOUND",
            details={"practice_id": practice_id}
        )


class UserNotFoundException(PracticeServiceException):
    """User not found"""
    def __init__(self, user_id: str):
        super().__init__(
            message=f"User with id {user_id} not found",
            code=404,
            error_code="USER_NOT_FOUND",
            details={"user_id": user_id}
        )


class DatabaseConnectionException(PracticeServiceException):
    """Database connection error"""
    def __init__(self, message: str = "Database connection error"):
        super().__init__(message, 500, error_code="DB_CONNECTION_ERROR")


class ValidationException(PracticeServiceException):
    """Data validation error"""
    def __init__(self, message: str = "Validation error", details: dict | None = None):
        super().__init__(message, 400, error_code="VALIDATION_ERROR", details=details)