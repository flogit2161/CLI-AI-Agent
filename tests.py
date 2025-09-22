from functions.get_files_info import get_files_info

current_result = get_files_info('calculator', ".")
print('Result for current directory:')
print(f"{current_result}")

pkg_result = get_files_info('calculator', 'pkg')
print("Result for 'pkg' directory:")
print(f'{pkg_result}')

bin_result = get_files_info('calculator', '/bin')
print("Result for '/bin' directory:")
print(f'{bin_result}')

prev_result = get_files_info('calculator', '../')
print("Result for '../' directory:")
print(f'{prev_result}')

