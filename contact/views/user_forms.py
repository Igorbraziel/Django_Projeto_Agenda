from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from contact.forms import RegisterForm

def register(request):
    form_action = reverse('contact:register')
    
    messages.info(request, 'Message Text')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        context = {
            'form': form,
            'form_action': form_action,
        }
        
        if form.is_valid():
            form.save()
        
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