from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from math import pow
from typing import Callable
import numbers
from py_expression_eval import Parser
from math_eval import safe_compute, precedence_map, compute, binops, safe_binops
import operator
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


class CalculationString(BaseModel):
    expression: str

    def __repr__(self):
        return f"{self.expression}"

class Operator:
    def __init__(self, symbol: str, implementation: Callable[[float, float], float], priority: int):
        self.symbol = symbol
        self.implementation = implementation
        self.priority = priority

class OperatorFactory:
        
    def register_operator(self, operator: Operator):
            name = operator.symbol
            # binops is the name of operations that have (a,b) params
            # safe_binops is a special case that uses safe_compute,
            # i decided to use compute with safe=false, so i am using binops accordingly
            if name in binops.keys(): 
                function = binops[name]
                del binops[name]

                # the search for precendence method searches by token and attaches a function to the token
                # so its very important not to have more than one implementation of the same thing
                # in the module ^ is bitwiseXOR so this inteferes with power which it implements under token **
                # as the request was for ^ to map to power, this needs to be cleared correcly to work
                if function in precedence_map.keys():
                    del precedence_map[function] # Without this, its impossible to replace existing functions with custom ones

            function = binops[name] = operator.implementation
            precedence_map[function] = operator.priority
        
    
    def get_operator(self, symbol: str) -> Operator:
        if symbol not in self.operators:
            raise ValueError(f"Invalid operator: {symbol}")
        return self.operators[symbol]

operator_factory = OperatorFactory()

def register_default_operators():

    # the module i used is much more advanced and has many more operators,
    # to show how i have actually completely stripped it down, i am clearing it's builtin abilities
    # i could ofcourse let them be, and it would work just fine
    binops.clear()
    precedence_map.clear()

    def my_pow(a,b):
        return pow(a,b)
    
    operator_factory.register_operator(Operator('^', my_pow, 5))
    
    def my_sum(a,b):
        return a+b
    
    operator_factory.register_operator(Operator('+', my_sum, 2))
    def my_sub(a,b):
        return a-b
    operator_factory.register_operator(Operator('-', my_sub, 2))
    
    def my_mul(a,b):
        return a*b
    operator_factory.register_operator(Operator('*', my_mul, 3))
    
    def my_div(a,b):
         return a / b if b != 0 else "Error: Division by zero"

    operator_factory.register_operator(Operator('/', my_div, 3))
    
    


def calculate(operator: str, operand1: float, operand2: float) -> float:
    try:
        op = operator_factory.get_operator(operator)
        return op.implementation(operand1, operand2)
    except KeyError as key:
        raise ValueError(f"Invalid operator: {key}")



app = FastAPI()
register_default_operators()


origins = ["*"]  # Replace with the allowed origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

@app.post("/calculate_str")
async def perform_calculation_str(calculation: CalculationString, style: bool = False):
    try:
        result = compute(calculation.expression)
        if style:
            if result % 2 == 0:
                color = "green"
            else:
                color = "red"
            return {"result": result, "color": color}
        else:
            return {"result": result}
    except KeyError as key:
        raise ValueError(f"Symbol {key} unknown in {CalculationString}")   


if __name__ == "__main__":
    uvicorn.run("app:app", port=8001, log_level="debug", reload=True)