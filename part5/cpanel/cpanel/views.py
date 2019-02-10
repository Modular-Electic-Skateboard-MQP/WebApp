from django.shortcuts import render
import pyrebase
from django.contrib import auth

config = {

    'apiKey': "AIzaSyBJN3d0umh5zKC8OgInDNPlKKEPSUoZlF8",
    'authDomain': "mesb-70fa5.firebaseapp.com",
    'databaseURL': "https://mesb-70fa5.firebaseio.com",
    'projectId': "mesb-70fa5",
    'storageBucket': "mesb-70fa5.appspot.com",
    'messagingSenderId': "196474953476"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()
session_id = "A"


def signIn(request):
    return render(request, "signIn.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "signIn.html", {"messg": message})
    #print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "home.html")


def logout(request):
    auth.logout(request)
    return render(request, 'signIn.html')


def signUp(request):
    return render(request, "signup.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", {"messg": message})
        uid = user['localId']

    data = {"name": name, "status": "1"}

    database.child("users").child("details").set(data)
    return render(request, "signIn.html")


def create(request):
    return render(request, 'create.html')


def post_create(request):
    return render(request, 'home.html')


def check(request):
    import datetime

    idtoken = session_id

    runID = list()
    runs = list()
    durations = list()
    peripherals = list()
    functions = list()
    vars = list()

    runID = database.child('runs').shallow().get().val()
    runID = list(runID)
    for i in runID:
        runs.append(database.child('runs/' + i).get().val())
        durations.append(database.child('runs/' + i + '/duration').get().val())
        peripherals.append(database.child('runs/' + i + '/peripherals').shallow().get().val())
        for p in peripherals:
            p = list(p)
            for x in range(len(p)):
                #print(p[x])
                functions.append(database.child('runs' + i + '/peripherals' + p[x] + 'funcs').shallow().get().val())
                #print(functions)
                vars.append(database.child('runs' + i + '/peripherals' + p[x] + 'Vars').get().val())

    #print(runID)
    #print(runs)
    #print(durations)
    #print(peripherals)
    #print(functions)
    #print(vars)
    #comb_lis = zip(runID, durations)
    return render(request, 'check.html', {'RID': runID})


def post_check(request):

    run = request.GET.get('z')
    #duration = database.child('runs/' + run + '/duration').get().val()
    peripherals = database.child('runs/' + run + '/peripherals').shallow().get().val()

    return render(request, 'post_check.html', {'periphs': peripherals})

def post_check2(request):

    run = request.GET.get('z')
    peri = request.GET.get('y')
    return render(request, 'post_check2.html')
