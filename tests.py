from functions.run_python_file import run_python_file

test_calc = run_python_file('calculator', 'main.py')
print(test_calc)

test_calc_inside = run_python_file('calculator', 'main.py', '["3 + 5"]')
print(test_calc_inside)

test_test = run_python_file("calculator", "tests.py")
print (test_test)

test_main = run_python_file("calculator", "../main.py")
print(test_main)

test_non = run_python_file("calculator", "nonexistent.py")
print(test_non)