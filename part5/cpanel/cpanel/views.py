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

    idtoken = session_id

    runID = list()
    runs = list()
    durations = list()
    peripherals = list()

    runID = database.child('runs').shallow().get().val()
    runID = list(runID)
    for i in runID:
        runs.append(database.child('runs/' + i).get().val())
        durations.append(database.child('runs/' + i + '/duration').get().val())
        peripherals.append(database.child('runs/' + i + '/peripherals').shallow().get().val())
    #print(runID)
    #print(runs)
    #print(durations)
    #print(peripherals)
    #print(functions)
    #print(vars)
    #comb_lis = zip(runID, durations)
    return render(request, 'check.html', {'RID': runID})

def curr_check(request):

    idtoken = session_id

    runID = list()
    runs = list()
    durations = list()
    peripherals = list()

    runID = database.child('runs').shallow().get().val()
    runID = list(runID)[-1]
    temp = ""
    for x in runID:
        temp+=x

    temp = str(temp)
    return render(request, 'curr_check.html', {'RID': temp})

def post_curr_check(request):
    runID = database.child('runs').shallow().get().val()
    runID = list(runID)[-1]
    temp = ""
    for x in runID:
        temp+=x

    temp = str(temp)
    peripherals = database.child('runs/' + temp + '/peripherals').shallow().get().val()
    peripherals = list(peripherals)
    names = list()
    vars = list()
    vars_names = list()
    vars_size = list()
    vars_type = list()
    vals = list()
    val_keys = list()
    val_vals = list()
    for x in range(len(peripherals)):
        aname= str(database.child('runs/' + temp + '/peripherals/' + peripherals[x] + '/name').get().val())
        names.append(aname)
        temp = list(database.child('runs/' + temp + '/peripherals/' + peripherals[x] + '/vars').shallow().get().val())
        vars.append(temp[x])

        for y in range(len(vars)):
            vname = str(vars[y])
            print(vname)
            print(database.child('runs/' + temp + '/peripherals/' + peripherals[x] + '/vars/' + vname + '/name').get().val())
            vars_names.append(vname)
            vars_size.append(database.child(
                'runs/' + temp + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/size').get().val())
            if (database.child(
                    'runs/' + temp + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/type').get().val() == 0):
                vars_type.append("Integer")
            elif (database.child(
                    'runs/' + temp + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/type').get().val() == 1):
                vars_type.append("String")
            else:
                vars_type.append("Float")
            vals.append(database.child(
                'runs/' + temp + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/val').get().val())

            for key, value in vals[y].items():
                val_keys.append(key)
                val_vals.append(value)

    print(vals)
    comb_list = zip(names, peripherals)
    comb_list2 = zip(vars_names, vars, vars_size, vars_type, vals)
    comb_list3 = zip(val_keys, val_vals)
    return render(request, 'post_curr_check.html', {'comb_lis': comb_list, 'comb_lis2': comb_list2, 'run': temp})

def post_check(request):

    run = request.GET.get('z')
    peripherals = database.child('runs/' + run + '/peripherals').shallow().get().val()
    peripherals = list(peripherals)
    names = list()
    vars = list()
    vars_names = list()
    vars_size = list()
    vars_type = list()
    vals = list()
    val_keys = list()
    val_vals = list()
    for x in range(len(peripherals)):
        names.append(database.child('runs/' + run + '/peripherals/' + peripherals[x] + '/name').get().val())
        temp = list(database.child('runs/' + run + '/peripherals/' + peripherals[x] + '/vars').shallow().get().val())
        vars.append(temp[x])

        for y in range(len(vars)):
            vars_names.append(database.child('runs/' + run + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/name').get().val())
            vars_size.append(database.child('runs/' + run + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/size').get().val())
            if (database.child('runs/' + run + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/type').get().val() == 0):
                vars_type.append("Integer")
            elif (database.child('runs/' + run + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/type').get().val() == 1):
                vars_type.append("String")
            else:
                vars_type.append("Float")
            vals.append(database.child('runs/' + run + '/peripherals/' + peripherals[x] + '/vars/' + vars[y] + '/val').get().val())


            for key, value in vals[y].items():
                val_keys.append(key)
                val_vals.append(value)

    print(vals)
    comb_list = zip(names, peripherals)
    comb_list2 = zip(vars_names, vars, vars_size, vars_type, vals)
    comb_list3 = zip(val_keys, val_vals)
    return render(request, 'post_check.html', {'comb_lis': comb_list, 'comb_lis2': comb_list2, 'run': run})


def post_check2(request):

    run = request.GET.get('z')
    peri = request.GET.get('y')
    print(run)
    vars = database.child('runs/' + run + '/peripherals').shallow().get().val()
    print(vars)
    #{'name': name}
    return render(request, 'post_check2.html')
