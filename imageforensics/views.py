from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from index.forms import UploadFileForm
from .models import ImageFile
from index.views import fileSize
import os

def index(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			uploaded_file = request.FILES['file']
			file_data = uploaded_file.read()
			fs = FileSystemStorage()
			filename = fs.save(f'imageforensics/{uploaded_file.name}', uploaded_file)
			ImageFile.objects.create(
				name=filename, 
				size=fileSize(uploaded_file.size), 
				format=signatureFile(file_data)
			)
			return redirect('image_forensics')
		context = {
			"user":request.user,
			"title":"Image Forensics",
		}
		return render(request,'imageforensics/imageforensics.html',context)
	return HttpResponseRedirect(reverse('masuk'))

def signatureFile(file):
	signature = {bytes.fromhex("89504E470D0A1A0A"):"png",
				 bytes.fromhex("49484452"):"png",
				 bytes.fromhex("FFD8"):"jpg",
				 bytes.fromhex("424D"):"bmp"}
	for key,value in signature.items():
		if key in file[:20]:
			return value

def cleanData(request):
	ImageFile.objects.all().delete()
	os.system("rm uploads/*")
	return HttpResponseRedirect(reverse('index'))

def getData(request):
	file_image = ImageFile.objects.all().values('id','name','size','format')
	data = list(file_image)
	return JsonResponse(data, safe=False)

def deleteData(request, id_):
	if request.user.is_authenticated:
		data = ImageFile.objects.get(id=id_)
		os.system("rm uploads/imageforensics/"+data.name)
		data.delete()
		return HttpResponseRedirect(reverse('image_forensics'))
	return HttpResponseRedirect(reverse('masuk'))
