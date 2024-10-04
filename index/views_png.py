from django.shortcuts import render
from .models import ImageFile
import binascii
import cv2

letter = ''.join([chr(i) for i in range(32,127)])

def analisaPNG(request, id_):
	fileName = ImageFile.objects.get(pk=id_)
	path_file = "uploads/"+fileName.name
	file = open(path_file,"rb").read()
	context = {
		"title":"Analysis PNG",
		"signature":signature(file),
		"IHDR":IHDR(file),
		"sBIT":sBIT(file),
		"bKGD":bKGD(file),
		"PLTE":PLTE(file),
		"tRNS":tRNS(file),
		"iTXt":iTXt(file),
		"tIME":tIME(file),
		"sRGB":sRGB(file),
		"gAMA":gAMA(file),
		"pHYs":pHYs(file),
		"tEXt":tEXt(file),
		"IEND":IEND(file),
		"IDAT":IDAT(file),
		"RGB_LSB":RGB_LSB(path_file),
		"RGB_MSB":RGB_MSB(path_file),
		"DATA":DATA(file),
		"otherData":otherData(file),
	}
	return render(request, 'index/analisa_png.html',context)

def signature(file):
	marker = file[:8].hex()
	return marker

def IHDR(file):
	field_marker = {"Width":4, "Height":4,"Size of Color":1,
				"Color Type":1,"Compression Method":1,"Filter Method":1,
				"Enclacement Method":1}
	type_ = b"IHDR"
	return process(file,field_marker, type_, "IHDR")

def sBIT(file):
	type_ = b"sBIT"
	length = int.from_bytes(file.split(type_)[0][-4:],byteorder='big')
	if length == 1:
		field_marker = {"Grayscale":1}
	elif length == 2:
		field_marker = {"Grayscale":1,"Alpha":1}
	elif length == 3:
		field_marker = {"Red":1,"Green":1,"Blue":1}
	else:
		field_marker = {"Red":1,"Green":1,"Blue":1,"Alpha":1}
	
	return process(file,field_marker, type_, "sBIT")

def bKGD(file):
	type_ = b"bKGD"
	length = int.from_bytes(file.split(type_)[0][-4:],byteorder='big')
	field_marker = {"Background Color Data":length}
	return process(file,field_marker, type_,"bKGD")

def PLTE(file):
	type_ = b"PLTE"
	length = int.from_bytes(file.split(type_)[0][-4:],byteorder='big')
	field_marker = {"Data PLTE":length}
	return process(file,field_marker, type_,"PLTE")

def tRNS(file):
	type_ = b"tRNS"
	length = int.from_bytes(file.split(type_)[0][-4:],byteorder='big')
	field_marker = {"Data tRNS":length}
	return process(file,field_marker,type_,"tRNS")

def iTXt(file):
	type_ = b"iTXt"
	length = int.from_bytes(file.split(type_)[0][-4:],byteorder="big")
	field_marker = {"Data iTXt":length}
	return process(file,field_marker,type_,"iTXt")

def tIME(file):
	field_marker = {"Year":2,"Month":1,"Day":1,"Hour":1,"Minute":1,"Second":1}
	type_ = b"tIME"
	return process(file,field_marker,type_,"tIME")

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

def IEND(file):
	field_marker = {"Data ":0}
	type_ = b"IEND"
	return process(file,field_marker, type_, "IEND")

def process(file, field_marker, type_, status_):
	list = []
	ascii_list = ["Data iTXt"]
	hexa_list = ["Data tRNS","Data PLTE"]
	if type_ in file:
		size_ = file.split(type_)[0][-4:]
	else:
		return ""
	data_ = file.split(type_)[1][:int.from_bytes(size_,byteorder='big')]	
	crc_ = binascii.crc32(type_+data_) & 0xFFFFFFFF
	status = "CRC "+status_+" FALSE"
	if bytes.fromhex(hex(crc_)[2:].rjust(8,'0')) in file:
		status = "CRC "+status_+" TRUE"
	data = [hex(i)[2:].rjust(2,'0') for i in data_]
	start, end = 0,0
	for field,size in field_marker.items():
		end += size
		try:
			if field in ascii_list:
				_bytes_ = ''.join([chr(int(i,16)) for i in data[start:end] if int(i,16)>=32 and int(i,16)<=126])
				list.append(field+" : "+_bytes_)
			elif field in hexa_list:
				list.append(field+" : "+"".join(data[start:end]))
			else:
				list.append(field+" : "+str(int("".join(data[start:end]),16)))
		except:
			list.append("Data : null")
		start += size
	return ("Marker identifier : "+type_.decode('ascii'),list,hex(crc_)[2:]+" "+status)
