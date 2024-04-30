import pytest
from fastapi.testclient import TestClient
from  app import app

client = TestClient(app)

@pytest.mark.parametrize("expression, expected", [
    ("2.0 ^ 3.0", 8.0),
    ("0.99+0.01+ 2.0 * 3.0 - 4.0 / 2.0 + 2.0 ^ 3.0", 13.0),
    ("(3 + 4) - 2 * 5 ", -3),
    ("0.99+0.01+ 2.0 * 3.0 - 4.0",3)
])
def test_calculate_string_endpoint(expression, expected):
    response = client.post("/calculate_str", json={
        "expression": expression
    })
    assert response.status_code == 200
    assert response.json()["result"] == expected


def test_division_by_zero():
    try:
        response = client.post("/calculate_str", json={
            "expression": "10/0"
        })

    except ZeroDivisionError:
        pass

 
@pytest.mark.parametrize("expression, expected", [
    ("2.0 ^ 3.0", "blue"),
    ("1*13", "red"),
    
])
def test_calculate_style(expression, expected):
    response = client.post("/calculate_str", json={
        "expression": expression
    }, params={"style":"true"})
    
    assert response.status_code == 200
    assert response.json()["color"] == expected
   