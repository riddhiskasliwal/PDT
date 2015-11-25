from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from .forms import LoginForm
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from .models import Signin

# Create your views here.
def login(request):
    title = "Please log in"
    c = {
        "title":title,
    }
    c.update(csrf(request))
    return render_to_response('login.html',c)

def auth_view(request):
    #if request.method == "POST":
        #print(request.POST)#for debugging
    username = request.POST.get('username','')#second param is default
    password = request.POST.get('password','')
    user = auth.authenticate(username=username, password=password)
    #if match is found, a user object is returned. if no match, None is ret.

    if user is not None:
        auth.login(request, user)
        for instance in Signin.objects.all():
            if(instance.username==username):
                if(instance.role=='Developer'):
                    print("Developer Status")
                    return HttpResponseRedirect('/developer')
                elif(instance.role=='Manager'):
                    print("Manager Status")
                    return HttpResponseRedirect('/manager')
                else:
                    print("Admin Status");
            return HttpResponseRedirect('/loggedin')
    else:
        title = "Your login details are invalid, please try again."
        c = {
            "title":title,
        }
        c.update(csrf(request))
        return render_to_response('login.html',c)

def loggedin(request):#this displays admin form and handles saving the form i.e. register user
    title_admin = "Please fill in the form to add a user."
    if request.method=='POST':
        print(request.POST)
        form = RegistrationForm(request.POST)#post in arg
        if form.is_valid():
            form.save()
            title_admin = "Add successful."
            c = {
                "title_admin": title_admin,
            }
            c.update(csrf(request))
            return render_to_response('admin.html',c)
        else:
            title_admin = "Form entered is not valid!"

    args = {
        "title_admin": title_admin,
    }
    args.update(csrf(request))
    args['reg_form']=RegistrationForm()#no post in arg, bog standard
    return render_to_response('admin.html',args)


def logout(request):
    auth.logout(request)
    title = "Logged out."
    c = {
        "title":title,
    }
    c.update(csrf(request))
    return render_to_response('login.html',c)

def curruser(request):
    if request.method=='POST':
        print("following are DB info")
        print(request.POST)
    signin = Signin.objects.all()
    c={
        "signin":signin
    }
    return render_to_response('current_users.html',c,RequestContext(request))

def manager(request):
    return render_to_response('manager.html',RequestContext(request))

def developer(request):
    return render_to_response('developer.html',RequestContext(request))