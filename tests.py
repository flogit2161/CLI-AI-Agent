from functions.get_files_content import get_files_content

lorem_result = get_files_content('calculator', 'lorem.txt')
print(lorem_result)

main_result = get_files_content("calculator", "main.py")
print(main_result)

pkg_result = get_files_content("calculator", "pkg/calculator.py")
print(pkg_result)

bin_result = get_files_content("calculator", "/bin/cat")
print(bin_result)

pkg_error_result = get_files_content("calculator", "pkg/does_not_exist.py")
print(pkg_error_result)

