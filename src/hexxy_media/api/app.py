import string

import uvicorn
from fastapi import Depends, FastAPI, Path, Query, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session

from hexxy_media.api.utils.lehmer import swizzle

from .db.engine import check_db_connection, get_session
from .db.model.pattern import Number
from .errors import NotFoundException

MAX_LEHMER_ITEMS = 1000

DEFAULT_LEHMER_START = string.ascii_lowercase[::-1]

LEHMER_FINISH = Path(
    openapi_examples={
        "default": {
            "summary": "Default format",
            "value": "bca",
        },
        "top_first": {
            "summary": "Default format (top_first=true)",
            "value": "acb",
        },
        "commas": {
            "summary": "Comma separated",
            "description": "`start`=`bottom,middle,top`",
            "value": "middle,bottom,top",
        },
    }
)

LEHMER_START = Query(
    default_factory=lambda: DEFAULT_LEHMER_START,
    openapi_examples={
        "default": {
            "summary": "Default",
            "value": DEFAULT_LEHMER_START,
        },
        "top_first": {
            "summary": "Default (top_first=true)",
            "value": DEFAULT_LEHMER_START[::-1],
        },
    },
)

LEHMER_TOP_FIRST = Query(
    default=False,
    description="If true, assume the first item is at the top of the stack.",
)

app = FastAPI(
    title="HexxyAPI",
    version="0.1.0",
)


@app.get("/health")
async def get_health():
    return {"status": "OK"}


@app.get("/lehmer/{finish}")
def get_lehmer(
    finish: str = LEHMER_FINISH,
    *,
    start: str = LEHMER_START,
    top_first: bool = LEHMER_TOP_FIRST,
) -> int:
    start_items = split_lehmer_list(start)
    finish_items = split_lehmer_list(finish)

    if top_first is True:
        start_items.reverse()
        finish_items.reverse()

    return swizzle(
        start=start_items,
        finish=finish_items,
    )


@app.get("/pattern/lehmer/{finish}")
async def get_pattern_lehmer(
    finish: str = LEHMER_FINISH,
    *,
    start: str = LEHMER_START,
    top_first: bool = LEHMER_TOP_FIRST,
    session: Session = Depends(get_session),
) -> Number:
    code = get_lehmer(finish, start=start, top_first=top_first)
    return await get_pattern_number(code, session=session)


@app.get("/pattern/number/{number}")
async def get_pattern_number(
    number: float,
    *,
    session: Session = Depends(get_session),
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


@app.exception_handler(ValueError)
def handle_ValueError(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


# TODO: use this as a Pydantic validator
def split_lehmer_list(raw: str) -> list[str]:
    for separator in [",", "|", ";", "/"]:
        if separator in raw:
            values = raw.split(separator)
            break
    else:
        values = list(raw)

    if len(set(values)) != len(values):
        raise ValueError("Duplicate items are not permitted")

    if len(values) > MAX_LEHMER_ITEMS:
        raise ValueError(f"Max number of items permitted is {1000}, got {len(values)}")

    return values


if __name__ == "__main__":
    check_db_connection()
    uvicorn.run(  # pyright: ignore[reportUnknownMemberType]
        app,
        host="0.0.0.0",
        port=5000,
        # TODO: there's probably a better way to do this...
        root_path="/api/v0",
    )
