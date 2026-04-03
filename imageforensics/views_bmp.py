from django.shortcuts import render
from .models import ImageFile
import binascii
import struct

def analisaBMP(request, id_):
	fileName = ImageFile.objects.get(pk=id_)
	path_file = "uploads/"+fileName.name
	file = open(path_file,"rb").read()
	context = {
		"title":"Analysis BMP",
		"image_url":"/"+path_file,
		"headerBMP": headerBMP(file),
		"DIBHeader": DIBHeader(file),
		"colorTable":colorTable(file),
		"extradata_padding":extradata_padding(file),
	}
	return render(request, 'imageforensics/analisa_bmp.html',context)

def headerBMP(file):
	header = {
		"Marker":bfType(file),"File Size":bfSize(file),"Reserved 1":bfReserved1(file),
		"Reserved 2":bfReserved2(file),"Data Offset Bit":bfOffBits(file),
	}
	return header

def bfType(file):
	return file[:2].decode()

def bfSize(file):
	file_size = len(file)
	b = file_size.to_bytes(3, byteorder='little')
	actual_size = int.from_bytes(b, byteorder='big') 
	header_size = int.from_bytes(file[2:6], byteorder='little')
	if file_size != header_size:
		bf_Size = f"Actual size = {hex(actual_size)[2:]}"
	else:
		bf_Size = hex(actual_size)[2:]
	return bf_Size

def bfReserved1(file):
	actual_reserved1 = hex(0)[2:]
	header_reserved1 = int.from_bytes(file[6:8], byteorder='little')
	if int(actual_reserved1) != header_reserved1:
		actual_reserved1 = "Actual reserved 1 = 0"
	return actual_reserved1

def bfReserved2(file):
	actual_reserved2 = hex(0)[2:]
	header_reserved2 = int.from_bytes(file[8:10], byteorder='little')
	if int(actual_reserved2) != header_reserved2:
		actual_reserved2 = "Actual reserved 1 = 0"
	return actual_reserved2

def bfOffBits(file):
	arr_header_offbits = [hex(i+14)[2:] for i in [12,40,52,56,108,124]]
	header_offbit = int.from_bytes(file[10:13], byteorder='little')
	result = "Possibility Offbits "
	for i in arr_header_offbits:
		if hex(header_offbit)[2:] == i:
			return str(i)
		else:
			result += f" {i}"
	return result

def DIBHeader(file):
	biWidth_biHeight_biBiSizeImage(file)
	header = {"Size Bitmap Info Header":biSize(file),"Image Width":biWidth(file),
			"Image Height":biHeight(file),"Planes":biPlane(file),"Bit Count":biBitCount(file),
			"Compression":4,"Image Size":biBiSizeImage(file),"X Pixels Per Meter":4,
			"Y Pixels Per Meter":4,"Colors Used":4,
			"Colors Important":4}
	return header

def biSize(file):
	arr_header_biSize = [12,40,52,56,108,124]
	header_biSize = int.from_bytes(file[14:17], byteorder='little')
	result = "Possibility biSize "
	for i in arr_header_biSize:
		if hex(header_biSize)[2:] == hex(i)[2:].rjust(2,'0'):
			return hex(i)[2:].rjust(2,'0')
		else:
			result += f" {hex(i)[2:].rjust(2,'0')}"
	return result

