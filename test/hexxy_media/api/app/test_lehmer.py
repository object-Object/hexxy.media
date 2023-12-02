import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ["finish", "want_code"],
    [
        ["a", 0],
        ["ba", 0],
        ["acb", 4],
        ["bca", 2],
        ["decba", 24],
    ],
)
def test_default(app: TestClient, finish: str, want_code: int):
    code = get_int(app, f"/lehmer/{finish}")
    assert code == want_code


@pytest.mark.parametrize(
    ["start", "finish", "want_code"],
    [
        ["a", "a", 0],
        ["ba", "ba", 0],
        ["cba", "acb", 4],
        ["cba", "bca", 2],
        ["edcba", "decba", 24],
        ["abcde", "abced", 1],
        ["bottom,middle,top", "middle,bottom,top", 2],
    ],
)
def test_start(app: TestClient, start: str, finish: str, want_code: int):
    code = get_int(app, f"/lehmer/{finish}?start={start}")
    assert code == want_code


@pytest.mark.parametrize(
    ["start", "finish", "want_code"],
    [
        ["a", "a", 0],
        ["ab", "ab", 0],
        ["abc", "bca", 4],
        ["abc", "acb", 2],
        ["abcde", "abced", 24],
        ["edcba", "decba", 1],
    ],
)
def test_top_first(app: TestClient, start: str, finish: str, want_code: int):
    code = get_int(app, f"/lehmer/{finish}?start={start}&top_first=1")
    assert code == want_code


def test_forbid_duplictes(app: TestClient):
    response = app.get("/lehmer/dcbaa?start=abacd")
    assert response.status_code == 400


def get_int(app: TestClient, url: str):
    response = app.get(url)
    response.raise_for_status()
    return int(response.content)
