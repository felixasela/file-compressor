from collections import Counter
from classes.huffman_algorithm import file_compressor

compressor = file_compressor("dummy.txt")

def test_get_probabilities():
    content = "abcabc"
    probs = compressor.get_probabilities(content)
    total = len(content) + 1
    assert probs['a'] == 2 / total
    assert probs['b'] == 2 / total
    assert probs['c'] == 2 / total
    assert probs['end'] == 1 / total

def test_make_tree():
    probs = {'a': 0.3, 'b': 0.2, 'c': 0.1, 'end': 0.4}
    tree = compressor.make_tree(probs)
    assert isinstance(tree, tuple)
    assert len(tree) == 3

def test_make_dictionary():
    probs = {'a': 0.3, 'b': 0.2, 'c': 0.1, 'end': 0.4}
    tree = compressor.make_tree(probs)
    dic = compressor.make_dictionary(tree)
    assert isinstance(dic, dict)
    for char in probs:
        assert char in dic

def test_compress_decompress():
    content = "abcabc"
    probs = compressor.get_probabilities(content)
    tree = compressor.make_tree(probs)
    dic = compressor.make_dictionary(tree)
    compressed_data = compressor.compress(dic, content)
    decompressed_content = compressor.decompress(compressed_data, dic)
    assert decompressed_content == content

def test_store_load(tmp_path):
    content = "abcabc"
    probs = compressor.get_probabilities(content)
    tree = compressor.make_tree(probs)
    dic = compressor.make_dictionary(tree)
    compressed_data = compressor.compress(dic, content)
    
    outfile = tmp_path / "compressed_data"
    compressor.store(compressed_data, dic, str(outfile))
    
    loaded_compressed_data, loaded_dic = compressor.load(str(outfile), str(outfile) + ".dic")
    decompressed_content = compressor.decompress(loaded_compressed_data, loaded_dic)
    assert decompressed_content == content

def test_read_file(tmp_path):
    content = "abcabc"
    file_path = tmp_path / "test_file.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    compressor = file_compressor(file_path)
    read_content = compressor.read_file()
    assert read_content == content

def test_reconstruct_tree():
    content = "abcabc"
    probs = compressor.get_probabilities(content)
    tree = compressor.make_tree(probs)
    dic = compressor.make_dictionary(tree)
    reconstructed_tree = compressor.reconstruct_tree(dic)
    assert isinstance(reconstructed_tree, dict)
    assert '0' in reconstructed_tree or '1' in reconstructed_tree
