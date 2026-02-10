"""
Calculator tool for performing mathematical calculations.
"""

from typing import Dict, Any, Union
import re
import math


class Calculator:
    """Tool for performing mathematical calculations safely."""
    
    def __init__(self):
        """Initialize calculator with safe evaluation."""
        # Allowed functions and constants
        self.safe_dict = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
            "math": math,
        }
        
        # Add math functions
        for func_name in dir(math):
            if not func_name.startswith("_"):
                func = getattr(math, func_name)
                if callable(func):
                    self.safe_dict[func_name] = func
    
    def execute(self, expression: str) -> str:
        """
        Execute a mathematical calculation.
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            Result as string
        """
        try:
            # Clean the expression
            expression = self._clean_expression(expression)
            
            # Evaluate safely
            result = self._safe_eval(expression)
            
            # Format result
            if isinstance(result, float):
                # Check if it's a whole number
                if result.is_integer():
                    return str(int(result))
                else:
                    # Round to reasonable precision
                    return str(round(result, 10))
            else:
                return str(result)
                
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def _clean_expression(self, expression: str) -> str:
        """
        Clean and preprocess the expression.
        
        Args:
            expression: Raw expression string
            
        Returns:
            Cleaned expression
        """
        # Remove common text prefixes
        expression = re.sub(r"^(calculate|compute|what is|what's|solve|evaluate)\s*", "", expression, flags=re.IGNORECASE)
        
        # Remove question marks and extra whitespace
        expression = expression.strip().rstrip("?")
        
        # Replace common text representations
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")
        
        # Remove spaces
        expression = expression.replace(" ", "")
        
        return expression
    
    def _safe_eval(self, expression: str) -> Union[int, float]:
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression: Mathematical expression
            
        Returns:
            Evaluation result
        """
        # Additional safety check - only allow numbers, operators, and safe functions
        allowed_chars = set("0123456789+-*/.()[]{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ, ")
        
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Expression contains invalid characters")
        
        try:
            # Use eval with safe dictionary
            result = eval(expression, self.safe_dict)
            return result
        except SyntaxError as e:
            raise ValueError(f"Invalid expression syntax: {str(e)}")
        except Exception as e:
            raise ValueError(f"Evaluation error: {str(e)}")
    
    def calculate(self, expression: str) -> Union[int, float]:
        """
        Calculate and return numeric result.
        
        Args:
            expression: Mathematical expression
            
        Returns:
            Numeric result
        """
        cleaned = self._clean_expression(expression)
        return self._safe_eval(cleaned)


if __name__ == "__main__":
    # Test the calculator
    calc = Calculator()
    
    test_expressions = [
        "25 * 4 + 100",
        "15 + 23",
        "100 / 4",
        "2 ** 8",
        "sqrt(16)",
        "sin(pi/2)"
    ]
    
    for expr in test_expressions:
        result = calc.execute(expr)
        print(f"{expr} = {result}")

