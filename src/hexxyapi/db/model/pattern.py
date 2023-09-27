from sqlmodel import Field, SQLModel
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

    __tablename__: str = "numbers"
    model_config = SQLModelConfig(table=True)

    number: float = Field(primary_key=True)
    pattern: str
    score: int
