import unittest
import ast
from app import check_undefined_variables_car  

class TestCheckUndefinedVariablesCar(unittest.TestCase):

    def test_no_undefined_variables(self):
        """Code that defines all variables before utilizng them will return no issues if it works."""
        code = """
x = x - 4
y = x + 5
def example():
    z = y * 2
    return z
"""
        tree = ast.parse(code)
        issues = check_undefined_variables_car(tree)
        self.assertEqual(issues, [], "Expected no issues but got some.")

    def test_one_undefined_variable(self):
        """Using an undefined variable should trigger an issue."""
        code = """
def example():
    a = 5
    b = c + a  
"""
        tree = ast.parse(code)
        issues = check_undefined_variables_car(tree)
        self.assertEqual(len(issues), 1, f"Expected 1 issue, got {len(issues)}.")
        self.assertIn("Variable 'c' is used but not defined.", issues[0]["message"])

    def test_assumed_defined_variables(self):
        """
        'env', 'time', 'max', 'np', 'contact' are assumed defined
        and should not trigger issues if they're used but not assigned.
        """
        code = """
def example():
    result = env.some_method()
    ts = time.time()
    val = max(10, 5)
    arr = np.array([1,2,3])
    if contact:
        return arr
"""
        tree = ast.parse(code)
        issues = check_undefined_variables_car(tree)
        self.assertEqual(issues, [], "Expected no issues for assumed defined variables.")

    def test_multiple_undefined_variables(self):
        """Multiple undefined variables need to flag issues."""
        code = """
m = 5
def example():
    result = a + k
    return result
"""
        tree = ast.parse(code)
        issues = check_undefined_variables_car(tree)
        self.assertEqual(len(issues), 2, f"Expected 2 issues, got {len(issues)}.")
        undefined_var = [issue["message"].split("'")[1] for issue in issues]
        self.assertIn("a", undefined_var)
        self.assertIn("k", undefined_var)

if __name__ == '__main__':
    unittest.main()
