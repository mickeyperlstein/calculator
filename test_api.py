import pytest
from fastapi.testclient import TestClient
from  app import app

client = TestClient(app)

@pytest.mark.parametrize("operand1, operator, operand2, expected", [
    (3, "+", 4, 7),
    (10, "-", 6, 4),
    (2, "*", 5, 10),
    (10, "/", 2, 5),
    (2, "^", 3, 8),
])
def test_calculate_endpoint(operand1, operator, operand2, expected):
    response = client.post("/calculate", json={
        "operand1": operand1,
        "operator": operator,
        "operand2": operand2
    })
    assert response.status_code == 200
    assert response.json()["result"] == expected

@pytest.mark.parametrize("expression, expected", [
    ("0.01 + 0.99+ 2 * 3 - 4 / 2 + 2 ^ 3", 13),
    ("(3 + 4) - 2 * 5 ", -3),
    ("10 - 3 + 2 * 4 / 2", 11),
])
def test_calculate_string_endpoint(expression, expected):
    response = client.post("/calculate_str", json={
        "expression": expression
    })
    assert response.status_code == 200
    assert response.json()["result"] == expected

def test_invalid_operator():
    response = client.post("/calculate", json={
        "operand1": 5,
        "operator": "%",
        "operand2": 3
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Invalid operator"

def test_division_by_zero():
    response = client.post("/calculate", json={
        "operand1": 10,
        "operator": "/",
        "operand2": 0
    })
    assert response.status_code == 200
    assert response.json()["result"] == "Error: Division by zero"