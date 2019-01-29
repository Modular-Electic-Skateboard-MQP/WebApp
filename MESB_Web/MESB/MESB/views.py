from django.shortcuts import render
import pyrebase


config = {
'apiKey': "AIzaSyBJN3d0umh5zKC8OgInDNPlKKEPSUoZlF8",
'authDomain': "mesb-70fa5.firebaseapp.com",
'databaseURL': "https://mesb-70fa5.firebaseio.com",
'projectId': "mesb-70fa5",
'storageBucket': "mesb-70fa5.appspot.com",
'messagingSenderId': "196474953476"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
def singIn(request):
    return render(request, "signIn.html")
def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid cerediantials"
        return render(request,"signIn.html",{"msg":message})
    print(user)
    return render(request, "home.html")
