from django.shortcuts import render

# Create your views here.

#Imports for Views
from django.http import HttpResponse

'''

<script src="https://www.gstatic.com/firebasejs/5.8.1/firebase.js"></script>
<script>
  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyBJN3d0umh5zKC8OgInDNPlKKEPSUoZlF8",
    authDomain: "mesb-70fa5.firebaseapp.com",
    databaseURL: "https://mesb-70fa5.firebaseio.com",
    projectId: "mesb-70fa5",
    storageBucket: "mesb-70fa5.appspot.com",
    messagingSenderId: "196474953476"
  };
  firebase.initializeApp(config);
</script>

'''

def home(request):
    return render(request, 'Home/home.html')