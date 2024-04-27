
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from math import pow
from typing import Callable


class Calculation(BaseModel):
    operator: str
    operand1: float
    operand2: float


class CalculationString(BaseModel):
    expression: str



class OperatorFactory:
    def __init__(self):
        self.operators = {}
    
    def register_operator(self, operator: str, implementation: Callable[[float, float], float]):
        self.operators[operator] = implementation
    
    def get_operator(self, operator: str) -> Callable[[float, float], float]:
        if operator not in self.operators:
            raise ValueError(f"Invalid operator: {operator}")
        return self.operators[operator]

operator_factory = OperatorFactory()

def register_default_operators():
    operator_factory.register_operator('+', lambda a, b: a + b)
    operator_factory.register_operator('-', lambda a, b: a - b)
    operator_factory.register_operator('*', lambda a, b: a * b)
    operator_factory.register_operator('^', lambda a, b: pow(a, b) )
    operator_factory.register_operator('/', lambda a, b: a / b if b != 0 else "Error: Division by zero")

register_default_operators()


def calculate(operator: str, operand1: float, operand2: float) -> float:
    operator_impl = operator_factory.get_operator(operator)
    return operator_impl(operand1, operand2)


def calculate_expression(expression):
    operands = expression.split()
    result = float(operands[0])

    for i in range(1, len(operands), 2):
        operator = operands[i]
        operand = float(operands[i + 1])

        result = calculate(operator, result, operand)
        
    return result


app = FastAPI()


@app.post("/calculate")
async def perform_calculation(calculation: Calculation):
    result = calculate(calculation.operator, calculation.operand1, calculation.operand2)
    return {"result": result}


@app.post("/calculate_str")
async def perform_calculation(calculation: CalculationString):
    result = calculate_expression(calculation.expression)
    return {"result": result}


if __name__ == "__main__":
    uvicorn.run("app:app", port=8001, log_level="debug", reload=True)
