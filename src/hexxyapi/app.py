from fastapi import Depends, FastAPI
from sqlmodel import Session

from .db.engine import get_session
from .db.model.pattern import Number
from .errors import NotFoundException

app = FastAPI(
    # TODO: there's probably a better way to do this than just pointing the proxy here
    root_path="/api/v0",
)


@app.get("/pattern/number/{number}")
async def get_number(
    *,
    session: Session = Depends(get_session),
    number: int,
) -> Number:
    result = session.get(Number, number)
    if result is None:
        raise NotFoundException("Number literal")

    return result
