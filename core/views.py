from django.shortcuts import redirect, render
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from user_profile.models import Profile
# Create your views here.
def home(request):
    return render(request,'core/home.html',{
        'title':'Home'
    })

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None :
            auth.login(request, user)
            messages.success(request,'Login successfully')
            print('Login sucessfully.Welcome..')
            return redirect('core:home')
        else:
            messages.error(request,'Invalid credentials.please check your username or password')
            print("Invalid credentials.please check your username")
            return redirect('core:signin')

    return render(request,'core/signin.html',{
       'title':'Signin'
    })

def signup(request):
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request,'This eamil already taken')
                print("This eamil already taken")
                return redirect('core:signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request,'This username already taken')
                print("This username already taken.")
                return redirect('core:signup')
            else:
                new_user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                new_user.save()
                user_credentials =auth.authenticate(username=username,password=password)
                messages.success(request,'Account created sucessfully')
                #create profile for new user
                get_new_user =User.objects.get(username=username)
                new_profile = Profile.objects.create(user=get_new_user)
                new_profile.save()
                #redirect user
                print("Account created sucessfully ")
                auth.login(request,user_credentials)
                return redirect('core:home')
        else:
            messages.error(request,'Password not match')
            print("Password not match")
            return redirect('core:signup')
        
    return render(request,'core/signup.html',{
       'title':'Signup'
    })

def signout(request):
    auth.logout(request)
    messages.error(request,"Logout sucessfully")
    print('Logout sucessfully!.Have a great day!')
    return redirect('core:signin')