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
		"IDAT":IDAT(file),
	}

	return render(request, 'index/analisa_png.html',context)

def signature(file):
	marker = [hex(i)[2:].rjust(2,'0') for i in file[:8]]
	return marker

def IHDR(file):
	list = []
	size_ = file.split(b"IHDR")[0][-4:]
	type_ = b"IHDR"
	data_ = file.split(b"IHDR")[1][:int.from_bytes(size_,byteorder='big')]
	crc_ = binascii.crc32(type_+data_) & 0xFFFFFFFF
	status = "CRC IHDR False"
	if bytes.fromhex(hex(crc_)[2:]) in file:
		status = "CRC IHDR True"
	field_IHDR = {"Width":4, "Height":4,"Size of Color":1,
				"Color Type":1,"Compression Method":1,"Filter Method":1,
				"Enclacement Method":1}
	data = [hex(i)[2:].rjust(2,'0') for i in data_]
	start, end = 0,0
	for field,size in field_IHDR.items():
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
				crc_list.append(check+" not found")
		except:
			pass
	print(crc_list)