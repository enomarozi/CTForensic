from django.shortcuts import render, redirect
from .models import ImageFile
import binascii

def analisaPNG(request, id_):
	fileName = ImageFile.objects.get(pk=id_)
	path_file = "uploads/"+fileName.name
	file = open(path_file,"rb").read()
	context = {
		"title":"Analysis PNG",
		"signature":signature(file),
		"IHDR":IHDR(file),
		"sRGB":sRGB(file),
		"gAMA":gAMA(file),
		"pHYs":pHYs(file),
		"IDAT":IDAT(file),
		"DATA":DATA(file),

	}
	return render(request, 'index/analisa_png.html',context)

def signature(file):
	marker = [hex(i)[2:].rjust(2,'0') for i in file[:8]]
	return marker

def IHDR(file):
	field_marker = {"Width":4, "Height":4,"Size of Color":1,
				"Color Type":1,"Compression Method":1,"Filter Method":1,
				"Enclacement Method":1}
	type_ = b"IHDR"
	return process(file,field_marker, type_, "IHDR")
	
def sRGB(file):
	field_marker = {"Rendering Intent":1}
	type_ = b"sRGB"
	return process(file,field_marker, type_, "sRGB")

def gAMA(file):
	field_marker = {"Rendering Intent":4}
	type_ = b"gAMA"
	return process(file,field_marker, type_, "gAMA")

def pHYs(file):
	field_marker = {"Pixels per unit X axis":4,"Pixels per unit Y axis":4,
				  "Unit specifier":1}
	type_ = b"pHYs"
	return process(file,field_marker, type_, "pHYs")

def process(file, field_marker, type_, status_):
	list = []
	if type_ in file:
		size_ = file.split(type_)[0][-4:]
	else:
		return "'Not Found'"
	data_ = file.split(type_)[1][:int.from_bytes(size_,byteorder='big')]	
	crc_ = binascii.crc32(type_+data_) & 0xFFFFFFFF
	status = "CRC "+status_+" FALSE"
	if bytes.fromhex(hex(crc_)[2:].rjust(8,'0')) in file:
		status = "CRC "+status_+" TRUE"
	data = [hex(i)[2:].rjust(2,'0') for i in data_]
	start, end = 0,0
	for field,size in field_marker.items():
		end += size
		list.append(field+" : "+str(int("".join(data[start:end]),16)))
		start += size
	return ("Marker identifier : "+type_.decode('ascii'),list,hex(crc_)[2:]+" "+status)

def IDAT(file):
	crc_list = []
	idat = file.split(b"IDAT")
	for i in range(len(idat)):
		try:
			size_ = idat[i][-4:]
			type_ = b"IDAT"
			data_ = idat[i+1][:int.from_bytes(size_, byteorder='big')]
			crc_ = binascii.crc32(type_+data_) & 0xFFFFFFFF
			check = bytes.fromhex(hex(crc_)[2:].rjust(8,'0'))
			if check in file:
				crc_list.append(''.join([hex(j)[2:].rjust(2,'0') for j in check]))
			else:
				crc_list.append(''.join([hex(j)[2:].rjust(2,'0') for j in check])+" Not Found")
		except:
			pass
	return crc_list

def DATA(file):
	print("Panjang file :",len(file))
	result = 0
	marker = [b"IHDR",b"sRGB",b"gAMA",b"pHYs"]
	result += 8
	for i in marker:
		data_length = int.from_bytes(file.split(i)[0][-4:],byteorder='big')
		result += 4+4+data_length+4
	print("result :",result)
	idat = file.split(b"IDAT")
	for i in range(len(idat)+1):
		try:
			size_ = int(idat[i][-4:].hex(),16)
			print(hex(size_))
			result += size_
		except:
			pass
	#print(result)