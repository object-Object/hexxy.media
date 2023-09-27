from fastapi import FastAPI

app = FastAPI(
    root_path="/api/v0",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
