from sqlmodel import Field, SQLModel  # pyright: ignore[reportUnknownVariableType]
from sqlmodel.typing import SQLModelConfig


class Number(SQLModel):
    """
    Table schema provided by Aly:
    ```sql
    CREATE TABLE numbers (
        number REAL PRIMARY KEY,
        pattern TEXT NOT NULL,
        score INTEGER NOT NULL
    );
    ```
    """

    __tablename__: str = "numbers"  # pyright: ignore[reportIncompatibleVariableOverride]
    model_config = SQLModelConfig(table=True)

    number: float = Field(primary_key=True)
    pattern: str
    score: int = Field(exclude=True)
