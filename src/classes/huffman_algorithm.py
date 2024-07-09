from typing import Counter


class file_compressor:

    def __init__(self, addres) -> None:
        self.addres = addres


    def read_file(self):
        addres = self.addres
        txt_readable = open(addres, mode= 'r')
        if txt_readable.readable() == True :
            content = txt_readable
            return content
        else:
            return 'File not readable'
        
    
    def get_probabilities(self, content):
        total = len(content) + 1
        c = Counter(content)
        res = {}
        for char,count in c.items():
            res[char] = float(count)/total
        res['end'] = 1.0/total
        print(res)
        return res