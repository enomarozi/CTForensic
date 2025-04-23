from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from networkforensics.models import NetworkFile
from imageforensics.models import ImageFile
import os

def index(request):
	return render(request,'index/index.html')

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