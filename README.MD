# Calculator project

## Backend
- fast-api
- math-eval

- [app.py](app.py) - the main code
- [test_api.py](test-api.py) - pytest tests

### math-eval
is a library that uses 
 - binops (binary operations) --> F(a,b) as a mapping between symbol to function in dict
 - precedence_dict - a dict that defines the function (above) with priority (precedence)

 requirements
  - create a claculator api
  - expressions can be sent, expressions can include m0ore than one operand
  - handle priorities and parathesis

## FrontEnd
- [calculator.html](calculator.html)

simple javascript with html just to show it works
