from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.main import app


client = TestClient(app)


def test_calculate_deposit_success():
    data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }
    response = client.post("/calculate", json=data)
    assert response.status_code == 200
    expected_result = {
        "31.01.2021": 10050.0,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75
    }
    assert response.json() == expected_result


def test_calculate_deposit_invalid_date():
    data = {
        "date": "31-01-2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }


    response = client.post("/calculate", json=data)


    assert response.status_code == 422


    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "date"],
                "msg": "String should match pattern '^\\d{2}\\.\\d{2}\\.\\d{4}$'",
                "type": "string_pattern_mismatch",
                "ctx": {"pattern": "^\\d{2}\\.\\d{2}\\.\\d{4}$"},
                "input": "31-01-2021"
            }
        ]
    }


def test_calculate_deposit_out_of_bounds():
    data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 5000,
        "rate": 6
    }


    response = client.post("/calculate", json=data)


    assert response.status_code == 422


