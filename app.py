
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class Calculation(BaseModel):
    operator: str
    operand1: float
    operand2: float


class CalculationString(BaseModel):
    expression: str


def calculate(operator, operand1, operand2):
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        if operand2 != 0:
            return operand1 / operand2
        else:
            return "Error: Division by zero"
    else:
        return "Error: Invalid operator"


def calculate_expression(expression):
    operands = expression.split()
    result = float(operands[0])

    for i in range(1, len(operands), 2):
        operator = operands[i]
        operand = float(operands[i + 1])

        if operator == '+':
            result += operand
        elif operator == '-':
            result -= operand
        elif operator == '*':
            result *= operand
        elif operator == '/':
            if operand != 0:
                result /= operand
            else:
                return "Error: Division by zero"
        else:
            return f"Error: Invalid operator '{operator}'"

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
