class Photo(tuple):

    def __new__(self, size, mtime, name):
        return tuple.__new__(Photo, (size, mtime, name))
 
