from django.shortcuts import render
from .models import ImageFile
import binascii

def analisaBMP(request, id_):
	fileName = ImageFile.objects.get(pk=id_)
	path_file = "uploads/"+fileName.name
	file = open(path_file,"rb").read()
	context = {
		"title":"Analysis BMP",
		"image_url":"/"+path_file,
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
			value = int(''.join([hex(i)[2:].rjust(2,'0') for i in file[start:end]][::-1]),16)
			if value == 0:
				marker.append("'"+field+" : 00'")
			else:
				marker.append("'"+field+" : "+str(value))
		start += size
	return marker

def colorTable(file):
	len_color = len(file[54:len(file)])
	width = int(''.join([hex(i)[2:].rjust(2,'0') for i in file[18:22]][::-1]),16)
	height = int(''.join([hex(i)[2:].rjust(2,'0') for i in file[22:26]][::-1]),16)
	bit = int(''.join([hex(i)[2:].rjust(2,'0') for i in file[28:30]][::-1]),16)
	calc = (width*height*(bit//8))+(width+height)
	if calc == len_color:
		return "'Image Color Table Sesuai'"
	else:
		return "'Image Color Table Tidak Sesuai, Size Header "+str(calc)+" Sedangkan True Color "+str(len_color)+"'"