from django.shortcuts import render
from .models import ImageFile
import time

def analisaZIP(request, id_):
    fileName = ImageFile.objects.get(pk=id_)
    path_file = "uploads/"+fileName.name
    file = [hex(i)[2:].rjust(2,'0') for i in open(path_file,"rb").read()]
    context = {
        "title":"Analysis ZIP",
        "fileHeader":fileHeader(file),
    }
    return render(request, 'index/analisa_zip.html',context)

def fileHeader(file):
    field = {"Signature":4,"Version":2,"Flags":2,"Compression":2,"Modif Time":2,
         "Modif Date":2,"CRC32":4,"Compressed Size":4,"Uncompressed size":4,
         "File Name Len":2,"Extra Field len":2}
    field["File Name"]=int(''.join(file[26:28][::-1]),16)
    field["Extra Field"]=int(''.join(file[28:30][::-1]),16)

    Flags = ["Encrypted file","Compression Option","Compression Option",
             "Data Descriptor","Enchanced Deflation","Compressed Patched Data",
             "Strong Encryption","Unused","Unused","Unused","Unused",
             "Language Encoding","Reserved","Mask Header Values","Reserved",
             "Reserved"]

    Compression_Method = ["No Compression","Shrunk","Reduce With Compression factor 1",
                          "Reduce With Compression factor 2","Reduce With Compression factor 3",
                          "Reduce With Compression factor 4","Imploded","Reserved","Deflated",
                          "Enhanced Deflated","PKWare DCL Imploded","Reserved","Compressed Using BZIP2",
                          "LZMA","Reserved","Reserved","Reserved","Compress Using IBM TERSE",
                          "IBM LZ77 z","PPMd Version 1, Rev 1"]

    ascii_convert = ["File Name","Extra Field"]
    hexa_convert = ["Signature","CRC32"]
    int_convert = ["Version","Flags","Compression","Modif Time","Modif Date",
                   "Compressed Size","Uncompressed size","File Name Len",
                   "Extra Field len"]

    start,end = 0,0
    status = ""
    for field,size in field.items():
        end += size
        value = ''.join([i[::-1] for i in file[start:end]])
        if field in ascii_convert:
            result = ''.join([chr(int(value[:i][-2:][::-1],16)) for i in range(2,len(value)+2,2)])
            print(field+" :",result)
        elif field in int_convert:
            if field == "Flags":
                status = Flags[int(value[::-1],16)]
            elif field == "Compression":
                status = Compression_Method[int(value[::-1],16)]
            print(field+" :",int(value[::-1],16),status)
        else:
            print(field+" :",value[::-1])
        start += size
        status = ""