def biWidth_biHeight_biBiSizeImage(file):
	header_biHeight = int.from_bytes(file[22:25], byteorder='little')
	header_biWidth = int.from_bytes(file[18:21], byteorder='little')
	header_biBiSizeImage = int.from_bytes(file[34:38], byteorder='little')
	bitCount = biBitCount(file)
	
	row_size = ((int(bitCount) * header_biHeight + 31) // 32) * 4
	actual_biWdith = int(biBiSizeImage(file),16) // row_size

	row_size = ((int(bitCount) * header_biWidth + 31) // 32) * 4
	actual_biHeight = int(biBiSizeImage(file),16) // row_size
	print(actual_biWdith, actual_biHeight, header_biBiSizeImage)


def biWidth(file):
	header_biHeight = int.from_bytes(file[22:25], byteorder='little')
	header_biWidth = int.from_bytes(file[18:21], byteorder='little')
	bitCount = biBitCount(file)
	row_size = ((int(bitCount) * header_biHeight + 31) // 32) * 4
	actual_biWdith = int(biBiSizeImage(file),16) // row_size
	if header_biWidth == actual_biWdith:
		return hex(actual_biWdith)[2:].rjust(2,'0')		
	return f"Possibility biWidth = {actual_biWdith}"

def biHeight(file):
	header_biHeight = int.from_bytes(file[22:25], byteorder='little')
	header_biWidth = int.from_bytes(file[18:21], byteorder='little')
	bitCount = biBitCount(file)
	row_size = ((int(bitCount) * header_biWidth + 31) // 32) * 4
	actual_biHeight = int(biBiSizeImage(file),16) // row_size
	if header_biHeight == actual_biHeight:
		return hex(actual_biHeight)[2:].rjust(2,'0')
	return f"Possibility biHeight = {actual_biHeight}"

def biPlane(file):
	header_biPlane = int.from_bytes(file[26:28], byteorder='little')
	return hex(header_biPlane)[2:].rjust(2,'0')

def biBitCount(file):
	arr_header_biBitCount = [1,4,8,16,24,32]
	header_biBitCount = int.from_bytes(file[28:32], byteorder='little')
	result = "Possibility biBitCount"
	for i in arr_header_biBitCount:
		if hex(header_biBitCount)[2:].rjust(2,'0') == hex(i)[2:].rjust(2,'0'):
			return str(i)
		else:
			result += f" {hex(i)[2:].rjust(2,'0')}"
	return result

def biBiSizeImage(file):
	header_biBiSizeImage = int.from_bytes(file[34:38], byteorder='little')
	return hex(header_biBiSizeImage)
# def process(file,header,start_):
# 	marker = []
# 	start, end=start_,start_
# 	for field,size in header.items():
# 		end += size
# 		if field == "Signature":
# 			marker.append("'Marker :"+file[start:end].decode('ascii')+"'")
# 		else:
# 			value = int(''.join([hex(i)[2:].rjust(2,'0') for i in file[start:end]][::-1]),16)
# 			if value == 0:
# 				marker.append("'"+field+" : 00'")
# 			else:
# 				marker.append("'"+field+" : "+str(value))
# 		start += size
# 	return marker

def colorTable(file):
	len_color = len(file[54:len(file)])
	width = int(''.join([hex(i)[2:].rjust(2,'0') for i in file[18:22]][::-1]),16)
	height = int(''.join([hex(i)[2:].rjust(2,'0') for i in file[22:26]][::-1]),16)
	bit = int(''.join([hex(i)[2:].rjust(2,'0') for i in file[28:30]][::-1]),16)
	calc = (width*height*(bit//8))+(width+height)
	if calc == len_color:
		return "'Image Color Table Sesuai'"
	else:
		return "'Image Color Table Tidak Sesuai, Size Header "+str(calc)+",dan True Color "+str(len_color)+"'"

def extradata_padding(file):
	pixel_offset = struct.unpack_from("<I", file, 10)[0]
	width = struct.unpack_from("<I", file, 18)[0]
	height = struct.unpack_from("<I", file, 22)[0]
	bits_per_pixel = struct.unpack_from("<H", file, 28)[0]
	bytes_per_pixel = bits_per_pixel // 8

	pixel_data = file[pixel_offset:]
	row_size_raw = width * bytes_per_pixel
	padding = (4 - (row_size_raw % 4)) % 4
	extradata = b""
	for y in range(height):
	    start = y * (row_size_raw + padding)
	    end = start + row_size_raw
	    pad_start = end
	    pad_end = end + padding
	    extradata += pixel_data[pad_start:pad_end]
	data = ''.join([hex(i)[2:].rjust(2,'0') for i in extradata])
	return data