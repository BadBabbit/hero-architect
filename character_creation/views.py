from django.shortcuts import render
from django.http import HttpResponse
import pyrebase

config={
    'apiKey': "AIzaSyD2rvIB6B7Zsmc6cR-hThQNK5OkKjW8Nvg",
    'authDomain': "hero-architect-db.firebaseapp.com",
    'databaseURL': "https://hero-architect-db-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "hero-architect-db",
    'storageBucket': "hero-architect-db.appspot.com",
    'messagingSenderId': "831658074086",
    'appId': "1:831658074086:web:9f8fd9afae32b09f12c027",
    'measurementId': "G-EZP1PHXXJP"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def test(request):
    get_data_test = database.child('test_key').get().val()
    return render(request, 'test.html', {
        'test_data': get_data_test
    })

# Create your views here.
