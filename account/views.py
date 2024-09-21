from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import CustomAuthenticationForm, RegistrasiForm
from datetime import datetime

def masuk(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('index'))
	if request.method == "POST":
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			messages.error(request, "Username Atau Password Salah.")
		else:
			messages.error(request, "Pendaftaran Gagal, Sepertinya Kesalahan Server")
	else:
		form = CustomAuthenticationForm()
	return render(request, 'account/masuk.html',{'form':form})

def registrasi(request):
	if request.method == "POST":
		form = RegistrasiForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			email = form.cleaned_data.get("email")
			password1 = form.cleaned_data.get("password1")
			password2 = form.cleaned_data.get("password2")
			today = datetime.today().date()
			if len(password1) >= 8 and len(password2) >= 8:
				if password1 == password2:
					user = User(username=username, email=email, date_joined=today)
					user.password = make_password(password2)
					user.save()
					messages.success(request, "Pendaftaran Berhasil, Silakan Coba Masuk")
				else:
					message.error(request, "Pendaftaran Gagal", "Password Tidak Sama dengan Konfirmasi Password")
			else:
				messages.error(request, "Pendaftaran Gagal, Panjang Password minimal 8 Karakter")
		else:
			messages.error(request, "Pendaftaran Gagal, Sepertinya Kesalahan Server")
	else:
		form = RegistrasiForm()
	return render(request, 'account/registrasi.html',{'form':form})

def keluar(request):
	logout(request)
	return HttpResponseRedirect(reverse('masuk'))
