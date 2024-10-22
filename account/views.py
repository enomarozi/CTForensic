from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import CustomAuthenticationForm, RegistrasiForm, PengaturanForm
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
		else:
			messages.error(request, "Username Atau Password Salah.")
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
					messages.success(request, "Pendaftaran Berhasil, Silakan Coba Masuk.")
				else:
					message.error(request, "Pendaftaran Gagal", "Password Tidak Sama dengan Konfirmasi Password.")
			else:
				messages.error(request, "Pendaftaran Gagal, Panjang Password minimal 8 Karakter.")
		else:
			messages.error(request, "Pendaftaran Gagal, Pastikan lagi Inputannya.")
	else:
		form = RegistrasiForm()
	return render(request, 'account/registrasi.html',{'form':form})

def pengaturan(request):
	if request.user.is_authenticated:
		form = PengaturanForm(request.POST)
		if form.is_valid():
			password_sekarang = form.cleaned_data.get("password_sekarang")
			password_baru = form.cleaned_data.get("password_baru")
			password_konfirmasi = form.cleaned_data.get("password_konfirmasi")
			if request.user.check_password(password_sekarang):
				if password_baru == password_konfirmasi:
					request.user.set_password(password_konfirmasi)
					request.user.save()
					update_session_auth_hash(request, request.user)
					messages.success(request,"Password berhasil diubah.")
				else:
					messages.error(request, "Password baru dan konfirmasi password tidak cocok.")
			else:
				messages.error(request, "Password sekarang salah.")
		else:
			form = PengaturanForm()

		context = {
		    'title': "Ganti Password",
		    'form': form,
		}	
		return render(request, 'account/pengaturan.html', context)
	else:
		form = CustomAuthenticationForm()
	return render(request, 'account/masuk.html',{'form':form})

def keluar(request):
	if request.user.is_authenticated:
		logout(request)
	return HttpResponseRedirect(reverse('masuk'))
