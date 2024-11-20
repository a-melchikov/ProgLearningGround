def get_testing_code(user_code: str, test_input: str, expected_output: str) -> str:
    """
    Generates a Python script to test user code with specified input and expected output.

    Args:
        user_code (str): The user's Python code as a string.
        test_input (str): Input to be provided to the user's code.
        expected_output (str): Expected output from the user's code.

    Returns:
        str: A string representing the testing script.
    """
    escaped_user_code = user_code.replace('"', '\\"').replace("'", "\\'")

    test_script = f"""
import sys
from io import StringIO
from unittest.mock import patch

# User-provided code
user_code = \"\"\"{escaped_user_code}\"\"\"

# Test runner function
def run_test(input_data, expected_output):
    try:
        # Redirect input and capture output
        with patch("builtins.input", side_effect=input_data.splitlines()), patch(
            "sys.stdout", new_callable=StringIO
        ) as mock_stdout:
            exec(user_code, {{}}, {{"__name__": "__main__"}})
            result = mock_stdout.getvalue().strip()

        # Compare results
        print(result, end=' ')
        if result == expected_output:
            print("PASS")
        else:
            print(f"FAIL: Expected '{{expected_output}}', got '{{result}}'")
    except Exception as e:
        print(f"FAIL: Exception occurred - {{e}}")

# Run the test
run_test('{test_input.replace("'", "\\'")}', '{expected_output.replace("'", "\\'")}')
"""
    return test_script
