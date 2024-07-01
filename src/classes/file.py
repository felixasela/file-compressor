class file_options:

    def __init__(self, addres) -> None:
        self.addres = addres


    def read_file(self):
        addres = self.addres
        txt_readable = open(addres, mode= 'r')
        if txt_readable.readable() == True :
            print(txt_readable.read())