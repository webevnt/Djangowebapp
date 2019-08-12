from django.shortcuts import render,redirect
from socialapp.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

def index(request):
    return render(request,'socialapp/index.html')

#@login_required
#def special(request):
    #return HttpResponse("You are logged in !")

@login_required
def userlogout(request):
    logout(request)
    return redirect('/')

def register(request):
    registered = False
    if request.method == 'POST':
        uform = UserForm(data=request.POST)
        pform = UserProfileInfoForm(data=request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            user.set_password(user.password)
            user.save()
            profile = pform.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(uform.errors,pform.errors)
    else:
        uform = UserForm()
        pform = UserProfileInfoForm()
    return render(request,'socialapp/registration.html',
                          {'user_form':uform,
                           'profile_form':pform,
                           'registered':registered})



def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('/') #HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'socialapp/login.html', {})


def view_profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'socialapp/profile.html', {'user': user})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        return render(request, 'password/changep.html', args = {'form': form})
