import binascii
import time
#file = [hex(i)[2:].rjust(2,'0') for i in open("image.png",'rb').read()]
file = open("gift-box.png",'rb').read()
def signature(file):
    signature = file[:8]
    list_ = ' '.join([hex(i)[2:].rjust(2,'0') for i in signature])
    print(list_)

def chunks_IHDR(file):
    list_ = []
    size_ = file.split(b"IHDR")[0][-4:]
    type_ = b"IHDR"
    data_ = file.split(b"IHDR")[1][:int.from_bytes(size_,byteorder='big')]
    crc_ = binascii.crc32(type_+data_) & 0xFFFFFFFF
    field_IHDR = {"Width":4,"Height":4,"Size of colour bytes":1,"Color Type":1,
                  "Compression method":1, "Filter method":1,"Enclacement method":1}
    data = [hex(i)[2:].rjust(2,'0') for i in data_]
    start, end = 0,0
    for field,size in field_IHDR.items():
        end += size
        list_.append(field+" : "+str(int(''.join(data[start:end]),16)))
        start += size
        
    for i in list_:
        print(i)

def chunks_IDAT(file):
    size_ = file.split(b"IDAT")[0][-4:]
    type_ = b"IDAT"
    data_ = file.split(b"IDAT")[1][:int.from_bytes(size_,byteorder='big')]
    crc_ = binascii.crc32(type_+data_) & 0xFFFFFFFF
    print(hex(crc_))

def search_IDAT(file):
    crc_list = []
    idat = file.split(b"IDAT")
    for i in range(len(idat)):
        try:
            size = idat[i][-4:]
            data = idat[i+1][:int.from_bytes(size,byteorder='big')]
            crc = binascii.crc32(b"IDAT"+data) & 0xFFFFFFFF
            crc_list.append(bytes.fromhex(hex(crc)[2:].rjust(8,'0')))
        except:
            pass
    for i in crc_list:
        if i in file:
            print(i,"ok")
        else:
            print(i,'fail')
search_IDAT(file)
