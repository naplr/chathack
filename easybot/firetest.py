import pyrebase

config = {
    "apiKey": "AIzaSyBbLf8k4NKQVXfjMg--POKkiQjHi2yuTxc",
    "authDomain": "chathack-db0fb.firebaseapp.com",
    "databaseURL": "https://chathack-db0fb.firebaseio.com",
    "storageBucket": "chathack-db0fb.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

db.child("userid").update({
    "text": "Hi guys",
    "intent": "hello_action"
})
