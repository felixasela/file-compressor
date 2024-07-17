import heapq
from collections import Counter
import json
import pickle


class file_compressor:
    def __init__(self, addres) -> None:
        self.addres = addres

    def read_file(self):
        addres = self.addres
        try:
            with open(addres, mode='r', encoding='utf-8') as txt_readable:
                return txt_readable.read()
        except Exception as e:
            return f'Error reading file: {str(e)}'

    def get_probabilities(self, content):
        total = len(content) + 1
        c = Counter(content)
        res = {}
        for char, count in c.items():
            res[char] = float(count) / total
        res['end'] = 1.0 / total
        return res

    def make_tree(self, probs):
        q = []
        for ch, pr in probs.items():
            heapq.heappush(q, (pr, 0, ch))

        while len(q) > 1:
            e1 = heapq.heappop(q)
            e2 = heapq.heappop(q)
            nw_e = (e1[0] + e2[0], max(e1[1], e2[1]) + 1, [e1, e2])
            heapq.heappush(q, nw_e)
        return q[0]

    def make_dictionary(self, tree):
        res = {}
        search_stack = [(tree, "")]
        while len(search_stack) > 0:
            node, prefix = search_stack.pop()
            if isinstance(node[2], list):
                search_stack.append((node[2][1], prefix + "1"))
                search_stack.append((node[2][0], prefix + "0"))
            else:
                res[node[2]] = prefix
        return res

    def compress(self, dic, content):
        res = ""
        for ch in content:
            code = dic.get(ch, "")
            res += code
        res = '1' + res + dic['end']
        res = res + (len(res) % 8 * "0")
        return int(res, 2)
    
    def store(self, data, dic, outfile):
        with open(outfile, 'wb') as outf:
            pickle.dump(data, outf)
        
        with open(outfile + ".dic", 'w') as outf:
            json.dump(dic, outf)
        print("Data and dictionary stored successfully.")


    def load(self, compressed_file, dic_file):
        with open(compressed_file, 'rb') as f:
            compressed_data = pickle.load(f)
        
        with open(dic_file, 'r') as f:
            dic = json.load(f)
        
        return compressed_data, dic

    def reconstruct_tree(self, dic):
        reverse_dic = {v: k for k, v in dic.items()}
        root = {}
        for bitstring, char in reverse_dic.items():
            node = root
            for bit in bitstring:
                if bit not in node:
                    node[bit] = {}
                node = node[bit]
            node['char'] = char
        return root

    def decompress(self, compressed_data, dic):
        bin_str = bin(compressed_data)[3:]
        root = self.reconstruct_tree(dic)
        node = root
        result = ""
        for bit in bin_str:
            if bit in node:
                node = node[bit]
                if 'char' in node:
                    if node['char'] == 'end':
                        break
                    result += node['char']
                    node = root
        return result