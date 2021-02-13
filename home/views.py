from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User 
# Create your views here.

def home(request):
    return render(request, 'home/home.html')


def about(request):
    messages.success(request, 'Welcome to About')
    return render(request, 'home/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']   
        print(name, email, phone, content)
        if(name=='' or email=='' or len(phone) < 10 or len(content) <= 10):
            messages.error(request, 'Please, fill the form properly!')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')

    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    allPosts = Post.objects.filter(title__icontains=query)
    params = {'allPosts': allPosts}
    return render(request, 'home/search.html', params)
    #return HttpResponse('This is search')


def handleSignup(request):
    if request.method == 'POST':
        #Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #checks for errorneour input
        if len(username) < 10 or len(username) > 25:
            messages.error(request, "Username must be between 10 to 15 characters!")
            return redirect('home')
        if len(pass1) < 8:
            messages.error(request, "Password must be more than 8 characters!")
            return redirect('home')
        if not username.isalnum() :
            messages.error(request, "Username must be alphanumeric!")
            return redirect('home')
        if (not lname.isalpha()) or ( not fname.isalpha()):
            messages.error(request, "Please check firstname or lastname!")
            return redirect('home')
        if pass1 != pass2 :
            messages.error(request, "Passwords do not match!")
            return redirect('home')
        


        #create the user

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account is has been successfully created")
        return redirect('/home')
    else:
        return HttpResponse('User not found')
    


def handleLogin(request):
    if request.method == 'POST':
        #Get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again!")
            return redirect('home')

    return HttpResponse("404- Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')
 