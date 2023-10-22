from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(status_code=404, detail=f"{name} not found")
