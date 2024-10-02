from django.shortcuts import render
from .models import ImageFile
import binascii

def analisaBMP(request, id_):
	fileName = ImageFile.objects.get(pk=id_)
	path_file = "uploads/"+fileName.name
	file = open(path_file,"rb").read()
	context = {
		"title":"Analysis BMP",
		"headerBMP": headerBMP(file),
		"infoHeaderBMP": infoHeaderBMP(file),
		"colorTable":colorTable(file),
	}
	return render(request, 'index/analisa_bmp.html',context)

def headerBMP(file):
	header = {
		"Signature":2,"File Size":4,"Reserved 1":2,
		"Reserved 2":2,"Data Offset":4,
	}
	return process(file,header,0)

def infoHeaderBMP(file):
	header = {"Size Bitmap Info Header":4,"Image Width":4,
			"Image Height":4,"Planes":2,"Bit Count":2,
			"Compression":4,"Image Size":4,"X Pixels Per Meter":4,
			"Y Pixels Per Meter":4,"Colors Used":4,
			"Colors Important":4}
	return process(file,header,14)

def process(file,header,start_):
	marker = []
	start, end=start_,start_
	for field,size in header.items():
		end += size
		if field == "Signature":
			marker.append("'Marker :"+file[start:end].decode('ascii')+"'")
		else:
			value = ''.join([hex(i)[2:].rjust(2,'0') for i in file[start:end]][::-1])
			marker.append(field+" : "+str(int(value,16)))
		start += size
	return marker

def colorTable(file):
	marker = []
	for i in file[55:245+55]:

		print(hex(i)[2:].rjust(2,'0'))
		time.sleep(0.2)
