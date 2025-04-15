from django.shortcuts import render
from .models import ImageFile
import time
import sys
import string

letter = string.ascii_lowercase+string.ascii_uppercase+string.digits+"{}_!"
sys.set_int_max_str_digits(10000)

def analisaJPG(request, id_):
    fileName = ImageFile.objects.get(pk=id_)
    path_file = "uploads/"+fileName.name
    file = [hex(i)[2:].rjust(2,'0') for i in open(path_file,"rb").read()]
    context = {
        "title":"Analysis JPG",
        "image_url":"/"+path_file,
        "SOI":SOI(file),
        "APP0":APP0(file),
        "APP1":APP1(file),
        "SOF":SOF(file),
        "DHT":DHT(file),
        "DRI":DRI(file),
        "DQT":DQT(file),
        "SOS":SOS(file),
        "Comment":Comment(file),
        "steghideData":steghideData(file),
        "Data":Data(file),
        "string_printable":string_printable(file),
    }
    return render(request, 'imageforensics/analisa_jpg.html',context)
def process(field, marker):
    stringData = []
    list_marker = ["Exif Identifier","Comment"]
    if marker:
        data = marker.split(' ')
        start, end = 0, 0
        for field,size in field.items():
            end += size
            if field in list_marker:
                _bytes_ = ''.join([chr(int(i,16)) for i in data[start:end] if int(i,16)>=32 and int(i,16)<=126])
                stringData.append(field+" : "+_bytes_)
            else:
                try:                
                    stringData.append(field+" : "+str(int(''.join(data[start:end]),16)))
                except:
                    pass
            start += size
        return stringData
    else:
        return None

def SOI(file):
    return file[:2]

def APP0(path_file):
    header = "e0"
    field = {"Marker identifier":2,"Length":2,"File Identifier Mark":5,
             "Major revision number":1,"Minor revision number":1,
             "Units for x/y densities":1,"X-density":2,"Y-density":2,
             "Thumbnail width":1,"Thumbnail height":1}
    return markerData(header, field, path_file)
def APP1(path_file):
    header = "e1"
    bytes_ = ' '.join(path_file)
    if "ff "+header in bytes_:
        length_ = bytes_.split("ff "+header)[1].split('ff')[0][1:-1].split(' ')
        field = {"Marker identifier":2,"Length":2,"Exif Identifier":len(length_)-2,
             "Tiff Header":1,"IFD":1}
        return markerData(header, field, path_file)
def SOF(path_file):
    header = "c0"
    field = {"Marker identifier":2,"Length":2,"Data Precision":1,
             "Image Height":2,"Image Width":2,"Number Component":1,
             "Each Componen":3}
    return markerData(header, field, path_file)
def DHT(path_file):
    header = "c4"
    field = {"Marker identifier":2,"Length":2,"HT information":1,
                "Number of Symbols":16,"Symbols":2}
    return markerData(header, field, path_file)
def SOS(path_file):
    header = "da"
    field = {"Marker identifier":2,"Length":2,"Number of Components in scan":1,
                "Each Component":2}
    return markerData(header, field, path_file)
def DQT(path_file):
    header = "db"
    field = {"Marker identifier":2,"Length":2,"QT information":1}
    return markerData(header, field, path_file)
def DRI(path_file):
    header = "dd"
    field = {"Marker identifier":2,"Length":2,"Restart interval":2}
    return markerData(header, field, path_file)
def Comment(path_file):
    header = "fe"
    bytes_ = ' '.join(path_file)
    if "ff "+header in bytes_:
        length_ = bytes_.split("ff "+header)[1].split('ff')[0][1:-1].split(' ')
        field = {"Marker identifier":2,"Length":2,"Comment":len(length_)-2}
        return markerData(header, field, path_file)
def markerData(header, field, path_file):
    marker = ""
    bytes_ = ' '.join(path_file)
    head = "ff "+header
    if head in bytes_:
        marker = head+""+bytes_.split(head)[1].split('ff')[0]
    result = process(field, marker)
    return result
def string_printable(path_file):
    result = ""
    data = ""
    for i in path_file:
        c = chr(int(i,16))
        if c in letter:
            result += c
        else:
            if len(result) >= 5:
                data += result+'\n'
            result = ''
    return data
def steghideData(path_file):
    import subprocess

    try:
        result = subprocess.run(
            ['steghide','info',path_file],
            capture_output=True,
            text=True
        )
        if "Stego data" in result.stdout:
            return "'Ada file Tertanam'"
        else:
            return "'Tidak ada file Tertanam'"
    except:
        return "'Steghide belum terinstall'"
def Data(path_file):
    header = "d9"
    bytes_ = ' '.join(path_file)
    if "ff "+header in bytes_:
        marker = bytes_.split("ff "+header)[1].split(' ')
    data = ''.join([chr(int(i,16)) for i in marker if i != ''])
    return data
