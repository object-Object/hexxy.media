import uvicorn

from .app import app

uvicorn.run(  # pyright: ignore[reportUnknownMemberType]
    app,
    host="0.0.0.0",
    port=5000,
)
