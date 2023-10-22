import uvicorn
from fastapi import Depends, FastAPI
from sqlmodel import Session

from .db.engine import check_db_connection, get_session
from .db.model.pattern import Number
from .errors import NotFoundException

app = FastAPI(
    title="HexxyAPI",
    version="0.1.0",
    # TODO: there's probably a better way to do this than just pointing the proxy here
    root_path="/api/v0",
)


@app.get("/health")
async def get_health():
    return {"status": "OK"}


@app.get("/pattern/number/{number}")
async def get_number(
    *,
    session: Session = Depends(get_session),
    number: float,
) -> Number:
    is_negative = number < 0
    if is_negative:
        number *= -1

    result = session.get(Number, number)
    if result is None:
        raise NotFoundException("Number literal")

    if is_negative:
        result.number *= -1
        result.pattern = "dedd" + result.pattern.removeprefix("aqaa")

    return result


if __name__ == "__main__":
    check_db_connection()
    uvicorn.run(  # pyright: ignore[reportUnknownMemberType]
        app,
        host="0.0.0.0",
        port=5000,
    )
