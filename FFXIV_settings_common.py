#Commong FFXIV Settings Funcitons
#Copyright Arthur Moore 2016
#BSD 3 Clause License

from struct import unpack,pack

#Exclusive or each byte of a string with a number
#Returns the modified string
def xor(in_str,num):
    output = []
    for i in in_str:
        #This doesn't work in python3 :(
        output.append(chr(ord(i) ^ num))
    #convert output to a string
    output = ''.join(output)
    return output

#Read and unpack a section of data
#Since FFXIV likes to xor the user data by a constant, that constant needs to be provided at object creation
class section:
    def __init__(self, value_to_xor_by, in_file = None):
        self.type = ''
        self.data = ''
        self.xor_value = value_to_xor_by
        if(in_file):
            self.read(in_file)

    def read(self,in_file):
        header = xor(in_file.read(3),self.xor_value)
        self.type = header[0]
        size = unpack('H',header[1:3])[0]
        #Going to go ahead and lop off the null terminating byte now
        self.data= xor(in_file.read(size),self.xor_value)[0:-1]

    def write(self,out_file):
        if(len(self.type) != 1):
            raise Exception('Invalid section type!')
        header= self.type + pack('H',len(self.data)+1)
        out_file.write(xor(header,self.xor_value))
        out_file.write(xor(self.data,self.xor_value))
        #Add back the null byte when writing
        out_file.write(xor('\x00',self.xor_value))

def read_section(in_file,xor_value):
    section = {}
    header = xor(in_file.read(3),xor_value)
    section['type'] = header[0]
    size = unpack('H',header[1:3])[0]
    #Going to go ahead and lop off the null terminating byte now
    section['data']= xor(in_file.read(size),xor_value)[0:-1]
    return section

def write_section(out_file,xor_value,section):
    if(len(section['type']) != 1):
            raise Exception('Invalid section type!')
    header= section['type'] + pack('H',len(section['data'])+1)
    out_file.write(xor(header,xor_value))
    out_file.write(xor(section['data'],xor_value))
    #Add back the null byte when writing
    out_file.write(xor('\x00',xor_value))

#Generic header format is
#0x00-0x03 Unknown
#0x04-0x07 File Size - 32 (in bytes)
#0x08-0x0B Valid Data Size - 16 (in bytes)
#0x0C-0x0F Unkown

#Make sure the file size from the header matches the true file size
#WARNING:  Will modify read position in file
def check_header_size(in_file):
    #Get the file's size
    in_file.seek(0,2)
    file_size = in_file.tell()
    #Read in file size from header
    in_file.seek(0x04,0)
    header_file_size = unpack('I',in_file.read(0x04))[0]
    #Confirm that the size matches
    if(file_size - header_file_size != 32):
        raise Exception('Invalid header size!')

#Get the size of actual (valid) data in the file
#WARNING:  Will modify read position in file
def get_data_size(in_file):
    in_file.seek(0x08)
    return unpack('I',in_file.read(4))[0]+16
