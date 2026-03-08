class UserNotFoundExpcection(Exception):
    detail = "User not found"

class UserNotCorrectPasswordExpcection(Exception):
    detail = "User password not correct"

class UserAlreadyExistsException(Exception):
    detail = "User already exists"

class TokenExpired(Exception):
    detail = "Token has expired"

class TokenNotCorrect(Exception):
    detail = "Token Not Correct"

class TaskNotFound(Exception):
    detail = "Task not found"
