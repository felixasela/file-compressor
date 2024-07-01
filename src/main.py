from classes.node import test
from classes.huffman_algorithm import huffman
from classes.file import file_options

test()
huffman()

addres = input('Enter the file path: ')

file_options = file_options(addres)

file_options.read_file()
