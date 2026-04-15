from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from index.forms import UploadFileForm
from .models import NetworkFile
from index.views import fileSize
import os

@login_required(login_url='masuk')
def index(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			uploaded_file = request.FILES['file']
			file_data = uploaded_file.read()
			fs = FileSystemStorage()
			filename = fs.save(f'networkforensics/{uploaded_file.name}', uploaded_file)
			if signatureFile(file_data) == None:
				messages.error(request, "File tidak valid atau bukan signature yang dikenali")
				return redirect('network_forensics')
			NetworkFile.objects.create(
				name=filename.split('/')[1],
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

@login_required(login_url='masuk')
def getData(request):
	file_image = NetworkFile.objects.all().values('id','name','size','format')
	data = list(file_image)
	return JsonResponse(data, safe=False)

@login_required(login_url='masuk')
def deleteData(request, id_):
	if request.user.is_authenticated:
		data = NetworkFile.objects.get(id=id_)
		os.system("rm uploads/networkforensics/"+data.name)
		data.delete()
		return HttpResponseRedirect(reverse('network_forensics'))
	return HttpResponseRedirect(reverse('masuk'))