def tEXt(file):
	crc_list = []
	text = file.split(b"tEXt")
	if len(text) == 1:
		return ""
	for i in range(len(text)):
		try:
			size_ = text[i][-4:]
			type_ = b"tEXt"
			data_ = text[i+1][:int.from_bytes(size_, byteorder='big')]
			crc_ = binascii.crc32(type_+data_) & 0xFFFFFFFF
			check = bytes.fromhex(hex(crc_)[2:].rjust(8,'0'))
			status = "CRC tEXt FALSE"
			if check in file:
				crc_list.append(''.join([chr(i) if i>0 else " : " for i in data_])+" "+check.hex())
				status = "CRC tEXt TRUE"
			else:
				crc_list.append('Not Found')
		except:
			pass
	return ("Marker identifier : "+type_.decode('ascii'),crc_list,check.hex()+" "+status)
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
				crc_list.append("Panjang IDAT "+str(i+1)+" : "+check.hex())
			else:
				crc_list.append("Panjang IDAT "+str(i+1)+" : "+check.hex()+" Not Found")
		except:
			pass
	return crc_list
def RGB_LSB(file):
	try:
		result = ''
		text = ''
		img = cv2.imread(file)
		image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		for i in image_rgb:
			for j in i:
				for k in j:
					if len(result) == 8:
						if chr(int(result,2)) in letter:
							text += chr(int(result,2))
							result = ''
					result += bin(k)[-1:]
	except Exception as e:
		text = "'Image Error : "+str(e)+"'"
	return text

def RGB_MSB(file):
	try:
		result = ''
		text = ''
		img = cv2.imread(file)
		image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		for i in image_rgb:
			for j in i:
				for k in j:
					if len(result) == 8:
						if chr(int(result,2)) in letter:
							text += chr(int(result,2))
							result = ''
					result += bin(k)[2:].rjust(8,'0')[:1]
	except Exception as e:
		text = "'Image Error : "+str(e)+"'"
	return text

def DATA(file):
	list_data = []
	result = 0
	marker = [b"IHDR",b"sBIT",b"tEXt",b"PLTE",b"tRNS",b"iTXt",b"tIME",b"bKGD",b"sRGB",b"gAMA",b"pHYs"]
	header = 8
	result += header
	for i in marker:
		if i in file:
			data_length = int.from_bytes(file.split(i)[0][-4:],byteorder='big')
			list_data.append("Panjang "+i.decode('ascii')+" : "+hex(data_length)[2:].rjust(8,'0'))
			result += 4+4+data_length+4
	idat = file.split(b"IDAT")
	for i in range(len(idat)):
		try:
			size_ = idat[i][-4:]
			if size_.hex() != "ae426082":
				list_data.append("Panjang IDAT "+str(i+1)+" : "+size_.hex())
				data = 4+4+int(size_.hex(),16)+4
				result += data
		except:
			pass
	footer = 12
	result += footer
	list_data.append("Panjang EOF : "+hex(footer)[2:].rjust(8,'0'))
	if result == len(file):
		return (list_data,"Panjang bytes file : "+str(result)+" Panjang bytes file sesuai")
	else:
		return (list_data,"Panjang bytes file tidak sesuai, pengukuran = "+str(result)+" sedangkan filenya = "+str(len(file)))

def otherData(path_file):
    data = path_file.split(b'IEND')
    return data[1][4:].decode('ascii')