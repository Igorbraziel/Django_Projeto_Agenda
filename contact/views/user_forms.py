from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from contact.forms import RegisterForm, RegisterUpdateForm

def register(request):
    form_action = reverse('contact:register')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        context = {
            'form': form,
            'form_action': form_action,
        }
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered User')
            return redirect('contact:login')
        
        return render(
            request, 
            'contact/register.html',
            context=context
        )

    form = RegisterForm()  
    
    context = {
        'form': form,
        'form_action': form_action,
    }
    
    return render(
        request,
        'contact/register.html',
        context=context
    )
    

def login_view(request):
    form = AuthenticationForm(request)
    form_action = reverse('contact:login')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'SUCCESSFUL LOGGED AS {user.username.upper()}')
            return redirect('contact:index')
        else:
            messages.error(request, 'USER AND PASSWORD INCORRECTS')
    
    context = {
        'form': form,
        'form_action': form_action,
    }        
    
    return render(
        request, 
        'contact/login.html',
        context
    )
    

@login_required(login_url='contact:login')    
def logout_view(request):
    auth.logout(request)
    messages.warning(request, 'SUCCESSFUL LOGOUT')
    return redirect('contact:login')


@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)
    
    if request.method == 'POST':
        form = RegisterUpdateForm(data=request.POST, instance=request.user)
        
        context = {
            'form': form
        }
        
        if form.is_valid():
            form.save()
            return redirect('contact:user_update')
        
    context = {
        'form': form
    }
    
    return render(
        request, 
        'contact/user_update.html',
        context=context
    )