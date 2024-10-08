from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .forms import UploadFileForm
from .models import ImageFile
import os
from . import views_jpg, views_png


def index(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			uploaded_file = request.FILES['file']
			file_data = uploaded_file.read()
			fs = FileSystemStorage()
			filename = fs.save(uploaded_file.name, uploaded_file)
			ImageFile.objects.create(
				name=filename, 
				size=fileSize(uploaded_file.size), 
				format=signatureFile(file_data)
			)
			return redirect('index')
		context = {
			"title":"Dashboard",
		}
		return render(request,'index/index.html',context)
	return HttpResponseRedirect(reverse('masuk'))

def signatureFile(file):
	signature = {bytes.fromhex("89504E470D0A1A0A"):"png",
				 bytes.fromhex("49484452"):"png",
				 bytes.fromhex("FFD8"):"jpg",
				 bytes.fromhex("424D"):"bmp",
				 bytes.fromhex("D4C3B2A1"):"pcap"}
	for key,value in signature.items():
		if key in file[:20]:
			return value
def fileSize(sizes):
	list_size = ["KB","MB","GB","TB"]
	result = 0
	size = sizes
	if size < 1024:
		fix = str(size)+" Bytes"
	else:
		for i in range(len(list_size)):
			if size > 1024: 
				size /= 1024
				fix = str(size).split('.')[0]+" "+list_size[i]
				if i >= 1:
					nilai = str(size).split('.')
					fix = nilai[0]+"."+nilai[1][:2]+" "+list_size[i]
	return fix

def cleanData(request):
	ImageFile.objects.all().delete()
	os.system("rm uploads/*")
	return HttpResponseRedirect(reverse('index'))

def getData(request):
	file_image = ImageFile.objects.all().values('id','name','size','format')
	data = list(file_image)
	return JsonResponse(data, safe=False)

def deleteData(request, id_):
	data = ImageFile.objects.get(id=id_)
	os.system("rm uploads/"+data.name)
	data.delete()
	return HttpResponseRedirect(reverse('index'))