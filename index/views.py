from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .forms import UploadFileForm
from .models import ImageFile
from .modelsNilai import InputNilai
import os
import time
import sys

sys.set_int_max_str_digits(10000)

def index(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data.get("file")
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                ImageFile.objects.create(
                    name=file.name, 
                    size=fileSize(file.size), 
                    format=filename.split('.')[1]
                )
            else:
                print(form.errors)
            return redirect('index')
        else:
            form = UploadFileForm()
        context = {
            "title":"Dashboard",
            "form":form,
        }
        return render(request,'index/index.html',context)
    return HttpResponseRedirect(reverse('masuk'))

def fileSize(sizes):
    list_size = ["KB","MB","GB","TB"]
    result = 0
    size = sizes
    for i in range(len(list_size)):
        if size > 1024: 
            size /= 1024
            fix = str(size).split('.')[0]+" "+list_size[i]
            if i >= 1:
                nilai = str(size).split('.')
                fix = nilai[0]+"."+nilai[1][:2]+" "+list_size[i]
    return fix

def analisaData(request, id_):
    fileName = ImageFile.objects.get(pk=id_)
    path_file = "uploads/"+str(fileName.name)
    file = [hex(i)[2:].rjust(2,'0') for i in open(path_file,"rb").read()]
    context = {
            "title":"Analysis",
            "SOI":SOI(file),
            "APP0":APP0(file),
            "APP1":APP1(file),
            "SOF":SOF(file),
            "DHT":DHT(file),
            "DRI":DRI(file),
            "DQT":DQT(file),
            "SOS":SOS(file),
            "string_printable":string_printable(file),
            "Data":Data(file),
        }
    return render(request, 'index/analisa.html',context)

def process(field, marker):
    list_ = []
    if marker:
        data = marker.split(' ')
        start, end = 0, 0
        for field,size in field.items():
            end += size
            if field == "Exif Identifier":
                _bytes_ = ''.join([chr(int(i,16)) for i in data[start:end] if int(i,16)>9 and int(i,16)<129])
                list_.append(field+" : "+_bytes_)
            else:                
                list_.append(field+" : "+str(int(''.join(data[start:end]),16)))
            start += size
        return list_
    else:
        return None

def SOI(path_file):
    return path_file[:2]

def APP0(path_file):
    marker = ""
    header = ["e0"]
    field = {"Marker identifier":2,"Length":2,"File Identifier Mark":5,
             "Major revision number":1,"Minor revision number":1,
             "Units for x/y densities":1,"X-density":2,"Y-density":2,
             "Thumbnail width":1,"Thumbnail height":1}

    bytes_ = ' '.join(path_file)
    for i in header:
        head = "ff "+i
        if head in bytes_:
            marker = head+""+bytes_.split(head)[1].split('ff')[0]
            break
    result = process(field, marker)
    return result

def APP1(path_file):
    marker = ""
    header = ["e1"]
    field = {"Marker identifier":2,"Length":2,"Exif Identifier":0,
             "Tiff Header":1,"IFD":1}

    bytes_ = ' '.join(path_file)
    for i in header:
        head = "ff "+i
        if head in bytes_:
            marker = head+""+bytes_.split(head)[1].split('ff')[0]
            field['Exif Identifier'] = ((len(marker.replace(' ',''))-(field['Marker identifier']*2)-(field['Length']*2)) // 2)-2
            break
    result = process(field, marker)
    return result

def SOF(path_file):
    marker = ""
    header = ["c0","c1","c3","c5","c6",
             "c7","c9","ca","cb","cd",
             "ce","c6"]
    field = {"Marker identifier":2,"Length":2,"Data Precision":1,
             "Image Height":2,"Image Width":2,"Number Component":1,
             "Each Componen":3}
    bytes_ = ' '.join(path_file)
    for i in header:
        head = "ff "+i
        if head in bytes_:
            marker = head+""+bytes_.split(head)[1].split('ff')[0]
            break
    result = process(field, marker)
    return result

def DHT(path_file):
    marker = ""
    header = ["c4"]
    field = {"Marker identifier":2,"Length":2,"HT information":1,
                "Number of Symbols":16,"Symbols":2}
    bytes_ = ' '.join(path_file)
    for i in header:
        head = "ff "+i
        if head in bytes_:
            marker = head+""+bytes_.split(head)[1].split('ff')[0]
            break
    result = process(field, marker)
    return result

def DRI(path_file):
    marker = ""
    header = ["dd"]
    field = {"Marker identifier":2,"Length":2,"Restart interval":2}
    bytes_ = ' '.join(path_file)
    for i in header:
        head = "ff "+i
        if head in bytes_:
            marker = head+""+bytes_.split(head)[1].split('ff')[0]
            break
    result = process(field, marker)
    return result
    
def DQT(path_file):
    marker = ""
    header = ["db"]
    field = {"Marker identifier":2,"Length":2,"QT information":1}
    bytes_ = ' '.join(path_file)
    for i in header:
        head = "ff "+i
        if head in bytes_:
            marker = head+""+bytes_.split(head)[1].split('ff')[0]
            break
    result = process(field, marker)
    return result

def SOS(path_file):
    marker = ""
    header = ["da"]
    field = {"Marker identifier":2,"Length":2,"Number of Components in scan":1,
                "Each Component":2}
    bytes_ = ' '.join(path_file)
    for i in header:
        head = "ff "+i
        if head in bytes_:
            marker = head+""+bytes_.split(head)[1].split('ff')[0]
            break
    result = process(field, marker)
    return result

def string_printable(path_file):
    result = ""
    data = []
    for i in path_file:
        c = int(i,16)
        if c >= 32 and c <= 128:
            result += chr(c)
            print(result)
        else:
            if len(result) != 0:
                record = InputNilai.objects.get(id=1)
                if result[record.nilai:] != "\n":
                    data.append(result[record.nilai:])
                    result = ''

    return data

def Data(path_file):
    header = ["d9"]
    bytes_ = ' '.join(path_file)
    for i in header:
        head = "ff "+i
        if head in bytes_:
            marker = bytes_.split(head)[1].split(' ')
    data = ''.join([chr(int(i,16)) for i in marker if i != ''])
    return data

def settingData(request,nilai,action):
    record = InputNilai.objects.get(id=1)
    if action == "tambah":
        record.nilai += nilai
    elif action == "kurang":
        record.nilai -= nilai
    record.save()
    return JsonResponse(record.nilai, safe=False)

def cleanData(request):
    ImageFile.objects.all().delete()
    os.system("rm uploads/*")
    return HttpResponseRedirect(reverse('index'))

def getData(request):
    file_image = ImageFile.objects.all().values('id','name','size','format')
    data = list(file_image)
    return JsonResponse(data, safe=False)
