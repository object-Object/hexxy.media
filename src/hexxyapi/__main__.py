import uvicorn

from hexxyapi.db.engine import check_connection

from .app import app

check_connection()

uvicorn.run(  # pyright: ignore[reportUnknownMemberType]
    app,
    host="0.0.0.0",
    port=5000,
)
