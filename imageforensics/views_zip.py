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

    Version = {0:"MS-DOS and OS/2 (FAT / VFAT / FAT32 file systems)",
               1:"Amiga",
               2:"OpenVMS",
               3:"UNIX",
               4:"VM/CMS",
               5:"Atari ST",
               6:"OS/2 H.P.F.S",
               7:"Macintosh",
               8:"Z-System",
               9:"CP/M",
               10:"Windows NTFS",
               11:"MVS (OS/390 -Z/OS)",
               12:"VSE",
               13:"Acorn Risc",
               14:"VFAT",
               15:"Alternate MVS",
               16:"BeOS",
               17:"Tandem",
               18:"OS/400",
               19:"OS/X (Darwin)",
               20:"Android",
               21:"iOS",
               22:"Linux",
               23:"Windows Subsystem for Linux(WSL)",
               24:"Chrome OS",
               25:"FreeBSD",
               26:"Haiku",
               27:"Plan 9",
               28:"WebAssembly",
               29:"AIX"}

    Flags = {0:"Encrypted file",
             1:"Compression Option",
             2:"Compression Option",
             3:"Data Descriptor",
             4:"Enchanced Deflation",
             5:"Compressed Patched Data",
             6:"Strong Encryption",
             7:"Unused",
             8:"Unused",
             9:"Unused",
             10:"Unused",
             11:"Language Encoding",
             12:"Reserved",
             13:"Mask Header Values",
             14:"Reserved",
             15:"Reserved"}

    Compression_Method = {0:"No Compression",
                          1:"Shrunk",
                          2:"Reduce With Compression factor 1",
                          3:"Reduce With Compression factor 2",
                          4:"Reduce With Compression factor 3",
                          5:"Reduce With Compression factor 4",
                          6:"Imploded",
                          7:"Reserved",
                          8:"Deflated",
                          9:"Enhanced Deflated",
                          10:"PKWare DCL Imploded",
                          11:"Reserved",
                          12:"Compressed Using BZIP2",
                          13:"Reserved",
                          14:"LZMA",
                          15:"Reserved",
                          17:"Reserved",
                          18:"Compress Using IBM TERSE",
                          19:"IBM LZ77 z",
                          98:"PPMd Version 1, Rev 1",
                          99:"BZIP2"}

    ascii_convert = ["File Name","Extra Field"]
    hexa_convert = ["Signature","CRC32"]
    int_convert = ["Version","Flags","Compression","Modif Time","Modif Date",
                   "Compressed Size","Uncompressed size","File Name Len",
                   "Extra Field len"]

    start,end = 0,0
    status = ""
    r_result = []
    for field,size in field.items():
        end += size
        value = ''.join([i[::-1] for i in file[start:end]])
        if field in ascii_convert:
            result = ''.join([chr(int(value[:i][-2:][::-1],16)) for i in range(2,len(value)+2,2)])
            r_result.append(field+" : "+str(result))
        elif field in int_convert:
            if field == "Flags":
                status = Flags[int(value[::-1],16)]
            elif field == "Compression":
                status = Compression_Method[int(value[::-1],16)]
            elif field == "Version":
                status = Version[int(value[::-1],16)]
            elif field == "Modif Time":
                status = mod_time(bin(int(value[::-1],16))[2:])
            elif field == "Modif Date":
                status = mod_date(bin(int(value[::-1],16)))
            elif field == "Compressed Size" or field == "Uncompressed size" or field == "File Name Len" or field == "Extra Field len":
                status = str(int(value[::-1],16))+" bytes"
            r_result.append(field+" : "+status)
        elif field in hexa_convert:
            data = ''.join([value[:i][-2:][::-1] for i in range(2,len(value)+2,2)])
            r_result.append(field+" : "+str(data))
        else:
            r_result.append(field+" : "+str(value[::-1]))
        start += size
        status = ""
    return r_result


def mod_time(binary):
    s,m,h = binary[-5:],binary[4:-5], binary[:-11]
    return str(int(h,2))+":"+str(int(m,2))+":"+str(int(s,2))

def mod_date(binary):
    d,m,y = binary[-5:],binary[7:-5], binary[:-9]
    return str(int(d,2))+"-"+str(int(m,2))+"-"+str(1980+int(y,2))