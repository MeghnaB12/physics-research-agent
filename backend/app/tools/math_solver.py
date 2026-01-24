import sympy
from sympy.parsing.sympy_parser import (
    parse_expr, 
    standard_transformations, 
    implicit_multiplication_application,
    convert_xor  # <--- This is the fix
)

class MathTool:
    def __init__(self):
        # Add convert_xor to the transformations so "x^2" becomes "x**2"
        self.transformations = (
            standard_transformations + 
            (implicit_multiplication_application, convert_xor)
        )

    def solve(self, equation_str: str, variable: str = None):
        """
        Solves algebraic equations.
        Args:
            equation_str: The equation (e.g., "x^2 - 4 = 0")
            variable: The variable to solve for (e.g., "x")
        """
        try:
            # 1. Clean input
            if "=" in equation_str:
                lhs, rhs = equation_str.split("=")
                expr_str = f"({lhs}) - ({rhs})"
            else:
                expr_str = equation_str

            # 2. Parse expression safely with XOR conversion
            parsed_expr = parse_expr(expr_str, transformations=self.transformations)
            
            # 3. Identify variable if not provided
            if not variable:
                free_symbols = list(parsed_expr.free_symbols)
                if len(free_symbols) == 1:
                    symbol = free_symbols[0]
                elif len(free_symbols) == 0:
                     return f"❌ No variables found in '{equation_str}'."
                else:
                    return f"❌ Error: Multiple variables found {free_symbols}. Please specify which one to solve for."
            else:
                symbol = sympy.Symbol(variable)

            # 4. Solve
            solution = sympy.solve(parsed_expr, symbol)
            return f"✅ Solution: {solution}"

        except Exception as e:
            return f"❌ Math Error: {str(e)}"

# Quick test block
if __name__ == "__main__":
    tool = MathTool()
    print(f"Test 1 (x^2 - 16): {tool.solve('x^2 - 16 = 0')}")
    print(f"Test 2 (implicit mult 2x=10): {tool.solve('2x = 10')}")