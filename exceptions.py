from fastapi import HTTPException


class AuthenticationException(HTTPException):
    def __init__(self, name: str):
        self.name = name
