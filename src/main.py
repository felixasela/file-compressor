from classes.huffman_algorithm import file_compressor

print(' 1. compress \n 2. decompress')
options = int(input('enter the number of the option: '))

if options == 1:
    file_path = input('Enter the file path: ')
    output_file = "compressed_output"
    
    try:
        compressor_instance = file_compressor(file_path)
        file_content = compressor_instance.read_file()
        
        probabilities = compressor_instance.get_probabilities(file_content)
        tree = compressor_instance.make_tree(probabilities)
        dictionary = compressor_instance.make_dictionary(tree)
        
        compressed_data = compressor_instance.compress(dictionary, file_content)
        compressor_instance.store(compressed_data, dictionary, output_file)
        
        print(f"File compressed and stored as {output_file}")
    
    except Exception as err:
        print(f"Compression error: {err}")

elif options == 2:
    compressed_file_path = input('Enter the compressed file path: ')
    dic_file_path = compressed_file_path + '.dic'
    
    try:
        compressor_instance = file_compressor("")
        compressed_data, dic = compressor_instance.load(compressed_file_path, dic_file_path)
        
        decompressed_content = compressor_instance.decompress(compressed_data, dic)
        print(f"Decompressed content:\n{decompressed_content}")
    
    except Exception as err:
        print(f"Decompression error: {err}")

else:
    print('Incorrect option')
