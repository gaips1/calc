import sys
import pytest
from unittest.mock import patch
import calc

@pytest.fixture(autouse=True)
def clean_state():
    calc.last_result = None
    calc.history = []
    with patch('os.system'):
        yield

def run_calc_scenario(capsys, inputs):
    full_inputs = inputs + ['0']
    
    with patch('builtins.input', side_effect=full_inputs):
        with pytest.raises(SystemExit):
            calc.main()
            
    captured = capsys.readouterr()
    return captured.out

@pytest.mark.parametrize("num1, num2, expected", [
    ("1", "10", "-9"),
    ("-190.2", "-100.3", "-89.9")
])
def test_subtraction(capsys, num1, num2, expected):
    inputs = ['2', num1, num2, ''] 
    output = run_calc_scenario(capsys, inputs)
    assert f"Результат: {expected}" in output

@pytest.mark.parametrize("num1, num2, expected", [
    ("-1", "0", "0"),
    ("-3", "-5", "15")
])
def test_multiplication(capsys, num1, num2, expected):
    inputs = ['4', num1, num2, '']
    output = run_calc_scenario(capsys, inputs)
    assert f"Результат: {expected}" in output

@pytest.mark.parametrize("num1, num2, expected_fragment", [
    ("10", "0", "Бесконечность"),
    ("9", "2", "4.5"),
    ("-9", "2", "-4.5"),
    ("-121", "-11", "11"),
    ("3.1415", "1999", "0.00157153576"),
    ("2", "3", "0.666666")
])
def test_division(capsys, num1, num2, expected_fragment):
    inputs = ['3', num1, num2, '']
    output = run_calc_scenario(capsys, inputs)
    
    if expected_fragment == "Бесконечность":
        assert "Бесконечность" in output
    else:
        assert expected_fragment in output

@pytest.mark.parametrize("num1, num2, expected", [
    ("10", "1", "0.1"),
    ("-10", "1", "-0.1"),
    ("50.6", "124.7", "63.0982"),
    ("37.88", "1487.65", "563.52182")
])
def test_percent(capsys, num1, num2, expected):
    inputs = ['5', num1, num2, '']
    output = run_calc_scenario(capsys, inputs)
    assert f"Результат: {expected}" in output