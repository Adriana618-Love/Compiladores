


class File:
    def __init__(self, name_file, path_file=''):
        """
        Args:
            name_file (string): nombre del archivo
            path_file (string): dirección del archivo
        """
        self.name_file = name_file
        import os
        self.path_file = os.path.join((os.getcwd(),path_file)[path_file],self.name_file)
        self.init_file()
    def init_file(self):
        """Si el file no existe, se crea
        """
        import os.path
        from os import path
        if not path.exists(self.path_file):
            self.file = open(self.path_file,'x')
            self.file.close()

    def append_line(self, line):
        self.file = open(self.name_file,'a')
        self.file.write(line)
        self.file.close()

    


        