'''
    this function read file
'''
def input_decoder_file(file_name):
    f = open(file_name, 'rb')
    file_string = f.read()
    return file_string

'''
    this function open write file
'''
def write_file_open(file_name):
    f = open(file_name,'wb')
    return f

'''
    this function close write file
'''
def write_file_close(f):
    f.close()