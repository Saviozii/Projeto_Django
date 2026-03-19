from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


#registro de conta:
def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = UserCreationForm()
    return render(request,'register.html',{'user_form':user_form})


#Login de conta:
def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request,data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            print (f'o usuario "{user.username}" entrou')
            return redirect('cars_view')
        else:
            return redirect('login')
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form':login_form})



# Logout excluir usuario
def logout_view(request):
    logout(request)                  
    return redirect('login')