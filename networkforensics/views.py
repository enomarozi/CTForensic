from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from index.forms import UploadFileForm
from index.models import NetworkFile
from index.views import fileSize
import os

def index(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			uploaded_file = request.FILES['file']
			file_data = uploaded_file.read()
			fs = FileSystemStorage()
			filename = fs.save(uploaded_file.name, uploaded_file)
			NetworkFile.objects.create(
				name=filename, 
				size=fileSize(uploaded_file.size), 
				format=signatureFile(file_data)
			)
			return redirect('network_forensics')
		context = {
			"user":request.user,
			"title":"Network Forensics",
		}
		return render(request,'networkforensics/networkforensics.html',context)
	return HttpResponseRedirect(reverse('masuk'))

def signatureFile(file):
	signature = {bytes.fromhex("D4C3B2A1"):"pcap",
				 bytes.fromhex("0A0D0D0A"):"pcapng",}
	for key,value in signature.items():
		if key in file[:20]:
			return value

def cleanData(request):
	NetworkFile.objects.all().delete()
	os.system("rm uploads/*")
	return HttpResponseRedirect(reverse('index'))

def getData(request):
	file_image = NetworkFile.objects.all().values('id','name','size','format')
	data = list(file_image)
	return JsonResponse(data, safe=False)

def deleteData(request, id_):
	if request.user.is_authenticated:
		data = NetworkFile.objects.get(id=id_)
		os.system("rm uploads/"+data.name)
		data.delete()
		return HttpResponseRedirect(reverse('index'))
	return HttpResponseRedirect(reverse('masuk'))
