from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from math import pow
from typing import Callable
import numbers
from py_expression_eval import Parser
from math_eval import operator
class Calculation(BaseModel):
    operator: str
    operand1: float
    operand2: float

class CalculationString(BaseModel):
    expression: str

class Operator:
    def __init__(self, symbol: str, implementation: Callable[[float, float], float], priority: int):
        self.symbol = symbol
        self.implementation = implementation
        self.priority = priority

class OperatorFactory:
    def __init__(self):
        Parser
        self.operators = {}
    
    def register_operator(self, operator: Operator):
        self.operators[operator.symbol] = operator
    
    def get_operator(self, symbol: str) -> Operator:
        if symbol not in self.operators:
            raise ValueError(f"Invalid operator: {symbol}")
        return self.operators[symbol]

operator_factory = OperatorFactory()

def register_default_operators():
    operator_factory.register_operator(Operator('+', lambda a, b: a + b, 1))
    operator_factory.register_operator(Operator('-', lambda a, b: a - b, 1))
    operator_factory.register_operator(Operator('*', lambda a, b: a * b, 2))
    operator_factory.register_operator(Operator('^', lambda a, b: pow(a, b), 3))
    operator_factory.register_operator(Operator('/', lambda a, b: a / b if b != 0 else "Error: Division by zero", 2))

register_default_operators()

def calculate(operator: str, operand1: float, operand2: float) -> float:
    op = operator_factory.get_operator(operator)
    return op.implementation(operand1, operand2)

# class Node:
#     def __init__(self,value,left,right):
#         self.left = left
#         self.right = right
#         self.value = value

#     def __repr__(self):
#         return f"{
#                 'operator': {self.value},
#                 'left': {self.left},
#                 'right': {self.right}
#             }"


# import re

# def create_tree(expression):
#     stack = []
#     tokens = re.findall(r"[-+*/^]|\d+(?:\.\d+)?|[A-Z]+", expression)
    
#     # Handle exponents
#     pow_idx = tokens.index("^")
#     while pow_idx > -1:
#         numB4 = tokens[pow_idx-1]
#         numafter = tokens[pow_idx+1]
#         op  = tokens[pow_idx]
#         tokens[pow_idx-1] = tokens[pow_idx] = tokens[pow_idx+1] = None
#         stack.append({
#                 'operator': op,
#                 'left': numB4,
#                 'right': numafter
#             })
#         try:
#             pow_idx = tokens.index("^")
#         except ValueError:
#             break
    
#     # Handle multiplication and division
#     mul_div_idx = next((i for i, x in enumerate(tokens) if x in ['*', '/']), -1)
#     while mul_div_idx > -1:
#         numB4 = tokens[mul_div_idx-1]
#         numafter = tokens[mul_div_idx+1]
#         op  = tokens[mul_div_idx]
#         tokens[mul_div_idx-1] = tokens[mul_div_idx] = tokens[mul_div_idx+1] = None
#         stack.append({
#                 'operator': op,
#                 'left': numB4,
#                 'right': numafter
#             })
#         try:
#             mul_div_idx = next((i for i, x in enumerate(tokens) if x in ['*', '/']), -1)
#         except ValueError:
#             break
    
#     # Handle addition and subtraction
#     add_sub_idx = next((i for i, x in enumerate(tokens[::-1]) if x in ['+', '-']), -1)
#     while add_sub_idx > -1:
#         numB4 = tokens[add_sub_idx-1]
#         numafter = tokens[add_sub_idx+1]
#         op  = tokens[add_sub_idx]
#         tokens[add_sub_idx-1] = tokens[add_sub_idx] = tokens[add_sub_idx+1] = None
#         stack.append({
#                 'operator': op,
#                 'left': numB4,
#                 'right': numafter
#             })
#         try:
#             add_sub_idx = next((i for i, x in enumerate(tokens[::-1]) if x in ['+', '-']), -1)
#         except ValueError:
#             break
    
#     if len(stack) != 1:
#         raise ValueError("Invalid expression")
#     return stack.pop()


# def print_tree(node, level=0):
#     if isinstance(node, dict):
#         print_tree(node['right'], level + 1)
#         print(' ' * 4 * level + '-> ' + node['operator'])
#         print_tree(node['left'], level + 1)
#     else:
#         print(' ' * 4 * level + '-> ' + str(node))

# def evaluate_tree(node):
#     if isinstance(node, dict):
#         left_value = evaluate_tree(node['left'])
#         right_value = evaluate_tree(node['right'])
#         operator = node['operator']
        
#         if operator == '+':
#             return left_value + right_value
#         elif operator == '-':
#             return left_value - right_value
#         elif operator == '*':
#             return left_value * right_value
#         elif operator == '/':
#             return left_value / right_value
#         elif operator == '^':
#             return left_value ** right_value
#         else:
#             raise ValueError(f"Invalid operator: {operator}")
#     else:
#         return node


def calculate_expression(expression):
    
    expression_tree = create_tree(expression)
    print_tree(expression_tree)
    result = evaluate_tree(expression_tree)
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