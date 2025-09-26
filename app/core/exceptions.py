class PracticeServiceException(Exception): 
    """Base exception for the practice service"""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = int(code)
        super().__init__(message)

class PracticeNotFoundException(PracticeServiceException):
    """Practice not found"""
    def __init__(self, message: str = "Practice not found"):
        super().__init__(message, 404)
        
class UserNotFoundException(PracticeServiceException):
    """User not found"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, 404)

class DatabaseConnectionException(PracticeServiceException):
    """Database connection error"""
    def __init__(self, message: str = "Database connection error"):
        super().__init__(message, 500)

class ValidationException(PracticeServiceException):
    """Data validation error"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, 400)