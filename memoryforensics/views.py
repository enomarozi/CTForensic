from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			uploaded_file = request.FILES['file']
			file_data = uploaded_file.read()
			fs = FileSystemStorage()
			filename = fs.save(f'memoryforensics/{uploaded_file.name}', uploaded_file)
			NetworkFile.objects.create(
				name=filename, 
				size=fileSize(uploaded_file.size), 
				format=signatureFile(file_data)
			)
			return redirect('memory_forensics')
		context = {
			"user":request.user,
			"title":"Memory Forensics",
		}
		return render(request,'memoryforensics/memoryforensics.html',context)
	return HttpResponseRedirect(reverse('masuk'))