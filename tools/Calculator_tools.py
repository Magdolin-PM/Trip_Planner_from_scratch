import json
import os
from typing import Union
import operator

from langchain_core.tools import tool


class CalculatorTools:
    def __init__(self):
        self.allowed_operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
        }

    @tool("Make a calculation")
    def calculate(self, expression: str) -> Union[float, str]:
        """Useful to perform mathematical calculations.
        Supports basic operations: +, -, *, /, **.
        Examples: '200*7' or '5000/20*10'"""
        
        try:
            # Parse the expression safely
            expression = expression.replace(' ', '')
            nums = []
            ops = []
            current_num = ''
            is_negative = False
            
            for i, char in enumerate(expression):
                if char == '-' and (i == 0 or expression[i-1] in self.allowed_operators):
                    is_negative = True
                elif char.isdigit() or char == '.':
                    current_num += char
                elif char in self.allowed_operators:
                    if current_num:
                        num = float(current_num)
                        nums.append(-num if is_negative else num)
                        current_num = ''
                        is_negative = False
                    if char == '*' and ops and ops[-1] == '*':  # Handle **
                        ops[-1] = '**'
                    else:
                        ops.append(char)
                else:
                    return "Error: Invalid character in expression"
            
            if current_num:
                num = float(current_num)
                nums.append(-num if is_negative else num)
            
            if not nums:
                return "Error: No numbers found"
                
            # Process operations in order of precedence
            result = nums[0]
            for i, op in enumerate(ops):
                if i + 1 < len(nums):
                    try:
                        result = self.allowed_operators[op](result, nums[i + 1])
                    except ZeroDivisionError:
                        return "Error: Division by zero"
                    except Exception as e:
                        return f"Error: {str(e)}"
                    
            return result
            
        except ValueError as e:
            return f"Error: Invalid number format - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"