from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm, RegistrasiForm, PengaturanForm
from datetime import datetime

def masuk(request):
	if request.user.is_authenticated:
		return redirect('index')
	if request.method == "POST":
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return HttpResponseRedirect(reverse('index'))
	else:
		form = CustomAuthenticationForm()
	return render(request, 'account/masuk.html',{'form':form})

def registrasi(request):
	if request.method == "POST":
		form = RegistrasiForm(data=request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, "Registration successful. Please log in.")
			return redirect('masuk')
	else:
		form = RegistrasiForm()
	return render(request, 'account/registrasi.html',{'form':form})

@login_required(login_url='masuk')
def pengaturan(request):
	if request.method == "POST":
		form = PengaturanForm(request.POST)
		if form.is_valid():
			password_sekarang = form.cleaned_data.get("password_sekarang")
			password_baru = form.cleaned_data.get("password_baru")
			password_konfirmasi = form.cleaned_data.get("password_konfirmasi")

			if request.user.check_password(password_sekarang):
				if password_baru == password_konfirmasi:
					if len(password_konfirmasi) < 8:
						messages.error(request, "New password must be at least 8 characters long.")
					else:
						request.user.set_password(password_konfirmasi)
						request.user.save()
						update_session_auth_hash(request, request.user)
						messages.success(request, "Password has been successfully changed.")
						return redirect('pengaturan')
				else:
					messages.error(request, "New password and confirmation do not match.")
			else:
				messages.error(request, "Current password is incorrect.")
		else:
			form = PengaturanForm()

		context = {
		    'title': "Change Password",
		    'form': form,
		}	
		return render(request, 'account/pengaturan.html', context)
	else:
		form = CustomAuthenticationForm()
	return render(request, 'account/masuk.html',{'form':form})

@login_required(login_url='masuk')
def keluar(request):
	logout(request)
	return redirect('masuk')
