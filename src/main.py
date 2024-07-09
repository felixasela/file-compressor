from classes.huffman_algorithm import file_compressor

# C:/Users/felix/OneDrive/Documentos/Personal/Documents/GitHubNotes.txt
addres = input('Enter the file path: ')

try:
    file_compressor = file_compressor(addres)
    file = file_compressor.read_file()
    file_content = file.read()
    file_compressor.get_probabilities(file_content)
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
