from functions.write_file import write_file

lorem_write = write_file('calculator', 'lorem.txt', "wait, this isn't lorem ipsum")
print(lorem_write)

more_lorem_write = write_file('calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet')
print(more_lorem_write)

temp_write = write_file('calculator', '/tmp/temp.txt', 'this should not be allowed')
print(temp_write)
